def form_capture(session):
    from bs4 import BeautifulSoup
    from form_extractor import get_form_details

    headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "www.allcleartravel.co.uk",
            "Origin": "https://www.allcleartravel.co.uk",
            "Referer": "https://www.allcleartravel.co.uk/",
            "sec-ch-ua": session.headers['sec-ch-ua'],
            "sec-ch-ua-Mobile": "?0",
            "sec-ch-ua-Platform": session.headers['sec-ch-ua-Platform'],
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": session.headers['User-Agent']}

    # Examine Quote Detail Form

    url=f'https://www.allcleartravel.co.uk/cgi-bin/lansaweb?PROCFUN+allclear7+alv7001+ALC+ENG'

    session.headers.update(headers)
    res=session.get(url)
    soup=BeautifulSoup(res.html.html, "html.parser")
    form_ext=soup.find("form")

    form_det=get_form_details(form_ext)

    action=form_det['action'].split('+')[1].upper()

    #Quote Form Detail Capture

    form_inpts=form_det['inputs']

    input_list=[]
    for input in form_inpts:
        if input['name'].strip()=='AWAWSID':
            qte_ref=input['value']
        if input['name'].strip()=='LSECNO':
            sec_ref=input['value']
        if input['type']!='hidden':
            input_list.append(input)
        if input['name'].strip()=='_PANEL':
            panel_ref=input['value'].strip()
        if input['name'].strip()=='_PROCESS':
            process_ref=input['value'].strip()
        if input['name'].strip()=='_FUNCTION':
            func_ref=input['value'].strip()

    return(session,
           qte_ref,
           sec_ref,
           input_list,
           panel_ref,
           process_ref,
           func_ref,
           action)

