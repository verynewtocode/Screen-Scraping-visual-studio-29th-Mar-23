def trip_type_generator():
    from random import choice
    tt_list = ['single', 'multi']
    return (choice(tt_list))

def cruise_generator():
    from random import choice
    cruise_list = ['y', 'n']
    return (choice(cruise_list))

def name_generator(gender):
    import names
    name = names.get_full_name(gender=gender)
    return (name,gender)

def dob_from_age(age):
    import pandas as pd
    import datetime as dt
    from random import randint
    age_num=pd.to_numeric(age)
    temp=dt.datetime.now()-dt.timedelta(days=(365.25*age_num)+randint(0,360))
    dob=temp.strftime("%d/%m/%Y")
    return(dob)

def email_generator(name):
    from random import randint, choice

    separator = ['.', '', '_']
    email_list = ['hotmail', 'gmail', 'outlook', 'googlemail', 'icloud', 'samsung']
    e_loc_list = ['.com', '.co.uk', '.ie', '.org', '.net']
    
    if randint(0,100)>50:
        ename=(name.split(' ')[0]+choice(separator)+name.split(' ')[1]).replace(' ', '').lower()
    else:
        ename=(name.split(' ')[0][0]+choice(separator)+name.split(' ')[1]).replace(' ', '').lower()

    if randint(0,100)>50:
        pad=''
    else:
        pad=str(randint(0,100))

    email=ename+pad+'@'+choice(email_list)+choice(e_loc_list)
    return (email)

def trip_date_generator(trip_type):
    from random import randint
    import datetime as dt

    today = dt.date.today()
    #Create days in the future the trip begins
    if trip_type=='A':
        days_futr=randint(7, 59)
        trip_len=365
    else:                           #Single Trips
        df_rand=randint(1,100)
        if df_rand<20:
            days_futr=0
        elif 28>df_rand>=20:
            days_futr=randint(1, 5)
        elif 33>df_rand>=28:
            days_futr=randint(6, 10)
        elif 38>df_rand>=33:
            days_futr=randint(11, 17)
        elif 44>df_rand>=38:
            days_futr=randint(18, 24)
        elif 50>df_rand>=44:
            days_futr=randint(25, 31)
        elif 56>df_rand>=50:
            days_futr=randint(32, 45)
        elif 74>df_rand>=56:
            days_futr=randint(46, 92)
        else: 
            days_futr=randint(93, 359)

        trip_len=1                   #Arbitrary Trip Length
        #Create Single Trip Lengths - Use DURATION Instead
        #tl_rand=randint(1,100)
        #if tl_rand<14:
        #    trip_len=randint(2, 5)
        #elif 55>tl_rand>=14:
        #    trip_len=randint(6, 10)
        #    trip_len
        #elif 85>tl_rand>=55:
        #    trip_len=randint(11, 17)
        #else: 
        #    trip_len=randint(18, 359)

    trip_com=today+dt.timedelta(days=days_futr)
    trip_end=trip_com+dt.timedelta(days=trip_len)

    return (trip_com, trip_end)

def destination_generator_multi():
    from random import choice

    dest_list = ['uk', 'eur', 'ww_excl', 'ww_incl']
    return (choice(dest_list))

def destination_generator_single():
    from random import choice

    dest_list = ['spain', 'france', 'italy', 'greece', 'other']
    return (choice(dest_list))

def postcode_picker():
    from random import choice
    f=open('Postcodes.txt', 'r')
    pc_list=f.read().split('\n')
    f.close()
    return(choice(pc_list))

def address_generator(df):
    from random import choice
    f=open(f'Postcodes\PAF.csv', 'r')
    add_list=f.read().split('\n')
    f.close()

    pc_list=[]
    town_list=[]
    add_line_1_list=[]
    house_num_list=[]

    for k in range(0,len(df)):
        add=list(choice(add_list[1:]).split(','))
        pc_list.append(add[0])
        town_list.append(add[1])
        add_line_1_list.append(add[2])
        house_num_list.append(add[3])
    return(pc_list, town_list, add_line_1_list, house_num_list)

def mobile_generator():
    from random import randint, choice
    mob='07'+choice(['1','3','4','5','7','8','9'])
    for k in range(0,8):
        mob=mob+(str(randint(1,9)))
    return(mob)
