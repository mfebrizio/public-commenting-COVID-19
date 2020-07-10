#!/usr/bin/env python
# coding: utf-8

# # Public Commenting in a Pandemic

# ## Data Cleaning

# In[1]:


# import packages
import pandas as pd
import numpy as np
import json
import time
import os
import datetime
import re


# In[2]:


# Specify the path of the folder where the data are saved
filePath = "C:/Users/mark/Box Sync/_MF/Assignments/Insights/Public Commenting and COVID-19/Data/Annual/"


# In[ ]:





# ## 2020

# In[3]:


# load CSV
fileName = 'endpoint_documents_PS_2020.csv'
with open(filePath+fileName,'r',encoding='utf-8') as loadfile:
    df2020 = pd.read_csv(loadfile, index_col='index')
df2020.info()


# In[4]:


# shorten/rename number of comments received column
df2020 = df2020.rename(columns={'numberOfCommentsReceived': 'commentsReceived'})

# create posted count column
df2020['commentsPosted'] = 1

df2020.loc[:,['commentsPosted','commentsReceived']].query('commentsReceived > 1')


# In[5]:


# create list for documentId's of entries to clean
cleaning_list = []
type(cleaning_list)


# ### Dates and Months

# In[6]:


# create new columns for year and month
df2020['postedYear'] = df2020['postedDate'].str.slice(start=0,stop=4)
df2020['postedMonth'] = df2020['postedDate'].str.slice(start=6,stop=7)

# convert to integers
df2020['postedYear'] = pd.to_numeric(df2020['postedYear'])
df2020['postedMonth'] = pd.to_numeric(df2020['postedMonth'])

# return new columns
print(df2020.loc[:,['postedYear','postedMonth']].dtypes)
df2020.loc[:,['postedYear','postedMonth']]


# In[7]:


# created new column with postedDate in datetime format
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.to_datetime.html
df2020['postedDatetime'] = pd.to_datetime(df2020['postedDate'], utc=True)
df2020.loc[:,['postedDate','postedDatetime']]


# In[8]:


# pivot by month
by_YearMonth = pd.pivot_table(df2020,values=['commentsPosted','commentsReceived'],
                              columns=['postedYear'],
                              index=['postedMonth'],
                              aggfunc=np.sum, margins=False)

by_YearMonth.loc[:,:]


# In[9]:


# query entries with Month == 6
queries = df2020.loc[:,['postedMonth','postedDate','documentId']].query('postedMonth == 6')
queries


# In[10]:


# add to cleaning list
docs_to_add = {'fix_month':
             queries.loc[:,'documentId'].tolist()}
cleaning_list.append(docs_to_add)
print(cleaning_list)


# In[11]:


# ----- Retrieve receivedDates for comments where Month==6 ----- #
import requests

# general variables for setting parameters
APIkey = "fYTx9mVjuwc2ZSsdqmbgdtSqx7HGUd3aCRkiH6bC"
baseURL = "https://api.data.gov:443/regulations/v3/document.json?"
dctId = ""

# set parameters
params = {'api_key': APIkey,
          'documentId': dctId}

# create objects for 
fix_month = cleaning_list[0]['fix_month']
range_fix = len(fix_month)
receivedFix = [] # list for adding receivedDate

# retrieve comments using Requests library and check GET request response 
for d in range(range_fix):
    dctId = fix_month[d]
    params.update({'documentId': dctId})

    dct_response = requests.get(baseURL, params=params)
    RL_remaining = int(dct_response.headers['X-RateLimit-Remaining'])

    if dct_response.status_code != 200:
        print('code '+str(dct_response.status_code)+' for page #'+str(pageIndex), 
              dct_response.text, sep='\n')
    if RL_remaining < 10:
        print('Rate Limit remaining: '+str(RL_remaining),
              "sleeping 1 minute...", sep='\n')
        time.sleep(60)

    this_receivedDate = dct_response.json()['receivedDate']
    receivedFix.append(this_receivedDate)

