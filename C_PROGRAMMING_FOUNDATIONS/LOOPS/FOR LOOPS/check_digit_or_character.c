#include <stdio.h>

int main() {
    char ch;
    printf("ENTER YOUR INPUT : ");
    scanf(" %c", &ch);

    if ((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z')) {
        printf("YOU ENTERED AN ALPHABET CHARACTER: %c\n", ch);
    } else if (ch >= '0' && ch <= '9') {
        printf("YOU ENTERED A DIGIT: %c\n", ch);
    } else {
        printf("YOU ENTERED A SPECIAL CHARACTER: %c\n", ch);
    }
    return 0;
}
