# pip install sodapy

import numpy as np
import pandas as pd
# from sodapy import Socrata
import time as time
from pandas.api.types import is_string_dtype
import pickle
from collections import OrderedDict
from manual_corrections import pac_correction
from manual_corrections import ie_correction
from synonyms import do_ie_synonyms
from synonyms import add_synonyms
from synonyms import do_pac_synonyms2
from donors_of_interest import make_donors_interest
from difflib import get_close_matches
import yaml
# from fuzzywuzzy import process
import json

# use cases:
# 1. search by contributor & summarize by party
# 2. summarize by candidate votes on a bill - IEs and donations to losing candidates will not be counted in bill votes

class Donor():

    def __init__(self):
        self.name = " "
        self.aliases = []  # stores list of synonyms when we combine_donors
        self.type = " "  # ind, pac, party, caucus
        self.filer_id = " "
        self.total_in = 0.0
        self.total_out = 0.0

        # only for PAC/caucus/party, empty for Individual donors
        self.money_in = pd.DataFrame(columns=['donor', 'donor_id', 'amount'])

        # amount, receiver, receiver type (Cand vs PAC)
        self.money_out = pd.DataFrame(columns=["receiver", "amount", "party", "type"])

        # money_out resolved to end candidates
        self.money_out_resolved = pd.DataFrame( columns=["receiver", "amount", "party", "type", "proportion"])

        self.has_resolved = False  # indicates whether money_out_resolved has been successfully computed yet
        self.pending_resolve = False # this is used to detect recursion loops in resolve_donations

    def __repr__(self):
        if self.money_out_resolved.empty:
            return "<Name:%s ID:%s Money in/out:%s / %s>" % (self.name, self.filer_id, self.money_in['amount'].sum(),
                                                             self.money_out['amount'].abs().sum())
        # note sum() will be 0 if df is empty
        this_d_plus = self.money_out_resolved.loc[(self.money_out_resolved['party']=='DEMOCRAT')&
                                                  (self.money_out_resolved['proportion']>0),'proportion'].sum()
        this_d_minus = self.money_out_resolved.loc[(self.money_out_resolved['party']=='DEMOCRAT')&
                                                  (self.money_out_resolved['proportion']<0),'proportion'].sum()
        this_r_plus = self.money_out_resolved.loc[(self.money_out_resolved['party'] == 'REPUBLICAN') &
                                                  (self.money_out_resolved['proportion'] > 0), 'proportion'].sum()
        this_r_minus = self.money_out_resolved.loc[(self.money_out_resolved['party'] == 'REPUBLICAN') &
                                                   (self.money_out_resolved['proportion'] < 0), 'proportion'].sum()
        return "<Name:%s ID:%s Money in/out:%s / %s  Pct: %s D+ / %s R+ / %s D- / %s R->" % (self.name, self.filer_id,
                self.money_in['amount'].sum(), self.money_out['amount'].sum(),
                int(100*this_d_plus),int(100*this_r_plus),int(100*this_d_minus),int(100*this_r_minus))

    def sum_donations(self):
        # check that money_in and money_out are non-empty (otherwise it would break), and if so sum them by receiver
        # include party and type (these won't vary for one receiver) so we don't lose these columns
        # the reset_index() is needed to put this back into a dataframe with the correct columns
        if (len(self.money_out) > 1):
            self.money_out = pd.DataFrame(self.money_out.groupby(['receiver', 'party', 'type']).sum()).reset_index()
        if (len(self.money_in) > 1):
            self.money_in = pd.DataFrame(self.money_in.groupby(['donor', 'donor_id']).sum()).reset_index()
        self.total_in = self.money_in['amount'].abs().sum()
        self.total_out = self.money_out['amount'].abs().sum()
        return

    def resolve_donations(self, fulldata):
        # TODO: check for second-level recursion problems, i.e. if PAC A -> PAC B -> PAC C -> PAC A
        # recursion is detected if PAC A -> PAC A or if PAC A -> PAC B -> PAC A
        print(self.name)
        if (self.has_resolved == True):
            return
        self.pending_resolve = True
        # reset the money_out_resolved dataframe
        self.money_out_resolved = pd.DataFrame(columns=["receiver", "amount", "party", "type", "proportion"])
        # check if this is a party pac
        my_party_name = 'No Party'
        if self.name in fulldata.party_pac_dict.keys():
            my_party_name = fulldata.party_pac_dict[self.name]
        # get number of donations to resolve
        n_donations = len(self.money_out)
        # check if money_out is empty
        if n_donations < 1:
            self.money_out_resolved = pd.DataFrame([[self.name, self.money_in.amount.abs().sum(), my_party_name, 'Terminal PAC', 1.0]],
                                                   columns=["receiver", "amount", "party", "type", "proportion"])
            # mark self as resolved
            self.pending_resolve = False
            self.has_resolved = True
            # print('Resolved no donations')
            return
        # for each line in money_out, check if it is to a candidate or pac, and update money_out_resolved
        # need to store list of zero receivers to process after this for loop
        zero_receivers = []
        for i in range(n_donations):
            # if candidate, then the amount is 100% to that candidate, so nothing to do
            # if pac, then get candidates/proportions from that pac, and allocate amounts accordingly
            this_receiver = self.money_out.iloc[i,]['receiver']
            this_amount = self.money_out.iloc[i,]['amount']
            this_party = self.money_out.iloc[i,]['party']
            this_type = self.money_out.iloc[i,]['type']
            if this_type == 'Candidate':
                this_add = pd.DataFrame([[this_receiver, this_amount, this_party, this_type, 0]],
                                        columns=["receiver", "amount", "party", "type", "proportion"])
                self.money_out_resolved = self.money_out_resolved.append(this_add, ignore_index=True)
            else:
                # this_amount can only be negative for a candidate (for IE spending against)
                if this_amount<0:
                    raise ValueError('in resolve_donations: this_amount should not be negative for a PAC')
                # look up the pac that this money went to
                if this_receiver in fulldata.all_donors:
                    # check if this donation is to self
                    if this_receiver == self.name:
                        # we are in a recursion loop because this PAC donated to itself
                        # raise warning and ignore this donation
                        print('resolve_donations: Recursion loop, ignoring donation to self by ' + self.name)
                        # remove from money_in and money_out
                        self.money_in = self.money_in.loc[self.money_in.donor != this_receiver, :]
                        zero_receivers = zero_receivers + [this_receiver]  # this will remove from money_out after for loop
                        # if this is the only donation then this is a terminal PAC, so set money_out_resolved and return
                        if (self.money_out_resolved.empty) & (i == (n_donations - 1)):
                            self.money_out_resolved = pd.DataFrame(
                                [[self.name, self.money_in.amount.abs().sum(), my_party_name, 'Terminal PAC', 1.0]],
                                columns=["receiver", "amount", "party", "type",
                                         "proportion"])
                            # remove from money_out since we are not continuing for loop (should make it empty)
                            self.money_out = self.money_out.loc[self.money_out.receiver != this_receiver, :]
                            # mark self as resolved
                            self.pending_resolve = False
                            self.has_resolved = True
                            return
                        else:
                            continue  # don't add to money_out_resolved since this was donation to self
                    # check for recursion loop PAC A -> PAC B -> PAC A
                    # check if receiver is also a donor to self, if so then fix to avoid recursion loop
                    if this_receiver in self.money_in.donor.values:
                        print('resolve_donations: Recursion loop from '+self.name+' to '+this_receiver)
                        # get both amounts
                        amount_to_me = fulldata.all_donors[this_receiver].money_out.loc[fulldata.all_donors[this_receiver].money_out.receiver == self.name, 'amount']
                        if len(amount_to_me)==1:
                            amount_to_me = amount_to_me.iloc[0]
                        else:
                            raise ValueError('resolve_donations: amount_to_me not length 1')
                        amount_from_me = this_amount
                        print('From: '+str(amount_from_me)+'  To: '+str(amount_to_me))
                        if amount_to_me > amount_from_me:
                            # subtract amount_from_me from donation to me
                            fulldata.all_donors[this_receiver].money_out.loc[fulldata.all_donors[this_receiver].money_out.receiver == self.name, 'amount'] = \
                                fulldata.all_donors[this_receiver].money_out.loc[fulldata.all_donors[this_receiver].money_out.receiver == self.name, 'amount'] - amount_from_me
                            self.money_in.loc[self.money_in.donor == this_receiver, 'amount'] = self.money_in.loc[self.money_in.donor == this_receiver, 'amount'] - amount_from_me
                            # remove line from self.money_out and this_receiver's money_in
                            fulldata.all_donors[this_receiver].money_in = fulldata.all_donors[this_receiver].money_in.loc[
                                    fulldata.all_donors[this_receiver].money_in.donor != self.name,:]
                            # self.money_out = self.money_out.loc[self.money_out.receiver != this_receiver,:]
                            # can't edit this while we are iterating over it, have to remove it after for loop
                            zero_receivers = zero_receivers + [this_receiver]
                            continue  # this donation from me to receiver is zero, so do not add to money_out_resolved
                        elif amount_to_me < amount_from_me:
                            # subtract amount_to_me from donation from me
                            self.money_out.loc[self.money_out.receiver==this_receiver,'amount'] = self.money_out.loc[self.money_out.receiver==this_receiver,'amount'] - amount_to_me
                            fulldata.all_donors[this_receiver].money_in.loc[fulldata.all_donors[this_receiver].money_in.donor == self.name, 'amount'] = \
                                fulldata.all_donors[this_receiver].money_in.loc[fulldata.all_donors[this_receiver].money_in.donor == self.name, 'amount'] - amount_to_me
                            # remove line from self.money_in and this_receiver's money_out
                            fulldata.all_donors[this_receiver].money_out = fulldata.all_donors[this_receiver].money_out.loc[
                                    fulldata.all_donors[this_receiver].money_out.receiver != self.name,:]
                            self.money_in = self.money_in.loc[self.money_in.donor != this_receiver, :]
                            # adjust this_amount
                            this_amount = this_amount - amount_to_me
                        elif amount_to_me == amount_from_me:
                            # remove line from self.money_in and this_receiver's money_out and this_receiver's money_in
                            fulldata.all_donors[this_receiver].money_out = fulldata.all_donors[this_receiver].money_out.loc[
                                    fulldata.all_donors[this_receiver].money_out.receiver != self.name,:]
                            fulldata.all_donors[this_receiver].money_in = fulldata.all_donors[this_receiver].money_in.loc[
                                    fulldata.all_donors[this_receiver].money_in.donor != self.name,:]
                            self.money_in = self.money_in.loc[self.money_in.donor != this_receiver, :]
                            # self.money_out = self.money_out.loc[self.money_out.receiver != this_receiver,:]
                            # can't edit this while we are iterating over it, have to remove it after for loop
                            zero_receivers = zero_receivers + [this_receiver]
                            continue  # this donation from me to receiver is zero, so do not add to money_out_resolved
                        else:
                            # this shouldn't happen, raise an error
                            print(this_receiver)
                            print(self.name)
                            print(amount_to_me)
                            print(amount_from_me)
                            raise ValueError('in resolve_donations: cant compare amount_to_me and amount_from_me ')
                    # now check for higher level recursion, e.g. A -> B -> C -> A
                    if fulldata.all_donors[this_receiver].pending_resolve == True:
                        # we found a recursion loop between self and this_receiver (and possibly others)
                        # since this_receiver is already pending.
                        # print info and skip this donation to break the recursion
                        print('In donor.resolve_donations: Recursion loop - skipped contribution')
                        print('Self: '+self.name+'  Receiver: '+this_receiver+'  Amount: '+str(this_amount))
                        # remove line from self.money_out and this_receiver's money_in
                        fulldata.all_donors[this_receiver].money_in = fulldata.all_donors[this_receiver].money_in.loc[
                                                fulldata.all_donors[this_receiver].money_in.donor != self.name, :]
                        # self.money_out = self.money_out.loc[self.money_out.receiver != this_receiver,:]
                        # can't edit this while we are iterating over it, have to remove it after for loop
                        zero_receivers = zero_receivers + [this_receiver]
                        continue  # skip this donation and go on to the next
                    # check if the receiver is resolved yet, if not, tell them to resolve
                    if not (fulldata.all_donors[this_receiver].has_resolved):
                        fulldata.all_donors[this_receiver].resolve_donations(fulldata)
                    # get money_out_resolved
                    pac_resolved = fulldata.all_donors[this_receiver].money_out_resolved
                    # allocate this_amount by proportion to candidates in pac_resolved
                    #
                    # Suppose PAC 1 gives $1000 to PAC 2. PAC 2 give $10 to Candidate A, and no other donations.
                    # Then PAC 2 resolved shows $10, 100% to Candidate A.
                    # Then PAC 1 resolved should not show $1000 * 100% = $1000 to Candidate A
                    # Must limit to $10.
                    #
                    # Resolve donations based on proportions of outgoing donations:
                    amount_resolved = this_amount * pac_resolved.loc[:, 'proportion']

                    ##### Old code section, no longer used
                    ##### Don't need prop_in and all these checks since we explicitly compute unspent balance
                    # Adjust based on proportion of money_in, but not if the PAC must have had a starting balance
                    if fulldata.all_donors[this_receiver].total_in>=fulldata.all_donors[this_receiver].total_out:
                        prop_in = this_amount / fulldata.all_donors[this_receiver].money_in.amount.sum()
                    else:
                        prop_in = 1.0
                    if prop_in>1.0:
                        raise ValueError('in resolve_donations: this_amount greater than sum of money_in')
                    # Limit amount_resolved to the amount that was spent (elementwise):
                    if any( (prop_in*abs(pac_resolved.loc[:, 'amount']))<(0.999*abs(amount_resolved) )):
                        temp_filter = ((amount_resolved>=0)*2)-1 # save the signs of each element
                        #expanding this to debug
                        # TODO: remove this debugging code.  This is fixed, and this section should not be reached.
                        amount_resolved_index = amount_resolved.index
                        temp1 = prop_in * pac_resolved.loc[:, 'amount']
                        temp2 = temp1.abs()
                        print('From '+self.name+' to '+this_receiver)
                        print(prop_in)
                        print(this_amount)
                        print(i)
                        print(amount_resolved)
                        print(temp1)

                        temp3 = amount_resolved.abs()
                        #temp2.index = amount_resolved_index
                        temp4 = pd.concat([temp3,temp2],axis=1).min(axis=1)
                        temp5 = temp_filter*temp4
                        amount_resolved = temp5
                        print(temp5)
                    ############# end of old code section
                    #
                    # construct DataFrame from pac_resolved and amount_resolved (proportion will be computed later)
                    this_add = pac_resolved.copy()
                    # relying on the order of amount to be the same as it was when we got the proportions
                    this_add.loc[:, 'amount'] = amount_resolved
                    this_add.loc[:, 'proportion'] = 0  # set to zero for now, it will be computed later
                    self.money_out_resolved = self.money_out_resolved.append(this_add, ignore_index=True)
                else:
                    # we didn't find this pac in our data, so we don't know where the money went!
                    # this should never happen, because if we saw a donation, we would have created an entry
                    # TODO: raise an error here, this shouldn't happen
                    this_add = pd.DataFrame([[this_receiver, this_amount, this_party, 'Unresolved PAC', 0]],
                                            columns=["receiver", "amount", "party", "type", "proportion"])
                    self.money_out_resolved = self.money_out_resolved.append(this_add, ignore_index=True)
        # done with for loop, so finish removing the zero receivers
        for i in zero_receivers:
            # remove from self.money_out
            self.money_out = self.money_out.loc[self.money_out.receiver != i, :]
        # check if money_out_resolved is empty (might have skipped all donations due to recursion loops)
        if self.money_out_resolved.empty:
            # mark unspent if there is money_in.  first check if there is money_in
            if self.money_in.empty:  # can't be recursion loop if no money in
                raise ValueError('resolve_donations: money_in and money_out_resolved cant both be empty')
            this_add = pd.DataFrame([[self.name, self.money_in.amount.abs().sum(), my_party_name, 'PAC Unspent Balance', 0]],
                                    columns=["receiver", "amount", "party", "type", "proportion"])
            self.money_out_resolved = self.money_out_resolved.append(this_add, ignore_index=True)
        else:
            # note resolution may have many intermediate pacs donating to the same candidates, so have to sum again
            # TODO: if negative and positive donations to same candidate, these will cancel out in sum
            self.money_out_resolved = pd.DataFrame(
                self.money_out_resolved.groupby(["receiver", "party", "type", "proportion"]).sum()).reset_index()
            # if this pac is reporting more money_in than money_out, then record it as unspent
            amount_balance = self.money_in.amount.abs().sum() - self.money_out_resolved.amount.abs().sum()
            # note the above line can be different from
            # amount_balance = self.money_in.amount.abs().sum() - self.money_out.amount.abs().sum()
            if amount_balance>0.01:
                this_add = pd.DataFrame([[self.name, amount_balance , my_party_name, 'PAC Unspent Balance', 0]],
                                        columns=["receiver", "amount", "party", "type", "proportion"])
                self.money_out_resolved = self.money_out_resolved.append(this_add, ignore_index=True)
                # store the unspent balance in money_out also so it balances?
                # this_add2 = pd.DataFrame([[self.name, amount_balance, my_party_name, 'PAC Unspent Balance']],
                #                         columns=["receiver", "amount", "party", "type"])
                # self.money_out = self.money_out.append(this_add2, ignore_index=True)
        # when all donations have been resolved
        # get total donation amount and divide to obtain proportion for each candidate
        # use abs() in denominator since amounts can be negative (e.g. from an IE)
        # no abs() in numerator since we want to preserve sign in the proportion
        self.money_out_resolved.loc[:, 'proportion'] = self.money_out_resolved.loc[:,
                                                       'amount'] / self.money_out_resolved.loc[:, 'amount'].abs().sum()
        # mark self as resolved
        self.pending_resolve = False
        self.has_resolved = True
        # print('Resolved with donations')
        return


