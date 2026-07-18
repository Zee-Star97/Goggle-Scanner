#include <stdio.h>

/* A simple 'Hello, World!' function*/
int main(void) {
    if (fputs("Hello, World!\n", stdout) == EOF) {
        return 1;
    }

    return 0;
}