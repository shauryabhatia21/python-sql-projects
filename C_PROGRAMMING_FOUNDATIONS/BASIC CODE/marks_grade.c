#include<stdio.h>
int main(){
    int marks;
    printf("ENTER YOUR MARKS");
    scanf("%d",&marks);
    if(marks<30)
    {printf("grade C");
    }
    else if (marks >= 30 && marks < 70)
    {
        printf("grade B");
    }
    else if(marks >= 70 && marks < 90)
    {
        printf ("grade A");
    }
    else if(marks >=90 && marks<=100)
    {        
        printf("grade A+");
    }
    else
    {
        printf("NOT A VALID INPUT");
    }
    return 0;
    
}