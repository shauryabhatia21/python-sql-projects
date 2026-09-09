#include<stdio.h>
int main(){ 
    int a,b;
    printf("enter your first number");
    scanf("%d", &a);

    printf("enter second number");
    scanf("%d",&b);

    int sum = a+b;

    printf("sum is : %d", sum);
    return 0;
}