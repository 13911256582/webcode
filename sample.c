#include <stdio.h>

void main(){
  int i, x;
  
  printf("input:");
  scanf("%d", &x);
  
  for(i=0; i<x; i++){
    printf("%d", i);
  }
  
  printf("\n");
}