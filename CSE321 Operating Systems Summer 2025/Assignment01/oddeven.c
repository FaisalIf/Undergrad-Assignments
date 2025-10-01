#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
   int num;

   for (int i = 0; i < argc - 1; i++) {
      num = atoi(argv[i + 1]);
      if (num % 2 == 0) {
         printf("%d is Even\n", num);
      } else {
         printf("%d is Odd\n", num);
      }
   }

   return 0;
}