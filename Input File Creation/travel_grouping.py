#Individual

def individual(df):
    from random import randint
    from form_functions import name_generator, dob_from_age, email_generator, mobile_generator

    title_list=[]
    name_list=[]
    dob_list=[]
    email_list=[]
    mob_list=[]

    for k in range(0,len(df)):
        randnum=randint(0,100)
        if randnum>=50:
            gender='male'
            title='Mr'
        elif 50>randnum>=1:
            gender='female'
            if randint(0, 100) > 20:
                title='Mrs'
            else:
                title='Miss'
        elif randnum<1:
            title='Dr'
            if randint(0,100)>52:
                gender='female'
            else:
                gender='male'
        name=name_generator(gender)[0]
        name_list.append(name)
        title_list.append(title)
        dob_list.append(dob_from_age(df['AGE'][k]))
        email_list.append(email_generator(name))
        mob_list.append(mobile_generator())

    return(title_list, name_list, dob_list, email_list, mob_list)

#Couple

def couple(df):
    from random import randint
    from form_functions import name_generator, dob_from_age, email_generator
    import pandas as pd

    title_list_c=[]
    name_list_c=[]
    age_list_c=[]
    dob_list_c=[]

    for k in range(0,len(df)):
        randnum=randint(0,100)
        if df['ATRVTY'][k]=='C':
            if randnum>3:
                if df['TITLE'][k]==('Mr'):
                    gender='female'
                    if randint(0, 100)>20:
                        title='Mrs'
                    else:
                        title='Miss'
                if df['TITLE'][k] in ('Mrs', 'Miss'):
                    gender='male'
                    title='Mr'
            else:
                if df['TITLE'][k] in ('Mrs', 'Miss'):
                    gender='female'
                    if randint(0, 100)>20:
                        title='Mrs'
                    else:
                        title='Miss'
                if df['TITLE'][k]==('Mr'):
                    gender='male'
                    title='Mr'
            title_list_c.append(title)
            #Same Surnamed Couple
            if df['TITLE'][k]!='Miss' and pd.to_numeric(df['AGE'][k])>30 and randint(0,100)>40:
                    name_list_c.append(name_generator(gender)[0].split(' ')[0]+' '+df['NAME'][k].split(' ')[1])
            else:
                name_list_c.append(name_generator(gender)[0])

            orig_age=pd.to_numeric(df['AGE'][k])
            new_age=randint(orig_age-5,orig_age+5)
            age_list_c.append(str(new_age))
            dob_list_c.append(dob_from_age(str(new_age)))
        else:
            title_list_c.append('')
            name_list_c.append('')
            age_list_c.append('')
            dob_list_c.append('')

    return(title_list_c, name_list_c, age_list_c, dob_list_c)

#Family

