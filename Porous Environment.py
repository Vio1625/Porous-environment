import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from copy import deepcopy
from time import time



def init(n,p):
    '''Fonction qui créer un tableau de taille (n x n) possédant E(p x n²) cases blanches (case avec un 1). Les autres cases sont noires (case avec un 0).'''
    if p<0.5:
        T=np.zeros((n,n)) # On crée un tableau de cases noires
        nb_casesB=np.math.floor(p*n*n) # On compte le nombre de cases blanches à placer dans le tableau
        nb_casesB=int(nb_casesB)
        L= [ ] # 0n crée une liste des indices de chaque case
        for i in range(n):
            for j in range(n):
                L+=[[i,j]]
        for k in range (nb_casesB): # On place toutes les cases blanches
            alea=np.random.randint(0,len(L))
            ligne,colonne=L[alea]
            T[ligne,colonne]=1
            del L[alea]
    else: # Si la probabilité est supérieure à 0,5 on fait le contraire (On construit un tableau de cases blanches puis on place les cases noires)
        T=np.ones((n,n))
        nb_casesN=np.math.ceil((1-p)*n*n)
        L= [ ]
        for i in range(n):
            for j in range(n):
                L+=[[i,j]]
        for k in range (nb_casesN):
            alea=np.random.randint(0,len(L))
            ligne,colonne=L[alea]
            T[ligne,colonne]=0
            del L[alea]
    return(np.array(T))


def remplissage(T):
    '''Fonction qui prend un tableau de cases noires et blanches créé par la fonction init et qui remplit en bleu les cases blanches reliées au haut du tableau. L'eau se propage entre les cases blanches ayant une arrête commune'''
    nbLigne,nbColonne=np.shape(T)
    iCaseAqua1=[] # Liste des cases bleues de la première ligne
    for indice in range(nbColonne): # On cherche toutes les cases blanches présentes dans la première ligne afin de les transformer en cases bleues
        if T[0,indice]==1:
            iCaseAqua1+=[indice]
            T[0,indice]=0.5
    iCaseAqua2=[] # Liste des cases bleues de la ligne d'en dessous
    iLigne=1
    while iCaseAqua1!=[] and iLigne<nbLigne :# Tant qu'il reste des cases bleues dans la dernière case que l'on a testé et qu'il reste des lignes que nous n'avons pas encore testé
        for iColonne in iCaseAqua1: # Toutes les cases blanches de la ligne du dessous qui ont leur arête du haut commune avec une case bleu se remplissent d'eau
            if T[iLigne,iColonne]==1:
                iCaseAqua2+=[iColonne]
                T[iLigne,iColonne]=0.5
        for iColonne in iCaseAqua2:#On se concentre ensuite sur la ligne du dessous
            iColonne1=iColonne
            iColonne2=iColonne # sauvegarde de la variable pour la 2 partie du for
            while iColonne1!=0 and T[iLigne,iColonne1-1]==1: # On regarde s'il y a des cases blanches à gauche des cases bleues afin de permettre à l'eau de se propager sur le côté
                iColonne1-=1
                iCaseAqua2+=[iColonne1]
                T[iLigne,iColonne1]=0.5
            while iColonne2!=nbColonne-1 and T[iLigne,iColonne2+1]==1: # On regarde s'il y a des cases blanches à droite des cases bleues afin de permettre à l'eau de se propager de l'autre côté. La sauvegarde de la valeur de iColonne avant le while était nécessaire car, quand l'eau se propage vers la gauche, la valeur change
                iColonne2+=1
                iCaseAqua2+=[iColonne2]
                T[iLigne,iColonne2]=0.5
        iCaseAqua1=iCaseAqua2 # On reinitialise les paramètres pour recommencer l'opération sur la ligne d'en-dessous
        iCaseAqua2=[]
        iLigne+=1
    return(T)


def remplissage1(T):
    '''Fonction remplissage adaptée pour le calcul de la probabilité de passage.
    Cette fonction remplit le tableau avec la même méthode que la précédente mais au lieu de renvoyer le tableau rempli, renvoit un booléen si l'eau est parvenue jusqu'en bas'''
    nbLigne,nbColonne=np.shape(T)
    iCaseAqua1=[]
    for indice in range(nbColonne):
        if T[0,indice]==1:
            iCaseAqua1+=[indice]
            T[0,indice]=0.5
    iCaseAqua2=[]
    iLigne=1
    while iCaseAqua1!=[] and iLigne<nbLigne :
        for iColonne in iCaseAqua1:
            if T[iLigne,iColonne]==1:
                iCaseAqua2+=[iColonne]
                T[iLigne,iColonne]=0.5
        for iColonne in iCaseAqua2:
            iColonne1=iColonne
            iColonne2=iColonne
            while iColonne1!=0 and T[iLigne,iColonne1-1]==1:
                iColonne1-=1
                iCaseAqua2+=[iColonne1]
                T[iLigne,iColonne1]=0.5
            while iColonne2!=nbColonne-1 and T[iLigne,iColonne2+1]==1:
                iColonne2+=1
                iCaseAqua2+=[iColonne2]
                T[iLigne,iColonne2]=0.5
        iCaseAqua1=iCaseAqua2
        iCaseAqua2=[]
        iLigne+=1
    if iCaseAqua1!=[]: # On compare le nombre de ligne au numéro de la dernière ligne remplie. Si l'eau parvient à traverser alors, la dernière ligne traitée dans le while n'est pas vide (il y a une ou plusieurs cases bleues dans la dernière ligne)
        PassageAqua=True
    else :
        PassageAqua=False
    return(PassageAqua)


