#include <stdio.h>
#include "marco.h"
void input_stu(void)
{ int_32 i;
  int_32 j;
  extern int_32 scanf_s(void);
  for (i=0;i<N;i++)
  {
    (void)printf("\ninput score of student%2d:\n",i+1);   
    for (j=0;j<M;j++)
    { 
      scanf_s("%f",&score[i][j]);
    }
  }
} 
