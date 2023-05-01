#Compiled Solver
#Felix

import numpy as np
import itertools
import pandas as pd
import wolframclient as wolf
from wolframclient.language import wlexpr, wl
from wolframclient.evaluation import WolframLanguageSession
import Keys #This is a supplementary file with some extra parameters
from wolframclient.serializers import export
import sys
import csv
import copy

def w(x,y):
    return 'Subscript[Global`w, ' + str(x) + ', ' + str(y) + ']'

def R_Solve(data):
    
    session=WolframLanguageSession()

    Type = "Roots"

    sud = np.array(data)

    mins = Keys.ValSet2[0]
    ref = Keys.Rep2

    refdict = dict()

    subs = dict()

    for i in range(len(sud)):
        for j in range(len(sud)):
            if sud[i,j] != 0:
                subs.update({w(i+1,j+1):mins[int(sud[i,j])-1]})


    #This generates all the equations

    K_dim = int(np.sqrt(sud.shape[0]))

    Size = sud.shape[0]**2
    leng = sud.shape[0]

    X = np.linspace(1,leng,leng)
    Y = np.linspace(1,leng,leng)
    X,Y = np.meshgrid(X,Y)

    XY = np.array((X.flatten(), Y.flatten()))

    KRoots = []
    KSP = []
    Ws =  np.full(X.shape,'o                                  ')

    for i in range(len(XY[0])):
        x=int(XY[:,i][0])
        y=int(XY[:,i][1])
        KRoots.append(w(x,y)+str('^')+str(int(leng))+' - 1, ')
        Ws[x-1,y-1] = w(x,y)

    for i in range(len(XY[0])):
        x=int(XY[:,i][0])
        y=int(XY[:,i][1])
        k = ''
        for j in range(leng):
            k += '('+w(x,y)+' - '+mins[j]+')'
        k+=', '
        KSP.append(k)

    Columns = Ws.T

    Squares = []

    for i in range(K_dim):
        for j in range(K_dim):

            mask = ((X-1)//K_dim==i)&((Y-1)//K_dim==j)

            square = np.array((X[mask].flatten(), Y[mask].flatten()))

            sq=[]

            for h in range(len(square[0])):
                x=int(square[:,h][0])
                y=int(square[:,h][1])
                sq.append(w(x,y))

            Squares.append(sq)

    Sqps = []  

    def NotSameP(pair, K_dim):

        if K_dim == 2:

            return '(' + pair[0] + " + " + pair[1] + ')*(' + pair[0] + '^2 + ' + pair[1] + '^2), '

        if K_dim == 3:

            return '(' + pair[0] +'^2 + ' + pair[0] + ' * ' + pair[1] +' + ' + pair[1] + '^2 )*(' + pair[0] +'^6 + '+ pair[1] +'^6 + ' + pair[0] + '^3 * ' + pair[1] + '^3), '


    "-----------------------------------------------------"

    if Type == "Roots":    

        K = KRoots
        refdicts = {3:Keys.RefDictRoots3, 2:Keys.RefDictRoots2}

        refdict = refdicts[K_dim]

        for i in range(len(Squares)):
            for pair in itertools.combinations(Squares[i],2):
                Sqps.append(NotSameP(pair, K_dim))


        Colps = []

        for i in range(len(Columns)):
            for pair in itertools.combinations(Columns[i], 2):
                Colps.append(NotSameP(pair, K_dim))

        Rowps = []

        for i in range(len(Ws)):
            for pair in itertools.combinations(Ws[i], 2):
                Rowps.append(NotSameP(pair, K_dim))    

        #print(K)    

    "-----------------------------------------------"

    j = ''

    for p in Sqps:
        j += p

    for p in K:
        j += p

    for p in Colps:
        j += p

    for p in Rowps:
        j += p

    for x in subs:
        j = j.replace(x,'('+subs[x]+')') 


    ##This essentially just takes the equations and plugs them through wolfram

    ws = ''

    for x in Ws.flatten():
        ws += x+', '

    for x in subs:
        ws = ws.replace(x+', ', '')

    Eval = session.evaluate(wlexpr('Solve[{'+j[:-2]+'}==0,{'+ws[:-2]+'}]'))

    ##This then takes the Evaluated answer and translates it (rather shoddily) to a readable array and exports as a csv

    Sols = dict()

    for i in range(len(Eval[0])):
        W = str(Eval[0][i][0])[0:]
        ans = complex(int(str(session.evaluate(wlexpr('Re['+str(Eval[0][i][1])+']')))), int(str(session.evaluate(wlexpr('Im['+str(Eval[0][i][1])+']')))))
        Sols.update({W:ans})
        #print(W+' = ' + str(ans))

    Solution = copy.deepcopy(Ws)

    for i, row in enumerate(Solution):
        for j, x in enumerate(row):
            if x in Sols:
                Solution[i,j] = Solution[i,j].replace(x, str(Sols[x]))
            if x in subs:
                Solution[i,j] = Solution[i,j].replace(x, str(subs[x]))
            for l, y in enumerate(refdict):
                Solution[i,j] = Solution[i,j].replace(y, str(refdict[y]))
            Solution[i,j] = Solution[i,j].replace('(', '')
            Solution[i,j] = Solution[i,j].replace(')', '')

    Solution = Solution.astype(int)  

    return Solution