class Candidate():

    def __init__(self):
        self.name = " "
        self.filer_id = " "
        self.party = " "
        self.type = ' '
        self.aliases = []  # stores list of synonyms when we combine_candidates
        self.total_in = 0.0
        self.money_in = pd.DataFrame(columns=["donor", "donor_id", "amount"])

    def __repr__(self):
        return "<Name:%s ID:%s money_in: %s>" % (self.name, self.filer_id, self.money_in['amount'].sum())

    def sum_donations(self):
        # group donations by donor so there is one line per donor with a total from that donor
        if (len(self.money_in) > 1):
            self.money_in = pd.DataFrame(self.money_in.groupby(['donor', 'donor_id']).sum()).reset_index()
        self.total_in = self.money_in['amount'].abs().sum()


class Data():
    def __init__(self):
        self.all_donors = {}  # list of all donors (ind and pac)
        self.all_candidates = {}  # list of all candidates
        self.party_pac_dict = {}  # map of pac names that are party organizations

    def sum_donations(self):
        for i in self.all_donors.keys():
            self.all_donors[i].sum_donations()
        for i in self.all_candidates.keys():
            self.all_candidates[i].sum_donations()

    def combine_candidates(self, cand_list, rename=False):
        # combine several Candidate() objects in self.all_candidates into a single Candidate()
        #
        # cand_list is a list of candidate names (strings) which are keys in self.all_candidates
        # rename = False uses first item in cand_list as name of the combined candidate
        # rename = text uses text as the new name
        #
        # make sure cand_list is a list
        if not isinstance(cand_list,list):
            if isinstance(cand_list, basestring):
                cand_list = [cand_list]
            else:
                raise ValueError('combine_candidates: cand_list should be string or list of strings')
        # remove duplicates
        cand_list = list(OrderedDict.fromkeys(cand_list))
        # if cand_list is length 1 this still works, it can rename a candidate and propogate that name change to donors
        # check if all strings in cand_list are valid keys in self.all_candidates
        if not set(cand_list).issubset(self.all_candidates.keys()):
            print('combine_candidates error: cand_list contains invalid key(s)')
            print(set(cand_list)-set(self.all_candidates.keys()))
            return
        # first item in donor_list will be the new key
        first_cand = self.all_candidates.pop(cand_list[0])
        new_cand = Candidate()
        new_cand.name = cand_list[0]
        if rename:
            new_cand.name = rename
        new_cand.aliases = cand_list
        new_cand.party = first_cand.party
        new_cand.type = first_cand.type  # could check that this matches the type of others in cand_list
        new_cand.filer_id = first_cand.filer_id
        new_cand.money_in = first_cand.money_in
        # if cand_list is length 1, this for loop will just be skipped, which is fine
        for i in cand_list[1:]:
            temp = self.all_candidates.pop(i)  # will raise error if i is not a valid key
            new_cand.money_in = new_cand.money_in.append(temp.money_in, ignore_index=True)
        # sum_donations again
        new_cand.sum_donations()  # this sum will erase if a donor made donations both for and against
        self.all_candidates[new_cand.name] = new_cand
        # Now we have to follow through to everyone in money_in and update them to the new candidate name
        all_givers = [x for x in new_cand.money_in['donor'] ]
        for i in all_givers:
            # for giver i, replace all occurences of cand_list with the new name
            for j in cand_list:
                self.all_donors[i].money_out.loc[self.all_donors[i].money_out.loc[:, 'receiver'] == j, 'receiver'] = new_cand.name
            self.all_donors[i].sum_donations()
        return


    def combine_donors(self, donor_list, rename = False):
        # remove duplicates
        donor_list = list(OrderedDict.fromkeys(donor_list))
        # make sure donor_list is a list
        if not isinstance(donor_list, list):
            if isinstance(donor_list, basestring):
                donor_list = [donor_list]
            else:
                raise ValueError('combine_donors: donor_list should be string or list of strings')
        # check if all strings in donor_list are valid keys in self.all_donors
        if not set(donor_list).issubset(self.all_donors.keys()):
            print('combine_donors warning: ignoring invalid key(s) in donor_list')
            print(set(donor_list)-set(self.all_donors.keys()))
            donor_list = list(set(donor_list)&set(self.all_donors.keys()))
            #TODO: check if donor_list is now empty; if so, we are not combining with a valid donor, so throw error and exit
        # first item in donor_list will be the new key
        first_donor = self.all_donors.pop(donor_list[0])
        new_donor = Donor()
        new_donor.name = donor_list[0]
        if rename:
            new_donor.name = rename
        new_donor.aliases = donor_list
        new_donor.type = first_donor.type
        new_donor.filer_id = first_donor.filer_id
        new_donor.money_in = first_donor.money_in
        new_donor.money_out = first_donor.money_out
        new_donor.has_resolved = False

        for i in donor_list[1:]:
            temp = self.all_donors.pop(i)  # will raise error if i is not a valid key
            new_donor.money_in = new_donor.money_in.append(temp.money_in, ignore_index=True)
            new_donor.money_out = new_donor.money_out.append(temp.money_out, ignore_index=True)
            # check if donor has established a type yet
            # when we get to a donor created by that donor's report in the original data (instead of created by
            # the receiver's report), then it will have a non-blank party
            if new_donor.type ==' ':
                new_donor.type = temp.type
        # Remove donors/receivers from money_in/money_out which are in donor_list, then sum_donations again
        new_donor.money_in = new_donor.money_in.loc[~new_donor.money_in.donor.isin(donor_list), :]
        new_donor.money_out = new_donor.money_out.loc[~new_donor.money_out.receiver.isin(donor_list), :]
        new_donor.sum_donations()
        self.all_donors[new_donor.name] = new_donor
        # Now we have to follow through to everyone in money_in and money_out and update them to the new donor name
        # first screen out any donations within the synonym set itself
        all_receivers = [x for x in new_donor.money_out['receiver'] if x not in donor_list]
        for i in all_receivers:
            if new_donor.money_out.loc[new_donor.money_out['receiver']==i,'type'].tolist()[0]=='Candidate':
                for j in donor_list:
                    self.all_candidates[i].money_in.loc[self.all_candidates[i].money_in.loc[:,'donor'] == j,'donor'] = new_donor.name
            else:
                for j in donor_list:
                    self.all_donors[i].money_in.loc[self.all_donors[i].money_in.loc[:,'donor'] == j,'donor'] = new_donor.name
        # now update this name for all donors to this entity
        # first screen out any donations within the synonym set itself
        all_givers = [x for x in new_donor.money_in['donor'] if x not in donor_list]
        for i in all_givers:
            # no candidates will be donors to this pac, so don't have to check type
            for j in donor_list:
                self.all_donors[i].money_out.loc[self.all_donors[i].money_out.loc[:, 'receiver'] == j, 'receiver'] = new_donor.name



