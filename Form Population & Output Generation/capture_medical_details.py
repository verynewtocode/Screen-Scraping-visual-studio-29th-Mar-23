def initiate_medical_search(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                            AREQUOTE, region_code):
    
    from bs4 import BeautifulSoup
    
    data={'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref,
          '_BUTTON': 'OK', '_CALFLD': '&NULL', '_PROCESS': process_ref, '_FUNCTION': 'ALV7003',
          '_OPROCESS': process_ref, '_OFUNCTION': func_ref, '_PARTITION': 'ALC', '_COLORFLD': '', 
          '_LW3TRCID': '', '_EXCHALLBL': '', 'ASTDRENTRY': 'N',
          'PMQ_COUNT': p['MQ_TRAVNO'], 'AMQ_COUNTC': p['MQ_TRAVNO'], 'LMQ_TITLE': '', 'PWMTRNO': p['MQ_TRAVNO'],
          'PTRVAGE': '0', 'LWMCDDS': '', 'AWAWSID': qte_ref, 'SV1MREF': '0', 'PWK_TRAVNO': p['MQ_TRAVNO'],
          'AWMWSID': qte_ref, 'SWMMCNO': '0', 'SWMLINK': '0', 'SWMLNKF': '0', 'AW_EDIT': '',
          'AWK_SHOW': '', 'ACOMPID': '', 'AUSERID': '', 'AMSDWSID': '', 'AWMSDWSID': '',
          'AWLSCCD': 'OPT', 'ABKGRND': 'Y', 'SWBBUCD': '', 'PWKQTNO': '0', 'AAXCOVT': p['ASTRIP'],        
          'AW2NMDS': 'WWW', 'ANAME': p['NAME'], 'ANOWS': '', 'ADEPTDATEA': '', 'ARETDATEA': '',
          'ADEPTDAT1': p['TRIP_START'], 'ANOSHOW': '', 'PREGION': '0', 'AREGIONA': region_code, 'ABRDISP': 'Y',
          'ARETDAT1': p['TRIP_END'], 'AWBSORC': '', 'PTOTRAV': p['MQ_TRAVNO'], 'ANOADD': '', 'AOVER31': '',
          'AW_VIEW': '', 'PMAX_MCNO': '0', 'PTMAX_MCNO': '0', 'AON_BLANK': '', 'AM_CHKMED': '',
          'ACHKTERMYN': '', 'ATERMP': '', 'ASTEP': '2', 'APROCEEDYN': '', 'ARESCHK': '',
          'AREQUOTE': '', 'ARESPFLG': '', 'ATOLDONCE': 'N', 'ACLASS': 'NIK&VIK', 'LSECNO': sec_ref,
          'PDOBD': str(int(p['DOB'].split('/')[0])), 'AALV7': 'Y', 'ACCRENEW': '', 'APPRENEW': '', 'PSTDROWNUM': '0'}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)
    
    #res = r.text
    #pos=res.find('WEBEVENT')
    #print('/n', res[pos - 1000:pos + 1000])

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