def proba() :
    '''Fontion qui trace la courbe de probabilité de passage de l'eau en fonction de la probabilité d'ouverture de chaque case'''
    t1=time()
    ValTest=list(np.arange(0,0.5,0.1))+list(np.arange(0.5,0.7,0.01))+list(np.arange(0.7,1,0.1))# Liste des valeurs de probabilité d'ouverture de cases à tester. Le pas est plus court entre 0,5 et 0,7 afin d'avoir des valeurs plus précises autour du point de probabilité critique.
    ProbaPassage=[] # Liste des probabilités de passage associée aux valeurs de la liste précedente
    for test in ValTest:
        nbPassage=0
        for i in range(100): # On fait plusieurs tests et on compte le nombre de fois où l'eau parvient à traverser afin d'optenir un nombre de passage moyen
            if remplissage1(init(128,test)):
                nbPassage+=1
        ProbaPassage+=[nbPassage/100]
    t2=time()
    print(t2-t1)
    plt.plot(ValTest,ProbaPassage) # On représente graphiquement la courbe des probabilités de passage en fonction des probabilités d'ouverture de chaque case
    plt.show()


def remplissage2(T):
    '''Fonction remplissage adaptée pour le calcul du nombre de cases bleues.
    Cette fonction remplit le tableau avec la même méthode que la première mais au lieu de renvoyer le tableau remplie, elle renvoit le nombre de cases bleues dans le tableau'''
    nbLigne,nbColonne=np.shape(T)
    iCaseAqua1=[]
    compteur=0 # On initialise un compteur qui augmente de 1 à chaque fois qu'une case blanche devient bleu
    for indice in range(nbColonne):
        if T[0,indice]==1:
            iCaseAqua1+=[indice]
            T[0,indice]=0.5
            compteur+=1
    iCaseAqua2=[]
    iLigne=1
    while iCaseAqua1!=[] and iLigne<nbLigne :
        for iColonne in iCaseAqua1:
            if T[iLigne,iColonne]==1:
                iCaseAqua2+=[iColonne]
                T[iLigne,iColonne]=0.5
                compteur+=1
        for iColonne in iCaseAqua2:
            iColonne1=iColonne
            iColonne2=iColonne
            while iColonne1!=0 and T[iLigne,iColonne1-1]==1:
                iColonne1-=1
                iCaseAqua2+=[iColonne1]
                T[iLigne,iColonne1]=0.5
                compteur+=1
            while iColonne2!=nbColonne-1 and T[iLigne,iColonne2+1]==1:
                iColonne2+=1
                iCaseAqua2+=[iColonne2]
                T[iLigne,iColonne2]=0.5
                compteur+=1
        iCaseAqua1=iCaseAqua2
        iCaseAqua2=[]
        iLigne+=1
    return(compteur)


def densite(n):
    '''Fonction qui trace la courbe de densité d'occupation en fonction de la probabilité d'ouverture des cases'''
    probaTest=np.arange(0.25,1,0.05) # Liste des valeurs de probabilité d'ouverture à tester
    densite=[] # Liste des densités associées
    for test in probaTest:
        SommeDensite=0 #On teste plusieurs fois le programme afin de faire une densité moyenne
        for i in range(10):
            nbCasesB=np.math.floor(test*n*n)
            SommeDensite+=remplissage2(init(n,test))/nbCasesB
        densite+=[SommeDensite/100]
    plt.plot(probaTest,densite)  # On représente graphiquement la courbe des densités d'occupation en fonction des probbailités d'ouverture de chaque case
    plt.show()


menu=int(input("Pour visualiser le milieux poreux intial puis, suite à l'écoulement de l'eau tapez 1 \n Pour visualiser la courbe de probabilité de passage de l'eau tapez 2 \n Pour visualiser la courbe de densité d'occupation tapez 3 \n"))

if menu==1:
    p=0.61
    n=128
    T=init(n,p)
    if p!=1:
        plt.matshow(T,cmap=ListedColormap(['black','white']))
    else: # Si la probabilité est de 1, le tableau n'aura que des cases blanches et pas de case noire
        plt.matshow(T,cmap=ListedColormap(['white']))
    plt.show()
    T2=deepcopy(T)
    A=remplissage(T)
    if p==1: #cas où il n'y a que des cases bleues
        plt.matshow(T,cmap=ListedColormap(['aqua']))
    elif remplissage2(T2)==np.math.floor(p*n*n): # cas où il n'y a que des cases blanches et bleues
        plt.matshow(A,cmap=ListedColormap(['black','aqua']))
    else: # fonctionne pour tous les autres cas
        plt.matshow(A,cmap=ListedColormap(['black','aqua','white']))
    plt.show()
elif menu==2:
    proba()
else:
    densite(128)