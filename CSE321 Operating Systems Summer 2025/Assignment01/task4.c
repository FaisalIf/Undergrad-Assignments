#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
   int numbers[] = {7, 4, 3, 13, 16, 6};
   int size = sizeof(numbers) / sizeof(numbers[0]);
   pid_t pid;

   char s0[10], s1[10], s2[10], s3[10], s4[10], s5[10];

   sprintf(s0, "%d", numbers[0]);
   sprintf(s1, "%d", numbers[1]);
   sprintf(s2, "%d", numbers[2]);
   sprintf(s3, "%d", numbers[3]);
   sprintf(s4, "%d", numbers[4]);
   sprintf(s5, "%d", numbers[5]);

   pid = fork();

   if (pid < 0) { 
      printf("Fork Unsuccessful\n");
   } else if (pid == 0) {
      execl("./sort", "./sort", s0, s1, s2, s3, s4, s5, NULL);
   } else {
      wait(NULL);
      execl("./oddeven", "./oddeven", s0, s1, s2, s3, s4, s5, NULL);
   }

   return 0;
}