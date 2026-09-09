#include<stdio.h>
int main(){
    char day;
    printf("Enter the day(S,M,t,W,TH,FR,SU): ");
    scanf("%c",&day);

    switch(day){

        case 'S': printf("SUNDAY \n");
                break;
        case 'M': printf("MONDAY \n");
                break;
        case 't': printf("TUESDAY \n");
                break;
        case 'W': printf("WEDNESDAY \n ");
                break;
        case 'TH': printf("THURSDAY \n");
                break;
        case 'F': printf("FRIDAY \n");
                break;
        case 'SU': printf("SATURDAY \n");
                break;
        default : printf("not a valid input \n");

    }
}