def post_form_req(session, p, qte_ref):
    import datetime as dt
    from random import randint

    #Write WSIDdatetime

    headers={'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '500',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.allcleartravel.co.uk',
            'Origin': 'https://www.allcleartravel.co.uk',
            'Referer': 'https://www.allcleartravel.co.uk/',
            'sec-ch-ua': session.headers['sec-ch-ua'],
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': session.headers['sec-ch-ua-platform'],
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': session.headers['User-Agent'],
            'X-KL-Ajax-Request': 'Ajax_Request',
            'X-Requested-With': 'XMLHttpRequest'}

    url=f'https://www.allcleartravel.co.uk/ajax/WriteWSIDdatetime.php?i={qte_ref}'

    today=dt.date.today().strftime("%d/%m/%Y")
    curr_time=dt.datetime.now().strftime("%T")

    data={'wsid': qte_ref, 'dt': str(int(today[0:2])), 'mt': str(int(today[3:5])), 'yt': str(int(today[8:10])), 'ht': str(int(curr_time[0:2])), 'nt': str(int(curr_time[3:5]))}

    session.headers.update(headers)
    r=session.post(url, data=data)

    #Upload Traveller-type

    url=f'https://www.allcleartravel.co.uk/ajax/traveller-type.php?i={qte_ref}'

    data={'wsid': qte_ref, 'scheme': 'OPT', 'bus': '114', 'tt': p['ATRVTY']}

    r=session.post(url, data=data)

    if p['ASTRIP']=='A':
        AREQUOTE='Y'
        SWBDEPV=''
        dateto=''
        dateannual=p['TRIP_START']
    else:
        AREQUOTE=''
        SWBDEPV=p['TRIP_START']
        dateto=p['TRIP_END']
        dateannual=p['QUOTE_INPUT_DATE']
    
    #Policy Type

    url=f'https://www.allcleartravel.co.uk/ajax/policy-type.php?i={qte_ref}'

    data={'wsid': qte_ref, 'pt': p['ASTRIP']}

    r=session.post(url, data=data)

    #Country Type

    if p['ASTRIP']=='S':                        #Single Trip

        # Upload Holiday Dates
        url = f'https://www.allcleartravel.co.uk/ajax/holiday-dates.php?i={qte_ref}'

        data = {'wsid': qte_ref, 'tt': p['TRIP_END'], 'tf': p['TRIP_START'], 'dy': int(p['DURATION'])+1,
                'ad': '', 'dt': str(int(today[0:2])), 'mt': str(int(today[3:5])),
                'yt': str(int(today[8:11])), 'ht': str(int(curr_time[0:2])), 'nt': str(int(curr_time[3:5]))}

        r = session.post(url, data=data)

        #Upload Destination Details
        url = f'https://www.allcleartravel.co.uk/ajax/country-type.php?i={qte_ref}'

        region_code=''                          #Region not used for Single Trip
        if p['CNTRY']=='U':
            if randint(1,100)>50:
                country_code='219'
            else:
                country_code='117'
        if p['CNTRY']=='S':
            country_code='82'
        if p['CNTRY']=='O':
            country_code='92'
        data = {'wsid': qte_ref, 'ct': country_code+','}

    if p['ASTRIP']=='A':                        #Annual Trip
        country_code=''                         #Country not used for Single Trip
        if p['AREGIONA']=='1':
            region_code='D'
        elif p['AREGIONA']=='2':
            region_code='E'
        elif p['AREGIONA']=='4':
            region_code='X'
        elif p['AREGIONA']=='5':
            region_code='W'
    
        # Upload Region Type
        url = f'https://www.allcleartravel.co.uk/ajax/region-type.php?i={qte_ref}'

        data = {'wsid': qte_ref, 'rt':p['AREGIONA']}
        r=session.post(url, data=data)

        # Upload Annual Holiday Dates
        url = f'https://www.allcleartravel.co.uk/ajax/holiday-dates-annual.php?i={qte_ref}'

        data = {'wsid': qte_ref, 'tt':'', 'tf': p['TRIP_START'], 'dy': '', 'ad': p['TRIP_START'],
                'dt': str(int(today[0:2])), 'mt': str(int(today[3:5])), 'yt': str(int(today[8:10])),
                'ht': str(int(curr_time[0:2])), 'nt': str(int(curr_time[3:5]))}

    r=session.post(url, data=data)

    #Email Address

    url=f'https://www.allcleartravel.co.uk/ajax/email-address.php?i={qte_ref}'

    data={'wsid': qte_ref, 'et': p['EMAIL']}

    r=session.post(url, data=data)

    #Postcode

    url=f'https://www.allcleartravel.co.uk/ajax/postcode.php?i={qte_ref}'

    data={'wsid': qte_ref, 'scheme': 'OPT', 'p1': p['POSTCODE'].replace(' ', ''), 'pno': p['MOBILE'],
        'mno': '', 'hno': p['HOUSE_NUM'], 'add1': p['ADD_LINE_1'], 'tn': p['TOWN'], 'cty': '',
        't1': p['TITLE'], 'f1': p['NAME'].split(' ')[0], 's1': p['NAME'].split(' ')[1],
        'em': p['EMAIL']}

    r=session.post(url, data=data)

    #Traveller Details

    url=f'https://www.allcleartravel.co.uk/ajax/traveller-details.php?i={qte_ref}'

    #Create Core Traveller Details as Dictionary
    trav_details={'wsid': qte_ref, 'scheme': 'OPT', 'dt': str(int(today[0:2])),
                  'mt': str(int(today[3:5])), 'yt': str(int(today[8:10])), 
                  'ht': str(int(curr_time[0:2])), 'nt': str(int(curr_time[3:5]))}
    
    #Append Each Traveller's Details as Dictionary Keys
    for trav in range(1,int(p['MQ_TRAVNO'])+1):
        if trav==1:
            trav_details['t'+str(trav)]=p['TITLE']
            trav_details['f'+str(trav)]=p['NAME'].split(' ')[0]
            trav_details['s'+str(trav)]=p['NAME'].split(' ')[1]
            trav_details['d'+str(trav)]=str(int(p['DOB'].split('/')[0]))
            trav_details['m'+str(trav)]=str(int(p['DOB'].split('/')[1]))
            trav_details['y'+str(trav)]=str(int(p['DOB'].split('/')[2]))
        else:
            trav_details['t'+str(trav)]=p[f'TITLE_{trav-1}']
            trav_details['f'+str(trav)]=p[f'NAME_{trav-1}'].split(' ')[0]
            trav_details['s'+str(trav)]=p[f'NAME_{trav-1}'].split(' ')[1]
            trav_details['d'+str(trav)]=str(int(p[f'DOB_{trav-1}'].split('/')[0]))
            trav_details['m'+str(trav)]=str(int(p[f'DOB_{trav-1}'].split('/')[1]))
            trav_details['y'+str(trav)]=str(int(p[f'DOB_{trav-1}'].split('/')[2]))

    data=trav_details
    r=session.post(url, data=data)

    #Cruise Check

    url=f'https://www.allcleartravel.co.uk/ajax/cruisecheck2.php?i={qte_ref}'

    if p['CRUCHK']=='N':
        data={'wsid': qte_ref, 'cr': p['CRUCHK'], 'co': ''}
    else:
        if p['CRUTYPE']=='Y':
                data={'wsid': qte_ref, 'cr': p['CRUCHK'], 'co': 'O'}
        if p['CRUTYPE']=='N':
                data={'wsid': qte_ref, 'cr': p['CRUCHK'], 'co': 'R'}

    r=session.post(url, data=data)

    #Marketing Permissions

    url=f'https://www.allcleartravel.co.uk/ajax/marketing-perms.php?i={qte_ref}'

    data={'wsid': qte_ref, 'ne': 'N', 'np': 'Y', 'ns': '', 'nt': 'Y', 'scheme': 'OPT',
        't1': p['TITLE'], 'f1': p['NAME'].split(' ')[0], 's1': p['NAME'].split(' ')[1],
        'd1': str(int(p['DOB'].split('/')[0])), 'm1': str(int(p['DOB'].split('/')[1])),
        'y1': str(int(p['DOB'].split('/')[2])), 'e1': p['EMAIL']}

    r=session.post(url, data=data)
    return(session, AREQUOTE, SWBDEPV, dateto, dateannual, country_code, region_code)

