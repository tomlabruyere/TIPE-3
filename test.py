# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:57:49 2020

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt

def tableau_V ():
    """le fichier csv contient des valeurs décimales écrite avec des ,
    et séparées par par des ;
    dans l'exemple propsé, on récupère les données de la première 
    et de la deuxième colonne (la 1e ligne étant exclue)"""
    f=open("mesures.csv","r")
    tab=f.readlines()#tab est une liste des valeurs de chaque ligne du tableau excel
    print(tab)
    N=len(tab)
    tab_x=np.zeros((N-1))#tableau vide
    tab_y=np.zeros((N-1))
    for i in range(1,len(tab)):
        ligne=tab[i]
        ligne=ligne.replace(",",".")
        ligne=ligne.split(";")
        x,y=ligne[0],ligne[1]
        x,y=float(x),float(y)
        tab_x[i-1],tab_y[i-1]=x,y#on remplit les tableaux
    return tab_x,tab_y       

def RegLin(X,u_X,Y,u_Y):
    """cette fonction prend pour argument 4 tableaux numpy,
    - le tableau X contient les valeurs en abscisse 
    - le tableau des incertitudes-types de X (qui peuvent être nulles !)
    - le tableau Y contient les valeurs en ordonnée
    - le tableau des incertitudes-types de Y
     cette fonction retourne Y(X) ainsi que l'équation de la droite et les incertitudes types associées"""
    M=10000#nbr itérations pour Monte Carlos
    tab_a=np.zeros((M))
    tab_b=np.zeros((M))
    for i in range(0,M):
        tab_X=np.random.normal(X,u_X)#On génère des valeurs aléatoires pour toutes les valeurs Xi
        tab_Y=np.random.normal(Y,u_Y)#On génère des valeurs aléatoires pour toutes les valeurs Yi
        p=np.polyfit(tab_X,tab_Y,1)#Régression linéaire : on trouve le polynôme d'ordre 1 (moindres carrés)
        tab_a[i]=p[0]#pente
        tab_b[i]=p[1]#Y(0)
    a = np.mean(tab_a)#moyenne des pentes
    b = np.mean(tab_b)#moyenne  des ordonnées à l'origine
    u_a=np.std(tab_a)#écart type ou incertitude-type
    u_b=np.std(tab_b)# écart type ou incertitude-type
    x=np.linspace(np.min(X),np.max(X),1000)
    y=a*x+b#Droite de régression
    plt.errorbar(X,Y,xerr=u_X,yerr=u_Y,linestyle="",marker='o',label="points expérimentaux")#points exp + barres d'erreur
    plt.plot(x,y,label="Y=aX+B \n\
    a = {0:.3f} +/- {1:.3f} \n\
    b = {2:.3f} +/- {3:.3f}".format(a,u_a,b,u_b))
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("regression")
    plt.legend()
    plt.show()





def etalon(a,u_a,b,u_b,Yreport):
    """cette fonction prend pour argument les valeur de a et b d'une fonction linéaire y(x)=ax+b 
    lu_a et u_b sont les incertitudes-types associées à a et b
    Yreport est l'ordonnée du point P dont on veut l'abscisse Xp (avec incertitude obtenue par MC)
    cette fonction retourne [Yreport, Xp, incertitude-type de Xp]"""
    M=10**4
    Tab_Xpred=np.zeros((M))
    for i in range (M):
        b_new=np.random.normal(b,u_b)
        a_new=np.random.normal(a,u_a)
        Xpred=(Yreport-b_new)/a_new
        Tab_Xpred[i]=Xpred
    Xpred=np.mean(Tab_Xpred)
    u_Xpred=np.std(Tab_Xpred)
    return [Yreport,Xpred,u_Xpred]


tab_t,tab_P=tableau_V()
u_p=np.ones((len(tab_t)))*10
u_t=np.zeros(len(tab_t))
RegLin(tab_t,u_t,tab_P,u_p)
print(etalon(3.3,0.2,943,11,0))

