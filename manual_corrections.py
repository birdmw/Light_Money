# We define 'party' as the party with which a candidate caucuses, if they have previously served in office.
# This is more reflective of their impact in the legislature.

def pac_correction(data_pac):
    # data_pac is a Data() object

    data_pac.all_candidates['TOM RODNEY'].party = 'REPUBLICAN'
    data_pac.all_candidates['SHELDON TIMOTHY M'].party = 'REPUBLICAN'
    data_pac.all_candidates['SHEA MATTHEW T'].party = 'REPUBLICAN'

    for i in data_pac.all_candidates['TOM RODNEY'].money_in.donor:
        data_pac.all_donors[i].money_out.loc[data_pac.all_donors[i].money_out.receiver=='TOM RODNEY','party'] = 'REPUBLICAN'
    for i in data_pac.all_candidates['SHELDON TIMOTHY M'].money_in.donor:
        data_pac.all_donors[i].money_out.loc[data_pac.all_donors[i].money_out.receiver=='SHELDON TIMOTHY M','party'] = 'REPUBLICAN'
    for i in data_pac.all_candidates['SHEA MATTHEW T'].money_in.donor:
        data_pac.all_donors[i].money_out.loc[data_pac.all_donors[i].money_out.receiver=='SHEA MATTHEW T','party'] = 'REPUBLICAN'

def ie_correction(data_ie):
    #### It appears the problem below was fixed in the data source between 10/26 and 11/10
    ##fix the reporting error made by Andeavor in reporting "for" the "against" position (should just be "against")
    #data_ie.all_candidates['1631, NO ON 1631'].money_in.amount = -data_ie.all_candidates[
    #    '1631, NO ON 1631'].money_in.amount
    #data_ie.all_donors['MARATHON PETROLEM CORP SUBSIDIARY ANDEAVOR LLC'].money_out.loc[
    #    data_ie.all_donors[
    #        'MARATHON PETROLEM CORP SUBSIDIARY ANDEAVOR LLC'].money_out.receiver == '1631, NO ON 1631', 'amount'
    #] = -data_ie.all_donors['MARATHON PETROLEM CORP SUBSIDIARY ANDEAVOR LLC'].money_out.loc[
    #    data_ie.all_donors[
    #        'MARATHON PETROLEM CORP SUBSIDIARY ANDEAVOR LLC'].money_out.receiver == '1631, NO ON 1631', 'amount'
    #]
    #####################
    #
    #fix the party labels as above
    #don't need to fix the money_out data in IE dataset since it is not propogated back to data_pac when they are merged
    data_ie.all_candidates['TOM, RODNEY'].party = 'REPUBLICAN'
    data_ie.all_candidates['SHELDON, TIMOTHY'].party = 'REPUBLICAN'
    #data_ie.all_candidates['SHEA, MATTHEW'].party = 'REPUBLICAN' #not in datatset as of 11/02

