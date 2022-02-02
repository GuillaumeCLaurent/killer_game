import random

actions_list = [f'a{i}' for i in range(1, 10)]
names_list = [f'p{i}' for i in range(1, 10)]

def shuffle(al, pl):
    n = len(al)
    res = {}
    ind_l= [i for i in range(0, n)]

    ind = random.choice(ind_l)
    first_ind = ind
    ind_l.remove(ind)

    while(len(ind_l)>1):  
   
        sec_ind = random.choice(ind_l)
        res[pl[ind]] = (al[sec_ind], pl[sec_ind])
        ind = sec_ind
        ind_l.remove(ind)
    
    
    res[pl[ind_l[0]]] = (al[first_ind], pl[first_ind])
 
    return res

sl = shuffle(actions_list, names_list)

for s in sl:
    print(s, sl[s])


