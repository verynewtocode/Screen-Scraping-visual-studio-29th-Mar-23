def proxy_selection():
    from random import choice, randint
    from locate import this_dir
    import os

    #Change path to retrieve functions
    my_dir=str(this_dir())
    if my_dir.split('\\')[-1] !='venv':
        filepath = os.path.realpath(f'{my_dir}/venv')
        os.chdir(filepath)
    
    #Import Proxies
    f=open(f'{my_dir}\Proxies\webshare IO Trial Proxy list.txt', 'r')
    content = f.read()
    f.close()

    string=content.replace('\n', ' ')
    a=string.find("'")
    up=string[0:a].split(' ')
    username=up[0]
    password=up[1]

    prox_list=list(string[a:].replace("'","").split(', '))
    return(username, password, prox_list)

def header_selection():
    from random import choice, randint

    header_list = ['windows_edge', 'android_chrome']
    chrome_version=randint(109, 110)
    chrome_version

    selection=choice(header_list)
    selection

    if selection == 'windows_edge':
        sec_ch_ua = f'"Chromium";v="{chrome_version}", "Not A(Brand";v="24", "Microsoft Edge";v="110"'
        sec_ch_ua_platform = 'Windows'
        user_agent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36 Edg/110.0.1587.50'

    elif selection == 'android_chrome':
        sec_ch_ua = f'"Not_A Brand";v="99", "Google Chrome";v "Chromium";v="{chrome_version}"'
        sec_ch_ua_platform = 'Chrome OS'
        user_agent = f'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36'

    # Header Parameters
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
               'Connection': 'keep-alive',
               # 'Content-Length': '1224',
               'Content-Type': 'application/x-www-form-urlencoded',
               # 'Cookie': 'AWSALBCORS=YxMtKIzkiJ2E4lRYxeDjeOfROe9BLtAsSYXmtfHoHNwJ5F1CfoaWOYnZK6foTrg3FAYkKx+skL6y73ebudw5EeusZWvWZAjCrY9s42zAGxOuM+Mc/wKTn6yM7OXY',
               # 'Host': 'report.allclear.gbqofs.io',
               'Origin': 'https://www.allcleartravel.co.uk',
               'Referer': 'https://www.allcleartravel.co.uk/',
               'sec-ch-ua': f"{sec_ch_ua}",
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': f"{sec_ch_ua_platform}",
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'cross-site',
               'User-Agent': f'{user_agent}'}
    return(headers)