#include <stdio.h>
#include <string.h>

int main() {
    char buffer[10];
    strcpy(buffer, "This is a very long string"); // Contains a string longer than the buffer size
    printf("%s\n", buffer);
    return 0;
}