def post_cust_details(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                      AREQUOTE, SWBDEPV, dateto, dateannual, country_code, region_code):

    from bs4 import BeautifulSoup

    #Create Variable 'cc' for inclusion of comma in 'ACOUNTRYMC'
    if p['ASTRIP']=='A':
        cc=''
        cntry=''
        country_code=''
    else:
        cc=country_code+','
        cntry=p['CNTRY']

    #Create Core Applicant Details as Dictionary
    data={'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref, '_BUTTON': 'OK',
          '_CALFLD': '&NULL',
          '_PROCESS': process_ref, '_FUNCTION': func_ref, '_OPROCESS': process_ref, '_OFUNCTION': func_ref,
          '_PARTITION': 'ALC', '_COLORFLD': '', '_LW3TRCID': '', '_EXCHALLBL': '', 'ASTDRENTRY': 'Z',
          'AWAWSID': qte_ref, 'AMSDWSID': '', 'AWLSCCD': 'OPT',
          'SAXAGE01': '0', 'SAXAGE02': '0', 'SAXAGE03': '0', 'SAXAGE04': '0', 'AWBTCTY': '', 'AW2NMDS': 'WWW',
          'AREGIONA': '', 'PREGION': '0', 'AAXCOVT': 'S', 'AADJUST': '', 'AOVER31': '', 'ABTNREGN': '',
          'ABTNTRAV': '', 'ASHOWDTE': '', 'SAXAGE05': '0', 'AWBSORC': '', 'AREQUOTE': '', 'SWBCYCD': '0',
          'PTOTRAV': '0', 'ACOUNTRYMC': cc, 'ACOUNTRYRN': '', 'ACNTRYSLCT': 'Y', 'ACNTRYHLD': '',
          'AALV7': 'Y', 'ASCHEME': '', 'ASHWRDT': '', 'AW2REDT': '', 'ASTEP': '1', 'AUNDER65': '',
          'LSECNO': sec_ref, 'ACLASS': 'NIK&VIK', 'ASTRIP': p['ASTRIP'],
          'SWBDEPV': SWBDEPV, 'dateto': dateto, 'CNTRY': cntry,
          'LOPT_CNTRY': country_code, 'ATRVTY': p['ATRVTY'], 'shbox': '',
          'dateannual': dateannual, 'CRUCHK': p['CRUCHK'], 'CRUTYPE': p['CRUTYPE'], 'travNumberHidden': p['MQ_TRAVNO'],
          'MQ_TRAVNO': ''}

    #Append Each Traveller's Details as Dictionary Keys
    for trav in range(1,int(p['MQ_TRAVNO'])+1):
        if trav==1:
            data['TITLE'+str(trav).zfill(2)]=p['TITLE']
            data['LFNAME'+str(trav).zfill(2)]=p['NAME'].split(' ')[0]
            data['LSNAME'+str(trav).zfill(2)]=p['NAME'].split(' ')[1]
            data['DOBD'+str(trav).zfill(2)]=str(int(p['DOB'].split('/')[0]))
            data['DOBM'+str(trav).zfill(2)]=str(int(p['DOB'].split('/')[1]))
            data['DOBY'+str(trav).zfill(2)]=str(int(p['DOB'].split('/')[2]))
        else:
            data['TITLE'+str(trav).zfill(2)]=p[f'TITLE_{trav-1}']
            data['LFNAME'+str(trav).zfill(2)]=p[f'NAME_{trav-1}'].split(' ')[0]
            data['LSNAME'+str(trav).zfill(2)]=p[f'NAME_{trav-1}'].split(' ')[1]
            data['DOBD'+str(trav).zfill(2)]=str(int(p[f'DOB_{trav-1}'].split('/')[0]))
            data['DOBM'+str(trav).zfill(2)]=str(int(p[f'DOB_{trav-1}'].split('/')[1]))
            data['DOBY'+str(trav).zfill(2)]=str(int(p[f'DOB_{trav-1}'].split('/')[2]))

    #Append Remaining Lead Applicant's Details as Dictionary Keys
    remainder={'AWDP1CD': p['POSTCODE'], 'WDAD01': p['HOUSE_NUM'],
                'streetwalker': p['ADD_LINE_1'], 'townwalker': p['TOWN'],
                'WDHTNO': p['MOBILE'], 'LWKEMAIL': p['EMAIL'], 'LNOEMAL': 'Y'}
    data.update(remainder)

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)
    soup=BeautifulSoup(r.content, "html.parser")
    form_ext=soup.find("form")

    from form_extractor import get_form_details
    form_det = get_form_details(form_ext)
    form_inpts = form_det['inputs']

    for input in form_inpts:
        if input['name'].strip() == '_PANEL':
            panel_ref = input['value'].strip()
        if input['name'].strip() == '_PROCESS':
            process_ref = input['value'].strip()
        if input['name'].strip() == '_FUNCTION':
            func_ref = input['value'].strip()

    return(session, action, panel_ref, process_ref, func_ref, region_code)