def merge_ie_candidates(data_pac, data_ie):
    # change keys on all data_ie.all_candidates to match keys on data_pac.all_candidates
    # this will allow easier merging of the IE donors
    # for each key in ie, split at comma
    # if there is a number, add it to appropriate ballot measure data
    # otherwise, check for first and last name appearing in a pac key
    # if there is 1 and only 1, then change ie key to pac key
    # otherwise write to log file
    pass

def merge_ie_pac(donor_ie, data2, donor_key):
    # donor_ie is an IE donor (a Donor object)
    # data2 is a full dataset (a Data object) into which donor_ie will be merged
    # donor_key is the key in data2 to merge into - data2.all_donors[donor_key]
    #
    # ie data has no money_in, so just get donor_ie.money_out and merge with data2.all_donors[donor_key].money_out
    # then get all recipients donor_ie.money_out.loc[:,'receiver'] and update in data2.all_candidates
    #
    data2.all_donors[donor_key].money_out = data2.all_donors[donor_key].money_out.append(donor_ie.money_out, ignore_index=True)
    cand_receivers = [i for i in donor_ie.money_out['receiver'] if donor_ie.money_out['type']=='Candidate' ]
    ballot_receivers = [i for i in donor_ie.money_out['receiver'] if donor_ie.money_out['type'] == 'Ballot']
    # todo: make sure for statements skip quietly if iteration set is empty
    for i in cand_receivers:
        # check if candidate exists in data2.all_candidates - if so append donation
        # if not check synonym list
        # if in synonym list, find the right one and append it
        # if still can't find it, create it and add donation and print message or write to log file
        # data2.all_candidates.keys()
        # todo: code here
        pass
    for i in ballot_receivers:
        # check if pac exists in data2.all_donors - if so append donation
        # if not check synonym list
        # if in synonym list, find the right one and append it
        # if still can't find it, create it and add donation and write to log file
        # should scrutinize name closely - any ballot committee should already exist in the larger pac dataset,
        # might need to merge pacs if the name is not found
        # data2.all_donors.keys()
        # todo: code here
        pass