def medical_search_1(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                     AREQUOTE, region_code):
    
    from bs4 import BeautifulSoup

    if p['MED_CON']=='Gout':
        SV1MREF='91308'
        SV1MREF_1='91308'
        LMQ_ANS1=''
        PSTDROWNUM='1'        
    if p['MED_CON']=='Corneal Ulcer':
        SV1MREF='91262'
        SV1MREF_1='91262'
        LMQ_ANS1='2'
        PSTDROWNUM='1'             
    if p['MED_CON']=='Appendicitis':
        SV1MREF='91217'
        SV1MREF_1='92348'
        LMQ_ANS1='1'
        PSTDROWNUM='5'                    #For Medical Questions Form
    if p['MED_CON']=='Haemangioma':
        SV1MREF='91312'
        SV1MREF_1='91312'
        LMQ_ANS1='1'
        PSTDROWNUM='1'            
    if p['MED_CON']=='Whooping Cough':
        SV1MREF='92058'
        SV1MREF_1='92058'
        LMQ_ANS1='2'
        PSTDROWNUM='1'                  

    data={'_NAME': 'AUV1CDDS', '_ROW': '3', '_COLUMN': '2', '_SELECT': '00', '_PANEL': panel_ref,
          '_BUTTON': 'OK', '_CALFLD': 'AUV1CDDS', '_PROCESS': process_ref, '_FUNCTION': func_ref,
          '_OPROCESS': process_ref, '_OFUNCTION': func_ref, '_PARTITION': 'ALC', '_COLORFLD': '', 
          '_LW3TRCID': '', '_EXCHALLBL': '', 
          'AUV1CDDS': p['MED_CON'].lower(), 'ASTDRENTRY': 'N', 'PSTDROWNUM': '0', 'AWAWSID': qte_ref,
          'SV1MREF': '0', 'PWMTRNO': p['MQ_TRAVNO'], 'PWK_TRAVNO': p['MQ_TRAVNO'],
          'SWMLNKF': '0', 'SWMLINK': '0', 'ACOMPID': '', 'AUSERID': '', 'AW_BROKER': '',
          'AMSDWSID': '', 'AWMSDWSID': '', 'AWLSCCD': 'OPT',
          'PTOTRAV': p['MQ_TRAVNO'], 'SQ1MREF': '0', 'AW2NMDS': 'WWW', 'ADEPTDATEA': '', 'ARETDATEA': '',
          'ADEPTDAT1': p['TRIP_START'], 'ARETDAT1': p['TRIP_END'], 'ATXDSP': '',
          'PREGION': '0', 'AREGIONA': region_code, 'ABKGRND': 'Y', 'ANOWS': '',
          'SWBBUCD': '', 'AAXCOVT': p['ASTRIP'], 'PWKQTNO': '0', 'AOVER31': '',
          'ANAME': p['NAME'], 'APPRENEW': '', 'ACCRENEW': '', 'AREQUOTE': '', 'ACOUNTRYRN': '',
          'ARESCHK': '','LSECNO': sec_ref, 'ACLASS': 'NIK&VIK', 'AFOCUS': '', 'AALV7': 'Y',
          'AM_BCCHK1': '', 'ASTEP': '3'}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)
    res = r.text

    #pos = res.find('WEBEVENT')
    #print('/n', res[pos - 1000:pos + 1000])

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
    return(session, action, panel_ref, process_ref, func_ref,
           SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM)

def medical_questions(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                      AREQUOTE, region_code, SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM):
    
    from bs4 import BeautifulSoup
    
    data={'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref,
          '_BUTTON': 'OK', '_CALFLD': '&NULL', '_PROCESS': process_ref, '_FUNCTION': func_ref,
          '_OPROCESS': process_ref, '_OFUNCTION': func_ref, '_PARTITION': 'ALC', '_COLORFLD': '', 
          '_LW3TRCID': '', '_EXCHALLBL': '', 
          'AUV1CDDS': p['MED_CON'], 'ASTDRENTRY': 'S', 'PSTDROWNUM': PSTDROWNUM, 'AWAWSID': qte_ref,
          'SV1MREF': SV1MREF_1, 'PWMTRNO': p['MQ_TRAVNO'], 'PWK_TRAVNO': p['MQ_TRAVNO'],
          'SWMLNKF': '0', 'SWMLINK': '0', 'ACOMPID': '', 'AUSERID': '', 'AW_BROKER': '',
          'AMSDWSID': '', 'AWMSDWSID': '', 'AWLSCCD': 'OPT', 'PTOTRAV': p['MQ_TRAVNO'], 'SQ1MREF': '0',
          'AW2NMDS': 'WWW', 'ADEPTDATEA': '', 'ARETDATEA': '',          
          'ADEPTDAT1': p['TRIP_START'], 'ARETDAT1': p['TRIP_END'], 'ATXDSP': 'Y',
          'PREGION': '0', 'AREGIONA': region_code, 'ABKGRND': 'Y', 'ANOWS': '',
          'SWBBUCD': '', 'AAXCOVT': p['ASTRIP'], 'PWKQTNO': '0', 'AOVER31': '',
          'ANAME': p['NAME'], 'APPRENEW': '', 'ACCRENEW': '', 'AREQUOTE': '', 'ACOUNTRYRN': '',
          'ARESCHK': '','LSECNO': sec_ref, 'ACLASS': 'NIK&VIK', 'AFOCUS': 'Y', 'AALV7': 'Y',
          'AM_BCCHK1': '', 'ASTEP': '3'}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)
    
    #res = r.text
    #pos = res.find('WEBEVENT')
    #print('/n', res[pos - 1000:pos + 1000])

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