print('Length of receivedFix is '+str(len(receivedFix)))

# replace postedDate with receivedDate for incorrect entries
fix_list = list(zip(fix_month,receivedFix))

for n in range(len(fix_list)):
    bool_fix = [True if item in fix_list[n][0] else False for item in df2020.loc[:,'documentId'].tolist()]
    df2020.loc[bool_fix,'postedDate'] = fix_list[n][1]

    # revise year and month columns
    df2020.loc[bool_fix,'postedYear'] = int(fix_list[n][1][0:4])
    df2020.loc[bool_fix,'postedMonth'] = int(fix_list[n][1][6:7])


# check if any obs have Month==6
queries = df2020.loc[:,['postedMonth','postedDate','documentId']].query('postedMonth == 6')
queries


# In[ ]:





# ### Agency groupings

# In[12]:


by_Agency = pd.pivot_table(df2020,
                           values=['commentsPosted','commentsReceived'],
                           index=['agencyAcronym'],
                           aggfunc=np.sum, margins=False)
print(len(by_Agency))
by_Agency


# In[13]:


agency_list = by_Agency.index.tolist()
print(len(agency_list),'\n')
print(agency_list)


# In[14]:


# create dictionary for Branch to Agency lookups
branch_dict = {'Judicial': ['USC'], 
               'Legislative': ['LOC', 'COLC'], 
               'Independent': ['AID', 'ATBCB', 'CFPB', 'CNCS', 'CPSC', 'CSB', 'EAC', 
                               'EEOC', 'FRTIB', 'FTC', 'GSA', 'NARA', 'NCUA', 'NLRB', 
                               'NRC', 'NTSB', 'OPM', 'PBGC', 'SBA', 'SSA'], 
               'Executive': ['DHS', 'CISA', 'FEMA', 'TSA', 'USCBP', 'USCG', 'USCIS', 
                             'DOC', 'BIS', 'ITA', 'NIST', 'NOAA', 'PTO', 'USBC', 'DOD', 
                             'COE', 'DARS', 'USA', 'USAF', 'DOE', 'EERE', 'DOI', 'BIA', 
                             'BLM', 'BOR', 'BSEE', 'FWS', 'NPS', 'OSM', 'DOJ', 'BOP', 'DEA', 
                             'EOIR', 'DOL', 'ETA', 'LMSO', 'MSHA', 'OFCCP', 'OSHA', 'WCPO', 
                             'DOS', 'DOT', 'FAA', 'FHWA', 'FMCSA', 'FRA', 'FTA', 'MARAD', 
                             'NHTSA', 'PHMSA', 'ED', 'EOP', 'CEQ', 'OMB', 'USTR', 'EPA', 'FAR', 'HHS', 'ATSDR', 'CDC', 'CMS', 'FDA', 'HHSIG', 'HRSA', 'HUD', 'TREAS', 'FINCEN', 'FISCAL', 'IRS', 'OCC', 'TTB', 'USDA', 
                             'AMS', 'APHIS', 'CCC', 'FCIC', 'FNS', 'FS', 'FSA', 'FSIS', 
                             'NRCS', 'RBS', 'RHS', 'RUS', 'VA']
              }
print(len(branch_dict))
print(branch_dict['Independent'])
print(len(branch_dict['Judicial']+
          branch_dict['Legislative']+
          branch_dict['Independent']+
          branch_dict['Executive']) - len(['LOC','EOP']))


# In[15]:


