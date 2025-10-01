#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/wait.h>

struct shared {
    char sel[100];
    int b;
};

int main() {
    int shmid, fd[2];
    char buffer[100];
    pid_t pid;

    shmid = shmget(IPC_PRIVATE, sizeof(struct shared), IPC_CREAT | 0666);
    if (shmid < 0) {
        perror("shmget");
        exit(1);
    }

    struct shared *sh = (struct shared *) shmat(shmid, NULL, 0);
    if (sh == (void *) -1) {
        perror("shmat");
        exit(1);
    }

    if (pipe(fd) == -1) {
        perror("pipe");
        exit(1);
    }

    printf("Provide Your Input From Given Options:\n");
    printf("1. Type a to Add Money\n");
    printf("2. Type w to Withdraw Money\n");
    printf("3. Type c to Check Balance\n");

    scanf("%s", sh->sel);
    sh->b = 1000;

    printf("Your selection: %s\n", sh->sel);

    pid = fork();

    if (pid == 0) {
        if (strcmp(sh->sel, "a") == 0) {
            int amt;
            printf("Enter amount to be added:\n");
            scanf("%d", &amt);
            if (amt > 0) {
                sh->b += amt;
                printf("Balance added successfully\n");
                printf("Updated balance after addition:\n%d\n", sh->b);
            } else {
                printf("Adding failed, Invalid amount\n");
            }
        }
        else if (strcmp(sh->sel, "w") == 0) {
            int amt;
            printf("Enter amount to be withdrawn:\n");
            scanf("%d", &amt);
            if (amt > 0 && amt < sh->b) {
                sh->b -= amt;
                printf("Balance withdrawn successfully\n");
                printf("Updated balance after withdrawal:\n%d\n", sh->b);
            } else {
                printf("Withdrawal failed, Invalid amount\n");
            }
        }
        else if (strcmp(sh->sel, "c") == 0) {
            printf("Your current balance is:\n%d\n", sh->b);
        }
        else {
            printf("Invalid selection\n");
        }

        close(fd[0]);
        write(fd[1], "Thank you for using", 20);
        close(fd[1]);

        shmdt(sh);
        exit(0);
    }
    else {
        wait(NULL);

        close(fd[1]);
        read(fd[0], buffer, sizeof(buffer));
        close(fd[0]);

        printf("%s\n", buffer);

        shmdt(sh);
        shmctl(shmid, IPC_RMID, NULL);
    }

    return 0;
}