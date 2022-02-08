import random
from sre_constants import _NamedIntConstant

actions_list = [f'a{i}' for i in range(1, 11)]
names_list = [f'p{i}' for i in range(1, 11)]

print(actions_list)
def shuffle(al, pl):
    list = [elmt for elmt in zip(actions_list, names_list)]
    random.shuffle(list)
    n = len(al)
    res = {}
    for i in range(n):
        ind1 = (i+1)%n
        ind2 = (i-1)%n
        res[list[i][1]] = (list[ind1][1], list[ind2][0])
    return res

    """
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
    """
    return res

sl = shuffle(actions_list, names_list)

for s in sl:
    print(s, sl[s])