def medical_collection(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
                      AREQUOTE, region_code, SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM):
    
    from bs4 import BeautifulSoup
    
    data={'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref,
          '_BUTTON': 'OK', '_CALFLD': '&NULL', '_PROCESS': process_ref, '_FUNCTION': func_ref, '_OPROCESS': process_ref,
          '_OFUNCTION': func_ref, '_PARTITION': 'ALC', '_COLORFLD': '', '_LW3TRCID': '', '_EXCHALLBL': '',
          '_BLNAME': 'AV6_QLT', 'LMQ_ANS1': LMQ_ANS1, '_BLEND': 'AV6_QLT', 'SSAVSTEMNO': '',
          'SV1MREF': SV1MREF, 'SV1CODE': SV1MREF, 'AWAWSID': qte_ref, 'PWMTRNO': p['MQ_TRAVNO'], 'ASTDRENTRY': 'N',
          'AMQ_RETA1': LMQ_ANS1, 'AMQ_RETA2': '', 'AMQ_RETA3': '', 'AMQ_RETA4': '', 'AMQ_RETA5': '',
          'AMQ_RETA6': '', 'AMQ_RETA7': '', 'AMQ_RETA8': '', 'AMQ_RETA9': '', 'AMQ_RETA10': '',
          'AMQ_RETA11': '', 'AMQ_RETA12': '', 'AMQ_RETA13': '', 'AMQ_RETA14': '', 'AMQ_RETA15': '',
          'AMQ_RETA16': '', 'AMQ_RETA17': '', 'AMQ_RETA18': '', 'AMQ_RETA19': '', 'AMQ_RETA20': '',
          'AMQ_RETA21': '', 'AMQ_RETA22': '', 'AMQ_RETA23': '', 'AMQ_RETA24': '', 'AMQ_RETA25': '',
          'AMQ_RETA26': '', 'AMQ_RETA27': '', 'AMQ_RETA28': '', 'AMQ_RETA29': '', 'AMQ_RETA30': '', 
          'AMQ_RETA31': '', 'AMQ_RETA32': '', 'AMQ_RETA33': '', 'AMQ_RETA34': '', 'AMQ_RETA35': '',
          'AMQ_RETA36': '', 'AMQ_RETA37': '', 'AMQ_RETA38': '', 'AMQ_RETA39': '', 'AMQ_RETA40': '',
          'AMQ_RETA41': '', 'AMQ_RETA42': '', 'AMQ_RETA43': '', 'AMQ_RETA44': '', 'AMQ_RETA45': '',
          'AMQ_RETA46': '',  'AREQUOTE': '', 'SWMMREF': '0', 'PWK_TRAVNO': p['MQ_TRAVNO'], 'SWMMCNO': '0',
          'SWMLINK': '0', 'SWMLNKF': '1', 'SW_WMLINK': '0', 'SW_LINK': SV1MREF, 'AW_EDIT': '',
          'AUSERID': '', 'AMSDWSID': '', 'AWMSDWSID': '', 'ARESCHK': '', 'AWLSCCD': 'OPT', 
          'AW2NMDS': 'WWW', 'PQUESTTOT': '1', 'SWBBUCD': '', 'ADEPTDAT1': p['TRIP_START'], 'ARETDAT1': p['TRIP_END'],
          'ADEPTDATEA': '', 'ARETDATEA': '', 'AOVER31': '', 'PTOTRAV': p['MQ_TRAVNO'],
          'LNAME': p['NAME'], 'PREGION': '0', 'ANOWS': '', 'PWKQTNO': '0', 'AAXCOVT': p['ASTRIP'], 
          'ACOUNTRYRN': '', 'ATOTQ': 'Y',  'ASTEP': '4', 'LV1CDDS': p['MED_CON'], 'AALV7': 'Y',
          'AREGIONA': region_code, 'SSAVEREF': '0', 'SSAVMCNO': '1', 'ACLASS': 'NIK&VIK', 'LSECNO': sec_ref}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)

    #res = r.text
    #pos = res.find('WEBEVENT')
    #print('/n', res[pos - 1000:pos + 1000])

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

