#include<stdio.h>
int main(){
    float square;
    printf("Enter the side of the square: ");
    scanf("%f",&square);

    float area= square *square;
    printf("the area of the square is %f", area);
    return 0;
}