get_ipython().run_cell_magic('time', '', "\n# references:\n    # https://stackoverflow.com/questions/49161120/pandas-python-set-value-of-one-column-based-on-value-in-another-column\n    # https://stackoverflow.com/questions/30446510/list-of-elements-to-boolean-array\n\n# create boolean arrays for each branch\nbool_jud = [True if item in branch_dict['Judicial'] else False for item in df2020.loc[:,'agencyAcronym'].tolist()]\nbool_leg = [True if item in branch_dict['Legislative'] else False for item in df2020.loc[:,'agencyAcronym'].tolist()]\nbool_ind = [True if item in branch_dict['Independent'] else False for item in df2020.loc[:,'agencyAcronym'].tolist()]\nbool_exe = [True if item in branch_dict['Executive'] else False for item in df2020.loc[:,'agencyAcronym'].tolist()]\n\n# create new column for branch\ndf2020['agencyBranch'] = ''\n\n# use boolean arrays to fill new column\ndf2020.loc[bool_jud,'agencyBranch'] = 'Judicial'\ndf2020.loc[bool_leg,'agencyBranch'] = 'Legislative'\ndf2020.loc[bool_ind,'agencyBranch'] = 'Independent'\ndf2020.loc[bool_exe,'agencyBranch'] = 'Executive'\n\ndf2020.loc[:,['agencyAcronym','agencyBranch']]")


# In[16]:


# query df by branch
df2020.query('agencyBranch == ""')


# In[17]:


# query df by multiple branches
df2020.query('agencyBranch == "Legislative" | agencyBranch == "Judicial" ')


# In[18]:


# create dict for Parent Agencies
parent_dict = dict(LOC = ['LOC', 'COLC'], 
                   DHS = ['DHS', 'CISA', 'FEMA', 'TSA', 'USCBP', 'USCG', 'USCIS'],
                   DOC = ['DOC', 'BIS', 'ITA', 'NIST', 'NOAA', 'PTO', 'USBC'],
                   DOD = ['DOD', 'COE', 'DARS', 'USA', 'USAF'],
                   DOE = ['DOE', 'EERE'],
                   DOI = ['DOI', 'BIA', 'BLM', 'BOR', 'BSEE', 'FWS', 'NPS', 'OSM'],
                   DOJ = ['DOJ', 'BOP', 'DEA', 'EOIR'],
                   DOL = ['DOL', 'ETA', 'LMSO', 'MSHA', 'OFCCP', 'OSHA', 'WCPO'],
                   DOS = ['DOS'],
                   DOT = ['DOT', 'FAA', 'FHWA', 'FMCSA', 'FRA', 'FTA', 'MARAD', 'NHTSA', 'PHMSA'],
                   ED = ['ED'],
                   EOP = ['EOP', 'CEQ', 'OMB', 'USTR'],
                   EPA = ['EPA'],
                   FAR = ['FAR'],
                   HHS = ['HHS', 'ATSDR', 'CDC', 'CMS', 'FDA', 'HHSIG', 'HRSA'],
                   HUD = ['HUD'],
                   TREAS = ['TREAS', 'FINCEN', 'FISCAL', 'IRS', 'OCC', 'TTB'],
                   USDA = ['USDA', 'AMS', 'APHIS', 'CCC', 'FCIC', 'FNS', 'FS', 'FSA', 'FSIS', 'NRCS', 'RBS', 'RHS', 'RUS'],
                   VA = ['VA']
                  )

x = 1
print(list(parent_dict.keys())[x])
print(list(parent_dict.values())[x])


# In[19]:


get_ipython().run_cell_magic('time', '', "\n# create new column for parent agency\ndf2020['agencyParent'] = ''\n\n# parent==acronym for judicial & independent agencies\ndf2020.loc[bool_jud,'agencyParent'] = df2020.loc[bool_jud,'agencyAcronym']\ndf2020.loc[bool_ind,'agencyParent'] = df2020.loc[bool_ind,'agencyAcronym']\n\n# set parent for executive & legislative agencies\ndictLength = len(parent_dict)\nlistValues = list(parent_dict.values())\nlistKeys = list(parent_dict.keys())\n\nfor key in range(dictLength):\n    print(list(parent_dict.keys())[key])\n    bool_array = [True if item in listValues[key] else False for item in df2020.loc[:,'agencyAcronym'].tolist()]\n    df2020.loc[bool_array,'agencyParent'] = [listKeys[key] if item in listValues[key] else '' for item in df2020.loc[bool_array,'agencyAcronym'].tolist()]\n\ndf2020.loc[:,['agencyAcronym','agencyParent','agencyBranch']]")


