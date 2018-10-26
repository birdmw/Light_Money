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
            'HOUSE DEMO CAMP COMM']

syn_sdcc = ['WASHINGTON SENATE DEMOCRATIC CAMPAIGN',
            'WA SENATE DEMOCRATIC CAMPAIGN (WSDC)',
            'WA SENATE DEMOCRATIC CAMPAIGN',
            'WA SENATE DEMO CAMP']

syn_microsoft = ['MICROSOFT PAC',
                 'MICROSOFT CORP',
                 'MICROSOFT',
                 'MICROSOFT CORPORATION PAC',
                 'MICROSOFT POLITICAL ACTION COMMITTEE',
                 'MICROSOFT CORPORATION']

syn_amazon = ['AMAZON.COM',
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
              'AMAZON',
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

syn_enterprise_wa = ['ENTERPRISE WASHINGTON',
                     'ENTERPRISE WA JOBSPAC',
                     'OUR OLYMPIC COMMUNITIES ENTERPRISE WA',
                     'CITIZENS FOR WORKING COURTS ENTERPRISE WASHINGTON',
                     'SOUTH SOUND FUTURE PAC ENTERPRISE WA',
                     'ENTERPRISE WASHINGTON JOBS PAC',
                     'CIT FOR PROGRESS ENTERPRISE WA',
                     "ENTERPRISE WASHINGTON'S JOBS PAC"]

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
data_pac.combine_donors(syn_enterprise_wa)
data_pac.combine_donors(syn_enterprise_holdings)

