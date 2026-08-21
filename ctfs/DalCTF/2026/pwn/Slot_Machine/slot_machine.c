#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define RESET   "\033[0m"
#define BOLD    "\033[1m"
#define RED     "\033[31m"
#define YELLOW  "\033[33m"
#define GREEN   "\033[32m"
#define CYAN    "\033[36m"
#define MAGENTA "\033[35m"
#define WHITE   "\033[97m"
#define DIM     "\033[2m"

int coins = 1;

void jackpot() {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("flag.txt not found");
        exit(1);
    }
    char flag[64];
    fgets(flag, sizeof(flag), f);
    fclose(f);
    puts("JACKPOT! How could that happen?");
    printf("Flag: %s\n", flag);
}

void help() {
    puts("Commands:");
    puts("  roll   - Start rolling (costs 1 coin)");
    puts("  coins  - Enter more coins");
    puts("  help   - Show this help");
    puts("  exit   - Exit the game");
}

static const char *sym_names[] = { " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 " };
static const char *sym_colors[] = { RED, YELLOW, GREEN, CYAN, MAGENTA, WHITE, YELLOW, CYAN, RED };
#define NUM_SYMS 9

void roll() {
    if (coins <= 0) {
        puts("Not enough coins! Use 'coins' to add more.");
        return;
    }
    coins--;

    // Pick 3 distinct symbols (guaranteed no match)
    int a = rand() % NUM_SYMS;
    int b;
    do { b = rand() % NUM_SYMS; } while (b == a);
    int c;
    do { c = rand() % NUM_SYMS; } while (c == a || c == b);

    const char *sa = sym_names[a], *ca = sym_colors[a];
    const char *sb = sym_names[b], *cb = sym_colors[b];
    const char *sc = sym_names[c], *cc = sym_colors[c];

    puts(DIM "  +---------+---------+---------+" RESET);
    puts(DIM "  |         |         |         |" RESET);
    printf(DIM "  |" RESET "   %s%s%s%s   " DIM "|" RESET
               "   %s%s%s%s   " DIM "|" RESET
               "   %s%s%s%s   " DIM "|" RESET "\n",
        BOLD, ca, sa, RESET,
        BOLD, cb, sb, RESET,
        BOLD, cc, sc, RESET);
    puts(DIM "  |         |         |         |" RESET);
    puts(DIM "  +---------+---------+---------+" RESET);

    printf(RED BOLD "\n  No match. You lose.\n" RESET);
    printf("  Coins remaining: %d\n", coins);
}

void enter_coins() {
    int amount;
    printf("How many coins to insert? ");
    fflush(stdout);
    if (scanf("%d", &amount) != 1 || amount <= 0) {
        puts("Invalid amount.");
    } else {
        coins += amount;
        printf("Inserted %d coin(s). Total: %d\n", amount, coins);
    }
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void game_loop() {
    char cmd[32];

    while (1) {
        printf("\nCoins: %d\n> ", coins);
        fflush(stdout);

        if (!gets(cmd)) break;

        if (strcmp(cmd, "roll") == 0) {
            roll();
        } else if (strcmp(cmd, "coins") == 0) {
            enter_coins();
        } else if (strcmp(cmd, "help") == 0) {
            help();
        } else if (strcmp(cmd, "exit") == 0) {
            puts("Thanks for playing. Goodbye!");
            return;
        } else {
            printf("Unknown command: '%s'\n", cmd);
            puts("Type 'help' to see available commands.");
        }
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);
    srand(time(NULL));

    puts("Welcome to Slot Machine  ");
    printf("You start with %d coin. Good luck!\n", coins);
    puts("Type 'help' for commands.");

    game_loop();
    return 0;
}
