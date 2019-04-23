// USAGE:
//  cc -o exec-as exec-as.c
//  exec-as <uid> <gid> <pwd> <cmd> [<args>]
//
// Why did I write my own (primitive) version of su?
// . su does not do 'exec' and 'chdir' together
// . enabling job control in the final user is a nightmare!
// . the final executable is just 8kB
// . helped me learn some aspect of low-level routines in linux :)
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <err.h>
int main(int argc, char** argv) {
    int uid, gid;
    char *dir, **cmd;
    uid = atoi(argv[1]);
    gid = atoi(argv[2]);
    dir = argv[3];
    cmd = &(argv[4]);
    if(setgid(gid) < 0)
        err(-1, "setgid(%i)", gid);
    if(setuid(uid) < 0)
        err(-2, "setuid(%i)", uid);
    if(chdir(dir) < 0)
        err(-3, "chdir(%s)", dir);
    execvp(cmd[0], cmd);
    err(-4, "%s", cmd[0]);
    // typically should not reach here!
    return -5;
}
