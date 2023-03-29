import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import os
from locate import this_dir
import datetime as dt
from random import choice, random
import re

#Change path to retrieve functions
my_dir=str(this_dir())
if my_dir.split('\\')[-1] !='venv':
    filepath = os.path.realpath(f'{my_dir}/venv')
    os.chdir(filepath)

#Import Input File referenced below
input_ref='Input_file_20230327T091556'
df=pd.read_csv(f'{filepath}\{input_ref}.csv', header=0, converters={'AREGIONA':str,
                                                                'MOBILE':str,
                                                                'MQ_TRAVNO':str,
                                                                'MED_CON':str})

#Create Master DataFrame to be Populated with Premiums for each Applicant
df_master=pd.DataFrame(columns=('File_Ref', 'ProvCode', 'Provider', 'Single Trip Premium', 'Annual Premium',
                                'MedVal', 'MedEx', 'BagVal', 'BagEx', 'CanxVal', 'CanxEx'))

#Select the rows in the Input File for which to Retrieve Quotes
for m_loop in range(0,1):
    p=df.iloc[m_loop]

    #Import Proxy list & Headers
    from proxy_header_functions import proxy_selection, header_selection

    headers=header_selection()

    username=proxy_selection()[0]
    password=proxy_selection()[1]
    proxy_list=proxy_selection()[2]

    #Randomly Select Proxy & Reformat for Session Inclusion
    proxy=choice(proxy_list).strip()
    prox_ins='http://'+username+':'+password+'@'+proxy
    proxies={'https': prox_ins}

    #1) Capture Quote Form Fields

    session=HTMLSession()
    session.headers.update(headers)
    session.proxies.update(proxies)

    from capture_quote_form_details import form_capture
    returned_form_details=form_capture(session)

    session=returned_form_details[0]
    qte_ref=returned_form_details[1]
    sec_ref=returned_form_details[2]
    input_list=returned_form_details[3]
    panel_ref=returned_form_details[4]
    process_ref=returned_form_details[5]
    func_ref=returned_form_details[6]
    action=returned_form_details[7]

    #2) Post Form Requirements

    from capture_quote_form_details import post_form_req
    returned_form_details=post_form_req(session, p, qte_ref)

    session=returned_form_details[0]
    AREQUOTE=returned_form_details[1]
    SWBDEPV=returned_form_details[2]
    dateto=returned_form_details[3]
    dateannual=returned_form_details[4]
    country_code=returned_form_details[5]
    region_code=returned_form_details[6]

    #3) Post Form Details

    from capture_quote_form_details import post_cust_details
    returned_form_details=post_cust_details(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                            AREQUOTE, SWBDEPV, dateto, dateannual, country_code, region_code)

    session=returned_form_details[0]
    action=returned_form_details[1]
    panel_ref=returned_form_details[2]
    process_ref=returned_form_details[3]
    func_ref=returned_form_details[4]

    #4) Medical Warranty

    from capture_quote_form_details import post_med_warranty
    returned_form_details=post_med_warranty(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                            AREQUOTE, region_code)

    session=returned_form_details[0]
    action=returned_form_details[1]
    panel_ref=returned_form_details[2]
    process_ref=returned_form_details[3]
    func_ref=returned_form_details[4]

    #Create a different path for Applicants with Medical Conditions

    if p['MED_CON']!='':    #Medical Conditions

        #5) Initiate Medical Search

        from capture_medical_details import initiate_medical_search
        returned_form_details=initiate_medical_search(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                                    AREQUOTE, region_code)
        session=returned_form_details[0]
        action=returned_form_details[1]
        panel_ref=returned_form_details[2]
        process_ref=returned_form_details[3]
        func_ref=returned_form_details[4]

        #6) Medical Search 1

        from capture_medical_details import medical_search_1
        returned_form_details=medical_search_1(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                            AREQUOTE, region_code)
        session=returned_form_details[0]
        action=returned_form_details[1]
        panel_ref=returned_form_details[2]
        process_ref=returned_form_details[3]
        func_ref=returned_form_details[4]
        SV1MREF=returned_form_details[5]
        SV1MREF_1=returned_form_details[6]
        LMQ_ANS1=returned_form_details[7]
        PSTDROWNUM=returned_form_details[8]

        #6a) Medical Questions

        from capture_medical_details import medical_questions
        returned_form_details=medical_questions(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                                AREQUOTE, region_code, SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM)
        session=returned_form_details[0]
        action=returned_form_details[1]
        panel_ref=returned_form_details[2]
        process_ref=returned_form_details[3]
        func_ref=returned_form_details[4] 

        #7) Medical Collection (Miss this step for Gout)

        if p['MED_CON']!='Gout':
            from capture_medical_details import medical_collection
            returned_form_details=medical_collection(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                                    AREQUOTE, region_code, SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM)
            session=returned_form_details[0]
            action=returned_form_details[1]
            panel_ref=returned_form_details[2]
            process_ref=returned_form_details[3]
            func_ref=returned_form_details[4]

        #8) Post Quote

            from capture_medical_details import post_quote
            returned_form_details=post_quote(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                            AREQUOTE, region_code, SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM)
            quotes=returned_form_details

        else:        #8) Post Quote

            from capture_medical_details import post_quote
            returned_form_details=post_quote(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                            AREQUOTE, region_code, SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM)
            quotes=returned_form_details

    else:   #No Medical Conditions

        #5) Medical Requirements Validation

        from capture_quote_form_details import post_med_validation
        returned_form_details=post_med_validation(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                                                AREQUOTE, region_code)

        session=returned_form_details[0]
        action=returned_form_details[1]
        panel_ref=returned_form_details[2]
        process_ref=returned_form_details[3]
        func_ref=returned_form_details[4]

        #6) Quotes Page

        from capture_quote_form_details import post_quote
        quotes=post_quote(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                        AREQUOTE, region_code)

    #9) Produce Output

    #Call Output Function
    from output_function import output_collation
    df_temp=output_collation(quotes, p, m_loop, input_ref)
    
    #Append Output to Master File
    frames=[df_master, df_temp]
    df_master=pd.concat(frames,axis=0)

df_master.to_csv(f'{input_ref}_output.csv',mode='w+',index=False)

