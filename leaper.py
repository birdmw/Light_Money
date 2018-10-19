# pip install sodapy

import numpy as np
import pandas as pd
from sodapy import Socrata
import time as time
from pandas.api.types import is_string_dtype


# use cases:
# 1. search by contributor & summarize by party
# 2. summarize by candidate votes on a bill
#
# Note that IEs and donations to losing candidates will not be counted in bill votes

class Donor():

    def __init__(self):
        self.name = " "
        self.aliases = []
        self.type = " "  # ind, pac, party, caucus
        self.filer_id = " "
        self.total_in = 0.0
        self.total_out = 0.0
        self.money_in = pd.DataFrame(
            columns=['donor', 'donor_id', 'amount'])  # only for PAC/caucus/party, empty for Individual donors
        self.money_out = pd.DataFrame(
            columns=["receiver", "amount", "party", "type"])  # amount, receiver, receiver type (Cand vs PAC)
        self.money_out_resolved = pd.DataFrame(
            columns=["receiver", "amount", "party", "type", "proportion"])  # money_out resolved to end candidates
        self.has_resolved = False  # indicates whether money_out_resolved has been successfully computed yet

    def __repr__(self):
        if self.money_out_resolved.empty:
            return "<Name:%s ID:%s Money in/out:%s / %s>" % (self.name, self.filer_id, self.money_in['amount'].sum(), self.money_out['amount'].sum())
        this_d = self.money_out_resolved.loc[self.money_out_resolved['party']=='DEMOCRAT','proportion']
        this_r = self.money_out_resolved.loc[self.money_out_resolved['party'] == 'REPUBLICAN', 'proportion']
        if this_d.empty:
            this_d = 0
        if this_r.empty:
            this_r = 0
        return "<Name:%s ID:%s Money in/out:%s / %s  Pct: %s D / %s R>" % (self.name, self.filer_id, self.money_in['amount'].sum(), self.money_out['amount'].sum(),int(100*this_d),int(100*this_r))

    def sum_donations(self):
        # check that money_in and money_out are non-empty (otherwise it would break), and if so sum them by receiver
        # include party and type (these won't vary for one receiver) so we don't lose these columns
        # the reset_index() is needed to put this back into a dataframe with the correct columns
        if (len(self.money_out) > 1):
            self.money_out = pd.DataFrame(self.money_out.groupby(['receiver', 'party', 'type']).sum()).reset_index()
        if (len(self.money_in) > 1):
            self.money_in = pd.DataFrame(self.money_in.groupby(['donor', 'donor_id']).sum()).reset_index()
        self.total_in = self.money_in['amount'].sum()
        self.total_out = self.money_out['amount'].sum()
        return

    def resolve_donations(self, fulldata, refresh = False):
        # need to check recursion problems - if called recursively on a pac which is already calling it, then throw error due to loop in donations
        if (self.has_resolved == True)&(refresh==False):
            return
        n_donations = len(self.money_out)
        # print(self.name)
        # print(n_donations)
        # check if money_out is empty
        if n_donations < 1:
            self.money_out_resolved = pd.DataFrame([[self.name, 0.0, "No Party", 'Terminal PAC', 1.0]],
                                                   columns=["receiver", "amount", "party", "type", "proportion"])
            # mark self as resolved
            self.has_resolved = True
            # print('Resolved no donations')
            return
        # for each line in money_out, check if it is to a candidate or pac
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
                self.money_out_resolved = self.money_out_resolved.append(this_add)
            else:
                # look up the pac that this money went to
                if this_receiver in fulldata.all_donors:
                    # check if the receiver is resolved yet, if not, tell them to resolve
                    if not (fulldata.all_donors[this_receiver].has_resolved):
                        fulldata.all_donors[this_receiver].resolve_donations(fulldata)
                    # get money_out_resolved
                    pac_resolved = fulldata.all_donors[this_receiver].money_out_resolved
                    # allocate this_amount by proportion to candidates in pac_resolved
                    amount_resolved = this_amount * pac_resolved.loc[:, 'proportion']
                    # construct DataFrame from pac_resolved and amount_resolved (proportion will be computed later)
                    this_add = pac_resolved.copy()
                    this_add.loc[:, 'amount'] = amount_resolved
                    this_add.loc[:,
                    'proportion'] = 0  # set to zero for now, it will be computed once all donations are resolved
                    self.money_out_resolved = self.money_out_resolved.append(this_add)
                else:  # we didn't find this pac in our data, so we don't know where the money went!
                    this_add = pd.DataFrame([[this_receiver, this_amount, this_party, 'Unresolved PAC', 0]],
                                            columns=["receiver", "amount", "party", "type", "proportion"])
                    self.money_out_resolved = self.money_out_resolved.append(this_add)
        # note resolution may have many intermediate pacs donating so the same candidates, so have to sum again
        self.money_out_resolved = pd.DataFrame(
            self.money_out_resolved.groupby(["receiver", "party", "type", "proportion"]).sum()).reset_index()
        # when all donations have been resolved
        # get total donation amount and divide to obtain proportion for each candidate, and save it
        self.money_out_resolved.loc[:, 'proportion'] = self.money_out_resolved.loc[:,
                                                       'amount'] / self.money_out_resolved.loc[:, 'amount'].sum()
        # mark self as resolved
        self.has_resolved = True
        # print('Resolved with donations')
        return


