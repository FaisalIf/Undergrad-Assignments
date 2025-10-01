#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_USERS 5
#define MAX_RESOURCES 5
#define MAX_NAME_LEN 20


typedef enum{ 
    READ = 1,    
    WRITE = 2,   
    EXECUTE = 4  
} Permission;


typedef struct{
    char name[MAX_NAME_LEN];
} User;

typedef struct{
    char name[MAX_NAME_LEN];
} Resource;


typedef struct{
    char userName[MAX_NAME_LEN];
    int permissions; 
} ACLEntry;


typedef struct{
    Resource resource;
    ACLEntry acl[MAX_USERS];
    int aclCount;
} ACLControlledResource;


typedef struct{
    char resourceName[MAX_NAME_LEN];
    int permissions; 
} Capability;


typedef struct{
    User user;
    Capability capabilities[MAX_RESOURCES];
    int capabilityCount;
} CapabilityUser;





void printPermissions(int perm){
    if (perm & READ) printf("READ ");
    if (perm & WRITE) printf("WRITE ");
    if (perm & EXECUTE) printf("EXECUTE ");
}


int hasPermission(int userPerm, int requiredPerm){
    return (userPerm & requiredPerm) == requiredPerm;
}

void addACLEntry(ACLControlledResource *res, const char *userName, int permissions) {
    if (res->aclCount < MAX_USERS) {
        strcpy(res->acl[res->aclCount].userName, userName);
        res->acl[res->aclCount].permissions = permissions;
        res->aclCount++;
    }
}

void addCapability(CapabilityUser *user, const char *resourceName, int permissions) {
    if (user->capabilityCount < MAX_RESOURCES) {
        strcpy(user->capabilities[user->capabilityCount].resourceName, resourceName);
        user->capabilities[user->capabilityCount].permissions = permissions;
        user->capabilityCount++;
    }
}


void checkACLAccess(ACLControlledResource *res, const char *userName, int perm){
    printf("ACL Check: User %s requests ", userName);
    printPermissions(perm);
    printf("on %s: ", res->resource.name);

    for (int i = 0; i < res->aclCount; i++) {
        if (strcmp(res->acl[i].userName, userName) == 0) {
            if (hasPermission(res->acl[i].permissions, perm)) {
                printf("Access GRANTED\n");
            } else {
                printf("Access DENIED\n");
            }
            return;
        }
    }
    printf("NO entry for resource %s: Access DENIED\n", res->resource.name);
}

void checkCapabilityAccess(CapabilityUser *user, const char *resourceName, int perm){
    printf("Capability Check: User %s requests ", user->user.name);
    printPermissions(perm);
    printf("on %s: ", resourceName);

    for (int i = 0; i < user->capabilityCount; i++) {
        if (strcmp(user->capabilities[i].resourceName, resourceName) == 0) {
            if (hasPermission(user->capabilities[i].permissions, perm)) {
                printf("Access GRANTED\n");
            } else {
                printf("Access DENIED\n");
            }
            return;
        }
    }
    printf("NO capability for %s: Access DENIED\n", resourceName);
}


int main(){
    User users[MAX_USERS] = {{"Alice"}, {"Bob"}, {"Charlie"}, {"David"}, {"Eve"}};
    Resource resources[MAX_RESOURCES] = {{"File1"}, {"File2"}, {"File3"}, {"Database"}, {"Printer"}};
    ACLControlledResource aclResources[MAX_RESOURCES];
    for (int i = 0; i < MAX_RESOURCES; i++) {
        aclResources[i].resource = resources[i];
        aclResources[i].aclCount = 0;
    }

    addACLEntry(&aclResources[0], "Alice", READ | WRITE); 
    addACLEntry(&aclResources[0], "Bob", READ);          
    addACLEntry(&aclResources[1], "Charlie", READ | EXECUTE); 
    addACLEntry(&aclResources[3], "Alice", READ | WRITE); 
    addACLEntry(&aclResources[3], "David", READ);          
    addACLEntry(&aclResources[4], "Eve", WRITE);         
    CapabilityUser capUsers[MAX_USERS];
    for(int i = 0; i < MAX_USERS; i++) {
        capUsers[i].user = users[i];
        capUsers[i].capabilityCount = 0;
    }
    addCapability(&capUsers[0], "File1", READ | WRITE);    
    addCapability(&capUsers[0], "Database", READ | WRITE); 
    addCapability(&capUsers[1], "File1", READ);             
    addCapability(&capUsers[2], "File2", READ | EXECUTE);    
    addCapability(&capUsers[3], "Database", READ);          
    addCapability(&capUsers[4], "Printer", WRITE);          

    printf("--- ACL Tests ---\n");
    checkACLAccess(&aclResources[0], "Alice", READ);
    checkACLAccess(&aclResources[0], "Bob", WRITE);
    checkACLAccess(&aclResources[0], "Charlie", READ);
    checkACLAccess(&aclResources[3], "David", READ);
    checkACLAccess(&aclResources[3], "David", WRITE);
    checkACLAccess(&aclResources[4], "Eve", WRITE);
    checkACLAccess(&aclResources[4], "Alice", WRITE);
    checkACLAccess(&aclResources[1], "Charlie", EXECUTE);
    checkACLAccess(&aclResources[1], "Charlie", READ | EXECUTE);
    printf("\n");

    printf("--- Capability Tests ---\n");
    checkCapabilityAccess(&capUsers[0], "File1", WRITE);
    checkCapabilityAccess(&capUsers[1], "File1", WRITE);
    checkCapabilityAccess(&capUsers[2], "File2", EXECUTE);
    checkCapabilityAccess(&capUsers[3], "Database", READ);
    checkCapabilityAccess(&capUsers[3], "Database", WRITE);
    checkCapabilityAccess(&capUsers[4], "Printer", WRITE);
    checkCapabilityAccess(&capUsers[0], "Printer", READ);
    checkCapabilityAccess(&capUsers[2], "File2", READ | WRITE);
    checkCapabilityAccess(&capUsers[0], "Database", READ | WRITE);
    return 0;
}