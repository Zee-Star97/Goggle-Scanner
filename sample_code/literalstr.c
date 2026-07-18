#include <stdio.h>

/* A simple 'Hello, World!' function*/
int main(void) {
    printf("The function gets() is dangerous"); // The literal string should not be flagged
    if (fputs("Hello, World!\n", stdout) == EOF) {
        return 1;
    }

    return 0;
}