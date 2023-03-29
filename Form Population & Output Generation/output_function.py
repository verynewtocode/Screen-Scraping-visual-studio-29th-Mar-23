def output_collation(quotes, p, m_loop, input_ref):

    import pandas as pd
    import re

    ########################
    # Providers & Premiums #
    ########################

    #Partition the Annual Trip Premiums

    quote_start=quotes.find("var fcabuttonClass = '.fca_btn_info' + i;")
    quote_end=quotes.find("badges = '';")
    ap_ext=quotes[quote_start:quote_end]

    #Retrieve Provider References for each Quote
    indx_list=[]
    ord_list=[]
    prm_list=[]
    pra_list=[]

    ord_start=list(m.start() for m in re.finditer('var ord =', ap_ext))
    prm_start=list(m.start() for m in re.finditer('var prm =', ap_ext))
    pra_start=list(m.start() for m in re.finditer('var pra =', ap_ext))

    for indx in ord_start:
        indx_list.append(ap_ext[indx-13:indx+12].split(')')[0].split('== ')[1].strip())
    for ord in ord_start:
        ord_list.append(ap_ext[ord:ord+25].split('}')[0].split('=')[1].strip('; '))
    for prm in prm_start:
        prm_list.append(ap_ext[prm:prm+25].split('}')[0].split('=')[1].strip('; '))
    for pra in pra_start:    
        pra_list.append(ap_ext[pra:pra+25].split('}')[0].split('=')[1].strip('; '))        

    #Re-order to place 264 & 274 at top of table

    for k in range(0,len(indx_list)):
        if indx_list[k]=='98':
            indx_list[k]=1
        elif indx_list[k]=='99':
            indx_list[k]=2
        else:
            indx_list[k]=int(indx_list[k])+2

    #Combine all lists & sort by index
    combined=list(zip(indx_list,ord_list,prm_list,pra_list))

    combined.sort(key=lambda x: x[0])

    #Remove Premiums without an Assignment (Provider equals zero)
    rem=[i for i in combined if i[1]=='0']
    for remove in rem:
        combined.remove(remove)

    df_prm_pra=pd.DataFrame(combined, columns=['Index','ProvCode','Single Trip Premium','Annual Premium'])

    #Excess and Cover Amount Retrieval

    #Retrieve Text containing Quote Detail
    add_start=quotes.find('AC 15 Month Ext products')
    add_end=quotes.find("console.log('t = ' + t);")
    char_removal=['\n', '"']
    add_ext=quotes[add_start:add_end].replace('&pound', '£')
    for char in char_removal:
        add_ext=add_ext.replace(char, '')

    #Retrieve Provider References for each Quote
    ord_list=[]
    ord_start=list(m.start() for m in re.finditer('ord ==', add_ext))
    for ord in ord_start:
        ord_list.append('ProvCode:'+add_ext[ord:ord+25].split(')')[0].split('==')[1])

    #Retrieve Cruise Cover Flag for each Quote
    ord_start.append(ord_start[len(ord_start)-1]+4000)          #Add EOF to incorporate last Policy
    crucov_list=[]
    crucov_start=list(m.start() for m in re.finditer('Cruise Cover Included', add_ext))
    for ord in range(1,len(ord_start)):
        flag=0
        for crucov in crucov_start:
            if ord_start[ord]>crucov>ord_start[ord-1]:
                crucov_list.append('Y')
                flag=1
        if flag==0:
            crucov_list.append('N')
    ord_start.pop()                                             #Remove EOF Reference

    df_crucov=pd.DataFrame(crucov_list, columns=['CruCov'])

    #Retrieve Excesses set by each Provider
    raw_ex_list=list(m.start() for m in re.finditer('prodLogo', add_ext))

    #Remove multiple instances of Product Logo in element text
    rmv_list=[]
    for k in range(0,len(raw_ex_list)-1):
        a=raw_ex_list[k+1]
        b=raw_ex_list[k]
        if a-b<250:
            rmv_list.append(k)

    for remove in rmv_list:
        del raw_ex_list[remove]

    master_list=[]
    excess_list_st=[]

    for k in range(0,len(ord_list)):
        excess_list_st.append(ord_list[k])
        if k<len(raw_ex_list)-1:
            provider=add_ext[raw_ex_list[k]:raw_ex_list[k+1]].split('>')[0].split('=')[3]
            if provider.split(' ')[-1].lower()=='class':
                provider=provider.rsplit(' ', 1)[0]
            excess_list_st.append('Provider: '+provider)
        ex=add_ext[raw_ex_list[k]:raw_ex_list[k]+1000].split('//')[0].split(';')
        for j in range(3,len(ex)):
            if len(ex[j])>0:
                if ex[j][-1]=='£':
                    excess_list_st.append(ex[j].split('=')[0].strip()+':'+ex[j+1].replace("'", ""))
                elif '=' in ex[j]:
                    excess_list_st.append(ex[j].split('=')[0].strip()+':'+ex[j].split('=')[1])

        #List comprehension to Remove Unnecessary Elements

        excess_list_st1=[x for x in excess_list_st if not 'SingleArt' in x and 
                                                    not 'EmergAss' in x and 
                                                    not 'i class' in x]
        #Final Removal of Unwanted Text
        excess_list=[]
        for excess in excess_list_st1:
            excess_list.append(excess.replace("'(Excess up to ","")
                                    .replace("'(Excess Up to ","")
                                    .replace("'(Excess ","")
                                    .replace("'","")
                                    .replace("£","")
                                    .strip(")'*"))

        dct={excess.split(':')[0]: excess.split(':')[1].strip() for excess in excess_list}
        master_list.append(dct)

    df_excess=pd.DataFrame(master_list,columns=(master_list[0].keys()))

    #Reformat Cancellation Excluded Column
    df_excess.loc[df_excess['CanxEx']=='', ['CanxVal','CanxEx']] = 'Cancellation Excluded'

    #Append Cruise Cover by Provider
    df_excess=df_excess.join(df_crucov)
    #df_excess.to_csv('AllClear Excess Table.csv',mode='w+',index=False)

    #Outputs the Quote Page HTML for testing purposes
    func=open(f'price_output_{m_loop}.html','w', encoding="utf-8")
    func.write(quotes)
    func.close()

    joined=pd.merge(df_prm_pra, df_excess, how='left', on="ProvCode")

    #Exclude the Quotes from Providers not offering Cruise Cover if Cruise Cover is required
    if p['CRUCHK']=='Y':
        joined=joined.loc[joined['CruCov']=='Y']

    #Move Annual Trip Premiums to correct column

    if p['ASTRIP']=='A':
        joined.loc[:, 'Annual Premium']=joined.loc[:, 'Single Trip Premium']
        joined.loc[:, 'Single Trip Premium']=0

    df_temp=joined[['ProvCode', 'Provider', 'Single Trip Premium', 'Annual Premium',
                    'MedVal', 'MedEx', 'BagVal', 'BagEx', 'CanxVal', 'CanxEx']]

    df_temp.insert(0, 'File_Ref', input_ref+'_'+str(p['ORIG_ORDER']))

    #Remove Multiple Quotes from Providers using ProvCode

    df_temp=df_temp.drop_duplicates(subset='ProvCode', keep='first')

    return(df_temp)