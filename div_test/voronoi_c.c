#include <stdio.h>
#include <stdlib.h>
#include <math.h>


int n_side;

//variales de iteracion
int i;
int j;
int k;
int l;



//sobre parametros
FILE *parametros;
int MAXCOLS=4;
int MAXROWS;
//sobre input
FILE *sampleIN;
int *x;
int *y;
int *z;
int *pert;
//sobre output
FILE *sampleOUT;
int *X;
int *Y;
int *Z;
int *PERT;


//FUNCIONES============
void reconocerParametros();
void cargarArreglosIniciales(int MAXROWS);
double dar_distancia(int i1,int j1,int k1,int i2,int j2,int k2);
int nodo_mas_cercano(int ii,int jj,int kk);
int construirGrid(int longitud);



int main(){
printf("Generando datos voronoi ...\n");
reconocerParametros();
cargarArreglosIniciales(MAXROWS);
int LONG=n_side*n_side*n_side;
printf("numero de voxeles = %d\n",LONG);
int control=construirGrid(LONG);

return 0;
        }




void reconocerParametros(){

parametros=fopen("params.txt","r");
fscanf(parametros,"%d", &n_side);
fscanf(parametros,"%d", &MAXROWS);
fclose(parametros);


x=(int*) malloc(MAXROWS * sizeof(int));
y=(int*) malloc(MAXROWS * sizeof(int));
z=(int*) malloc(MAXROWS * sizeof(int));
pert=(int*) malloc(MAXROWS * sizeof(int));

if((x==NULL)||(y==NULL)||(z==NULL)||(pert==NULL)){
printf("malloc failed ,damn");
exit(1);
}
}

void cargarArreglosIniciales(int mrows){
sampleIN=fopen("nodos.txt","r");
for(int i=0; i < mrows ;i++){
//printf("scan row %d \n",i);
fscanf(sampleIN,"%d %d %d %d", &x[i], &y[i], &z[i], &pert[i]);

}
fclose(sampleIN);
}


double dar_distancia(int i1,int j1,int k1,int i2,int j2,int k2){
double r=sqrt(pow((i1-i2),2)+pow((j1-j2),2)+pow((k1-k2),2));
if(sqrt(pow((i1-n_side-i2),2)+pow((j1-j2),2)+pow((k1-k2),2))<r){
r=sqrt(pow((i1-n_side-i2),2)+pow((j1-j2),2)+pow((k1-k2),2));}
else if(sqrt(pow((i1-i2),2)+pow((j1-n_side-j2),2)+pow((k1-k2),2))<r){
r=sqrt(pow((i1-i2),2)+pow((j1-n_side-j2),2)+pow((k1-k2),2));}
else if(sqrt(pow((i1-i2),2)+pow((j1-j2),2)+pow((k1-n_side-k2),2))<r){
r=sqrt(pow((i1-i2),2)+pow((j1-j2),2)+pow((k1-n_side-k2),2));}
return r;
}



int nodo_mas_cercano(int ii,int jj,int kk){
    
    double dist=pow(n_side,2); //al azar numero grande
    int perten=0;
    for(l = 0;l<MAXROWS;l++){
    double d1=dar_distancia(ii,jj,kk,x[l],y[l],z[l]);
    if(d1<dist){
    dist=d1;
    perten=pert[l];
    }
    }
    return perten;
}









int construirGrid(int longitud){

X=(int*) malloc(longitud * sizeof(int));
Y=(int*) malloc(longitud * sizeof(int));
Z=(int*) malloc(longitud * sizeof(int));
PERT=(int*) malloc(longitud * sizeof(int));

sampleOUT=fopen("voronoi_3D.txt","w");

int m_pp=0;
for(i=0;i<n_side;i++){
printf("printing i = %d / %d \n",i+1,n_side);
for(j=0;j<n_side;j++){

for(k=0;k<n_side;k++){
int pp = nodo_mas_cercano(i,j,k);
if(pp > m_pp){
m_pp=pp;
}
fprintf(sampleOUT,"%d %d %d %d\n",i,j,k,pp);

}
}
}
printf("%d nodos usados en Voronoi.\n",m_pp);
fclose(sampleOUT);
return 0;
}












