
def do_pac_synonyms(data_pac):
    # data_pac is a Data() object

    syn_realtors = ['WA REALTORS PAC',
                    'WASHINGTON ASSOCIATION OF REALTORS (PAC)',
                    'WASHINGTON ASSOCIATION OF REALTORS PAC',
                    'WA ASSOCIATION OF REALTORS POLITICAL AFFAIRS COUNCIL',
                    'WASHINGTON ASSOCIATION OF REALTORS',
                    'WA. ASSOC. OF REALTORS PAC',
                    'WA ASSOCIATION OF REALTORS',
                    'WA ASSOCIATION OF REALTORS PAC',
                    'WA ASSOC. OF REALTORS PAC',
                    'WA ASSN OF REALTORS PAC',
                    'WA ASSOC OF REALTORS POLITICAL AFFAIRS COUNCIL',
                    'WA ASSOC OF REALTORS PAC',
                    'WA ASSO OF REALTORS',
                    'ASSOCIATION OF WASHINGTON REALTORS',
                    'WASHINGTON REALTORS',
                    'WASHINGTON ASSOC OF REALTORS POLITICAL AFFAIRS COUNCIL',
                    'WA ASSN OF REALTORS POLITICAL AFFAIRS COUNCIL',
                    'WASHINGTON ASSN OF REALTORS',
                    'WASHINGTON ASSOCIATION OF REALTORS POLITICAL AFFAIRS COUNCIL']

    syn_srcc = ['SENATE REPUBLICAN CAMPAIGN COMMITTEE',
                'SENATE REPUB CAMP COMM', 'SENATE REPUBLICAN CAMPAIGN COM',
                'SENATE REPUBLICAN CAMPAIGN CMTE']

    syn_hrcc = ['HOUSE REPUBLICAN ORGANIZATION COMMITTEE',
                'HOUSE REPUBLICAN',
                'HOUSE REPUBLICAN ORGANIZATIONAL COMMITTEE',
                'HOUSE REPUBLICAN ORGANIZATIONA',
                'HOUSE REPUB ORG COMM']

    syn_hdcc = ['HOUSE DEMOCRATIC CAUCUS CAMPAIGN COMMITTEE',
                'HOUSE DEMOCRATIC CAMPAIGN COMMITTEE',
                'HOUSE DEMO CAMPAIGN COMMITTEE',
                'WASHINGTON HOUSE DEMOCRATIC CAMPAIGN COMMITTEE',
                'HOUSE DEMOCRATIC CAMPAIGN COMMITTEE/ HDCC',
                'HOUSE DEMOCRATIC CAMPAIGN COMMITTEE / HDCC',
                'HOUSE DEMOCRACTIC CAMPAIGN COMMITTEE',
                'HOUSE DEMO CAMP COMM',
                'HOUSE DEMOCRATIC  CAMPAIGN',
                'HOUSEDEMOCRATIC CAUCUS CAMPAIGN COMMITTEE',
                'HOUSE DEMOCRATIC CAUCUS CAMPAIGN COMM.']

    syn_sdcc = ['WASHINGTON SENATE DEMOCRATIC CAMPAIGN',
                'WA SENATE DEMOCRATIC CAMPAIGN (WSDC)',
                'WA SENATE DEMOCRATIC CAMPAIGN',
                'WA SENATE DEMO CAMP',
                'WASHINGTON STATE DEMOCRATIC CAMPAIGN']  # this is a version manually investigated in candidate reports

    syn_microsoft = ['MICROSOFT',
                     'MICROSOFT PAC',
                     'MICROSOFT CORP',
                     'MICROSOFT CORPORATION PAC',
                     'MICROSOFT POLITICAL ACTION COMMITTEE',
                     'MICROSOFT CORPORATION']

    syn_amazon = ['AMAZON',
                  'AMAZON.COM',
                  'AMAZON.COM SERVICES INC.',
                  'AMAZON SERVICES, INC.',
                  'AMAZON.COM SERVICES, INC.',
                  'AMAZON.COM SERVICES',
                  'AMAZON.COM SERVICES INC',
                  'AMAZON FULFILLMENT SERVICES INC.',
                  'AMAZON.COM SERVICE INC',
                  'AMAZON FULFILMENT SERVICES INC.',
                  'AMAZON SERVICES INC.',
                  'AMAZON FULFILLMENT SERVICES INC',
                  'AMAZON FULFILLMENT SERVICES, INC.',
                  'AMAZON.COM INC.',
                  'AMAZON FULFILLMENT SERVICE INC',
                  'AMAZON.COM SERVICES, INC',
                  'AMAZON FULFILLMENT SERVICES',
                  'AMAZON FULFILLMENT CENTER',
                  'AMAZON FULFILLMENT SERVICES, INC']

    syn_values = ['WASHINGTON VALUES PAC', 'WA VALUES PAC']

    syn_enterprise_holdings = ['ENTERPRISE HOLDINGS, INC PAC',
                               'ENTERPRISE HOLDINGS INC. PAC',
                               'ENTERPRISE HOLDINGS INC PAC',
                               'ENTERPRISE HOLDINGS, INC. POLITICAL ACTION COMMITTEE',
                               'ENTERPRISE HOLDINGS, INC. PAC',
                               'ENTERPRISE HOLDINGS',
                               'ENTERPRISE HOLDINGS INC POLITICAL ACTION COMMITTEE',
                               'ENTERPRISE HOLDINGS INC',
                               'ENTERPRISE HOLDINGS INC. POLIT',
                               'ENTERPRISE HOLDINGS, INC.']

    syn_anheuser = ['ANHEUSER BUSCH CO.',
                    'ANHEUSER BUSCH COMPANIES',
                    'ANHEUSER BUSCH COS',
                    'ANHEUSER BUSCH COMPANY',
                    'ANHEUSER-BUSCH CO. INC.',
                    'ANHEUSER-BUSCH COS., INC.',
                    'ANHEUSER-BUSCH COS. INC.',
                    'ANHEUSER BUSCH COS, INC',
                    'ANHEUSER-BUSCH COMPANIES',
                    'ANHEUSER-BUSCH CO.',
                    'ANHEUSER BUSCH',
                    'ANHEUSER-BUSCH CO., INC',
                    'ANHEUSER-BUSCH']

    syn_naiop = ['NAIOP WASHINGTON STATE PAC',
                 'NAIOP WA PAC',
                 'NAIOP PAC',
                 'NAIOP WASHINGTON',
                 'NAIOP WASHINGTON CHAPTER',
                 'NAIOP WA',
                 'NAIOPWA PAC',
                 'NAIOP  WASHINGTON STATE',
                 'NAIOP WA STATE PAC']

    # does not exist: 'WASHINGTON STATE HOUSE REPUBLICAN LEADERSHIP PAC'

    data_pac.combine_donors(syn_hrcc)
    data_pac.combine_donors(syn_hdcc)
    data_pac.combine_donors(syn_srcc)
    data_pac.combine_donors(syn_sdcc)
    data_pac.combine_donors(syn_amazon)
    data_pac.combine_donors(syn_realtors)
    data_pac.combine_donors(syn_microsoft)
    data_pac.combine_donors(syn_values)
    data_pac.combine_donors(syn_anheuser)
    data_pac.combine_donors(syn_naiop)
    data_pac.combine_donors(syn_enterprise_holdings)

    syn_enterprise_wa = ['ENTERPRISE WASHINGTON',
                         'CIT FOR PROGRESS ENTERPRISE WA',
                         'OUR OLYMPIC COMMUNITIES ENTERPRISE WA',
                         'CITIZENS FOR WORKING COURTS ENTERPRISE WASHINGTON',
                         'PEOPLE FOR JOBS ENTERPRISE WA',
                         'ENTERPRISE WASHINGTON JOBS PAC',
                         'SOUTHWEST COMMUNITIES ENTERPRISE WA',
                         'NORTH CASCADE JOBS ENTERPRISE WA',
                         'SOUTH SOUND FUTURE PAC ENTERPRISE WA',
                         "ENTERPRISE WASHINGTON'S JOBS PAC",
                         'ENTERPRISE WA JOBS PAC']

    data_pac.combine_donors(syn_enterprise_wa)

    data_pac.combine_donors(['HARRY TRUMAN FUND', 'HARRY TRUMAN TRUST FUND'])

    data_pac.combine_donors(['REAGAN FUND', 'THE REAGAN FUND'])

    data_pac.combine_donors(['KENNEDY FUND',
                             'THE KENNEDY FUND'])

    data_pac.combine_donors(['THE LEADERSHIP COUNCIL',
                             'THE LEADERSHIP COUNSIL'])

    data_pac.combine_donors(['SOUTH SOUND WOMENS LEADERSHIP PAC',
                             "SOUTH SOUND WOMEN'S LEADERSHIP PAC", ])

    # 'WA FORWARD (THE LEADERSHIP COUNCIL)' #the only instance of this PAC, no alias

    data_pac.combine_donors(['MAINSTREAM REPUB OF WA ST PAC',
                             'MAINSTREAM REPUBLICANS OF WA PAC',
                             'MAINSTREAM REPUBLICANS OF WA',
                             'MAINSTREAM REPUBLICANS OF WASHINGTON',
                             'MAINSTREAM REPUBLICANS',
                             'MAINSTREAM REPUBLICANS OF WASHINGTON PAC'])

    data_pac.combine_donors(['WA STATE REPUBLICAN PARTY',
                             'WA ST REPUB PARTY EXEMPT',
                             'WA ST REPUB PARTY NON EXEMPT',
                             'WASHINGTON STATE REPUBLICAN PARTY - EXEMPT ACCOUNT',
                             'WASHINGTON STATE REPUBLICAN PARTY'])

    data_pac.combine_donors(['WA STATE DEMOCRATIC PARTY',
                             'WASHINGTON STATE DEMOCRATIC CENTRAL COMMITTEE',
                             'WA ST DEMO CENT COMM NON EXEMPT',
                             'WA STATE DEMOCRATS',
                             'WASHIINGTON STATE DEMOCRATS',
                             'WA STATE DEMOCRATIC CENTRAL COMMITTEE',
                             'WASHINGTON STATE DEMOCRATIC PARTY',
                             'WASHINGTON STATE DEMOCRATIC CENTRAL COMMITTEE -FEDERAL',
                             'WA ST DEMO CENT COMM EXEMPT',
                             'WASHINGTON STATE DEMOCRATIC COMMITTEE - NONEXEMPT',
                             'WASHINGTON STATE DEMOCRATS',
                             'WASH. STATE DEMOCRATS',
                             'WA STATE DEMOCRATS / WSDCC',
                             'WASHINGTON STATE DEMOCRATIC CENTRAL'])

    data_pac.combine_donors(['WA TEAMSTERS LEGISLATIVE LEAGUE',
                             'WASHINGTON TREAMSTERS LEGISLATIVE LEAGUE',
                             'WASHINGTON TEAMSTER LEGISLATIVE LEAGUE',
                             'WA TEAMSTERS LEG LEAGUE',
                             'WASHINGTON TEAMSTERS LEGISLATIVE LEAGUE',
                             'TEAMSTERS LEGISLATIVE LEAGUE PAC',
                             'WASHINGTON TEAMSTER LEGISTLATIVE LEAGUE'])

    data_pac.combine_donors(['GUN OWNERS ACTION LEAGUE OF WA.',
                             'GUN OWNERS ACTION LEAGUE OF WA',
                             'GUN OWNERS ACTION LEAGUE OF WASHINGTON PAC',
                             'GUN OWNERS ACTION LEAGUE',
                             'GUN OWNERS ACTION LEAGUE OF WASHINGTON'])

    data_pac.combine_donors(['SEIU 1199NW',
                             'SEIU HEALTHCARE 1199 NW',
                             'SEIU HEALTHCARE 1199 NW PAC FUND',
                             'SERVICE EMPLOYEES INTERNATIONAL UNION 1199NW',
                             'SEIU HEALTCHARE 1199NW',
                             'SEIU HEALTHCARE 1199NW PAC FUND',
                             'SEIU HEALTHCARE UNITED FOR QUALITY CARE 1199NW',
                             'SEIU 1199 NW HEALTHCARE',
                             'SEIU HEALTHCARE 1199NW PAC',
                             'SEIU 1199 NW',
                             'SEIUHEALTHCARE 1199NW',
                             'SEIU HEALTHCARE 1199 NW PAC',
                             'SEIU HEALTHCARE 1199NW',
                             'SEIU LOCAL 1199 (HEALTHCARE WORKERS)',
                             'SEIU 1199 NW PAC',
                             'SEIU 1199',
                             'SEIU HEALTHCARE 1199 NW--PAC',
                             'SEIU 1199NW QUALITY CARE',
                             'SEIU HEALTHCARE UNITED FOR QUALITY CARE 1199 NW',
                             'SIEU 1199',
                             'SEIUHEALTHCARE 1199 NW'])

    data_pac.combine_donors(['SEIU 775',
                             'SEIU HEALTHCARE 775NW QUALITY CARE CMTE',
                             'SEIU HEALTHCARE 775 NW',
                             'SEIU 775 NW HEALTHCARE',
                             'SEIU LOCAL 775',
                             'SEIU HEALTHCARE 775',
                             'SERVICE EMPLOYEES INTL UNION 775 QUALITY CARE COMM',
                             'SEIU HEALTHCARE 775NW',
                             'SEIU 775NW',
                             'SEIU 775 QUALITY CARE',
                             'SEIU #775',
                             'SEIU 775 QUALITY CARE COMMITTEE'])

    data_pac.combine_donors(['WASHINGTON EDUCATION ASSOCIATION',
                             'WA EDUCATION ASSOC. PAC',
                             'WASHINGTON EDUCATION ASSOCIATION PAC',
                             'WEA /PAC',
                             'WASHINGTON EDUCATIONAL ASSOCIATION PAC',
                             'WEA-PAC',
                             'WA EDUCATION ASSOCIATION (WEAPAC)',
                             'WASHINGTON EDUCATION ASSOC. PAC',
                             'WA EDUCATION ASSOCIATION',
                             'WA EDUCATION ASSN. PAC',
                             'WA EDUCATION ASSN PAC (WEA PAC)',
                             'WASHINGTON EDUCATION ASSOOCIATION PAC',
                             'WASHNGTON EDUCATION ASSOCIATION',
                             'WASHINGTON EDUCATION ASSOCIATION - POLITICAL ACTION COMMITTEE',
                             'WA EDUCATION ASSN (WEAPAC)',
                             'WASHINGTON EDUCATION ASSOCIATION POLITICAL ACTION COMMITTEE',
                             'WA EDUCATION ASSN',
                             'WASHINTON EDUCATION ASSOCIATION',
                             'WASHINGON EDUCATION ASSOC PAC',
                             'WASHINGTON EDUCATION ASSO PAC',
                             'WA EDUCATION ASSOCIATION PAC (WEA PAC)',
                             'WEAPAC',
                             'WA EDUCATION ASSOCIATION POLITICAL ACTION COMMITTEE',
                             'WASHINGTON EDUCATION ASSOC PAC',
                             'WA EDUCATION ASSN PAC',
                             'WEA',
                             'WASHINGTON EDUCATION ASSOC.',
                             'WASHINGTOM EDUCATION ASSOCIATION',
                             'WA EDUCATION ASSOCIATION PAC',
                             'WEA PAC',
                             'WEA PAC / WA EDUCATION ASSN PAC',
                             'WA EDUCATION ASSN PAC / WEAPAC'])

    data_pac.combine_donors(['BP AMERICA EMPLOYEE PAC',
                             "BP NORTH AMERICA EMPLOYEE'S PAC",
                             'BP NORTH AMERICA EMPLOYEE',
                             'BP NORTH AMERICAN EMPLOYEE PAC',
                             'BP NORTH AMERICA EMPLOYEES PAC',
                             'BP NORTH AMERICA EMPLOYEE PAC'])

    data_pac.combine_donors(['COCA COLA NORTH AMERICA',
                             'THE COCA-COLA COMPANY',
                             'COCA-COLA NORTH AMERICA',
                             'COCA COLA'])

    data_pac.combine_donors(['PEPSI COLA NW BUSINESS UNIT',
                             'PEPSICO, INC.',
                             'PEPSI NORTHWEST BEVERAGES LLC'])

    data_pac.combine_donors(['AMERICAN FUEL AND PETROCHEMICAL MANUFACTURERS',
                             'AMERICAN FUEL & PETROCHEMICAL MANUFACTURERS'])

    data_pac.combine_donors(['ONEAMERICA VOTES JUSTICE FUND',
                             'ONEAMERICAN VOTES JUSTICE FUND',
                             'ONE AMERICA VOTES JUSTICE FUND'])

    data_pac.combine_donors(['WA STATE ASSOCIATION FOR JUSTICE',
                             'WSAJ JUSTICE FOR ALL PAC',
                             'WASHINGTON STATE ASSOCIATION FOR JUSTICE',
                             'JUSTICE FOR ALL PAC',
                             'WA ST ASSN FOR JUSTICE JUSTICE FOR ALL',
                             'WA STATE ASSOC. FOR JUSTICE',
                             'WASHINGTO STATE ASSOCIATION OF JUSTICE',
                             'JUSTICE FOR ALL'])

    data_pac.combine_donors(['PUYALLUP TRIBE OF INDIANS',
                             'PUYALLLUP TRIBE OF INDIANS',
                             'PUYALLUP TRIBE',
                             'PUYALLUP TRIBES OF INDIANS',
                             'PUYALLUP  TRIBE OF INDIANS'])

    data_pac.combine_donors(['MUCKLESHOOT INDIAN TRIBE', 'MUCKLESHOOT INDIAN TRIBE TAX FUND'])

    data_pac.combine_donors(['EVERYTOWN FOR GUN SAFETY AF',
                             'EVERYTOWN FOR GUN SAFETY ACTION FUND',
                             'EVERYTOWN FOR GUN SAFETY'])

    data_pac.combine_donors(['PHILLIPS 66',
                             'PHILLIPS 66 CORPORATION',
                             'PHILLIPS 66, WESTERN REGION',
                             'PHLLIPS 66 COMPANY',
                             'PHILLIPS 66 CO.',
                             'PHILLIPS 66 CO',
                             'PHILLUPS 66 COMPANY',
                             'PHILLIPS 66 COMPANY',
                             'PHLLIPS 66'])

    data_pac.combine_donors(['SHEET METAL WORKERS LOCAL 66',
                             'SHEET METAL WORKERS LOCAL 66 POLITICAL ACTION COMMITTEE',
                             'SHEET METAL WORKERS LOCAL UNION 66',
                             'SHEET METAL WORKERS LOCAL #66',
                             'SHEET METAL WORKERS LOCAL 66 PAC'])

    data_pac.combine_donors(['ANDEAVOR', 'ANDEAVOR REFINERY', 'ANDEAVOR ANACORTES REFINERY'])

    data_pac.combine_donors(['DR PEPPER SNAPPLE GROUP',
                             'KEURIG DR PEPPER (FKA DR PEPPER SNAPPLE GROUP, INC.)',
                             'DR PEPPER SNAPPLE GROUP, INC.'])

    data_pac.combine_donors(['BOEING COMPANY',
                             'THE BOEING CO PAC',
                             'THE BOEING CO (PAC)',
                             'BOEING POLITICAL ACTION COMMITTEE',
                             'THE BOEING COMPANY PAC - A MULTICANIDIDATE COMMITTEE',
                             'BOEING COMPANY PAC',
                             'THE BOEING COMPANY POLITICAL ACTION COMMITTEE',
                             'THE BOEING CO',
                             'THE BOEING COMPANY POLITICAL ACTION COMPANY',
                             'THE BOEING CO.',
                             'THE BOEING COMPANY PAC',
                             'THE BOEING COMPANY',
                             'THE BOEING COMPANY POLITICAL A'])

    data_pac.combine_donors(['BOEING EMPLOYEES CREDIT UNION',
                             "BECU-BOEING EMPLOYEES' CREDIT UNION",
                             'BOEING EMPLOYEES CREDIT UNION (BECU)'])

    data_pac.combine_donors(['WEYERHAEUSER CO',
                             'WEYERHAUSER',
                             'WEYERHAEUSER COMPANY',
                             'WEYERHAUSER NR COMPANY',
                             'WEYERHAEUSER',
                             'WEYERHAEUSER COMAPANY',
                             'WEYERHAEUSER NR COMPANY'])

    data_pac.combine_donors(['SNOHOMISH COUNTY REPUBLICAN PARTY',
                             'SNOHOMISH COUNTY REPUBLICAN PA',
                             'SNOHOMISH CO REPUB CENT COMM NON EXEMPT'])

    data_pac.combine_donors(['SNOHOMISH COUNTY DEMOCRATS',
                             'SNOHOMISH CO DEMO CENT COMM NON EXEMPT',
                             'SNOHOMISH COUNTY DEMOCRATIC COMMITTEE'])

    data_pac.combine_donors(['SOUTH KING COUNTY DEMOCRATS', 'SOUTH KING CO DEMOCRATS'])

    data_pac.combine_donors(['SOUTH KING COUNTY DESERVES BETTER', 'SOUTH KING CO DESERVES BETTER'])

    data_pac.combine_donors(['KING COUNTY REPUBLICAN PARTY',
                            'KING CO REPUB CENT COMM EXEMPT',
                            'KING COUNTY REPUBLICAN CENTRAL COMMITTEE NEX',
                            'KING CO REPUB CENT COMM NON EXEMPT'])

    data_pac.combine_donors(['FARMERS INSURANCE',
                             'FARMERS GROUP, INC.',
                             'FARMERS GROUP INC',
                             'FARMERS EMPLOYEES & AGENT PAC',
                             'FARMERS GROUP, INC. (FARMERS EMPLOYEES &',
                             'FARMERS EMPLOYEES AND AGENTS PAC',
                             'FARMERS EMPLOYEES &  AGENTS PA'])

    data_pac.combine_donors(['ALLSTATE INSURANCE CO',
                             'ALLSTATE INSURANCE COMPANY',
                             'ALLSTATE INSURANCE',
                             'ALLSTATE INSURANCE CO.'])

    data_pac.combine_donors(['WASHINGTON BEVERAGE ASSOCIATION',
                             'WASINGTON BEVERAGE ASSOCIATION',
                             'WASHINGTON BEVERAGE ASSOCIATION POLITICAL ACTION COMMITTEE',
                             'WA BEVERAGE ASSOCIATION PAC',
                             'WA BEVERAGE ASSOCIATION',
                             'WASHINGTON BEVERAGE ASSOC PAC',
                             'WA BEVERAGE ASSOC',
                             'WA BEVERAGE ASSN',
                             'WASHINGTON BEVERAGE ASSOCIATION PAC',
                             'WA BEVERAGE ASSN PAC',
                             'WASH. BEVERAGE ASSOC. PAC',
                             'WASHINGTON BEVERAGE ASSN',
                             'WA BEVERAGE ASSN.',
                             'WASHINGTON BEVERAGE ASSOCIATION, PAC',
                             'WASHINGTON BEVERAGE ASSOCIATIO',
                             'WA BEVERAGE ASSOC. PAC',
                             'WA BEVERAGE ASSOC PAC',
                             'WASHINGTON STATE BEVERAGE ASSOCIATION'])

    data_pac.combine_donors(['ONEAMERICA VOTES',
                             'ONE AMERICA',
                             'ONEAMERICA VOTES JUSTICE FUND'])

    data_pac.combine_donors(['JP MORGAN CHASE',
                             'JP MORGAN AND CO. PAC',
                             'JP MORGAN CHASE & CO PAC',
                             'JPMORGAN CHASE',
                             'JPMORGAN CHASE & CO',
                             'JPMORGAN CHASE & CO PAC',
                             'JPMORGAN CHASE & CO INC.',
                             'JPMORGAN CHASE & CO. PAC'])

    data_pac.combine_donors(['NORTHWEST REGIONAL ORGANIZING COALITION PAC',
                             'NW REGIONAL ORGANIZING COALITION PAC',
                             'NORTHWEST REGIONAL ORGANIZING COALITION'])

    data_pac.combine_donors(['WASHINGTON CONSERVATION VOTERS',
                             'WASHINGTON CONSERVATION VOTERS PAC',
                             'WA CONSERVATION VOTERS ACTION FUND',
                             'WA CONSERVATION VOTERS',
                             'WA CONSERVATION VOTERS ACTION FUND (WCV)',
                             'WASHINGTON CONSERVATION VOTERS ACTION FUND'])

    data_pac.combine_donors(['WASHINGTON ANGLER FOR CONSERVATION PAC',
                             'WASHINGTON ANGLERS FORCONSERVATION',
                             'WASHINGTON ANGLERS FOR CONSERVATION',
                             'WASHINGTON ANGLERS FOR CONSERVATION PAC',
                             'WA ANGLERS FOR CONSERVATION',
                             'WA ANGLERS FOR CONSERVATION PAC'])

    data_pac.combine_donors(['23RD LEGISLATIVE DISTRICT DEMOCRATS',
                             'WA STATE 16TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '45TH DISTRICT DEMOCRATS',
                             '1ST LD DEMOCRATIC PARTY',
                             '6TH LD DEMOCRATS',
                             '3RD LEG DIST DEMO EXEMPT',
                             'SIXTH LEGISLATIVE DISTRICT DEMOCRATIC COMMITTEE',
                             '21ST LEGISLATIVE DISTRICT DEMOCRATS',
                             '34TH DISTRICT DEMOCRATS',
                             '41ST DISTRICT DEMOCRATS',
                             '44TH LEG DIST DEMO NON EXEMPT',
                             'WASHINGTON 2ND LEGISLATIVE DISTRICT DEMOCRATS',
                             '35TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '4TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '4TH DISTRICT DEMOCRATS',
                             '39TH DISTRICT DEMOCRATS',
                             '33RD DISTRICT DEMOCRATS',
                             '47TH DISTRICT DEMOCRATS',
                             '5TH DISTRICT DEMOCRATS',
                             '17TH LEGISLATIVE DISTRICT DEMOCRATIC CENTRAL COMMITTEE',
                             '49TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '46TH DISTRICT DEMOCRATS',
                             '23RD LEG DIST DEMO NON EXEMPT',
                             '20TH LEGISLATIVE DISTRICT DEMOCRATIC COMMITTEE',
                             '23RD LEG DIST DEMO COMM POLITICAL ACCT, 2018',
                             '2ND LEG DIST DEMO ORG VICTORY FUND NON EXEMPT',
                             'WA STATE 16TH LEGISLATIVE DISTRICT DEMOCRATIC CENTRAL COMMITTEE',
                             '20TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '38TH LEG DIST DEMO COMM NON EXEMPT',
                             '30TH DISTRICT DEMOCRATIC ORGANIZATION',
                             '37TH LEG DIST DEMO CENT COMM NON EXEMPT',
                             '10TH DISTRICT DEMOCRATS',
                             '46TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '10TH DIST DEMO NON EXEMPT',
                             '44TH LEGISLATIVE DEMOCRATS',
                             '9TH LEGISLATIVE DISTRICT DEMOCRATS',
                             'LEGISLATIVE DISTRICT NO. 24 DEMOCRATS',
                             '41ST DIST DEMO ORG NON EXEMPT',
                             '26TH LEG DIST DEMO CENT COMM NON EXEMPT',
                             '26TH DISTRICT DEMOCRATS',
                             '21ST LD DEMOCRATIC PARTY',
                             '3RD LEG DIST DEMO NON EXEMPT',
                             '26TH LD DEMOCRATS',
                             '5TH DIST DEMO NON EXEMPT',
                             '44TH LD DEMOCRATIC PARTY',
                             'SIXTH LEGISLATIVE DISTRICT DEMOCRATS',
                             '42ND LEG DIST DEMO COMM NON EXEMPT',
                             '35TH LEG DIST DEMO COMM POLITICAL ACCT, 2018',
                             '47TH DIST DEMO NON EXEMPT',
                             'THIRD LEGISLATIVE DISTRICT DEMOCRATS',
                             '37TH DISTRICT DEMOCRATS',
                             '1ST DIST DEMO NON EXEMPT',
                             '46TH DIST DEMO ORG',
                             '28TH DIST DEMO CENT COMM VICTORY FUND NON EXEMPT',
                             '25TH DISTRICT DEMOCRATS',
                             '27TH DIST DEMO ORG VICTORY FUND',
                             '19TH LEG DIST DEMO CENT COMM NON EXEMPT',
                             '18TH LEG DIST DEMO CENT COMM NON EXEMPT',
                             '48TH DISTRICT DEMOCRATS',
                             '18TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '35 LD DEMOCRATS',
                             '25TH LEG DIST DEMO NON EXEMPT',
                             '33RD DISTRICT DEMOCRATIC ORGANIZATION',
                             '6TH LD DEMOCRATIC COMMITTEE',
                             '16TH LEGISLATIVE DISTRICT DEMOCRATIC CENTRAL COMMITTEE',
                             '27TH DISTRICT DEMOCRATS',
                             '44TH DISTRICT DEMOCRATS',
                             '31ST LEG DIST DEMO NON EXEMPT',
                             '27TH LEGISLATIVE DISTRICT DEMOCRATS - EXEMPT FUND',
                             '42ND LD DEMOCRATS',
                             '45TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '24TH LEG DIST DEMO CENT COMM NON EXEMPT',
                             '36TH DIST DEMO PARTY NON EXEMPT',
                             '11TH DISTRICT DEMOCRATS',
                             '48TH DIST DEMO ORG NON EXEMPT',
                             '30TH DIST DEMO ORG NON EXEMPT',
                             '31ST DIST DEMO ADMIN-EXEMPT ACCT',
                             '28TH DISTRICT DEMOCRATS VICTORY FUND',
                             '38TH LEGISLATIVE DISTRICT DEMOCRATS 2017',
                             '18TH LEGISLATIVE DISTRICT DEMOCRATIC CENTRAL COMMITTEE',
                             '1ST DISTRICT DEMOCRATS',
                             '33RD DIST DEMO ORG NON EXEMPT',
                             '9TH LEGISLATIVE DISTRICT DEMOCRACTS',
                             '46TH DISTRICT DEMOCRATIC ORG',
                             '19TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '25TH LD DEMOCRATIC PARTY',
                             '30TH DISTRICT DEMOCRATS',
                             '38TH DIST DEMO EXEMPT',
                             '35TH LD DEMOCRATS',
                             '23RD LD DEMOCRATS',
                             '31ST LEGISLATIVE DISTRICT DEMOCRATS',
                             '27TH DIST DEMO ORG EXEMPT FUND',
                             '28TH DIST DEMO CENT COMM EXEMPT',
                             '45TH LEG DIST DEMO NON EXEMPT',
                             '26TH LEGISLATIVE DISTRICT DEMOCRATS',
                             '42ND LEGISLATIVE DISTRICT DEMOCRATS',
                             '34TH DIST DEMO NON EXEMPT',
                             '28TH LEGISLATIVE DISTRICT DEMOCRATS VICTORY FUND',
                             '42ND LEG DIST DEMO COMM',
                             '25TH LEGISLATIVE DISTRICT DEMOCRATIC PARTY',
                             '35TH LEG DISTRICT DEMOCRATS',
                             '32ND DIST DEMO CAMP FUND NON EXEMPT',
                             '39TH LEG DIST DEMO PARTY ORG NON EXEMPT',
                             '35TH LEG DIST DEMO COMM POLITICAL ACCT'], rename='LOCAL DEMOCRATIC ORGS')

    data_pac.combine_donors(['17TH LEG DIST REPUB COMM NON EXEMPT',
                             '43RD DIST REPUB PARTY EXEMPT',
                             '7TH DIST REPUB COMM',
                             '43RD DIST REPUB PARTY NON EXEMPT',
                             '45TH LEG DIST REPUB NON EXEMPT',
                             '36TH DIST REPUB NON EXEMPT',
                             'TWENTY SEVENTH DISTRICT REP CLUB',
                             'TWENTY SEVENTH DISTRICT REPUBLICAN CLUB',
                             '5TH DISTRICT REPUBLICAN POLITICAL COMMITTEE',
                             '45TH LEG DIST REPUB EXEMPT',
                             '42ND LEG DISTRICT COMMITTEE GOP EXEMPT',
                             '5TH DIST REPUB POL COMM NON EXEMPT',
                             '47TH DIST REPUB NON EXEMPT',
                             '5TH DIST REPUB POL COMM EXEMPT',
                             '5TH LEGISLATIVE DISTRICT REPUBLICANS',
                             '2ND DIST LEG REPUB COMM NON EXEMPT',
                             '33RD DISTRICT REPUBLICANS',
                             '47TH DISTRICT REPUBLICANS',
                             '21ST LEGISLATIVE DISTRICT REPUBLICAN PARTY',
                             'KING COUNTY 46TH DISTRICT REPUBLICANS',
                             '1ST LEGISLATIVE DISTRICT REPUBLICAN COMMITTEE',
                             '6TH DISTRICT REPUBLICAN ACTION COMMITTEE',
                             '26TH LEG DIST REPUB COMM NON EXEMPT',
                             '28TH DIST REPUB LEG COMM NON EXEMPT',
                             '42ND LEG DIST COMM GOP EXEMPT',
                             '42ND LEG DIST COMM GOP NON EXEMPT',
                             '25TH LEG DIST REPUB COMM',
                             '47TH DIST REPUBLICANS',
                             '24TH LEG DIST REPUB COMM NON EXEMPT',
                             '26TH LEGISLATIVE DISTRICT REPUBLICAN COMMITTEE',
                             '31ST DISTRICT REPUBLICANS',
                             '41ST DISTRICT REPUBLICAN COMMITTEE',
                             '30TH DISTRICT REPUBLICANS'
                             ], rename='LOCAL REPUBLICAN ORGS')

    data_pac.combine_donors(['WASHINGTON HEALTH CARE ASSOCIATION',
                             'WASHINGTON HEALTHCARE ASSOCIATION POLITICAL ACTION COMMITTEE',
                             'WASHINGTON HEALTH CARE ASSOC. PAC',
                             'WA HEALTH CARE ASSN PAC / WHCA PAC',
                             'WA HEALTH CARE ASSN (WHCA PAC)',
                             'WASHINGTON HEALTH CARE ASSOC PAC',
                             'WASHINGTON HEALTH CARE ASSOCIATION PAC',
                             'WA HEALTH CARE ASSN PAC (WHCA)',
                             'WA HEALTHCARE ASSN PAC',
                             'WA HEALTHCARE ASSOC. PAC',
                             'WASHINGTON HEALTHCARE ASSOCIATION PAC',
                             'WHCA PAC / WA HEALTH CARE ASSN',
                             'WASHINGTON HEALTH CARE ASSOC',
                             'WA HEALTH CARE ASSOCIATION WHCA PAC',
                             'WA HEALTH CARE ASSN PAC',
                             'WA HEALTH CARE ASSOCIATION',
                             'WASHINGTON HEALTHCARE ASSOCIATION',
                             'WA HEALTH CARE ASSOC. PAC',
                             'WASHINGTON HEALTHCARE ASSOCIAT',
                             'WA HEALTH CARE ASSOCIATION PAC',
                             'WA HEALTHCARE ASSOCIATION',
                             'WA. HEALTH CARE ASSOC. PAC (WHCA - PAC)',
                             'WA HEALTH CARE ASSN PAC / WHCA',
                             'WHCA (WASH HEALTH CARE ASSOC)',
                             'WA HEALTH CARE ASSOC',
                             'WASHINGTON HEALTH CARE ASSN',
                             'WASHINGTON HEALTH CARE ASSOCIA',
                             'WA HEALTH CARE ASSN'])

    data_pac.combine_donors(['PUBLIC SCHOOL EMPLOYEES OF WA',
                             'PSE SEIU 1948 POLITCAL FUND',
                             'PUBLIC SCHOOL EMPLOYEES OF WA.',
                             'PUBLIC SCHOOL EMPLOYEES OF WAS',
                             'PSE OF WA',
                             'PSE SEIU 1948 POLITICAL FUND / PUBLIC SCHOOL EMPLOYEES SEIU LOCAL 1948',
                             'PSE SEIU 1948',
                             'PUBLIC SCHOOL EMPLOYEES OF WA (PSE OF WA) (SEIU LOCAL 1948)',
                             'PSE SEIU 1948 - POLITICAL FUND',
                             'PUBLIC SCHOOL EMPLOYEES ASSOC',
                             'PSE SEIU 1948 POLITICAL FUND',
                             'PUBLIC SCHOOL EMPLOYEES OF WA PAC',
                             'PUBLIC SCHOOL EMPLOYEES SEIU 1948',
                             'PUBLIC SCHOOL EMPLOYEES OF WA (PSE)',
                             'PUBLIC SCHOOL EMPLOYEES OF WA POLITICAL FUND',
                             'PUBLIC SCHOOL EMPLOYEES OF WASHINGTON POLITICAL FUND',
                             'PUBLIC SCHOOL EMPLOYEES WA POLITICAL FUND',
                             'PUBLIC SCHOOL EMPLOYEES SEIU 1948-POLITICAL FUND CAMPAIGN ACCOUNT',
                             'PUBLIC SCHOOL EMP OF WA POLITICAL FUND',
                             'PUBLIC SCHOOLS EMPLOYEES',
                             'PUBLIC SCHOOL EMPOLOYEES OF WA',
                             'PUBLIC SCHOOL EMPLOYEES',
                             'PUBLIC SCHOOL EMPLOYEES OF WASHINGTON',
                             'PSE SEIU 1948 PAC',
                             'PSE SEIU 1948 - POLITICAL FUND CAMPAIGN ACCOUNT'])

    data_pac.combine_donors(['WA HOSPITALITY ASSOCIATION',
                             'WA HOSPITALITY ASSO',
                             'WASHINGTON HOSPITALITY ASSOC / PAC',
                             'WASHINGTON HOSPITALITY ASSOC',
                             'WA HOSPITALITY ASSO PAC',
                             'WA HOSPITALITY ASSOC',
                             'WASHINGTON HOSPITALITY ASSOC. PAC',
                             'WA HOSPITALITY ASSOCIATION PAC',
                             'WASHINGTON HOSPITALITY ASSOC PAC',
                             'WASHINGTON HOSPITALITY ASSOCIATION',
                             'WA HOSPITALITY PAC',
                             'WA HOSPITALITY ASSN PAC',
                             'WA HOSPITALITY ASSOC. PAC',
                             'WASHINGTON HOSPITALITY ASSN. PAC',
                             'WASHINGTON HOSPITALITY ASSOCIATION - PAC',
                             'WASHINGTON HOSPITALITY ASSOCIA',
                             'WA HOSPITALITY ASSN',
                             'WASHINGTON HOSPITALITY ASSOCIATION PAC',
                             'WASHINGTON HOSPITALITY ASSOCIATION POLITIAL ACTION COMMITTEE',
                             'WASHINGTON HOSPITALITY ASSN',
                             'WA HOSPITALITY ASSOC PAC',
                             'WASHINGTON HOSPITALITY ASSN PAC'])

    data_pac.combine_donors(['WA HOSPITAL PAC / WHPAC',
                             'WASHINGTON STATE HOSPITAL ASSOC',
                             'WASHINGTON STATE HOSPITAL ASSOCIATION',
                             'WHPAC',
                             'WASHINGTON HOSPITAL PAC',
                             'WA HOSPITAL PAC',
                             'WASHINGTON HOSPITAL POLITICAL ACTION COMMITTEE',
                             'WA HOSPITAL PAC / WH PAC',
                             'WASHINGTON HOSPITAL PAC (WHPAC)',
                             'WA HOSPITAL PAC (WHPAC)',
                             'WHPAC / WA HOSPITAL PAC'])

    data_pac.combine_donors(['NEW DIRECTION PAC', 'NEW DIRECTION'])

    data_pac.combine_donors(['ASSOCIATED GENERAL CONTRACTORS',
                             'BUILD PAC',
                             'ASSOCIATED GENERAL CONTRACTORS OF WA (BUILD PAC)',
                             'ASSOC GENERAL CONTRACTORYS OF WA',
                             'ASSOCIATEDD GENERAL CONTRACTORS OF WA',
                             'AGC - ASSOCIATED GENERAL CONTRACTOR',
                             'ASSOCIATED CONTRACTORS OF WA / BUILD PAC',
                             'ASSOCIATED GENERAL CONTRACTORS OF WA',
                             'ASSOCIATED GENERAL CONTRACTORS OF WASHINGTONS BUILD PAC',
                             'ASSOCIATED GENERAL CONTRACTORS OF WA BUILD PAC',
                             'ASSOCIATION OF GENERAL CONTRACTORS OF WA',
                             'INLAND NORTHWEST AGC',
                             'ASSOCIATED GENERAL CONTRACTORS BUILD PAC',
                             'ASSOC GENERAL CONTRACTORS OF WA BUILD PAC',
                             'ASSOC GENERAL CONTRACTORS OF WA (BUILD PAC)',
                             'GENERAL CONTRACTORS OF WA / BUILD PAC',
                             "ASSOCIATED GEN'L CONTRACTORS OF WA BUILD PAC",
                             'INLAND NW AGC BUILD EAST PAC',
                             'ASSOC. GENERAL CONTRACTORS OF WA. BUILD PAC',
                             'AGC OF WASHINGTON',
                             'ASSOCIATED GENERAL CONTRATORS OF WA BUILD PAC',
                             'ASSOCIATION OF GENERAL CONTRACTORS OF WA BUILD PAC',
                             'ASSOCIATED GENERAL CONTRACTORS OF WASHINGTON PAC',
                             'ASSOCIATED GENERAL CONTRACTORS OF WASHINGTON - BUILD PAC',
                             'AGC OF WASHINGTON BUILD PAC',
                             'INLAND NW AGC',
                             'ASSOCIATED GENERAL CONTRACTORS OF WASHINGTON BUILD PAC',
                             'ASSOCIATED GENERAL CONTRACTOS OF WASHINGTON PAC',
                             'ASSOCIATED GENERAL CONTRACTORS OF WASHINGTON'])

    data_pac.combine_donors(['BUILDING INDUSTRY ASSOCIATION',
                             'BUILDING INDUSTRY ASSOCAITION OF WA',
                             'BIAW',
                             'BUILDING INDUSTRY ASSOC OF WASHINGTON',
                             'BUILDING INDUSTRY ASSN OF CLARK CO BUILDING INDUSTRY GROUP',
                             'BUILDING INDUSTRY ASSOCIATION PAC',
                             'BUILDING INDUSTRY ASSOCIATION OF CLARK COUNTY',
                             'BUILDING INDUSTRY ASSOCIATION OF WHATCOM COUNTY',
                             'BUILDING INDUSTRY ASSOCIATION OF WASHINGTON'])

    data_pac.combine_donors(['WASHBANK PAC', 'WASHBANKPAC', 'WA BANKERS ASSOC',
                             'WASHBANKPAC STATE', 'WASHBANKPAC STATE FUND', 'WASHINGTON BANKERS ASSOCIATION'])

    data_pac.combine_donors(['WA MORTGAGE BANKERS ASSOCIATION',
                             'WA MORTGAGE BANKERS ASSOC. PAC',
                             'WASHINGTON MORTGAGE BANKERS ASSOCIATION',
                             'WASHINGTON MORTGAGE BANKERS ASSOCATION',
                             'WA MORTGAGE BANKERS ASSN',
                             'WA MORTGAGE BANKERS ASSN PAC',
                             'WA MORTGAGE BANKERS ASSOCIATION PAC',
                             'WASHINGTON MORTGAGE BANKERS ASSOC PAC',
                             'WA MORTGAGE BANKERS ASSOC',
                             'WASHINGTON MORTGAGE BANKERS ASSOCIATION PAC'])

    data_pac.combine_donors(['COMMUNITY BANKERS OF WA',
                             'CBW PAC COMMUNITY BANKERS OF WA',
                             'COMMUNITY BANKERS OF WASHINGTO',
                             'CBW PAC - COMMUNITY BANKERS OF WA',
                             'CBW PAC COMMUNITY BANKERS OF WASHINGTON',
                             'COMMUNITY BANKERS OF WASHINGTON PAC',
                             'COMMUNITY BANKERS OF WASHINGTON',
                             'COMMUNITY BANKERS OF WA PAC',
                             'COMMUNITY BANKERS OF WA (CBW PAC)'])

    data_pac.combine_donors(['WALMART', 'WAL-MART STORES, INC.', 'WALMART STORES, INC'])




def do_ie_synonyms(data_ie):
    # For IE candidate synonyms, must do 1631, 1634, 1639, and 940 first so that the local ones are found correctly

    data_ie.combine_candidates(cand_list=[i for i in data_ie.all_candidates.keys() if (i.find('940') >= 0)],
                               rename='940')
    data_ie.combine_candidates(cand_list=[i for i in data_ie.all_candidates.keys() if (i.find('1631') >= 0)],
                               rename='1631')
    data_ie.combine_candidates(cand_list=[i for i in data_ie.all_candidates.keys() if (i.find('1634') >= 0)],
                               rename='1634')
    data_ie.combine_candidates(cand_list=[i for i in data_ie.all_candidates.keys() if (i.find('1639') >= 0)],
                               rename='1639')
    data_ie.combine_candidates(
        cand_list=[i for i in data_ie.all_candidates.keys() if (i.find('0,', 0, 3) >= 0) | (i.find('1,', 0, 3) >= 0)],
        rename='Local Ballot Measures')