def post_med_warranty(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref, AREQUOTE, region_code):

    from bs4 import BeautifulSoup

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "Accept-Encoding": "gzip, deflate, br",
               "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               "Content-Length": "1104",
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
               "Host": "www.allcleartravel.co.uk",
               "Origin": "https://www.allcleartravel.co.uk",
               "Referer": "https://www.allcleartravel.co.uk/",
               "Sec-Ch-Ua": session.headers['sec-ch-ua'],
               "Sec-Ch-Ua-Mobile": "?0",
               "Sec-Ch-Ua-Platform": session.headers['Sec-Ch-Ua-Platform'],
               "Sec-Fetch-Dest": "document",
               "Sec-Fetch-Mode": "navigate",
               "Sec-Fetch-Site": "same-origin",
               "Sec-Fetch-User": "?1",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": session.headers['User-Agent']}

    data = {'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref, '_BUTTON': 'OK',
            '_CALFLD': '&NULL',
            '_PROCESS': process_ref, '_FUNCTION': func_ref, '_OPROCESS': process_ref, '_OFUNCTION': func_ref,
            '_PARTITION': 'ALC', '_COLORFLD': '', '_LW3TRCID': '', '_EXCHALLBL': '',
            'ASTDRENTRY': 'N', 'AWLSCCD': 'OPT', 'AW_SCCD': '', 'AWAWSID': qte_ref, 'AW_ISMED': '', 'AMSDWSID': '',
            'AMQ_COMTRA': '',
            'LWBQE01': 'N', 'LWBQE02': p['LWBQE02'], 'LWBQE03': 'N',  # Medical Conditions
            'ARESCHK': '', 'AADJUST': '', 'PTOTRAV': p['MQ_TRAVNO'], 'AWBCOCD': '', 'AW2NMDS': 'WWW',
            'AREGIONA': region_code, 'PREGION': '0', 'AREQUOTE': '', 'AWAITYN': '', 'ACHKTERM': '',
            'ACHKWAIT': '', 'ALT1Y01': '', 'ALT1Y02': '', 'ALT1Y03': '', 'ALT1Y04': '',
            'ALT1Y05': '', 'ALT1Y06': '', 'ALT1Y07': '', 'ALT1Y08': '', 'ALT1Y09': '',
            'ALT1Y10': '', 'AAXCOVT': p['ASTRIP'], 'AWBSORC': p['ATRVTY'], 'AALV7': 'Y', 'ACOUNTRYRN': '',
            'AMOPOST': 'Y', 'AMOTXFG': '', 'AMOTLFG': 'Y', 'AMOEMFG': 'N', 'SAXAGE01': str(p['AGE']),
            'LFNAME01': p['NAME'].split(' ')[0], 'LTITLE01': p['TITLE'], 'LSNAME01': p['NAME'].split(' ')[1],
            'AWDP1CD': p['POSTCODE'].split(' ')[0], 'AWDP2CD': p['POSTCODE'].split(' ')[1],
            'LWDWTNO': '', 'LWDHTNO': p['MOBILE'], 'LMOEMAL': p['EMAIL'], 'PDOBD': str(int(p['DOB'].split('/')[0])),
            'PDOBM': str(int(p['DOB'].split('/')[1])),
            'PDOBC': str(int(p['DOB'].split('/')[2]))[0:2], 'PDOBY': str(int(p['DOB'].split('/')[2]))[2:4],
            'ACLASS': 'NIK&VIK', 'LSECNO': sec_ref}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    session.headers.update(headers)
    r=session.post(url, data=data)

    from form_extractor import get_form_details
    soup=BeautifulSoup(r.content, "html.parser")
    form_ext=soup.find("form")

    from form_extractor import get_form_details
    form_det=get_form_details(form_ext)
    form_inpts=form_det['inputs']

    for input in form_inpts:
        if input['name'].strip() == '_PANEL':
            panel_ref = input['value'].strip()
        if input['name'].strip() == '_PROCESS':
            process_ref = input['value'].strip()
        if input['name'].strip() == '_FUNCTION':
            func_ref = input['value'].strip()

    action = form_det['action'].split('+')[1].upper()

    return(session, action, panel_ref, process_ref, func_ref, region_code)