def wrapper_get_close_matches(word,possibilities,n=1,cutoff=0.7):
    temp = get_close_matches(word=word, possibilities=possibilities,n=n,cutoff=cutoff)
    if len(temp)==0:
        temp = ['No Match']
    return temp[0]

def resolved_to_dataframe(data,donor_list):
    # finds data.all_donors[i].money_out_resolved for all i in donor_list
    # adds a column of donor names and combines all of these into a dataframe to return
    #
    # check if donor_list is a list
    if not isinstance(donor_list, list):
        if isinstance(donor_list, basestring):
            donor_list = [donor_list]
        else:
            raise ValueError('combine_donors: donor_list should be string or list of strings')
    # check if all donor_list are valid keys
    if not set(donor_list).issubset(data.all_donors.keys()):
        print('resolved_to_dataframe: invalid donor values on donor_list')
        return
    # check if money_out_resolved exists for all donor_list
    if any([data.all_donors[i].money_out_resolved.empty for i in donor_list]):
        print('resolved_to_dataframe: money_out_resolved is empty for values of donor_list')
    data_out = pd.DataFrame()
    for i in donor_list:
        this_add = data.all_donors[i].money_out_resolved
        this_add['donor'] = i
        data_out = data_out.append(this_add, ignore_index=True)
    return data_out

################################
# JSON save and load functions

def save_to_json(data, filename = 'data.json'):
    with open(filename, "w") as write_file:
        json.dump(data, write_file)

def load_from_json(filename = 'data.json'):
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    return data

################################
# Pickle Save and Load functions for intermediate data
# Usage:
# save_to_file(data2,'data2.pkl')
# data2 = load_from_file('data2.pkl')
#

def save_to_pkl(data, filename='data.pkl'):
    # todo: check for valid filename
    pickle_out = open(filename, 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()
    print('Saved to file: ' + filename)


def load_from_pkl(filename='data.pkl'):
    pickle_in = open(filename, "rb")
    print('Loading from file: ' + filename)
    return pickle.load(pickle_in)


def load_ie_data(filename):
    # check if file exists, if so load it
    iedata = pd.read_csv(filename)
    # todo: screen out 2017 election year data (if needed, or just filter at source)
    # we can't screen by election year for ie data; they only report calendar year
    # we need to get all donations from 2017 which were used for 2018 election year
    # so we have to screen out spending which was done in 2017

    my_cols = ['origin', 'sponsor_id', 'sponsor_name', 'candidate_last_name', 'candidate_first_name', 'candidate_party',
               'ballot_name', 'ballot_number', 'portion_of_amount', 'for_or_against']
    # drop all columns except my_cols
    iedata = iedata[my_cols]
    # drop all rows except 'Identified Entities' rows
    iedata = iedata.loc[iedata.loc[:, 'origin'] == 'C6.3 - Identified Entities']  # better way to do this?
    print(iedata.shape)

    # convert the donation amount from str to float
    if is_string_dtype(iedata['portion_of_amount']):
        iedata['portion_of_amount'] = iedata['portion_of_amount'].str.replace(',', '').astype('float')
    # construct ballot name from number and name, stripping decimal from the float (if present).
    # note str.replace is regex by default and breaks if set to regex=False
    iedata['ballot_name_full'] = iedata['ballot_number'].astype('str').str.replace('\.0', '') + ', ' + iedata[
        'ballot_name']
    # construct full candidate name
    iedata['candidate_name_full'] = iedata['candidate_last_name'] + ', ' + iedata['candidate_first_name']

    # construct receiver type so we can tell candidates from other stuff
    iedata['receiver_type'] = 'Candidate'
    # if no candidate name, then assume it is ballot measure
    iedata.loc[iedata.loc[:, 'candidate_name_full'].isnull(), 'receiver_type'] = 'Ballot'
    # if ballot name is missing but there is a ballot number, then use ballot number as the name (this has been observed to happen)
    iedata.loc[
        iedata.loc[:, 'ballot_name_full'].isnull() & iedata.loc[:, 'ballot_number'].notnull(), 'ballot_name_full'] = \
        iedata.loc[
            iedata.loc[:, 'ballot_name_full'].isnull() & iedata.loc[:,
                                                         'ballot_number'].notnull(), 'ballot_number'].astype(
            'str').str.replace('\.0', '')+','
    data1 = Data()
    n_rows = iedata.shape[0]
    for i in range(n_rows):
        this_row = iedata.iloc[i,]
        this_giver_name = this_row["sponsor_name"]
        this_giver_id = this_row["sponsor_id"]
        if pd.isna(this_giver_id):
            raise ValueError('IE sponsor_id should not be missing')
        if this_row['receiver_type'] == 'Candidate':
            this_receiver_name = this_row['candidate_name_full']
        elif this_row['receiver_type'] == 'Ballot':
            this_receiver_name = this_row['ballot_name_full']
        else:
            raise ValueError('receiver_type must be candidate or ballot')

        this_receiver_party = this_row['candidate_party']  # this will be NaN for ballot measures
        if pd.isna(this_receiver_party):
            if this_row['receiver_type'] == 'Candidate':
                this_receiver_party = 'Missing'
            elif this_row['receiver_type'] == 'Ballot':
                this_receiver_party = 'Ballot'
            else:
                this_receiver_party = 'None'

        this_amount = this_row["portion_of_amount"]
        if this_row["for_or_against"] == "Against":
            this_amount = -this_amount
        this_receiver_type = this_row['receiver_type']

        # check if candidate already exists
        if this_receiver_name in data1.all_candidates:
            # if so, add to that candidate data
            # this_cand = data1.all_candidates[this_receiver_name]
            this_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                    columns=['donor', 'donor_id', 'amount'])
            data1.all_candidates[this_receiver_name].money_in = data1.all_candidates[
                this_receiver_name].money_in.append(this_add, ignore_index=True)
        # todo: check that this_cand.party = this_receiver_party
        # what to do if they are different?
        # data1.all_candidates[this_receiver_name].party = this_receiver_party

        else:
            # create new candidate and add to data
            new_cand = Candidate()
            new_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                   columns=['donor', 'donor_id', 'amount'])
            new_cand.money_in = new_cand.money_in.append(new_add, ignore_index=True)
            new_cand.name = this_receiver_name
            new_cand.type = this_receiver_type
            new_cand.party = this_receiver_party
            data1.all_candidates[this_receiver_name] = new_cand

        # check if donor already exists
        if this_giver_name in data1.all_donors:
            # if so, add to that donor data
            this_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                    columns=["receiver", "amount", "party", "type"])
            data1.all_donors[this_giver_name].money_out = data1.all_donors[this_giver_name].money_out.append(this_add, ignore_index=True)
        else:
            # create new donor and add them
            new_donor = Donor()
            new_donor.name = this_giver_name
            new_donor.filer_id = this_giver_id
            new_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                   columns=["receiver", "amount", "party", "type"])
            new_donor.money_out = new_donor.money_out.append(new_add, ignore_index=True)
            data1.all_donors[this_giver_name] = new_donor

    return data1


