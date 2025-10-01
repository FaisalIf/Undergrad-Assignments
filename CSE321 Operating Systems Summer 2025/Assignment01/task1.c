#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
   FILE *file = fopen(argv[1], "a");
   char input[256];
   while (1) {
      printf("Enter string (or -1 to stop): ");
      scanf("%s", input);
      if (strcmp(input, "-1") == 0) {
         break;
      }
      fprintf(file, "%s\n", input);
   }
   fclose(file);
   return 0;
}