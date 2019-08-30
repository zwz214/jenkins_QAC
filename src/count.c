#include <stdio.h>
#include "marco.h"
void aver_stu(void)
{
  int_32 i;
  int_32 j;
  float_32 s;  //const float_32 t=5.0F;
  for (i=0;i<N;i++)
  {
    s = 0.0F;
    for (j = 0; j < M; j++)
    {
      s += score[i][j];
    }     
    a_stu[i]=s/5.0;
  }
}

void aver_cour(void)
{
  int_32   i;
  int_32   j;
  float_32 s;
  for (j=0;j<M;j++)
  {
    s=0.0F;
    for (i = 0; i < N; i++)
    {
      s += score[i][j];
    }
    a_cour[j]=s/(float_32)N;
  }
}

float_32 highest(void)
{ 
  float_32 high;
  int_32   i;
  int_32   j;  
  high=  score[0][0]; 
  for (i = 0; i < N;i++)
  {   
    for (j = 0; j < M; j++)
    {
      if (score[i][j] > high)
      {		  
	high = score[i][j];
	r = i + 1;
        c = j + 1;
      }  
    }
	  
  }
  return(high);
  
}

float_32 s_var(void)
{
  int_32 i;
  float_32 sumx,sumxn;
  sumx=0.0F;
  sumxn=0.0F;
  for (i=0;i<N;i++)
  {
    sumx+=a_stu[i]*a_stu[i];
    sumxn+=a_stu[i];
  }
  return(sumx/(float_32)N-((sumxn/ (float_32)N)*(sumxn/ (float_32)N)));
}
