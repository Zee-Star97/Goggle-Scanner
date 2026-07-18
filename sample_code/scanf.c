#include <stdio.h>

int main() {
    char name[15];
    scanf("%s", name);  // No length limit specified
    printf("Hello, %s!\n", name);
    return 0;
}