# In[20]:


df2020.loc[:,['agencyAcronym','agencyParent','agencyBranch']].query('agencyParent == ""')


# In[21]:


print(len(df2020.query('agencyBranch == "Independent"')) + 
      len(df2020.query('agencyBranch == "Judicial"')))


# In[22]:


by_AgencyParent = pd.pivot_table(df2020,
                           values=['commentsPosted','commentsReceived'],
                           index=['agencyBranch','agencyParent'],
                           aggfunc=np.sum, margins=False)
print(len(by_AgencyParent))
by_AgencyParent.query('agencyBranch == "Executive"')


# In[ ]:





# ### MCC, Duplicate, or Significantly Similar Comments

# In[23]:


# view MCC comments that are posted as "Representative" comments
    # e.g., "This agency received 21 duplicate or significantly similar comments."
    # Ex: https://www.regulations.gov/document?D=FNS-2019-0009-5664
lookup = ['documentId','title','organization','attachmentCount','commentsPosted','commentsReceived','agencyAcronym','agencyParent','agencyBranch']

df2020.loc[:,lookup].query('commentsReceived != commentsPosted')


# In[24]:


# create bool array for agency-marked MCCs (i.e., representative comments)
bool_MCC = df2020['commentsPosted']!=df2020['commentsReceived']
print(bool_MCC.value_counts(),'\n')

# create bool array for comments to group as representative
    # reference for regex: https://docs.python.org/3/howto/regex.html
bool_group = df2020.loc[:,'title'].str.contains('MM[\d]+|Mass Mail|Mass Comment', regex=True, case=True)
print(bool_group.value_counts(),'\n')

# create bool array for comments that overlap (both R&G)
bool_RnG = bool_MCC & bool_group
print(bool_RnG.value_counts(),'\n')

# create new column
df2020['MCCfilter'] = 'Unique'

# use boolean arrays to fill new column
df2020.loc[bool_MCC,'MCCfilter'] = 'Representative'
df2020.loc[bool_group,'MCCfilter'] = 'Grouped'
df2020.loc[bool_RnG,'MCCfilter'] = 'Both R&G'

# convert new column to categorical
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html#pandas.DataFrame.astype
df2020 = df2020.astype({'MCCfilter': 'category'})
print(df2020.loc[:,'MCCfilter'].value_counts())

df2020.loc[:,['documentId','docketId','agencyAcronym','title','commentsPosted','commentsReceived','MCCfilter']]


# In[25]:


df2020.loc[:,['MCCfilter','title','commentsPosted','commentsReceived']].query('MCCfilter == "Both R&G"')


# In[26]:


by_MCCfilter = pd.pivot_table(df2020, values=['commentsPosted','commentsReceived'],
                              index=['MCCfilter'],
                              aggfunc=np.sum, margins=True)

by_MCCfilter


# In[27]:


# filter comments for grouping
MMfilter = df2020.loc[np.array(df2020['MCCfilter']=='Grouped') | np.array(df2020['MCCfilter']=='Both R&G'),:]

pd.pivot_table(MMfilter, 
               values=['commentsPosted','commentsReceived'], 
               index=['docketId'], 
               aggfunc=np.sum)


# In[28]:


# determine number of MCC campaigns in docket and verify tally of comments
docket = 'CEQ-2019-0003'
restriction = MMfilter['docketId']==docket
obs = 1
num = 0
massTally = num
obsTally = []