class Candidate():

    def __init__(self):
        self.name = " "
        self.filer_id = " "
        self.party = " "
        self.type = ' '
        self.total_in = 0.0
        self.money_in = pd.DataFrame(columns=["donor", "donor_id", "amount"])

    def __repr__(self):
        return "<Candidate name:%s filer_id:%s >" % (self.name, self.filer_id)

    def sum_donations(self):
        # should check that these are non-empty first - NaNs break it
        if (len(self.money_in) > 1):
            self.money_in = pd.DataFrame(self.money_in.groupby(['donor', 'donor_id']).sum()).reset_index()
        self.total_in = self.money_in['amount'].sum()


class Data():
    def __init__(self):
        self.all_donors = {}  # list of all donors (ind and pac)
        self.all_candidates = {}  # list of all candidates

    def combine_donors(self, donor_list):
        # check if donor_list is longer than 1
        # check if all strings in donor_list are valid keys in self.all_donors

        # first item in donor_list will be the new key
        first_donor = self.all_donors.pop(donor_list[0])
        new_donor = Donor()
        new_donor.name = donor_list[0]
        new_donor.aliases = donor_list
        new_donor.type = first_donor.type
        new_donor.filer_id = first_donor.filer_id
        new_donor.money_in = first_donor.money_in
        new_donor.money_out = first_donor.money_out
        new_donor.has_resolved = False

        for i in donor_list[1:]:
            temp = self.all_donors.pop(i)  # will raise error if i is not a valid key
            new_donor.money_in = new_donor.money_in.append(temp.money_in)
            new_donor.money_out = new_donor.money_out.append(temp.money_out)
        new_donor.sum_donations()
        self.all_donors[new_donor.name] = new_donor

# Save and Load functions
# Usage:
# save_to_file(data2,'data2.pickle')
# data2 = load_from_file('data2.pickle')
#

