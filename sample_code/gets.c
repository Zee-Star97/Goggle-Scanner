#include <stdio.h>

int main() {
    char input[20];
    gets(input);  // Unsafe: no bounds checking
    printf("You entered: %s\n", input);
    return 0;
}