def post_quote(session, p, qte_ref, action, sec_ref, panel_ref, process_ref, func_ref,
               AREQUOTE, region_code, SV1MREF, SV1MREF_1, LMQ_ANS1, PSTDROWNUM):
    
    data={'_NAME': '&NULL', '_ROW': '01', '_COLUMN': '01', '_SELECT': '00', '_PANEL': panel_ref,
          '_BUTTON': 'OK', '_CALFLD': '&NULL', '_PROCESS': process_ref, '_FUNCTION': func_ref,
          '_OPROCESS': process_ref,
          '_OFUNCTION': func_ref, '_PARTITION': 'ALC', '_COLORFLD': '', '_LW3TRCID': '', '_EXCHALLBL': '',
          'ASTDRENTRY': 'N', 'PMQ_COUNT': p['MQ_TRAVNO'], 'AMQ_COUNTC': p['MQ_TRAVNO'], 'LMQ_TITLE': '', 'PWMTRNO': p['MQ_TRAVNO'],
          'PTRVAGE': '0', 'LWMCDDS': p['MED_CON'], 'AWAWSID': qte_ref, 'SV1MREF': SV1MREF, 'PWK_TRAVNO': p['MQ_TRAVNO'],
          'AWMWSID': qte_ref, 'SWMMCNO': '1', 'SWMLINK': '0', 'SWMLNKF': '1', 'AW_EDIT': '',
          'AWK_SHOW': 'Y', 'ACOMPID': '', 'AUSERID': '', 'AMSDWSID': '', 'AWMSDWSID': '',
          'AWLSCCD': 'OPT', 'ABKGRND': 'Y', 'SWBBUCD': '', 'PWKQTNO': '0', 'AAXCOVT': p['ASTRIP'],
          'AW2NMDS': 'WWW', 'ANAME': p['NAME'], 'ANOWS': '', 'ADEPTDATEA': '', 'ARETDATEA': '',
          'ADEPTDAT1': p['TRIP_START'], 'ANOSHOW': '', 'PREGION': '0', 'AREGIONA': region_code, 'ABRDISP': 'Y',
          'ARETDAT1': p['TRIP_END'], 'AWBSORC': '', 'PTOTRAV': p['MQ_TRAVNO'], 'ANOADD': '', 'AOVER31': '',
          'AW_VIEW': '', 'PMAX_MCNO': '0', 'PTMAX_MCNO': '0', 'AON_BLANK': '', 'AM_CHKMED': '',
          'ACHKTERMYN': '', 'ATERMP': '', 'ASTEP': '2', 'APROCEEDYN': '', 'ARESCHK': '',
          'AREQUOTE': '', 'ARESPFLG': 'N', 'ATOLDONCE': 'N', 'ACLASS': 'NIK&VIK', 'LSECNO': sec_ref,
          'PDOBD': str(int(p['DOB'].split('/')[0])), 'AALV7': 'Y', 'ACCRENEW': '', 'APPRENEW': '', 'PSTDROWNUM': '0'}

    url = f'https://www.allcleartravel.co.uk/CGI-BIN/LANSAWEB?WEBEVENT+{action}+ALC+ENG'

    r=session.post(url, data=data)
    quotes=r.text

    #pos=quotes.find('lowestPrice')
    #print('\n',quotes[pos-500:pos+500])

    session.close()

    return(quotes)