def load_pac_data(filename, nrows=0, debug=True, name_dict = {}):
    # filename is the name of the data file to load
    # nrows: if 0, load all data; if >0, only load first nrows
    # check if file exists, if so load it
    # candidate and PAC donations
    campdata = pd.read_csv(filename)
    # note ignore mixed type warnings on columns 11, 23 since we do not use them
    my_cols = ['filer_id', 'type', 'filer_name', 'party', 'ballot_number', 'for_or_against', 'amount', 'code',
               'contributor_name', 'contributor_address', 'contributor_city', 'contributor_zip']
    campdata = campdata[my_cols]
    if debug:
        print(campdata.shape)
    # note filer_id values in this file do not match the filer_id values in the IE data file
    # the for_or_against value is merely descriptive of ballot committees here, it does not indicate spending against a candidate
    # convert amount str to float
    if is_string_dtype(campdata['amount']):
        campdata['amount'] = campdata['amount'].str.replace(',', '').astype('float')

    # exclude rows with amount <= 0
    campdata = campdata.loc[(campdata.loc[:, 'amount'] > 0), :]
    if debug:
        print(campdata.shape)

    # drop rows from Individual donors (for now, since interest is mostly in PACs)
    # TODO: include individuals with notably large donations, e.g. over $20,000
    campdata = campdata.loc[(campdata.loc[:, 'code'] != 'Individual'), :]
    print(campdata.shape)

    # TODO: Correct party affiliations to align candidates with their caucus: Tim Sheldon R, Rodney Tom R, etc.
    # This is being done manually for now

    # compute number of rows to load
    nrows = int(nrows)
    if nrows==0:
        nrows = campdata.shape[0]
    if nrows>campdata.shape[0]:
        print('Loading full data set')
        nrows = campdata.shape[0]

    # convert names using synonym dictionary
    if name_dict:
        # could probably do this faster by iterating through name_dict.keys() instead of through nrows
        for i in range(nrows):
            this_row = campdata.iloc[i,]
            this_giver_name = this_row["contributor_name"]
            this_receiver_name = this_row['filer_name']
            if this_giver_name in name_dict.keys():
                col_index = campdata.columns.get_loc('contributor_name')
                campdata.iloc[i, col_index] = name_dict[this_giver_name]
            if this_receiver_name in name_dict.keys():
                col_index = campdata.columns.get_loc('filer_name')
                campdata.iloc[i,col_index] = name_dict[this_receiver_name]

    start = time.time()

    print(start)
    print(nrows)

    data2 = Data()

    print('Meow')

    for i in range(nrows):
        this_row = campdata.iloc[i,]
        this_giver_name = this_row["contributor_name"]
        # this_giver_address = this_row['contributor_address']
        # this_giver_city = this_row['contributor_city']
        # this_giver_zip = this_row['contributor_zip']
        this_receiver_id = this_row['filer_id']
        this_receiver_name = this_row['filer_name']
        this_receiver_type = this_row['type']
        if pd.isna(this_receiver_type):
            this_receiver_type = 'None'
        this_receiver_party = this_row['party']
        # this_receiver_party will be NaN for ballot measures and PACs, and the nans can break stuff
        if pd.isna(this_receiver_party):
            this_receiver_party = 'None'
        this_amount = float(this_row['amount'])
        this_giver_id = 'None'  # donor id is not provided in this data

        if this_receiver_type == 'Candidate':
            # check if we have seen this candidate before
            if this_receiver_name in data2.all_candidates:
                # if so, add to that candidate data
                this_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                        columns=['donor', 'donor_id', 'amount'])
                data2.all_candidates[this_receiver_name].money_in = data2.all_candidates[
                    this_receiver_name].money_in.append(this_add, ignore_index=True)
            # todo: check that this_cand.party = this_receiver_party
            # data2.all_candidates[this_receiver_id] = this_cand
            else:
                # create new candidate and add to data
                new_cand = Candidate()
                new_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                       columns=['donor', 'donor_id', 'amount'])
                new_cand.money_in = new_cand.money_in.append(new_add, ignore_index=True)
                new_cand.name = this_receiver_name
                new_cand.type = this_receiver_type
                new_cand.party = this_receiver_party
                # add new_cand to the dictionary
                data2.all_candidates[this_receiver_name] = new_cand
            # now process the donor to this candidate
            # check if donor already exists
            if this_giver_name in data2.all_donors:
                # if so, add to that donor data
                this_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                        columns=["receiver", "amount", "party", "type"])
                data2.all_donors[this_giver_name].money_out = data2.all_donors[this_giver_name].money_out.append(
                    this_add, ignore_index=True)
            else:
                # create new donor and add
                new_donor = Donor()
                new_donor.name = this_giver_name
                # new_donor.filer_id = this_giver_id #no donor id from C3 data
                new_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                       columns=["receiver", "amount", "party", "type"])
                new_donor.money_out = new_donor.money_out.append(new_add, ignore_index=True)
                data2.all_donors[this_giver_name] = new_donor
        else:  # receiver type is not Candidate, should only be Political Committee
            # check if we have seen this pac before (maybe as a donor) and update data
            if this_receiver_name in data2.all_donors:
                this_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                        columns=['donor', 'donor_id', 'amount'])
                data2.all_donors[this_receiver_name].money_in = data2.all_donors[this_receiver_name].money_in.append(
                    this_add, ignore_index=True)
                # if we have only seen this pac before as a donor, then we don't have a value for type and filer_id
                if data2.all_donors[this_receiver_name].type != this_receiver_type:
                    data2.all_donors[this_receiver_name].type = this_receiver_type
                    data2.all_donors[this_receiver_name].filer_id = this_receiver_id
            else:
                # create new pac and add to data
                new_pac = Donor()
                new_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                       columns=['donor', 'donor_id', 'amount'])
                new_pac.money_in = new_pac.money_in.append(new_add, ignore_index=True)
                new_pac.name = this_receiver_name
                new_pac.type = this_receiver_type
                new_pac.filer_id = this_receiver_id
                data2.all_donors[this_receiver_name] = new_pac
            # now process the donors to this donor/pac
            # check if donor already exists
            if this_giver_name in data2.all_donors:
                # if so, add to that donor data
                this_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                        columns=["receiver", "amount", "party", "type"])
                data2.all_donors[this_giver_name].money_out = data2.all_donors[this_giver_name].money_out.append(
                    this_add, ignore_index=True)
            else:
                # create new donor and add
                new_donor = Donor()
                new_donor.name = this_giver_name
                # new_donor.filer_id = this_giver_id #no donor id from C3 data
                new_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                       columns=["receiver", "amount", "party", "type"])
                new_donor.money_out = new_donor.money_out.append(new_add, ignore_index=True)
                data2.all_donors[this_giver_name] = new_donor
    end = time.time()
    if debug:
        print(end - start)
        print(len(data2.all_donors.keys()))
    return data2

    