while obs > 0:
    # use two different regex patterns -- Mass Mail Campaign #\\b and MMx#\\b
    bool_lookup = MMfilter.loc[restriction,'title'].str.contains('Mass Mail Campaign '+str(num)+r'\b|MM'+str(num)+r'\b',
                                                                 regex=True, case=True)
    
    try: # try 1
        obs = int(bool_lookup.value_counts()[True])
        print('MCC '+str(num)+' -- obs = '+str(obs))
        massTally = num
        obsTally.extend([obs])
    except:
        print('Error occurred for MCC'+str(num))
        try: # try 2
            num = num + 1
            bool_lookup = MMfilter.loc[restriction,'title'].str.contains('Mass Mail Campaign '+str(num)+r'\b|MM'+str(num)+r'\b', regex=True, case=True)
            obs = int(bool_lookup.value_counts()[True])
        except:
            print('Error occurred for MCC'+str(num))
            try: # try 3
                num = num + 1
                bool_lookup = MMfilter.loc[MMfilter['docketId']!=docket,'title'].str.contains('Mass Mail Campaign '+str(num)+r'\b|MM'+str(num)+r'\b', regex=True, case=True)
                obs = int(bool_lookup.value_counts()[True])
            except:
                print('Error occurred for MCC'+str(num))
                obs = 0
    else:
        num = num + 1

print('MCC tally = '+str(massTally)+' -- obs tally = '+str(sum(obsTally)))
print(len(MMfilter.loc[restriction,:]))


# In[29]:


get_ipython().run_cell_magic('time', '', "\n# mission: create new DataFrame of CEQ MCC campaigns for merging with df2020\n\n# create lists for populating df columns\nidList = [] ## documentId\ntitleList = [] ## title\nnumList = [] ## MCC number\nobsList = [] ## comments posted for an MCC\n\n# populate lists with for loop and regex\nfor num in range(massTally+1):\n    regex_search = 'Mass Mail Campaign '+str(num)+r'\\b|MM'+str(num)+r'\\b'\n    bool_search = MMfilter.loc[restriction,'title'].str.contains(regex_search,\n                                                                 regex=True, case=True)\n    try: # try 1\n        idList.extend(MMfilter.loc[restriction,:].loc[bool_search,'documentId'].tolist())\n        titleList.extend(MMfilter.loc[restriction,:].loc[bool_search,'title'].tolist())\n        obs = int(bool_search.value_counts()[True])\n        obsList.extend([obs]*obs)\n        numList.extend([num]*obs)\n        if num%50==0:\n            print('Just finished MCC'+str(num))\n    except:\n        print('Error occurred for MCC'+str(num))\n        continue\n\n# zip lists into new list and generate df\ndataList = list(zip(idList,titleList,numList,obsList))\ndfCEQMCC = pd.DataFrame(dataList, columns = ['documentId', 'title', 'MCCnumber', 'commentsGrouped'])\n\n# check whether length of new df is correct\nif len(dfCEQMCC) == len(MMfilter.loc[restriction,:]):\n    print(dfCEQMCC.info())\nelse:\n    print('Check DataFrame before merge. It might be missing entries.')")


# In[30]:


print(len(df2020))
df2020Grouped = df2020.merge(dfCEQMCC, how='outer', on=['documentId','title'], indicator=True, validate='1:1')
df2020Grouped = df2020Grouped.rename(columns={"_merge": "_merge_CEQMCC"})
df2020Grouped.info()


# In[31]:


pd.pivot_table(df2020Grouped, values=['commentsGrouped','commentsPosted'],
               index=['postedMonth'], columns=['MCCfilter'],
               aggfunc='count', dropna=False, fill_value=0, margins=True)


# In[32]:


pd.pivot_table(df2020Grouped, values=['commentsGrouped','commentsPosted'],
               index=['_merge_CEQMCC'],
               aggfunc='count', dropna=False, fill_value=0, margins=True)


# #### Assign representative comments for MCCs

# In[33]:


# create new column for representative comment
df2020Grouped['represent'] = 'Fill'

bool_nan = df2020Grouped['_merge_CEQMCC']=='left_only'
df2020Grouped.loc[bool_nan,'represent'] = 'Unidentified' ## for non-MCCs or those that haven't been identified

bool_rep = df2020Grouped.loc[(~bool_nan),'title'].str.contains('Mass Mail Campaign '+r'\b', regex=True, case=True)
df2020Grouped.loc[bool_rep&(~bool_nan),['represent']] = 'Yes' ## for representative comments