def family(df):
    from random import randint
    from form_functions import name_generator, dob_from_age, email_generator

    #Define number of family members
    fam_list=[]
    for k in range(0,len(df)):
        if df['ATRVTY'][k]=='F':
            randnum=randint(0,100)
            if 10>randnum>=0:
                fam_num=2
            if 30>randnum>=10:
                fam_num=3
            if 60>randnum>=30:
                fam_num=4
            if 90>randnum>=60:
                fam_num=5
            if 95>randnum>=90:
                fam_num=6
            if randnum>=95:
                fam_num=7
            fam_list.append(fam_num)
        else:
            fam_list.append(0)

    title_list_f=[]
    name_list_f=[]
    age_list_f=[]
    dob_list_f=[]

    for k in range(0,len(df)):
        if df['ATRVTY'][k]=='F':

            title_list_temp=[]
            name_list_temp=[]
            age_list_temp=[]
            dob_list_temp=[]

            for l in range(2,fam_list[k]+1):
                if fam_list[k]==2:              #1 Adult 1 Child
                    randnum=randint(0,100)
                    age=randint(1,17)
                    if randnum>=50:
                        gender='male'
                        title='Mr'
                    else:
                        gender='female'
                        title='Miss'
                    title_list_temp.append(title)
                    name=name_generator(gender)[0].split(' ')[0]+' '+df['NAME'][k].split(' ')[1]

                else:                           #2 Adults Remainder Children
                    if l==2:                    #Create 2nd Adult
                        randnum=randint(0,100)
                        age=randint(int(df['AGE'][k])-5,int(df['AGE'][k])+5)
                        if df['TITLE'][k]=='Mr':
                            gender='female'
                            if age>24 and randnum<1:
                                title='Dr'
                            elif age>24 and randint(0, 100)>30:
                                title='Mrs'
                            else:
                                title='Miss'
                        else:
                            gender='male'
                            if age>24 and randnum<1:
                                title='Dr'
                            else:
                                title='Mr'
                                
                        title_list_temp.append(title)
                        if title=='Miss' or randnum<20:
                            name=name_generator(gender)[0]
                        else:
                            name=name_generator(gender)[0].split(' ')[0]+' '+df['NAME'][k].split(' ')[1]
                    elif l>2:                    #Create Children
                        randnum=randint(0,100)
                        age=randint(1,17)
                        if randnum>=50:
                            gender='male'
                            title='Mr'
                        else:
                            gender='female'
                            title='Miss'
                        title_list_temp.append(title)
                        name=name_generator(gender)[0].split(' ')[0]+' '+df['NAME'][k].split(' ')[1]

                name_list_temp.append(name)
                age_list_temp.append(age)
                dob_list_temp.append(dob_from_age(age))

            title_list_f.append(title_list_temp)
            name_list_f.append(name_list_temp)
            age_list_f.append(age_list_temp)
            dob_list_f.append(dob_list_temp)
        else:
            title_list_f.append('')
            name_list_f.append('')
            age_list_f.append('')
            dob_list_f.append('')
    return(title_list_f, name_list_f, age_list_f, dob_list_f)

#Group
def group(df):
    from random import randint
    from form_functions import name_generator, dob_from_age, email_generator

    group_list=[]
    for k in range(0,len(df)):
        if df['ATRVTY'][k]=='G':
            randnum=randint(0,100)
            if 20>randnum>=0:
                group_num=2
            if 38>randnum>=20:
                group_num=3
            if 54>randnum>=38:
                group_num=4
            if 68>randnum>=54:
                group_num=5
            if 80>randnum>=68:
                group_num=6
            if 88>randnum>=80:
                group_num=7
            if 94>randnum>=88:
                group_num=8
            if 98>randnum>=94:
                group_num=9
            if randnum>=98:
                group_num=10
            group_list.append(group_num)
        else:
            group_list.append(0)

    #Summarise by Group Number
    #summ={}
    #for item in group_list:
    #    summ[item]=summ.get(item, 0) + 1
    #dict(sorted(summ.items()))

    title_list_g=[]
    name_list_g=[]
    age_list_g=[]
    dob_list_g=[]

    for k in range(0,len(df)):
        if df['ATRVTY'][k]=='G':

            title_list_temp=[]
            name_list_temp=[]
            age_list_temp=[]
            dob_list_temp=[]

            for l in range(2,group_list[k]+1):
                randnum=randint(0,100)
                age=randint(1,100)
                if randnum>=50:
                    gender='male'
                    title='Mr'
                elif 50>randnum>=1:
                    gender='female'
                    if age>24 and randint(0, 100)>30:
                        title='Mrs'
                    else:
                        title='Miss'
                elif age>24 and randnum<1:
                    title='Dr'
                    if randint(0,100)>52:
                        gender='female'
                    else:
                        gender='male'
                title_list_temp.append(title)
                if age<18: #Child shares parents surname
                    name=name_generator(gender)[0].split(' ')[0]+' '+df['NAME'][k].split(' ')[1]
                else:
                    name=name_generator(gender)[0]
                name_list_temp.append(name)
                age_list_temp.append(age)
                dob_list_temp.append(dob_from_age(age))

            title_list_g.append(title_list_temp)
            name_list_g.append(name_list_temp)
            age_list_g.append(age_list_temp)
            dob_list_g.append(dob_list_temp)   
        else:
            title_list_g.append('')
            name_list_g.append('')
            age_list_g.append('')
            dob_list_g.append('')
    return(title_list_g, name_list_g, age_list_g, dob_list_g)