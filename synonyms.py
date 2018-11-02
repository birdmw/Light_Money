
def do_synonyms(data_pac):
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

    data_pac.combine_donors(['WA ST REPUB PARTY EXEMPT',
                             'WA STATE REPUBLICAN PARTY',
                             'WA ST REPUB PARTY NON EXEMPT',
                             'WASHINGTON STATE REPUBLICAN PARTY - EXEMPT ACCOUNT',
                             'WASHINGTON STATE REPUBLICAN PARTY'])

    data_pac.combine_donors(['WASHINGTON STATE DEMOCRATIC CENTRAL COMMITTEE',
                             'WA ST DEMO CENT COMM NON EXEMPT',
                             'WA STATE DEMOCRATS',
                             'WASHIINGTON STATE DEMOCRATS',
                             'WA STATE DEMOCRATIC CENTRAL COMMITTEE',
                             'WASHINGTON STATE DEMOCRATIC PARTY',
                             'WA STATE DEMOCRATIC PARTY',
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
