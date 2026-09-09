#include <stdio.h>
int main(){
    int a,b;
    printf("Enter your first number");
    scanf("%d", &a);

    printf("Enter your second number");
    scanf("%d", &b);

    int product = a*b;

    printf("your result is : %d",product);
}