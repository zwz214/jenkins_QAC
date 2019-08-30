#include <stdio.h>
#include "marco1.h"
int main(void)
{ int_32 i;
  int_32 j;
  float_32 h;
  input_stu();
  aver_stu();
  aver_cour();
  (void)printf("\n  NO.     cour1   cour2   cour3   cour4   cour5   aver\n");   //PRQA S 5124 EOF
  for(i=0;i<N;i++)
  {
    (void)printf("\n NO %2d ",i+1);
    for (j = 0; j < M; j++)
    {
      (void)printf("%8.2f", score[i][j]);
    }
    (void)printf("%8.2f\n",a_stu[i]);
  }
  (void)printf("\naverage:");       
  for (j = 0; j < M; j++)
  {
    (void)printf("%8.2f", a_cour[j]);                                     
  }
	  
  (void)printf("\n");
  h=highest();
  (void)printf("highest:%7.2f   NO. %2d   course %2d\n",h,r,c);
  (void)printf("variance %8.2f\n",s_var());
  return 0;
}
