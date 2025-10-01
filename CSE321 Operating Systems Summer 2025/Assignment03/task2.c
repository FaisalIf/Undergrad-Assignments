#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>
#include <sys/wait.h>

struct msg {
    long int type;
    char txt[6];
};

int main() {
    key_t key;
    int msgid;
    struct msg message;

    key = ftok("progfile", 65);
    msgid = msgget(key, 0666 | IPC_CREAT);
    if (msgid < 0) {
        perror("msgget");
        exit(1);
    }

    char workspace[20];
    printf("Please enter the workspace name:\n");
    scanf("%s", workspace);

    if (strcmp(workspace, "cse321") != 0) {
        printf("Invalid workspace name\n");
        msgctl(msgid, IPC_RMID, NULL);
        exit(0);
    }

    message.type = 1;  
    strcpy(message.txt, workspace);
    msgsnd(msgid, &message, sizeof(message.txt), 0);
    printf("Workspace name sent to otp generator from log in: %s\n", workspace);

    pid_t pid = fork();

    if (pid == 0) {
        msgrcv(msgid, &message, sizeof(message.txt), 1, 0);
        printf("OTP generator received workspace name from log in: %s\n", message.txt);

        int otp = getpid();
        sprintf(message.txt, "%d", otp);

        message.type = 2;
        msgsnd(msgid, &message, sizeof(message.txt), 0);
        printf("OTP sent to log in from OTP generator: %s\n", message.txt);

        message.type = 3;
        msgsnd(msgid, &message, sizeof(message.txt), 0);
        printf("OTP sent to mail from OTP generator: %s\n", message.txt);

        pid_t pid2 = fork();

        if (pid2 == 0) {
            msgrcv(msgid, &message, sizeof(message.txt), 3, 0);
            printf("Mail received OTP from OTP generator: %s\n", message.txt);

            message.type = 4;
            msgsnd(msgid, &message, sizeof(message.txt), 0);
            printf("OTP sent to log in from mail: %s\n", message.txt);

            exit(0);
        } else {
            wait(NULL);
            exit(0);
        }
    }
    else {
        wait(NULL);

        msgrcv(msgid, &message, sizeof(message.txt), 2, 0);
        char otp_from_gen[6];
        strcpy(otp_from_gen, message.txt);
        printf("Log in received OTP from OTP generator: %s\n", otp_from_gen);

        msgrcv(msgid, &message, sizeof(message.txt), 4, 0);
        char otp_from_mail[6];
        strcpy(otp_from_mail, message.txt);
        printf("Log in received OTP from mail: %s\n", otp_from_mail);

        if (strcmp(otp_from_gen, otp_from_mail) == 0) {
            printf("OTP Verified\n");
        } else {
            printf("OTP Incorrect\n");
        }

        msgctl(msgid, IPC_RMID, NULL);
    }

    return 0;
}