bool_notrep = df2020Grouped.loc[(~bool_nan),'title'].str.contains('MM[\d]+ Comment'+r'\b', regex=True, case=True)
df2020Grouped.loc[bool_notrep&(~bool_nan),['represent']] = 'No' ## for grouped comments that aren't representative

print(bool_nan.value_counts(), 
      bool_rep.value_counts(), 
      bool_notrep.value_counts(), sep='\n\n')

df2020Grouped = df2020Grouped.astype({'represent': 'category'})
print('\n', 
      df2020Grouped.loc[:,'represent'].value_counts())

# pivot against MCC filter
pd.pivot_table(df2020Grouped, index=['represent'], values=['documentId'], columns=['MCCfilter'],
               aggfunc='count', fill_value=0, margins=True)


# In[34]:


df2020Grouped.query('represent == "Yes"').sort_values('MCCnumber', ascending=True)[['MCCnumber','documentId']]


# In[35]:


# ----- Create new DataFrame of Representative Comments ----- #

# list of docIds for representative comments
repIdList = df2020Grouped.query('represent == "Yes"').sort_values('MCCnumber', ascending=True)['documentId'].tolist()

# create list of MMC, docId of earliest postedDate in MCC, docId of latest postedDate in MCC
MCCList = []
postedLast = []
lastDate = []

for MCC in range(1,120):
    MCCList.extend([MCC])
    postedLast.extend(df2020Grouped.query('MCCnumber == @MCC').
                      sort_values('postedDate', ascending=False).head(1)['documentId'])
    lastDate.extend(df2020Grouped.query('MCCnumber == @MCC').
                    sort_values('postedDate', ascending=False, na_position='last').head(1)['postedDate'])

# ----- Retrieve receivedDates for representative comments ----- #
import requests

# general variables for setting parameters
APIkey = "fYTx9mVjuwc2ZSsdqmbgdtSqx7HGUd3aCRkiH6bC"
baseURL = "https://api.data.gov:443/regulations/v3/document.json?"
dctId = ""

# set parameters
params = {'api_key': APIkey,
          'documentId': dctId}

# using postedLast list
range_last = len(postedLast)
receivedLast = [] # list for adding receivedDate of each postedLast entry

# retrieve comments using Requests library and check GET request response 
for d in range(range_last):
    dctId = postedLast[d]
    params.update({'documentId': dctId})

    dct_response = requests.get(baseURL, params=params)
    RL_remaining = int(dct_response.headers['X-RateLimit-Remaining'])

    if dct_response.status_code != 200:
        print('code '+str(dct_response.status_code)+' for page #'+str(pageIndex), 
              dct_response.text, sep='\n')
    if RL_remaining < 10:
        print('Rate Limit remaining: '+str(RL_remaining),
              "sleeping 1 minute...", sep='\n')
        time.sleep(60)

    this_receivedDate = dct_response.json()['receivedDate']
    receivedLast.append(this_receivedDate)

print('Length of receivedLast is '+str(len(receivedLast)))

# ----- Generate df from the lists ----- #
dateList = list(zip(repIdList, MCCList, postedLast, lastDate, receivedLast))
dfRepresent = pd.DataFrame(dateList, columns = ['documentId', 'MCCnumber', 'lastId', 'lastDate', 'receivedDate'])
dfRepresent['represent'] = 'Yes'
dfRepresent = dfRepresent.astype({'represent': 'category'})
dfRepresent.info()


# In[36]:


print(dfRepresent.loc[:,['MCCnumber','receivedDate']].sort_values('receivedDate', ascending=False))


# In[37]:


dfRepresent = dfRepresent[['MCCnumber','lastId','lastDate','receivedDate']]
dfRepresent


# In[38]:


