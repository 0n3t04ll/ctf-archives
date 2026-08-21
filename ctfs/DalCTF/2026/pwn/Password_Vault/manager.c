#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LOGINS 8

typedef struct {
    void (*can_check)(void);
    char  username[12];
    char  password[12];
} Login;

static Login *logins[MAX_LOGINS];

static char  *pwd_buf  = NULL;
static size_t pwd_size = 0;

static void read_master_key(void)
{
    puts("\n[*] Reading master key...");
    FILE *f = fopen("flag.txt", "r");
    if (!f) { puts("flag.txt not found — create it for testing"); return; }
    char buf[64];
    fgets(buf, sizeof(buf), f);
    fclose(f);
    printf("[+] Master key: %s\n", buf);
}

static void access_denied(void)
{
    puts("[!] Access denied — You don't have the master key.");
}

static int read_int(const char *p)
{
    printf("%s", p); 
    fflush(stdout);

    int v; 
    if (scanf("%d", &v) != 1) exit(1);
    getchar();

    return v;
}

static check_slot_taken(int i){
    if (i < 0 || i >= MAX_LOGINS) { 
      puts("  bad slot"); 
      return 0; 
    }
    if (logins[i]){ 
      puts("  slot taken"); 
      return 0;
    }
    return 1;
}

static check_slot_empty(int i){
    if (i < 0 || i >= MAX_LOGINS) { 
      puts("  bad slot"); 
      return 0; 
    }
    if (!logins[i]){ 
      puts("  slot empty"); 
      return 0;
    }
    return 1;
}

static void new_login(void)
{
    int i = read_int("  slot [0-7]: ");
    if(!check_slot_taken(i)) return;

    Login *l = malloc(sizeof(Login));
    l->can_check = access_denied;

    printf("  username: "); fflush(stdout);
    fgets(l->username, sizeof(l->username), stdin);
    l->username[strcspn(l->username, "\n")] = '\0';

    printf("  password: "); fflush(stdout);
    fgets(l->password, sizeof(l->password), stdin);
    l->password[strcspn(l->password, "\n")] = '\0';

    logins[i] = l;
    printf("  [+] login for '%s' saved in slot %d\n", l->username, i);
}

static void delete_login(void)
{
    int i = read_int("  slot [0-7]: ");
    if(!check_slot_empty(i)) return;
    printf("  [-] deleting login for '%s'\n", logins[i]->username);
    free(logins[i]);
}

static void check_master_key(void)
{
    int i = read_int("  slot [0-7]: ");
    if(!check_slot_empty(i)) return;
    logins[i]->can_check(); 
}

static void set_password(void)
{
    if (pwd_buf){ 
      free(pwd_buf); 
      pwd_buf = NULL;
    }

    int size = read_int("  password buffer size: ");
    if (size <= 0 || size > 512) { 
      puts("  bad size"); 
      return; 
    }

    pwd_buf  = malloc((size_t) size);
    pwd_size = (size_t) size;

    printf("  enter password: "); 
    fflush(stdout);
    fread(pwd_buf, 1, pwd_size, stdin);
    puts("  [+] password stored");
}

int main(void)
{
    setvbuf(stdout, NULL, _IONBF, 0);

    puts("=== FFD Password Manager ===");

    int c;
    for (;;) {
        puts("\n  1. new login");
        puts("  2. delete login");
        puts("  3. set password");
        puts("  4. check master key");
        puts("  0. quit");
        printf("  > "); fflush(stdout);

        if (scanf("%d", &c) != 1) break;
        getchar();

        switch (c) {
            case 0: return 0;
            case 1: new_login();       break;
            case 2: delete_login();    break;
            case 3: set_password();    break;
            case 4: check_master_key(); break;
            default: puts("  unknown option");
        }
    }
}
