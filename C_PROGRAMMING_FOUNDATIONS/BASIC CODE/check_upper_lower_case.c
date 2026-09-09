#include<stdio.h>
int main(){
    char ch;
    printf("ENTER YOUR LETTER");
    scanf("%c",&ch);

    if(ch>='A' && ch<='Z')
    {
    printf("UPPERCASE");
    }
    else if(ch>='a' && ch<='z')
    {
    printf("LOWERCASE");
    }
    else
    {
        printf("YOU ARE NOT ENTER A LETTER");
    }
    return 0;

}