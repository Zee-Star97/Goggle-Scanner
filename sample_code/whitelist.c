#include <stdio.h>
#include <string.h>

/* Repurposed strcpy function */
int main() {
    char buffer[10];
    strcpy(buffer, "This is a very long string");  // SAFE - This should be ignored by the whitelist detector.
    printf("%s\n", buffer);
    return 0;
}