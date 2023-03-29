import os
from locate import this_dir
import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from random import randint, choice
import itertools
import datetime as dt

#Change path to retrieve functions
my_dir=str(this_dir())
if my_dir.split('\\')[-1] !='venv':
    filepath = os.path.realpath(f'{my_dir}/venv')
    os.chdir(filepath)

#Import Functions to Retrieve the Form Details
from form_extractor import get_form_details
#Import Functions to import the proxy list & header
from proxy_header_functions import proxy_selection, header_selection

username=proxy_selection()[0]
password=proxy_selection()[1]
proxies=proxy_selection()[2]

#Randomly Select Proxy & Reformat for Session Inclusion
proxy=choice(proxies).strip()
prox_ins='http://'+username+':'+password+'@'+proxy
proxies={'https': prox_ins}

#Manage Header
headers=header_selection()

# initialize an HTTP session and Extract Form Response
url=f'https://www.allcleartravel.co.uk/cgi-bin/lansaweb?PROCFUN+allclear7+alv7001+ALC+ENG'

s=HTMLSession()
s.headers.update(headers)
s.proxies.update(proxies)

res=s.get(url)
s.close()

#Parse the Form Response Data & Extract Input Criteria
soup=BeautifulSoup(res.html.html, "html.parser")
form_ext=soup.find("form")

form_det=get_form_details(form_ext)
inputs=form_det['inputs']

#########################
# Input Field Selection #
#########################

#State the Inputs we are interested in Collating (excluding RESDO1)
selection=['ASTRIP', 'CNTRY', 'AREGIONA', 'CRUCHK', 'CRUTYPE', 'ATRVTY']

#Create dictionary of Inputs
input_=dict()
for k in range(0,len(selection)):
    input_list=[]
    for input in inputs:
        if input['name'].strip()==selection[k]:
            input_list.append(input['value'].strip())
        input_list=list(dict.fromkeys(input_list))
        input_[selection[k]]=input_list

#Append empty field for destination duplication
input_['CNTRY'].append('')

#Add Lead Customer Age
input_['AGE']=['24', '38', '51', '55', '60', '65', '70', '75', '80', '90']

#Add Trip Duration
input_['DURATION']=['3', '8', '14', '30', '45', '365']

#Medical Warranty managed later with a random distribution
#input_['LWBQE01']=['N', 'Y'] #Unfit to travel
#input_['LWBQE02']=['N', 'Y'] #On a medical waiting list
#input_['LWBQE03']=['N', 'Y'] #Terminal Prognosis

#Create every permutation of Inputs
iter_feed=[]
input_.keys()
for keys in input_.keys():
    #print(keys,input_[keys])
    iter_feed.append(input_[keys])

iterations=list(itertools.product(*iter_feed))

#Remove Single trips with Regional Permutations
rem_single=[i for i in iterations if i[0]=='S' and i[2]!='']
for remove in rem_single:
    iterations.remove(remove)

#Remove Trips with Impossible Trip Lengths
rem_satl=[i for i in iterations if (i[0]=='S' and i[7]=='365') or
                                   (i[0]=='A' and i[7]!='365')]
for remove in rem_satl:
    iterations.remove(remove)

#Remove Annual trips with Country Permutations
rem_annual=[i for i in iterations if i[0]=='A' and i[1]!='']
for remove in rem_annual:
     iterations.remove(remove)

#Remove trips without designated Country or Region
rem_blank=[i for i in iterations if i[1]=='' and i[2]=='']
for remove in rem_blank:
     iterations.remove(remove)

#Remove trips without a Cruise, but with a Cruise Type Assigned
rem_blank=[i for i in iterations if i[3]=='N' and i[4]=='Y']
for remove in rem_blank:
     iterations.remove(remove)

iterations.sort()
dfa=pd.DataFrame(iterations,columns=(input_.keys()))

#Randomise order of file
rand_list=[]
for k in range(0,len(dfa)):
    rand_list.append(randint(0,1000000))
dfa['rand']=rand_list
dfa=dfa.sort_values(by=['rand'])
dfa.reset_index(inplace=True, drop=False)
dfa=dfa.drop('rand', axis=1)
dfa=dfa.rename(columns={'index':'ORIG_ORDER'})

#Create Trip Start and End Dates
from form_functions import trip_date_generator

trip_com_list=[]
trip_end_list=[]
lead_time_list=[]
for k in range(0,len(iterations)):
    duration=int(dfa['DURATION'][k])
    trip_type=dfa['ASTRIP'][k]
    trip_com=trip_date_generator(trip_type)[0]
    trip_end=trip_com+dt.timedelta(days=duration)     #Single Trips use Duration
    lead_time=1+(trip_com-dt.date.today()).days

    trip_com_list.append(trip_com.strftime("%d/%m/%Y"))
    trip_end_list.append(trip_end.strftime("%d/%m/%Y"))
    lead_time_list.append(str(lead_time))

dfa['TRIP_START']=trip_com_list
dfa['TRIP_END']=trip_end_list
dfa['QUOTE_INPUT_DATE']=dt.datetime.today().strftime('%d/%m/%Y')
dfa['LEAD_TIME']=lead_time_list

