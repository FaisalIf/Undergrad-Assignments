#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <semaphore.h>
#include <time.h>

#define CHAIRS 3
#define STUDENTS 10

pthread_mutex_t mutex;
sem_t st_sleep;
sem_t student_sem;
int waiting = 0;
int served = 0;
int done = 0;

void* student(void* num) {
   int id = *(int*)num;
   usleep((rand()%500+100)*1000);
   pthread_mutex_lock(&mutex);
   if (waiting < CHAIRS) {
      waiting++;
      printf("Student %d started waiting for consultation\n", id);
      sem_post(&student_sem);
      pthread_mutex_unlock(&mutex);
      sem_wait(&st_sleep);
      printf("Student %d is getting consultation\n", id);
      usleep((rand()%300+100)*1000);
      printf("Student %d finished getting consultation and left\n", id);
      pthread_mutex_lock(&mutex);
      served++;
      printf("Number of served students: %d\n", served);
      pthread_mutex_unlock(&mutex);
   } else {
      printf("No chairs remaining in lobby. Student %d Leaving.....\n", id);
      pthread_mutex_unlock(&mutex);
   }
   return NULL;
}

void* tutor(void* arg) {
   while (1) {
      sem_wait(&student_sem);
      pthread_mutex_lock(&mutex);
      if (done && waiting == 0) {
         pthread_mutex_unlock(&mutex);
         break;
      }
      if (waiting > 0) {
         waiting--;
         printf("A waiting student started getting consultation\n");
         printf("Number of students now waiting: %d\n", waiting);
         printf("ST giving consultation\n");
         sem_post(&st_sleep);
      }
      pthread_mutex_unlock(&mutex);
   }
   return NULL;
}

int main() {
   pthread_t stid;
   pthread_t sids[STUDENTS];
   int ids[STUDENTS];
   srand(time(NULL));
   pthread_mutex_init(&mutex, NULL);
   sem_init(&st_sleep, 0, 0);
   sem_init(&student_sem, 0, 0);
   pthread_create(&stid, NULL, tutor, NULL);
   for (int i = 0; i < STUDENTS; i++) {
      ids[i] = i;
      pthread_create(&sids[i], NULL, student, &ids[i]);
   }
   for (int i = 0; i < STUDENTS; i++)
      pthread_join(sids[i], NULL);
   pthread_mutex_lock(&mutex);
   done = 1;
   pthread_mutex_unlock(&mutex);
   sem_post(&student_sem);
   pthread_join(stid, NULL);
   pthread_mutex_destroy(&mutex);
   sem_destroy(&st_sleep);
   sem_destroy(&student_sem);
   return 0;
}