print(len(df2020Grouped))
df2020Represent = df2020Grouped.merge(dfRepresent, how='outer', on=['MCCnumber'], indicator=True, validate='m:1')
df2020Represent = df2020Represent.rename(columns={'_merge': '_merge_represent'})
df2020Represent = df2020Represent.drop(columns=['commentDueDate','commentStartDate','openForComment'])
df2020Represent = df2020Represent.fillna(value={'commentsGrouped': 0, 
                                                'MCCnumber': 0}, downcast='infer')
df2020Represent = df2020Represent.astype({'MCCnumber': 'int64',
                                          'commentsGrouped': 'int64', 
                                          'docketType': 'category', 
                                          'agencyBranch': 'category'})

df2020Represent.info()


# In[39]:


df2020Represent['receivedDate'].value_counts()


# In[ ]:





# ### Filter Comments for Analysis 

# In[40]:


pd.pivot_table(df2020Represent, values=['documentId','commentsPosted','commentsReceived','commentsGrouped'],
               index = ['MCCfilter'], aggfunc={'documentId': 'count',
                                               'commentsPosted': np.sum,
                                               'commentsReceived': np.sum,
                                               'commentsGrouped': np.max}, margins=True)


# In[41]:


pd.pivot_table(df2020Represent, values=['commentsPosted','commentsReceived'], columns=['represent'],
                              index=['MCCfilter'],
                              aggfunc={'commentsPosted':'count',
                                       'commentsReceived': np.sum}, fill_value=0, margins=True)


# In[42]:


df2020Represent.query('represent == "No" & (MCCfilter=="Both R&G")').loc[:,['agencyParent','documentId','commentsReceived','commentsPosted','commentsGrouped','title','MCCnumber']]


# In[43]:


# populate two new columns for analysis of comments
# first, number of comments including MCC totals
df2020Represent['commentsWithMCC'] = np.nan

bool_WithMCC = (df2020Represent['represent']=='Unidentified') ## comments where MCCs haven't been identified
df2020Represent.loc[bool_WithMCC,'commentsWithMCC'] = df2020Represent.loc[bool_WithMCC,'commentsReceived']

bool_WithMCC = (df2020Represent['represent']=='Yes') & (df2020Represent['MCCfilter']=='Both R&G') ## comments that I assigned to represent an MCC but commentsPosted!=commentsReceived (ie, metadata indicates additional commentReceived)
df2020Represent.loc[bool_WithMCC,'commentsWithMCC'] = (df2020Represent.loc[bool_WithMCC,'commentsReceived'] + 
                                                       df2020Represent.loc[bool_WithMCC,'commentsGrouped'] - 1)

bool_WithMCC = (df2020Represent['represent']=='Yes') & (df2020Represent['MCCfilter']=='Grouped') ## comments that I assigned to represent an MCC and commentsPosted==commentsReceived
df2020Represent.loc[bool_WithMCC,'commentsWithMCC'] = df2020Represent.loc[bool_WithMCC,'commentsGrouped']

bool_WithMCC = (df2020Represent['represent']=='No') & (df2020Represent['MCCfilter']=='Both R&G') ## comments grouped with an MCC representative but commentsPosted!=commentsReceived
df2020Represent.loc[bool_WithMCC,'commentsWithMCC'] = df2020Represent.loc[bool_WithMCC,'commentsReceived']

bool_WithMCC = (df2020Represent['represent']=='No') & (df2020Represent['MCCfilter']=='Grouped') ## comments grouped with an MCC representative and and commentsPosted==commentsReceived
df2020Represent.loc[bool_WithMCC,'commentsWithMCC'] = 0

print(df2020Represent['commentsWithMCC'].isna().value_counts(),'\n')


# second, number of comments excluding MCC totals (representative comments count as 1)
df2020Represent['commentsNoMCC'] = np.nan

bool_NoMCC = (df2020Represent['represent']=='Unidentified') ## comments where MCCs haven't been identified
df2020Represent.loc[bool_NoMCC,'commentsNoMCC'] = df2020Represent.loc[bool_NoMCC,'commentsPosted']