def save_to_file(data, filename='data.pickle'):
    # todo: check for valid filename
    pickle_out = open(filename, 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()
    print('Saved to file: ' + filename)


def load_from_file(filename='data.pickle'):
    pickle_in = open(filename, "rb")
    print('Loading from file: ' + filename)
    return pickle.load(pickle_in)


def load_ie_data(filename):
    # check if file exists, if so load it
    iedata = pd.read_csv(filename)
    my_cols = ['origin', 'sponsor_id', 'sponsor_name', 'candidate_last_name', 'candidate_first_name', 'candidate_party',
               'ballot_name', 'ballot_number', 'portion_of_amount', 'for_or_against']
    iedata = iedata[my_cols]
    iedata = iedata.loc[iedata.loc[:, 'origin'] == 'C6.3 - Identified Entities']  # better way to do this?
    print(iedata.shape)

    # convert the donation amount from str to float
    if is_string_dtype(iedata['portion_of_amount']):
        iedata['portion_of_amount'] = iedata['portion_of_amount'].str.replace(',', '').astype('float')
    # construct ballot name from number and name, stripping decimal from the float. note str.replace is regex by default and breaks if set to regex=False
    iedata['ballot_name_full'] = iedata['ballot_number'].astype('str').str.replace('\.0', '') + ', ' + iedata[
        'ballot_name']
    # construct full candidate name
    iedata['candidate_name_full'] = iedata['candidate_last_name'] + ', ' + iedata['candidate_first_name']

    # construct receiver type so we can tell candidates from other stuff
    iedata['receiver_type'] = 'candidate'
    # if no candidate name, then assume it is ballot measure
    iedata.loc[iedata.loc[:, 'candidate_name_full'].isnull(), 'receiver_type'] = 'ballot'
    # if ballot name is missing but there is a ballot number, then use ballot number as the name (this has been observed to happen)
    iedata.loc[
        iedata.loc[:, 'ballot_name_full'].isnull() & iedata.loc[:, 'ballot_number'].notnull(), 'ballot_name_full'] = \
        iedata.loc[
            iedata.loc[:, 'ballot_name_full'].isnull() & iedata.loc[:,
                                                         'ballot_number'].notnull(), 'ballot_number'].astype(
            'str').str.replace('\.0', '')
    data1 = Data()
    n_rows = iedata.shape[0]
    for i in range(n_rows):
        this_row = iedata.iloc[i,]
        this_giver_name = this_row["sponsor_name"]
        this_giver_id = this_row["sponsor_id"]
        if pd.isna(this_giver_id):
            raise ValueError('IE sponsor_id should not be missing')
        if this_row['receiver_type'] == 'candidate':
            this_receiver_name = this_row['candidate_name_full']
        elif this_row['receiver_type'] == 'ballot':
            this_receiver_name = this_row['ballot_name_full']
        else:
            raise ValueError('receiver_type must be candidate or ballot')

        this_receiver_party = this_row['candidate_party']  # this will be NaN for ballot measures
        if pd.isna(this_receiver_party):
            if this_row['receiver_type'] == 'candidate':
                this_receiver_party = 'Missing'
            elif this_row['receiver_type'] == 'ballot':
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
                this_receiver_name].money_in.append(
                this_add)
        # this_cand.money_in = this_cand.money_in.append(this_add)
        # todo: check that this_cand.party = this_receiver_party
        # data1.all_candidates[this_receiver_name] = this_cand

        else:
            # create new candidate and add to data
            new_cand = Candidate()
            new_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                   columns=['donor', 'donor_id', 'amount'])
            new_cand.money_in = new_cand.money_in.append(new_add)
            new_cand.name = this_receiver_name
            new_cand.type = this_receiver_type
            new_cand.party = this_receiver_party
            data1.all_candidates[this_receiver_name] = new_cand

        # check if donor already exists
        if this_giver_id in data1.all_donors:
            # if so, add to that donor data
            # this_donor = data1.all_donors[this_giver_id]
            # todo: check this_giver_name against this_donor.name
            this_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                    columns=["receiver", "amount", "party", "type"])
            data1.all_donors[this_giver_id].money_out = data1.all_donors[this_giver_id].money_out.append(this_add)
        # this_donor.money_out = this_donor.money_out.append(this_add)
        # data1.all_donors[this_giver_id] = this_donor
        else:
            # create new donor and add
            new_donor = Donor()
            new_donor.name = this_giver_name
            new_donor.filer_id = this_giver_id
            new_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                   columns=["receiver", "amount", "party", "type"])
            new_donor.money_out = new_donor.money_out.append(new_add)
            data1.all_donors[this_giver_id] = new_donor

    return data1


