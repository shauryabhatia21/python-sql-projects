#include<stdio.h>
int main(){
    int marks;
    printf("ENTER STUDENT MaRKS \n");
    scanf("%d", &marks);
    if (marks>=30 && marks<100)
    {
        printf("PASS \n");
    }
    else if (marks<30 && marks<100)
    {
        printf("FAIL \n");
    }
     else
    {
        printf("NOT A VALID INPUT \n");
    }
    return 0;
}