def post_med_validation(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                        AREQUOTE, region_code):

    from bs4 import BeautifulSoup

    data={'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref,
          '_BUTTON': 'OK', '_CALFLD': '&NULL', '_PROCESS': process_ref, '_FUNCTION': func_ref,
          '_OPROCESS': process_ref,
          '_OFUNCTION': func_ref, '_PARTITION': 'ALC', '_COLORFLD': '', '_LW3TRCID': '', '_EXCHALLBL': '',
          'ASTDRENTRY': 'N', 'PMQ_COUNT': p['MQ_TRAVNO'], 'AMQ_COUNTC': p['MQ_TRAVNO'], 'LMQ_TITLE': '', 'PWMTRNO': p['MQ_TRAVNO'],
          'PTRVAGE': '0', 'LWMCDDS': '', 'AWAWSID': qte_ref, 'SV1MREF': '0', 'PWK_TRAVNO': p['MQ_TRAVNO'],
          'AWMWSID': qte_ref, 'SWMMCNO': '0', 'SWMLINK': '0', 'SWMLNKF': '0', 'AW_EDIT': '',
          'AWK_SHOW': '', 'ACOMPID': '', 'AUSERID': '', 'AMSDWSID': '', 'AWMSDWSID': '',
          'AWLSCCD': 'OPT', 'ABKGRND': 'Y', 'SWBBUCD': '', 'PWKQTNO': '0', 'AAXCOVT': p['ASTRIP'],
          'AW2NMDS': 'WWW', 'ANAME': p['NAME'], 'ANOWS': '', 'ADEPTDATEA': '', 'ARETDATEA': '',
          'ADEPTDAT1': p['TRIP_START'], 'ANOSHOW': '', 'PREGION': '0', 'AREGIONA': region_code, 'ABRDISP': 'Y',
          'ARETDAT1': p['TRIP_END'], 'AWBSORC': '', 'PTOTRAV': p['MQ_TRAVNO'], 'ANOADD': '', 'AOVER31': '',
          'AW_VIEW': '', 'PMAX_MCNO': '0', 'PTMAX_MCNO': '0', 'AON_BLANK': '', 'AM_CHKMED': '',
          'ACHKTERMYN': '', 'ATERMP': '', 'ASTEP': '2', 'APROCEEDYN': '', 'ACCRENEW': '', 'APPRENEW': '',
          'ARESCHK': '', 'AREQUOTE': '', 'ARESPFLG': '', 'LSECNO': sec_ref,
          'PDOBD': str(int(p['DOB'].split('/')[0])), 'ACLASS': 'NIK&VIK', 'AALV7': 'Y', 'ATOLDONCE': 'N',
          'PSTDROWNUM': '0'}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)

    soup=BeautifulSoup(r.content, "html.parser")
    form_ext=soup.find("form")

    from form_extractor import get_form_details
    form_det = get_form_details(form_ext)
    form_inpts = form_det['inputs']

    for input in form_inpts:
        if input['name'].strip() == '_PANEL':
            panel_ref = input['value'].strip()
        if input['name'].strip() == '_PROCESS':
            process_ref = input['value'].strip()
        if input['name'].strip() == '_FUNCTION':
            func_ref = input['value'].strip()

    action=form_det['action'].split('+')[1].upper()
    return(session, action, panel_ref, process_ref, func_ref)

