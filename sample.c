#include <stdio.h>

void main(){
  int i, x;
 
  x = 10;
  printf("\n*");
  scanf("%d", &x);

 
  for(i=0; i<x; i++){
    printf("%d", i);
  }

  printf("\n");
}
