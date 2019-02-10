"""
Created on Sat Feb  9 22:58:03 2019

@author: david
"""
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime
import itertools as itt

DATA=np.load("div_test.npy")

n_side=DATA.shape[0]

#=========================FUNCIONES=======================
def vecinos3D(ii,jj,kk,tam_r):
    ii_a=(ii-1)%tam_r
    ii_b=(ii+1)%tam_r
    jj_a=(jj-1)%tam_r
    jj_b=(jj+1)%tam_r
    kk_a=(kk-1)%tam_r
    kk_b=(kk+1)%tam_r 
    
    xx=[ii_a,ii,ii_b]
    yy=[jj_a,jj,jj_b]
    zz=[kk_a,kk,kk_b]
    
    L=list(itt.product(*[xx,yy,zz]))
 
    L=np.array(L).T
    
    return L[0],L[1],L[2]
def revisarVecinos(ii,jj,kk,Pertenencia,tam_r):
    xx,yy,zz=vecinos3D(ii,jj,kk,tam_r)
    tam=len(xx)
    pert=[]
    for i in range (tam):
        p_i=Pertenencia[xx[i],yy[i],zz[i]]
        pert.append(p_i)
    suma=np.sum(pert)
    if(suma==0):
        return 0
    else:
        pert=np.array(pert)
        pert=list(pert[pert!=0])
        return max(set(pert), key=pert.count)
        


def dist_nodo_cercano(ii,jj,kk,x,y,z):
    d=np.inf
    xx=0
    yy=0
    zz=0
    for i in range (len(x)):
        dist=np.sqrt((x[i]-ii)**2+(y[i]-jj)**2+(z[i]-kk)**2)
        if (dist<d):
            d=dist
            xx=x[i]
            yy=y[i]
            zz=z[i]
    return d,xx,yy,zz


def darVacios(Pertenencia):
    return len(np.where(Pertenencia==0)[0])

#===================WATERSHED==============================

def watershed(filename,filename_out,d_tolerancia,vacios_tolerancia):
    DIV=np.load(filename)
    DIV=DIV[1:-1,1:-1,1:-1]
    tam=np.shape(DIV)[0]
    N_intervalos=20*tam
    
    div_max=round(np.amax(DIV)+5,-1)
    div_min=round(np.amin(DIV)-5,-1)
    N_intervalos=7*tam
    
    
    barrido=np.linspace(div_max,div_min,N_intervalos)
    #barrido=np.concatenate((barridoA,barridoA))
    
    tam_b=len(barrido)
    delta=barrido[0]-barrido[1]
    Pertenencia=np.zeros([tam,tam,tam])
    
    
    x_nodos=[]
    y_nodos=[]
    z_nodos=[]
    cont_nodos=1
    
    cont_iteraciones=0
    
    
    vacios=[]
    vacios.append(darVacios(Pertenencia))
    while(vacios[-1]>vacios_tolerancia):
        print(str(round((100*vacios[-1]/(tam**3)),6)) + " % del espacio está vacio ("+str(vacios[-1])+" voxeles)")   
        c=0
        for lev in barrido:
            if(c%10==0):
                print(str(round(c*100/tam_b,2))+" % evaluado ("+str(darVacios(Pertenencia))+" voxeles)")
            c+=1
            cota_inf=lev
            cota_sup=lev+delta
            aa=np.where((DIV<cota_sup)&(DIV>=cota_inf)&(Pertenencia==0))
            xx,yy,zz=aa[0],aa[1],aa[2]
            rec=len(xx)
            for i in range (rec):
                x,y,z=xx[i],yy[i],zz[i]
                pert=revisarVecinos(x,y,z,Pertenencia,tam)
                if(pert!=0):
                    Pertenencia[x,y,z]=pert
                else:
                    d,ii,jj,kk=dist_nodo_cercano(x,y,z,x_nodos,y_nodos,z_nodos)
                    if(d>d_tolerancia):
                        Pertenencia[x,y,z]=cont_nodos
                        cont_nodos+=1
                        x_nodos.append(x)
                        y_nodos.append(y)
                        z_nodos.append(z)
        cont_iteraciones+=1
        vacios.append(darVacios(Pertenencia))
    aa=np.where(Pertenencia==0)
    xx,yy,zz=aa[0],aa[1],aa[2]
    rec=len(xx)
    for i in range (rec):
        d,ii,jj,kk=dist_nodo_cercano(xx[i],yy[i],zz[i],x_nodos,y_nodos,z_nodos)
        Pertenencia[xx[i],yy[i],zz[i]]=Pertenencia[ii,jj,kk]

    np.save(filename_out,Pertenencia)
    return cont_nodos-1,cont_iteraciones



#============Main======================================================
    
file_stats=open("STATS.csv","w")
file_stats.write("Parches,Iteraciones,VaciosTol,DistanciaTol,FileIN,FileOut,Time"+"\n")

name_in="div_test.npy"
name_out="pert_test.npy"

tol_vacios=0
DistanciaTol=1

nodos,it=watershed(name_in,name_out,DistanciaTol,tol_vacios)

file_stats.write(str(nodos)+","+str(it)+","+str(tol_vacios)+","+str(DistanciaTol)+","+name_in+","+name_out+","+strftime("%Y.%m.%d-%H:%M:%S", gmtime())+"\n")
file_stats.close()