#include <stdio.h>

/* This is a comment // with an internal comment
   strcpy(dest, src); // Should not be flagged
*/

/* A simple 'Hello, World!' function*/
int main(void) {
    if (fputs("Hello, World!\n", stdout) == EOF) {
        return 1;
    }

    return 0;
}