#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

int *fib;
int *ind;

void *fib_seq(void *arg) {
   int n = *(int *)arg;
   fib = (int *)malloc(sizeof(int) * (n + 1));
   
   if (!fib) {
      perror("array allocation failed");
      exit(1);
   }
   
   if (n >= 0) {
      fib[0] = 0;
   }
   if (n >= 1) {
      fib[1] = 1;
   }
   
   for (int i = 2; i <= n; i++) {
      fib[i] = fib[i - 1] + fib[i - 2];
   }
   
   return NULL;
}

void *fib_val(void *arg) {
   void **args = (void **)arg;
   int n = *(int *)args[0];
   int s = *(int *)args[1];
   
   for (int i = 0; i < s; i++) {
      int search_index = ind[i];
      if (search_index >= 0 && search_index <= n) {
         printf("result of search #%d = %d\n", i + 1, fib[search_index]);
      } else {
         printf("result of search #%d = -1\n", i + 1);
      }
   }
   
   return NULL;
}

int main() {
   int n;
   int s;
   pthread_t t1, t2;
   
   printf("Enter the term of fibonacci sequence:\n");
   scanf("%d", &n);

   if (n < 0 || n > 40) {
      printf("n must be between 0 and 40\n");
      return 1;
   }
   
   printf("How many numbers you are willing to search?:\n");
   scanf("%d", &s);

   if (s <= 0) {
      printf("The number of searches s must be greater than 0\n");
      return 1;
   }
   
   ind = (int *)malloc(sizeof(int) * s);
   if (!ind) {
      perror("array allocation failed");
      exit(1);
   }
   
   for (int i = 0; i < s; i++) {
      int ix;
      printf("Enter search %d:\n", i + 1);
      scanf("%d", &ix);
      ind[i] = ix;
   }
   
   pthread_create(&t1, NULL, fib_seq, &n);
   pthread_join(t1, NULL);
   
   for (int i = 0; i <= n; i++) {
      printf("a[%d] = %d\n", i, fib[i]);
   }
   
   void *args[] = {&n, &s};
   pthread_create(&t2, NULL, fib_val, args);
   pthread_join(t2, NULL);
   
   free(ind);
   free(fib);
   
   return 0;
}