def main_load(file_ie, file_pac):
    donor_synonym_dict = {}  # dict of synonym:main_name for donors
    donor_synonym_dict = do_pac_synonyms2(donor_synonym_dict)
    data_ie = load_ie_data(file_ie)
    data_pac = load_pac_data(file_pac,name_dict=donor_synonym_dict)
    data_ie.sum_donations()
    data_pac.sum_donations()
    
    print("Make manual corrections")
    pac_correction(data_pac)
    ie_correction(data_ie)

    do_ie_synonyms(data_ie)

    data_ie.sum_donations()
    data_pac.sum_donations()

    print('Converting data_ie.all_candidates.keys() to match data_pac.all_candidates.keys()')
    oldname = [i for i in data_ie.all_candidates.keys() if not any(char.isdigit() for char in i)]
    newname = [wrapper_get_close_matches(i, data_pac.all_candidates.keys()) for i in oldname]
    cand_change = pd.DataFrame.from_items([('oldnames', oldname), ('newnames', newname)])
    # Write out a log file of all the matches.  Cases with 'No Match' will be dropped.
    # All cases must be manually verified for accuracy and manually fixed (e.g. William Colyer != William Cooper)
    f = open("log-candidate name matching IE to PAC.txt", "w")
    for i in range(len(cand_change.oldnames)):
        f.write("%s\n" % [cand_change.iloc[i, :][0], cand_change.iloc[i, :][1]])
    f.close()
    # manual fix for Colyer/Cooper
    cand_change.newnames.loc[cand_change.newnames == 'COOPER WILLIAM T'] = 'No Match'
    # drop cases with no match - these are usually local candidates using mini-reporting with only small IE donations
    cand_change = cand_change.loc[cand_change.newnames != 'No Match', :]
    # update the key names using combine_candidates
    for i in range(len(cand_change.oldnames)):
        data_ie.combine_candidates([cand_change.iloc[i, :].oldnames], rename=cand_change.iloc[i, :].newnames)
    # now the candidate names/keys in data_ie match the ones in data_pac

    print('Finding matches between data_ie.all_donors.keys() and data_pac.all_donors.keys()')
    oldname = data_ie.all_donors.keys()
    newname = [wrapper_get_close_matches(i, data_pac.all_donors.keys()) for i in oldname]
    # donor_change is a map from oldnames (in data_ie) to newnames (in data_pac)
    donor_change = pd.DataFrame.from_items([('oldnames', oldname), ('newnames', newname)])
    # manually fix some of the mistakes made by the automated method
    temp = [i for i in data_ie.all_donors.keys() if i.find('ENTERPRISE WA') >= 0]
    for i in temp:
        donor_change.newnames.loc[donor_change.oldnames == i] = 'ENTERPRISE WASHINGTON'
    donor_change.newnames.loc[donor_change.oldnames == 'MARATHON PETROLEM CORP SUBSIDIARY ANDEAVOR LLC'] = 'ANDEAVOR'
    donor_change.newnames.loc[
        donor_change.oldnames == 'NRA POLITICAL VICTORY FUND'] = 'NATIONAL RIFLE ASSOCIATION OF AMERICA'
    donor_change.newnames.loc[donor_change.oldnames == 'WA EDUCATION ASSN PAC'] = 'WASHINGTON EDUCATION ASSOCIATION'
    donor_change.newnames.loc[
        donor_change.oldnames == 'WASHINGTON REALTORS POLITICAL ACTION COMMITTEE'] = 'WA REALTORS PAC'
    donor_change.newnames.loc[donor_change.oldnames == 'FRIENDS OF ELAINE PHELPS'] = 'No Match'
    donor_change.newnames.loc[donor_change.oldnames == 'WA FORWARD'] = 'WA FORWARD (THE LEADERSHIP COUNCIL)'
    donor_change.newnames.loc[donor_change.oldnames == 'BUILDING INDUSTRY ASSOCIATION OF CLARK COUNTY BUILDING INDUSTRY GROUP'] = 'BUILDING INDUSTRY ASSOCIATION'
    # write out the mapping for further manual inspection
    f = open("log-donor name matching IE to PAC.txt", "w")
    for i in range(len(donor_change.oldnames)):
        f.write("%s\n" % [donor_change.iloc[i, :][0], donor_change.iloc[i, :][1]])
    f.close()
    # now data_ie.all_candidates.keys() are consistent with data_pac.all_candidates except ballot measures
    # and we have a map of data_ie.all_donors.keys() to keys in data_pac.all_donors.keys()

    #####
    # Merge the IE candidates data into the PAC candidates data
    # for each candidate in data_ie,
    # we append its money_in to the corresponding candidate in data_pac, correcting the donor names as we go
    # and update each donor in data_pac with the donation
    # TODO: maybe more efficient to change the approach here to use a dictionary instead of dataframe (see donor_old_to_new below)
    for i in cand_change.newnames:
        print(i)
        this_donors = data_ie.all_candidates[i].money_in.donor.copy()
        this_name = data_ie.all_candidates[i].name
        this_party = data_ie.all_candidates[i].party
        this_type = data_ie.all_candidates[i].type
        # if there is only one donor, it will return as a string, so convert to a list to use with the for statement
        if isinstance(this_donors, basestring):
            this_donors2 = [this_donors]
        else:
            this_donors2 = this_donors  # doing this to avoid the setting with copy warning on this_donors
        # for each donor in this candidate's money_in:
        for j in this_donors2:
            # get the amount from donor j to candidate i
            this_amount = data_ie.all_candidates[i].money_in.amount.loc[this_donors == j].values[0]
            # get the new pac donor name
            new_donor = donor_change.newnames.loc[donor_change.oldnames == j].values[0]
            # change the old ie donor name to the new pac donor name
            # TODO: Next line gives "set on copy of slice" warning.  Tested and it works.  How to avoid warning?
            data_ie.all_candidates[i].money_in.donor.loc[this_donors2 == j] = new_donor
            # if the new name is 'No Match' then this donor is not in data_pac;
            # so don't update data_pac, give a log message showing amount, and after for loop, drop the no match rows
            if new_donor == 'No Match':
                print('No Match - skipped:')
                print(j)
                print(this_amount)
            else:
                # update the donor's money_out with this candidate
                this_add = pd.DataFrame([[this_name, this_amount, this_party, this_type]],
                                              columns=["receiver", "amount", "party", "type"])
                data_pac.all_donors[new_donor].money_out = data_pac.all_donors[
                                new_donor].money_out.append(this_add, ignore_index=True)
        # drop the no match rows
        data_ie.all_candidates[i].money_in = data_ie.all_candidates[i].money_in.loc[
            data_ie.all_candidates[i].money_in.donor != 'No Match', :]
        # append ie candidate's updated money_in to the pac candidate's money_in
        data_pac.all_candidates[i].money_in = data_pac.all_candidates[i].money_in.append(
            data_ie.all_candidates[i].money_in, ignore_index=True)

    # Merge the IE initiative groups in to the PAC initiative groups
    # Combine initiative groups into single group for or against each initiative
    data_pac.combine_donors(donor_list=['DE-ESCALATE WA I-940'], rename='FOR 940')
    data_pac.combine_donors(donor_list=['COPS AGAINST I-940  WA COUNCIL OF POLICE & SHERIFFS', 'COALITION FOR A SAFER WA'],
                                                rename='AGAINST 940')
    data_pac.combine_donors(donor_list=['CLEAN AIR CLEAN ENERGY WA'], rename='FOR 1631')
    data_pac.combine_donors(donor_list=['NO ON 1631',
                                        'NO ON 1631 (SPONSORED BY WESTERN STATES PETROLEUM ASSN)',
                                         'I-1631 SPONSORED BY ASSOC OF WA BUSINESS'], rename='AGAINST 1631')
    data_pac.combine_donors(donor_list=['YES! TO AFFORDABLE GROCERIES (SEE EMAIL FOR REST OF NAME)'], rename='FOR 1634')
    data_pac.combine_donors(donor_list=['HEALTHY KIDS COALITION'], rename='AGAINST 1634')
    data_pac.combine_donors(donor_list=['SAFE SCHOOLS SAFE COMMUNITIES'], rename='FOR 1639')
    data_pac.combine_donors(donor_list=['STOP 1639 - SPONSOR SHALL NOT BE INFRINGED', 'SHALL NOT BE INFRINGED',
                                        'SAVE OUR SECURITY NO ON I-1639',
                                        'WASHINGTONIANS AND THE NATIONAL RIFLE ASSN FOR FREEDOM'],rename='AGAINST 1639')
    donor_old_to_new = dict(zip(donor_change.oldnames, donor_change.newnames))
    donor_new_to_old = dict(zip(donor_change.newnames, donor_change.oldnames))

    this_ie_label_list = ['940', '1631', '1634', '1639']
    this_pac_label_dict = {'940': ['FOR 940', 'AGAINST 940'],
                           '1631': ['FOR 1631', 'AGAINST 1631'],
                           '1634': ['FOR 1634', 'AGAINST 1634'],
                           '1639': ['FOR 1639', 'AGAINST 1639']}
    for this_ie_label in this_ie_label_list:
        this_pac_label = this_pac_label_dict[this_ie_label]
        # get positive (for) rows and negative (against) rows and put them in the appropriate places, converting donor names too
        for i in range(len(data_ie.all_candidates[this_ie_label].money_in)):
            this_row = data_ie.all_candidates[this_ie_label].money_in.iloc[i, :]
            this_donor = this_row.donor
            this_donor_id = this_row.donor_id
            this_amount = this_row.amount
            # convert old (IE) name to new (PAC) name
            this_donor = donor_old_to_new[this_donor]
            # skip any donors that have no match in PAC data
            if this_donor != 'No Match':
                if this_amount >= 0:
                    this_add = pd.DataFrame([[this_donor, this_donor_id, this_amount]],
                                            columns=['donor', 'donor_id', 'amount'])
                    data_pac.all_donors[this_pac_label[0]].money_in = data_pac.all_donors[
                        this_pac_label[0]].money_in.append(this_add, ignore_index=True)
                else:
                    # convert negative spend to a positive contribution to the Against side
                    this_amount = this_amount * (-1)
                    this_add = pd.DataFrame([[this_donor, this_donor_id, this_amount]],
                                                columns=['donor', 'donor_id', 'amount'])
                    data_pac.all_donors[this_pac_label[1]].money_in = data_pac.all_donors[
                            this_pac_label[1]].money_in.append(this_add, ignore_index=True)

    # mark all party organizations with their party so donor percentages reflect their party
    data_pac.party_pac_dict = {'WA STATE DEMOCRATIC PARTY':'DEMOCRAT',
                               'WA STATE REPUBLICAN PARTY': 'REPUBLICAN',
                               'LOCAL DEMOCRATIC ORGS':'DEMOCRAT',
                               'LOCAL REPUBLICAN ORGS': 'REPUBLICAN',
                               'SENATE REPUBLICAN CAMPAIGN COMMITTEE': 'REPUBLICAN',
                               'HOUSE REPUBLICAN ORGANIZATION COMMITTEE': 'REPUBLICAN',
                               'HOUSE DEMOCRATIC CAUCUS CAMPAIGN COMMITTEE':'DEMOCRAT',
                               'WASHINGTON SENATE DEMOCRATIC CAMPAIGN':'DEMOCRAT',
                               'HARRY TRUMAN FUND':'DEMOCRAT',
                               'REAGAN FUND': 'REPUBLICAN',
                               'KENNEDY FUND':'DEMOCRAT',
                               'THE LEADERSHIP COUNCIL': 'REPUBLICAN',
                               'MAINSTREAM REPUB OF WA ST PAC': 'REPUBLICAN'}

    donors_interest = ['WA REALTORS PAC',
                           'COCA COLA NORTH AMERICA',
                           'PEPSI COLA NW BUSINESS UNIT',
                           'DR PEPPER SNAPPLE GROUP',
                           'ANHEUSER BUSCH CO.',
                           'BOEING COMPANY',
                           'BOEING EMPLOYEES CREDIT UNION',
                           'ANDEAVOR',
                           'PHILLIPS 66',
                           'AMERICAN FUEL AND PETROCHEMICAL MANUFACTURERS',
                           'BP AMERICA',
                           'BP AMERICA EMPLOYEE PAC',
                           'WEYERHAEUSER CO',
                           'KOCH INDUSTRIES, INC.',
                           'WASHINGTON EDUCATION ASSOCIATION',
                           'MUCKLESHOOT INDIAN TRIBE']

    # for i in data_pac.all_donors.keys(): # for processing all donors
    for i in donors_interest:
        data_pac.all_donors[i].resolve_donations(data_pac)
        
    return data_pac
    