#Append Remaining Parameters
dfb=dfa.reindex(columns=('TITLE', 'NAME', 'DOB', 'EMAIL', 'MOBILE',
                         'POSTCODE', 'TOWN', 'ADD_LINE_1', 'HOUSE_NUM',
                         'TITLE_1', 'NAME_1', 'AGE_1', 'DOB_1',
                         'TITLE_2', 'NAME_2', 'AGE_2', 'DOB_2',
                         'TITLE_3', 'NAME_3', 'AGE_3', 'DOB_3',
                         'TITLE_4', 'NAME_4', 'AGE_4', 'DOB_4',
                         'TITLE_5', 'NAME_5', 'AGE_5', 'DOB_5',
                         'TITLE_6', 'NAME_6', 'AGE_6', 'DOB_6',
                         'TITLE_7', 'NAME_7', 'AGE_7', 'DOB_7',
                         'TITLE_8', 'NAME_8', 'AGE_8', 'DOB_8',
                         'TITLE_9', 'NAME_9', 'AGE_9', 'DOB_9',
                         'LWBQE01', 'LWBQE02', 'LWBQE03',
                         'MED_CON', 'MQ_TRAVNO'), fill_value='')
df=pd.concat([dfa, dfb], axis=1)

#Sampling
#df=df.sample(n=25, axis=0)
#df.reset_index(inplace=True, drop=True)

############################
# Create Traveller Details #
############################

#Individual

from travel_grouping import individual

#Call travel_grouping Individual Function
returns=individual(df)

df['TITLE']=returns[0]
df['NAME']=returns[1]
df['DOB']=returns[2]
df['EMAIL']=returns[3]
df['MOBILE']=returns[4]

#Populate Address Details

from form_functions import address_generator

returns=address_generator(df)

df['POSTCODE']=returns[0]
df['TOWN']=returns[1]
df['ADD_LINE_1']=returns[2]
df['HOUSE_NUM']=returns[3]

#Couple

from travel_grouping import couple

#Call travel_grouping Couple Function
returns=couple(df)

df['TITLE_1']=returns[0]
df['NAME_1']=returns[1]
df['AGE_1']=returns[2]
df['DOB_1']=returns[3]

#Family

from travel_grouping import family

returns=family(df)

title_list_f=returns[0]
name_list_f=returns[1]
age_list_f=returns[2]
dob_list_f=returns[3]

for k in range(0,len(df)):
    if df['ATRVTY'][k]=='F':
        for l in range(0,len(title_list_f[k])):

            df.iloc[k,22+(l*4)]=title_list_f[k][l]
            df.iloc[k,23+(l*4)]=name_list_f[k][l]
            df.iloc[k,24+(l*4)]=age_list_f[k][l]
            df.iloc[k,25+(l*4)]=dob_list_f[k][l]

    else:
        continue

#Group

from travel_grouping import group

returns=group(df)

title_list_g=returns[0]
name_list_g=returns[1]
age_list_g=returns[2]
dob_list_g=returns[3]

for k in range(0,len(df)):
    if df['ATRVTY'][k]=='G':
        for l in range(0,len(title_list_g[k])):

            df.iloc[k,22+(l*4)]=title_list_g[k][l]
            df.iloc[k,23+(l*4)]=name_list_g[k][l]
            df.iloc[k,24+(l*4)]=age_list_g[k][l]
            df.iloc[k,25+(l*4)]=dob_list_g[k][l]

    else:
        continue

#Medical Warranty

#On a medical waiting list

mwl_list=[]

for k in range(0,len(df)):
    ages=set()
    ages={df['AGE'][k], df['AGE_1'][k], df['AGE_2'][k], df['AGE_3'][k],
            df['AGE_4'][k], df['AGE_5'][k], df['AGE_6'][k], df['AGE_7'][k],
            df['AGE_8'][k], df['AGE_9'][k]}
    max_age=max([int(i) for i in ages if i!=''])
    score=randint(1,1000)+max_age
    if score>=1030:
        mwl_list.append('Y')
    else:
        mwl_list.append('N')

#Unfit to travel or Terminal Prognosis results in no prices being offered
df['LWBQE01']='N'
df['LWBQE02']=mwl_list
df['LWBQE03']='N'

#Medical Conditions

med_conditions=['Gout', 'Corneal Ulcer', 'Appendicitis', 'Haemangioma', 'Whooping Cough']

med_con_list=[]

for k in range(0,len(df)):
    ages=set()
    ages={df['AGE'][k], df['AGE_1'][k], df['AGE_2'][k], df['AGE_3'][k],
            df['AGE_4'][k], df['AGE_5'][k], df['AGE_6'][k], df['AGE_7'][k],
            df['AGE_8'][k], df['AGE_9'][k]}
    max_age=max([int(i) for i in ages if i!=''])
    score=randint(1,1000)+max_age
    if score>=1030:
        med_con_list.append(choice(med_conditions))
    else:
        med_con_list.append('')
df['MED_CON']=med_con_list

#Number of travellers

trav_num_list=[]

for k in range(0,len(df)):
    titles=(df['TITLE'][k], df['TITLE_1'][k], df['TITLE_2'][k], df['TITLE_3'][k],
            df['TITLE_4'][k], df['TITLE_5'][k], df['TITLE_6'][k], df['TITLE_7'][k],
            df['TITLE_8'][k], df['TITLE_9'][k])
    trav_num_pop=[i for i in titles if i!='']
    trav_num=len(trav_num_pop)
    trav_num_list.append(trav_num)
df['MQ_TRAVNO']=trav_num_list

#Create a Datetime Timestamp and apply to CSV
ts=dt.datetime.today().strftime("%Y%m%dT%H%M%S")
df.to_csv(f'Input_file_{ts}.csv',mode='w+', index=False)
