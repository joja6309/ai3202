import sys 
from World_Grid_MDP import*
from MDP import*
import pprint
ep = float(sys.argv[2])
listOflists = []
i = 0;
f = open(str(sys.argv[1]))
roWcount = 0
for line in f:
    i += 1
    if (i == 5):
        rowCount = len(Aline)
       
    Aline = line.split()
    if len(Aline) != 0:
        listOflists.append(Aline)
listOflists.reverse()
the_Grid =  World_Grid_MDP(listOflists,terminals=[(0, 0), (len(listOflists), rowCount)])
print_path(the_Grid,ep)