def IEnPAC_to_csv(fname_ie, fname_pac, configuration):
    
    # use yaml to load config into dictionary and pass params accordingly
    # also contains a link to another file of synonyms

    filename_IE = fname_ie
    filename_pac = fname_pac

    data = main_load(filename_IE, filename_pac)

    # live in docker
    transactions = []
    for donor in data.all_donors.keys():
        if data.all_donors[donor].has_resolved:
            df_recipients = data.all_donors[donor].money_out_resolved
            df_recipients = df_recipients.set_index(['receiver'])
            for recipient in df_recipients.index.values.tolist():
                transactions.append((donor, recipient, df_recipients.ix[recipient]['amount']))

    df = pd.DataFrame(transactions)
    return df


if __name__ == '__main__':
    print("Running Main")

    filename_IE = 'data\Independent_Campaign_Expenditures_and_Electioneering_Communications20181110.csv'
    filename_pac = 'data\Contributions_to_Candidates_and_Political_Committees20181110.csv'

    # data_final = main_load(filename_IE, filename_pac)

    
    print('Generate synonym dictionary')
    start = time.time()
    donor_synonym_dict = {}  # dict of synonym:main_name for donors
    donor_synonym_dict = do_pac_synonyms2(donor_synonym_dict)
    end = time.time()
    print(end - start)

    print("Read in and process IE data")
    data_ie = load_ie_data('data\Independent_Campaign_Expenditures_and_Electioneering_Communications20181110.csv')

    print("Read in and process PAC/Candidate data")
    print('If there is a DtypeWarning about columns (11,23) we can ignore it')
    data_pac = load_pac_data('data\Contributions_to_Candidates_and_Political_Committees20181110.csv',
                             name_dict=donor_synonym_dict)
    #data_pac = load_pac_data('data\small test data.csv')

    print("Sum donations (multiple donations from a donor to a receiver are summed)")
    data_ie.sum_donations()
    data_pac.sum_donations()

    print("Make manual corrections")
    pac_correction(data_pac)
    ie_correction(data_ie)

    print('Combine entities which are actually synonyms of a single entity')
    start = time.time()
    do_ie_synonyms(data_ie)
    end = time.time()
    print(end - start)

    print("Sum donations again")
    data_ie.sum_donations()
    data_pac.sum_donations()

    print('Converting data_ie.all_candidates.keys() to match data_pac.all_candidates.keys()')
    oldname = [i for i in data_ie.all_candidates.keys() if not any(char.isdigit() for char in i)]
    newname = [wrapper_get_close_matches(i, data_pac.all_candidates.keys()) for i in oldname]
    cand_change = pd.DataFrame.from_items([('oldnames', oldname), ('newnames', newname)])
    # Write out a log file of all the matches.  Cases with 'No Match' will be dropped.
    # All cases must be manually verified for accuracy and manually fixed (e.g. William Colyer != William Cooper)
    f = open("log-candidate name matching IE to PAC.txt", "w")
    for i in range(len(cand_change.oldnames)):
        f.write("%s\n" % [cand_change.iloc[i, :][0], cand_change.iloc[i, :][1]])
    f.close()
    # manual fix for Colyer/Cooper
    cand_change.newnames.loc[cand_change.newnames == 'COOPER WILLIAM T'] = 'No Match'
    # drop cases with no match - these are usually local candidates using mini-reporting with only small IE donations
    cand_change = cand_change.loc[cand_change.newnames != 'No Match', :]
    # update the key names using combine_candidates
    for i in range(len(cand_change.oldnames)):
        data_ie.combine_candidates([cand_change.iloc[i, :].oldnames], rename=cand_change.iloc[i, :].newnames)
    # now the candidate names/keys in data_ie match the ones in data_pac

    print('Finding matches between data_ie.all_donors.keys() and data_pac.all_donors.keys()')
    oldname = data_ie.all_donors.keys()
    newname = [wrapper_get_close_matches(i, data_pac.all_donors.keys()) for i in oldname]
    # donor_change is a map from oldnames (in data_ie) to newnames (in data_pac)
    donor_change = pd.DataFrame.from_items([('oldnames', oldname), ('newnames', newname)])
    # manually fix some of the mistakes made by the automated method
    temp = [i for i in data_ie.all_donors.keys() if i.find('ENTERPRISE WA') >= 0]
    for i in temp:
        donor_change.newnames.loc[donor_change.oldnames == i] = 'ENTERPRISE WASHINGTON'
    donor_change.newnames.loc[donor_change.oldnames == 'MARATHON PETROLEM CORP SUBSIDIARY ANDEAVOR LLC'] = 'ANDEAVOR'
    donor_change.newnames.loc[
                    donor_change.oldnames == 'NRA POLITICAL VICTORY FUND'] = 'NATIONAL RIFLE ASSOCIATION OF AMERICA'
    donor_change.newnames.loc[donor_change.oldnames == 'WA EDUCATION ASSN PAC'] = 'WASHINGTON EDUCATION ASSOCIATION'
    donor_change.newnames.loc[
                    donor_change.oldnames == 'WASHINGTON REALTORS POLITICAL ACTION COMMITTEE'] = 'WA REALTORS PAC'
    donor_change.newnames.loc[donor_change.oldnames == 'FRIENDS OF ELAINE PHELPS'] = 'No Match'
    donor_change.newnames.loc[donor_change.oldnames == 'WA FORWARD'] = 'WA FORWARD (THE LEADERSHIP COUNCIL)'
    donor_change.newnames.loc[donor_change.oldnames == 'BUILDING INDUSTRY ASSOCIATION OF CLARK COUNTY BUILDING INDUSTRY GROUP'] = 'BUILDING INDUSTRY ASSOCIATION'
    # write out the mapping for further manual inspection
    f = open("log-donor name matching IE to PAC.txt", "w")
    for i in range(len(donor_change.oldnames)):
        f.write("%s\n" % [donor_change.iloc[i, :][0], donor_change.iloc[i, :][1]])
    f.close()
    # now data_ie.all_candidates.keys() are consistent with data_pac.all_candidates except ballot measures
    # and we have a map of data_ie.all_donors.keys() to keys in data_pac.all_donors.keys()

    #####
    # Merge the IE candidates data into the PAC candidates data
    # for each candidate in data_ie,
    # we append its money_in to the corresponding candidate in data_pac, correcting the donor names as we go
    # and update each donor in data_pac with the donation
    # TODO: maybe more efficient to change the approach here to use a dictionary instead of dataframe (see donor_old_to_new below)
    for i in cand_change.newnames:
        print(i)
        this_donors = data_ie.all_candidates[i].money_in.donor.copy()
        this_name = data_ie.all_candidates[i].name
        this_party = data_ie.all_candidates[i].party
        this_type = data_ie.all_candidates[i].type
        # if there is only one donor, it will return as a string, so convert to a list to use with the for statement
        if isinstance(this_donors, basestring):
            this_donors2 = [this_donors]
        else:
            this_donors2 = this_donors  # doing this to avoid the setting with copy warning on this_donors
        # for each donor in this candidate's money_in:
        for j in this_donors2:
            # get the amount from donor j to candidate i
            this_amount = data_ie.all_candidates[i].money_in.amount.loc[this_donors == j].values[0]
            # get the new pac donor name
            new_donor = donor_change.newnames.loc[donor_change.oldnames == j].values[0]
            # change the old ie donor name to the new pac donor name
            # TODO: Next line gives "set on copy of slice" warning.  Tested and it works.  How to avoid warning?
            data_ie.all_candidates[i].money_in.donor.loc[this_donors2 == j] = new_donor
            # if the new name is 'No Match' then this donor is not in data_pac;
            # so don't update data_pac, give a log message showing amount, and after for loop, drop the no match rows
            if new_donor == 'No Match':
                print('No Match - skipped:')
                print(j)
                print(this_amount)
            else:
                # update the donor's money_out with this candidate
                this_add = pd.DataFrame([[this_name, this_amount, this_party, this_type]],
                                        columns=["receiver", "amount", "party", "type"])
                data_pac.all_donors[new_donor].money_out = data_pac.all_donors[
                    new_donor].money_out.append(this_add, ignore_index=True)
        # drop the no match rows
        data_ie.all_candidates[i].money_in = data_ie.all_candidates[i].money_in.loc[
                                             data_ie.all_candidates[i].money_in.donor != 'No Match', :]
        # append ie candidate's updated money_in to the pac candidate's money_in
        data_pac.all_candidates[i].money_in = data_pac.all_candidates[i].money_in.append(
            data_ie.all_candidates[i].money_in, ignore_index=True)

    # Merge the IE initiative groups in to the PAC initiative groups
    # Combine initiative groups into single group for or against each initiative
    data_pac.combine_donors(donor_list=['DE-ESCALATE WA I-940'], rename='FOR 940')
    data_pac.combine_donors(
        donor_list=['COPS AGAINST I-940  WA COUNCIL OF POLICE & SHERIFFS', 'COALITION FOR A SAFER WA'],
        rename='AGAINST 940')
    data_pac.combine_donors(donor_list=['CLEAN AIR CLEAN ENERGY WA'], rename='FOR 1631')
    data_pac.combine_donors(donor_list=['NO ON 1631',
                                        'NO ON 1631 (SPONSORED BY WESTERN STATES PETROLEUM ASSN)',
                                        'I-1631 SPONSORED BY ASSOC OF WA BUSINESS'], rename='AGAINST 1631')
    data_pac.combine_donors(donor_list=['YES! TO AFFORDABLE GROCERIES (SEE EMAIL FOR REST OF NAME)'], rename='FOR 1634')
    data_pac.combine_donors(donor_list=['HEALTHY KIDS COALITION'], rename='AGAINST 1634')
    data_pac.combine_donors(donor_list=['SAFE SCHOOLS SAFE COMMUNITIES'], rename='FOR 1639')
    data_pac.combine_donors(donor_list=['STOP 1639 - SPONSOR SHALL NOT BE INFRINGED', 'SHALL NOT BE INFRINGED',
                                        'SAVE OUR SECURITY NO ON I-1639',
                                        'WASHINGTONIANS AND THE NATIONAL RIFLE ASSN FOR FREEDOM'],
                            rename='AGAINST 1639')
    donor_old_to_new = dict(zip(donor_change.oldnames, donor_change.newnames))
    donor_new_to_old = dict(zip(donor_change.newnames, donor_change.oldnames))

    this_ie_label_list = ['940', '1631', '1634', '1639']
    this_pac_label_dict = {'940': ['FOR 940', 'AGAINST 940'],
                           '1631': ['FOR 1631', 'AGAINST 1631'],
                           '1634': ['FOR 1634', 'AGAINST 1634'],
                           '1639': ['FOR 1639', 'AGAINST 1639']}
    for this_ie_label in this_ie_label_list:
        this_pac_label = this_pac_label_dict[this_ie_label]
        # get positive (for) rows and negative (against) rows and put them in the appropriate places, converting donor names too
        for i in range(len(data_ie.all_candidates[this_ie_label].money_in)):
            this_row = data_ie.all_candidates[this_ie_label].money_in.iloc[i, :]
            this_donor = this_row.donor
            this_donor_id = this_row.donor_id
            this_amount = this_row.amount
            # convert old (IE) name to new (PAC) name
            this_donor = donor_old_to_new[this_donor]
            # skip any donors that have no match in PAC data
            if this_donor != 'No Match':
                if this_amount >= 0:
                    this_add = pd.DataFrame([[this_donor, this_donor_id, this_amount]],
                                            columns=['donor', 'donor_id', 'amount'])
                    data_pac.all_donors[this_pac_label[0]].money_in = data_pac.all_donors[
                        this_pac_label[0]].money_in.append(this_add, ignore_index=True)
                else:
                    # convert negative spend to a positive contribution to the Against side
                    this_amount = this_amount * (-1)
                    this_add = pd.DataFrame([[this_donor, this_donor_id, this_amount]],
                                            columns=['donor', 'donor_id', 'amount'])
                    data_pac.all_donors[this_pac_label[1]].money_in = data_pac.all_donors[
                        this_pac_label[1]].money_in.append(this_add, ignore_index=True)

    # mark all party organizations with their party so donor percentages reflect their party
    data_pac.party_pac_dict = {'WA STATE DEMOCRATIC PARTY':'DEMOCRAT',
                               'WA STATE REPUBLICAN PARTY': 'REPUBLICAN',
                               'LOCAL DEMOCRATIC ORGS':'DEMOCRAT',
                               'LOCAL REPUBLICAN ORGS': 'REPUBLICAN',
                               'SENATE REPUBLICAN CAMPAIGN COMMITTEE': 'REPUBLICAN',
                               'HOUSE REPUBLICAN ORGANIZATION COMMITTEE': 'REPUBLICAN',
                               'HOUSE DEMOCRATIC CAUCUS CAMPAIGN COMMITTEE':'DEMOCRAT',
                               'WASHINGTON SENATE DEMOCRATIC CAMPAIGN':'DEMOCRAT',
                               'HARRY TRUMAN FUND':'DEMOCRAT',
                               'REAGAN FUND': 'REPUBLICAN',
                               'KENNEDY FUND':'DEMOCRAT',
                               'THE LEADERSHIP COUNCIL': 'REPUBLICAN',
                               'MAINSTREAM REPUB OF WA ST PAC': 'REPUBLICAN'}

    print("Resolve donations to track all donations through to final candidate/ballot issue (selected entities only)")

    donors_interest = make_donors_interest()

    start = time.time()
    #save_to_json(data_pac.all_donors, 'data_pac.json')
    end = time.time()
    print(end - start)

    start = time.time()
    #data_pac2 = load_from_json('data_pac.json')
    end = time.time()
    print(end - start)

    start = time.time()
    # for i in data_pac.all_donors.keys(): # for processing all donors
    if donors_interest:
        for i in donors_interest:
            data_pac.all_donors[i].resolve_donations(data_pac)
    end = time.time()
    print(end - start)

    print('Done')
    # print('Example of money spent by one donor:')
    # print(data_pac.all_donors['WA REALTORS PAC'].money_out)
    print(data_pac.all_donors['WA REALTORS PAC'].money_out_resolved)

    # save_to_file(data_pac, 'data_pac.pkl')

    # todo: don't let negative IE spending offset positive spending on a candidate

    # [d.name, d.money_out_resolved for d in data_pac.all_donors]
    #
    # for d in data_pac.all_donors:
    #     money_out = d.money_out.to_dict() # dataframe
    #     name = d.name
    #     money_out.to

    # pickle.dump(data_pac, "data_pac_x.pkl")
