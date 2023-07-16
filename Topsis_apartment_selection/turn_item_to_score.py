import re

def alter_house_type(x):
    '''按照house_type對各屋型進行評分'''
    if x == '別墅' or x == '透天厝':
        return 3
    elif x =='電梯大樓' or x == '住宅大樓':
        return 2
    else:
        return 1

def alter_rent_type(x):
    '''按照rent_type對各房型進行評分'''
    if x =='獨立套房':
        return 3
    elif x =='分租套房':
        return 2
    elif x == '雅房':
        return 1
    else:
        return 4

def alter_role_type(x):
    '''按照role對各身分進行評分'''
    if x == '屋主':
        return 3
    elif x =='代理人':
        return 2
    else:
        return 1
#以下尚未處理完
def alter_post_time(x):
    pattern = '\d+'
    result =np.nan
    if '分' in x:
        result = re.findall(pattern,x)
    elif '小時' in x:
        result = re.findall(pattern,x)
    elif '天' in x:
        result = re.findall(pattern,x)
    elif '月' in x:
        result = re.findall(pattern,x)
    if result != np.nan:
        result = [int(i) for i in result]
    return result

def alter_update_time(x):
    pass

def alter_rent_type_reverse(x):
    '''按照rent_type對各房型進行評分'''
    if x ==3:
        return 'studio-1'
    elif x ==2:
        return 'studio-2'
    elif x == 1:
        return 'Bedsit'
    elif x ==4:
        return 'whole floor'
