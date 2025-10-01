#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
   pid_t pid1, pid2;

   pid1 = fork();

   if (pid1 < 0) {
      printf("Fork Unsuccessful\n");
   } else if (pid1 == 0) {
      printf("2. Child process ID: %d\n", getpid());

      pid2 = fork();
      if (pid2 < 0) {
         printf("Fork Unsuccessful\n");
      } else if (pid2 == 0) {
         printf("3. Grand Child process ID: %d\n", getpid());
         exit(0);
      }

      pid2 = fork();
      if (pid2 < 0) {
         printf("Fork Unsuccessful\n");
      } else if (pid2 == 0) {
         printf("4. Grand Child process ID: %d\n", getpid());
         exit(0);
      }

      pid2 = fork();
      if (pid2 < 0) {
         printf("Fork Unsuccessful\n");
      } else if (pid2 == 0) {
         printf("5. Grand Child process ID: %d\n", getpid());
         exit(0);
      }

      wait(NULL);
      wait(NULL);
      wait(NULL);

      exit(0);
   } else {
      printf("1. Parent process ID : %d\n", getpid());
      wait(NULL);
   }

   return 0;
}