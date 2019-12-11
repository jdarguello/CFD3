import matplotlib.pyplot as plt 
from sympy import *
import sqlite3 as sql
import math
import numpy as np
from IPython.display import display, Markdown
from ipywidgets import *

class Solve():
    def __init__(self, Tp, Tipo, Peclet, data, Dx, Dy, it, dom, subs):
        Tp = (Tp,)
        #---Base de datos---
        nodos = None
        while nodos is None:
            con = sql.connect('App/data.db')
            nodos = con.execute("SELECT * FROM nodes ORDER BY ID ASC").fetchall()
            elementos = con.execute("SELECT * FROM elements ORDER BY p ASC").fetchall()
            con.close()
        #---Ecuación específica---
        #Creación de símbolos generales
        a_p, a_S, a_N, a_E, a_W, T_p, T_S, T_N, T_E, T_W, u, v, x, y, a_p0, b, F_S, F_N, F_E, F_W, D_S, D_N, D_E, D_W, Q_g = \
            symbols("a_p, a_S, a_N, a_E, a_W, T_p, T_S, T_N, T_E, T_W, u, v, x, y, a_{p0}, b, F_S, F_N, F_E, F_W, D_S, D_N, D_E, D_W, Q_g")
        T_p0 = Symbol("T_p ^0")
        rho, A, K = symbols("\\rho, A, K")
        A_pE, A_pW, A_pN, A_pS = symbols("A_{pE}, A_{pW}, A_{pN}, A_{pS}")
        
        #Fs y Ds
        K = data['Propiedades']['K']
        rrho = Peclet*K
        D_E = K*(Dy/Dx)
        D_W = D_E
        D_N = K*(Dx/Dy)
        D_S = D_N
        F_E = rho*u*Dy
        F_W = rho*u*Dy
        F_N = rho*v*Dx
        F_S = rho*v*Dx
        Cons = {}
        if Tipo == "Upwind":
            Cons[A_pE], Cons[A_pW], Cons[A_pN], Cons[A_pS] = 1,1,1,1
        elif Tipo == "Diferencias Centradas":
            Cons[A_pE], Cons[A_pW], Cons[A_pN], Cons[A_pS] = 1-0.5*abs(F_E/D_E), 1-0.5*abs(F_W/D_W), 1-0.5*abs(F_N/D_N), 1-0.5*abs(F_S/D_S)
        else:
            Cons[A_pE], Cons[A_pW], Cons[A_pN], Cons[A_pS] = Max(0, 1-0.5*abs(F_E/D_E)), Max(0, 1-0.5*abs(F_W/D_W)), Max(0, 1-0.5*abs(F_N/D_N)), Max(0, 1-0.5*abs(F_S/D_S))
        Cons[rho] = rrho
        Ec = (Tp[0].subs(Cons),)
        
        #Condiciones de frontera
        nodoss = self.BC(nodos)
        #print(nodoss)
        
        #Ts
        display(Markdown("_Progreso..._"))
        maximo = 0
        for i in range(it):
            for el in elementos:
                for Tss in [(T_N, el[1]), (T_S, el[2]), (T_E, el[4]), (T_W, el[5])]:
                    maximo += 1
        for j in range(1,subs[1]+1):
            for i in range(1,subs[0]+2):
                maximo += 1
        f = FloatProgress(min=0, max=maximo)
        display(f)
        Ts = {}
        for i in range(it):
            for el in elementos:
                for Tss in [(T_N, el[1]), (T_S, el[2]), (T_E, el[4]), (T_W, el[5])]:
                    f.value += 1
                    if np.isnan(nodoss[Tss[1]-1][3]):
                        Ts[Tss[0]] = 0
                    else:
                        Ts[Tss[0]] = nodoss[Tss[1]-1][3]
                Ts[T_p0] = nodoss[el[3]-1][4]
                #¿Lado de la derecha?
                if nodoss[el[3]-1][1] > 0 and nodoss[el[2]-1][2] == 0:
                    
                    Ts[T_S] = T_p
                #Cálculo de v y u
                if nodoss[el[1]-1][2] < dom[1]:
                    Ts[v] = -2*nodoss[el[1]-1][1]*(1-(nodoss[el[3]-1][2]+(nodoss[el[1]-1][2]-nodoss[el[3]-1][2])/2)**2)
                else:
                    Ts[v] = 0
                if nodoss[el[4]-1][2] < dom[0]:
                    Ts[u] = 2*nodoss[el[3]-1][2]*(1-(nodoss[el[3]-1][1] + (nodoss[el[4]-1][1]-nodoss[el[3]-1][1])/2)**2)
                else:
                    Ts[u] = 0
                #print(solve(Ec[0].subs(Ts)))
                nodoss[el[3]-1][3] = solve(Ec[0].subs(Ts))[0]
                nodoss[el[3]-1][4] = nodoss[el[3]-1][3]
                #¿Lado de la derecha?
                if nodoss[el[3]-1][1] > 0 and nodoss[el[2]-1][2] == 0:
                    nodoss[el[2]-1][3] = nodoss[el[3]-1][3]
        
        #---Esquema---
        #print(nodoss)
        id = 0
        T = np.zeros((subs[0]+2, subs[1]+2))
        #f.value = 0
        for j in range(1,subs[1]+1):
            for i in range(1,subs[0]+2):
                f.value += 1
                if self.Condicion(id, nodoss,dom):
                    id += subs[0]+2
                else:
                    id += 1
                if nodoss[id-1][2] == dom[1]:
                    id += 1
                #print(id)
                T[i][j] = nodoss[id-1][3]
        #print(T)
        display(Markdown("__Resultados:__"))
        plt.figure(figsize=(12,8))
        plt.imshow(T, cmap=plt.cm.get_cmap('jet'), interpolation='spline16')
        plt.colorbar()
    
    def Condicion(self, id, nodoss,dom):
        return nodoss[id-1][1] == 0 or nodoss[id-1][1] == dom[0]/2
        
    def BC(self, nodos):
        nodoss = np.zeros((len(nodos), 5))
        for i in range(len(nodos)):
            for j in range(5):
                nodoss[i][j] = nodos[i][j+1]
            if nodoss[i][2] == 0 and nodoss[i][1] < 0:
                nodoss[i][3] = 1+math.tanh(10)*(2+nodoss[i][1]+1)
            if nodoss[i][2] == 0 and nodoss[i][1] > 0:
                nodoss[i][3] = np.nan
        return nodoss
        
        
        
        