def load_pac_data(filename):
    # check if file exists, if so load it
    # candidate and PAC donations
    campdata = pd.read_csv(filename)
    # note ignore mixed type warnings on columns 11, 23 since we do not use them
    my_cols = ['filer_id', 'type', 'filer_name', 'party', 'ballot_number', 'for_or_against', 'amount', 'code',
               'contributor_name', 'contributor_address', 'contributor_city', 'contributor_zip']
    campdata = campdata[my_cols]
    print(campdata.shape)
    # note filer_id values in this file do not match the filer_id values in the IE data file
    # the for_or_against value is merely descriptive of ballot committees here, it does not indicate spending against a candidate
    # convert amount str to float
    if is_string_dtype(campdata['amount']):
        campdata['amount'] = campdata['amount'].str.replace(',', '').astype('float')

    # exclude rows with amount <= 0
    campdata = campdata.loc[(campdata.loc[:, 'amount'] > 0), :]
    print(campdata.shape)

    # drop rows from Individual donors (for now, since interest is mostly in PACs)
    # TODO: include individuals with notably large donations, e.g. over $20,000
    campdata = campdata.loc[(campdata.loc[:, 'code'] != 'Individual'), :]
    print(campdata.shape)

    data2 = Data()
    n_rows = campdata.shape[0]
    print(n_rows)

    start = time.time()

    for i in range(campdata.shape[0]):
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
        this_receiver_party = this_row[
            'party']  # this will be NaN for ballot measures and PACs, and the nans can break stuff
        if pd.isna(this_receiver_party):
            this_receiver_party = 'None'
        this_amount = this_row['amount']
        this_giver_id = 'None'  # donor id is not provided in this data

        if this_receiver_type == 'Candidate':
            # check if we have seen this candidate before
            if this_receiver_id in data2.all_candidates:
                # if so, add to that candidate data
                # this_cand = data2.all_candidates[this_receiver_id]
                this_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                        columns=['donor', 'donor_id', 'amount'])
                # this_cand.money_in =
                data2.all_candidates[this_receiver_id].money_in = data2.all_candidates[
                    this_receiver_id].money_in.append(this_add)
            # todo: check that this_cand.party = this_receiver_party
            # data2.all_candidates[this_receiver_id] = this_cand
            else:
                # create new candidate and add to data
                new_cand = Candidate()
                new_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                       columns=['donor', 'donor_id', 'amount'])
                new_cand.money_in = new_cand.money_in.append(new_add)
                new_cand.name = this_receiver_name
                new_cand.type = this_receiver_type
                new_cand.party = this_receiver_party
                # add new_cand to the dictionary
                data2.all_candidates[this_receiver_id] = new_cand
            # now process the donor to this candidate
            # check if donor already exists
            if this_giver_name in data2.all_donors:
                # if so, add to that donor data
                # this_donor = data2.all_donors[this_giver_name]
                # todo: check this_giver_name against ids and use id instead
                this_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                        columns=["receiver", "amount", "party", "type"])
                data2.all_donors[this_giver_name].money_out = data2.all_donors[this_giver_name].money_out.append(
                    this_add)
            else:
                # create new donor and add
                new_donor = Donor()
                new_donor.name = this_giver_name
                # new_donor.filer_id = this_giver_id #no donor id from C3 data
                new_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                       columns=["receiver", "amount", "party", "type"])
                new_donor.money_out = new_donor.money_out.append(new_add)
                data2.all_donors[this_giver_name] = new_donor
        else:  # receiver type is not Candidate, should only be Political Committee
            if this_receiver_name in data2.all_donors:  # check if we have seen this pac before (maybe as a donor) and update data
                this_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                        columns=['donor', 'donor_id', 'amount'])
                data2.all_donors[this_receiver_name].money_in = data2.all_donors[this_receiver_name].money_in.append(
                    this_add)
            # todo: check that this_cand.party = this_receiver_party
            else:
                # create new pac and add to data
                new_pac = Donor()
                new_add = pd.DataFrame([[this_giver_name, this_giver_id, this_amount]],
                                       columns=['donor', 'donor_id', 'amount'])
                new_pac.money_in = new_pac.money_in.append(new_add)
                new_pac.name = this_receiver_name
                new_pac.type = this_receiver_type
                new_pac.filer_id = this_receiver_id
                data2.all_donors[this_receiver_name] = new_pac
            # now process the donors to this donor/pac
            # check if donor already exists
            if this_giver_name in data2.all_donors:
                # if so, add to that donor data
                # this_donor = data2.all_donors[this_giver_name]
                # todo: check this_giver_name against ids and use id instead
                this_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                        columns=["receiver", "amount", "party", "type"])
                data2.all_donors[this_giver_name].money_out = data2.all_donors[this_giver_name].money_out.append(
                    this_add)
            else:
                # create new donor and add
                new_donor = Donor()
                new_donor.name = this_giver_name
                # new_donor.filer_id = this_giver_id #no donor id from C3 data
                new_add = pd.DataFrame([[this_receiver_name, this_amount, this_receiver_party, this_receiver_type]],
                                       columns=["receiver", "amount", "party", "type"])
                new_donor.money_out = new_donor.money_out.append(new_add)
                data2.all_donors[this_giver_name] = new_donor

    end = time.time()
    print(end - start)
    print(len(data2.all_donors.keys()))
    return data2


if __name__ == '__main__':
    print("Running Main")

    print(time.time())
    print("Read in and process IE data")
    data_ie = load_ie_data('Independent_Campaign_Expenditures_and_Electioneering_Communications.csv')

    print(time.time())
    print("Read in and process PAC/Candidate data")
    # data_pac = load_pac_data('Contributions_to_Candidates_and_Political_Committees.csv')
    data_pac = load_pac_data('small test data.csv')
    print('We can ignore the DtypeWarning about columns (11,23) because those are not used.')

    print(time.time())
    print("Sum donations (multiple donations from a donor to a receiver are summed)")
    for i in data_ie.all_donors.keys():
        data_ie.all_donors[i].sum_donations()
    print(time.time())
    for i in data_ie.all_candidates.keys():
        data_ie.all_candidates[i].sum_donations()
    print(time.time())
    for i in data_pac.all_candidates.keys():
        data_pac.all_candidates[i].sum_donations()
    print(time.time())
    for i in data_pac.all_donors.keys():
        data_pac.all_donors[i].sum_donations()
    print(time.time())

    print("Resolve donations to track all donations through to final candidate/ballot issue")

    print(len(data_pac.all_donors.keys()))
    start = time.time()
    for i in range(len(data_pac.all_donors.keys())):
        data_pac.all_donors[data_pac.all_donors.keys()[i]].resolve_donations(data_pac)
    end = time.time()
    print(end - start)

    print("Not shown: Data.combine_donors to combine records with different spellings of a donor name into one record")
    print(' ')
    print('Example of money spent by one donor:')
    print(data_pac.all_donors[data_pac.all_donors.keys()[3]].money_out)
    print(data_pac.all_donors[data_pac.all_donors.keys()[3]].money_out_resolved)