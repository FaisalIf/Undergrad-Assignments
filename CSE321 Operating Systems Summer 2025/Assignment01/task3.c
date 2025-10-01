#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>

int main() {
   pid_t a, b, c;
   FILE *file = fopen("count.txt", "w");
   fprintf(file, "c");
   fclose(file);

   a = fork();
   if (a >= 0) {
      file = fopen("count.txt", "a");
      fprintf(file, "c");
      fclose(file);
   }

   b = fork();
   if (b >= 0) {
      file = fopen("count.txt", "a");
      fprintf(file, "c");
      fclose(file);
   }

   c = fork();
   if (c >= 0) {
      file = fopen("count.txt", "a");
      fprintf(file, "c");
      fclose(file);
   }

   if (getpid() % 2 != 0) {
      pid_t odd_fork = fork();
      if (odd_fork >= 0) {
         file = fopen("count.txt", "a");
         fprintf(file, "c");
         fclose(file);
      }
   }

   if (a > 0 && b > 0 && c > 0) {
      int count = 0;
      char ch;
      wait(NULL);
      wait(NULL);
      wait(NULL);
      file = fopen("count.txt", "r");
      while (fscanf(file, "%c", &ch) == 1) {
         count++;
      }
      fclose(file);
      printf("Total processes created: %d\n", count);
   }

   return 0;
}