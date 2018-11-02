# We define 'party' as the party with which a candidate caucuses, if they have previously served in office.
# This is more reflective of their impact in the legislature.

def party_correction(data_pac):
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