def post_quote(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref, AREQUOTE, region_code):

    from bs4 import BeautifulSoup

    data={'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref,
          '_BUTTON': 'OK', '_CALFLD': '&NULL', '_PROCESS': process_ref, '_FUNCTION': func_ref,
          '_OPROCESS': process_ref,
          '_OFUNCTION': func_ref, '_PARTITION': 'ALC', '_COLORFLD': '', '_LW3TRCID': '', '_EXCHALLBL': '',
          'ASTDRENTRY': 'C', 'PMQ_COUNT': p['MQ_TRAVNO'], 'AMQ_COUNTC': p['MQ_TRAVNO'], 'LMQ_TITLE': '', 'PWMTRNO': p['MQ_TRAVNO'],
          'PTRVAGE': '0', 'LWMCDDS': '', 'AWAWSID': qte_ref, 'SV1MREF': '0', 'PWK_TRAVNO': p['MQ_TRAVNO'],
          'AWMWSID': qte_ref, 'SWMMCNO': '0', 'SWMLINK': '0', 'SWMLNKF': '0', 'AW_EDIT': '',
          'AWK_SHOW': '', 'ACOMPID': '', 'AUSERID': '', 'AMSDWSID': '', 'AWMSDWSID': '',
          'AWLSCCD': 'OPT', 'ABKGRND': 'Y', 'SWBBUCD': '', 'PWKQTNO': '0', 'AAXCOVT': p['ASTRIP'],
          'AW2NMDS': 'WWW', 'ANAME': p['NAME'].upper(), 'ANOWS': '', 'ADEPTDATEA': '', 'ARETDATEA': '',
          'ADEPTDAT1': p['TRIP_START'], 'ANOSHOW': '', 'PREGION': '0', 'AREGIONA': region_code, 'ABRDISP': 'Y',
          'ARETDAT1': p['TRIP_END'], 'AWBSORC': '', 'PTOTRAV': p['MQ_TRAVNO'], 'ANOADD': '', 'AOVER31': '',
          'AW_VIEW': '', 'PMAX_MCNO': '0', 'PTMAX_MCNO': '0', 'AON_BLANK': '', 'AM_CHKMED': '',
          'ACHKTERMYN': '', 'ATERMP': '', 'ASTEP': '2', 'APROCEEDYN': '', 'ARESCHK': '', 'AMEDICAL': 'Y',
          'AREQUOTE': '', 'ARESPFLG': 'N', 'ATOLDONCE': 'N', 'ACLASS': 'NIK&VIK', 'LSECNO': sec_ref,
          'AALV7': 'Y', 'ACCRENEW': '', 'APPRENEW': '', 'PSTDROWNUM': '0'}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)
    quotes=r.text

    session.close()

    return(quotes)