bool_NoMCC = (df2020Represent['represent']=='Yes') & (df2020Represent['MCCfilter']=='Both R&G') ## comments that I assigned to represent an MCC but commentsPosted!=commentsReceived
df2020Represent.loc[bool_NoMCC,'commentsNoMCC'] = df2020Represent.loc[bool_NoMCC,'commentsPosted']

bool_NoMCC = (df2020Represent['represent']=='Yes') & (df2020Represent['MCCfilter']=='Grouped') ## comments that I assigned to represent an MCC and commentsPosted==commentsReceived
df2020Represent.loc[bool_NoMCC,'commentsNoMCC'] = df2020Represent.loc[bool_NoMCC,'commentsPosted']

bool_NoMCC = (df2020Represent['represent']=='No') ## comments grouped with an MCC representative
df2020Represent.loc[bool_NoMCC,'commentsNoMCC'] = 0

print(df2020Represent['commentsNoMCC'].isna().value_counts(),'\n')


# convert new columns to integers
df2020Represent = df2020Represent.astype({'commentsWithMCC': 'int64', 
                                          'commentsNoMCC': 'int64'})


# In[44]:


# populate new column for analyzing comment dates; should fix issue with late posted comments
df2020Represent['analysisDate'] = ''

bool_date = df2020Represent['represent']=='Unidentified' ## comments where MCCs haven't been identified
df2020Represent.loc[bool_date,'analysisDate'] = df2020Represent.loc[bool_date,'postedDate']

bool_date = df2020Represent['represent']!='Unidentified' ## comments with identified MCCs
df2020Represent.loc[bool_date,'analysisDate'] = df2020Represent.loc[bool_date,'receivedDate']

print(df2020Represent['analysisDate'].isna().value_counts(),'\n')
print((df2020Represent['analysisDate']=='').value_counts(),'\n')


# In[56]:


pd.pivot_table(df2020Represent, values=['receivedDate','postedDate','analysisDate'], index=['represent'],
                              aggfunc='count', dropna=False, margins=True)


# In[46]:


# create new columns for year and month
df2020Represent['analysisYear'] = df2020Represent['analysisDate'].str.slice(start=0,stop=4)
df2020Represent['analysisMonth'] = df2020Represent['analysisDate'].str.slice(start=6,stop=7)

# convert to integers
df2020Represent = df2020Represent.astype({'analysisYear': 'int64', 
                                          'analysisMonth': 'int64'})

# return new columns
print(df2020Represent.loc[:,['analysisYear','analysisMonth']].dtypes)
df2020Represent.loc[:,['analysisYear','analysisMonth']]


# In[ ]:





# ## Check Results // Export for Analysis

# In[48]:


# pivot comments (excluding MCCs)

pd.pivot_table(df2020Represent, values=['commentsNoMCC'], columns=['postedMonth'],
                              index=['analysisMonth'],
                              aggfunc=np.sum, fill_value=0)


# In[54]:


# pivot comments (including MCCs)

pd.pivot_table(df2020Represent, values=['commentsWithMCC'], columns=['postedMonth'],
                              index=['analysisMonth'],
                              aggfunc=np.sum, fill_value=0)


# In[63]:


print(df2020Represent.columns.tolist(),'\n')


# In[62]:


# export dataframe for analysis
write_columns = ['agencyBranch', 'agencyParent', 'agencyAcronym', 'docketId', 'docketType', 
                 'documentId', 'submitterName', 'title', 'organization', 'attachmentCount', 
                 'analysisDate', 'analysisYear', 'analysisMonth', 
                 'commentsWithMCC', 'commentsNoMCC', 
                 'MCCfilter', 'MCCnumber', 'represent']

savePath = "C:/Users/mark/Box Sync/_MF/Assignments/Insights/Public Commenting and COVID-19/Data/Annual/"
saveFile = 'cleaned_PS_2020.csv'

# write to csv, reference: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
with open(savePath+saveFile, 'w', encoding='utf-8') as outfile:
    df2020Represent.to_csv(outfile, index_label='index', line_terminator='\n', columns=write_columns)


# In[ ]:




