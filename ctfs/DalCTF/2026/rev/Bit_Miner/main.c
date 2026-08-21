// The storage details are not important for this challenge
// #include "storage.h"
#include <time.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define USERNAME_LENGTH 64
#define PASSWORD_LENGTH 64
#define PATH_LENGTH 96

#define FLAG "fake{not_the_real_flag}"
#define FLAG_PRICE 9999999999999999

typedef struct _Account {
	unsigned long bits;
	unsigned int speed_upgrades;
	unsigned int bonus_upgrades;
	unsigned int bonus_chance_upgrades;
} Account;
extern void storage_init();
extern bool storage_username_sanitized(const char *username);
extern bool storage_user_exists(const char *username);
extern bool storage_check_password(const char *username, const char *password);
extern bool storage_create_user(const char *username, const char *password);
extern Account storage_get_account(const char *username);
extern void storage_save_account(const char *username, Account account);

void welcome();
void login();
int options();
void shop();
void buy(int item, int level, unsigned long price, unsigned long bits);
void mine();

char username[USERNAME_LENGTH];

int main() {
	srand(time(NULL));

	storage_init();

	welcome();

	login(); // Username is now set

	while (true) {
		int option = options();
		switch (option) {
			case 1:
				mine();
				break;
			case 2:
				shop();
				break;
			default:
				printf("Thanks for playing!\n");
				exit(0);
		}
	}
}

void welcome() {
	printf("\t Welcome to...\n\n\n");
	printf(" ___ _ _   __  __ _               \n");
	printf("| _ |_) |_|  \\/  (_)_ _  ___ _ _  \n");
	printf("| _ \\ |  _| |\\/| | | ' \\/ -_) '_|\n");
	printf("|___/_|\\__|_|  |_|_|_||_\\___|_|  \n\n\n"); 
}

void login() {
	while (true) {
		printf("Username: ");
		bool success = fgets(username, USERNAME_LENGTH, stdin);

		if (!success) {
			printf("There was an error reading your username\n");
			continue;
		}

		if (!storage_username_sanitized(username)) {
			printf("Username must be alpha-numeric\n");
			continue;
		}

		if (storage_user_exists(username)) {
			printf("Logging in as \"%s\"\nPassword: ", username);

			char password[PASSWORD_LENGTH];
			success = fgets(password, PASSWORD_LENGTH, stdin);

			if (!success) {
				printf("There was an error reading your password\n");
				continue;
			}

			if (storage_check_password(username, password)) {
				break;
			}

			printf("Wrong password\n");
			continue;
		}

		printf("Registering as \"%s\"\nPassword: ", username);

		char password[PASSWORD_LENGTH];
		success = fgets(password, PASSWORD_LENGTH, stdin);

		if (!success) {
			printf("There was an error reading your password\n");
			continue;
		}

		if (!storage_create_user(username, password)) {
			printf("Failed to create user \"%s\"\n", username);
			continue;
		}

		break;
	}
}

int options() {
	char option_chr = 'X';

	while (option_chr < '1' || option_chr > '3') {
		printf("Options:\n\tMine (1)\n\tShop (2)\n\tExit (3)\n\nOption: ");
		
		do {
			option_chr = fgetc(stdin);
		} while (option_chr <= ' ');
	}

	return (int)(option_chr - '0');
}

void shop() {
	int MAX_LEVEL = 20;
	Account account = storage_get_account(username);

	long speed_cost = 10, bonus_cost = 10, bonus_chance_cost = 10;
	for (int i = 0; i < account.speed_upgrades; i++) {
		speed_cost *= 2;
	}
	for (int i = 0; i < account.bonus_upgrades; i++) {
		bonus_cost *= 2;
	}
	for (int i = 0; i < account.bonus_chance_upgrades; i++) {
		bonus_chance_cost *= 2;
	}

	printf("Welcome to the shop!\n\n");
	printf("Balance: %lu bits\n\n", account.bits);
	printf("Choose what you'd like to buy:\n");
	if (account.speed_upgrades < MAX_LEVEL) {
		printf("\tSpeed Upgrade        (level %d): %18lu bits (1)\n", account.speed_upgrades + 1, speed_cost);
	}
	if (account.bonus_upgrades < MAX_LEVEL) { 
		printf("\tBonus Upgrade        (level %d): %18lu bits (2)\n", account.bonus_upgrades + 1, bonus_cost);
	}
	if (account.bonus_chance_upgrades < MAX_LEVEL) {
		printf("\tBonus Chance Upgrade (level %d): %18lu bits (3)\n", account.bonus_chance_upgrades + 1, bonus_chance_cost);
	}
	printf("\tFlag                          : %18lu bits (4)\n", FLAG_PRICE);
	printf("\tExit (5)\n\n");

	char option_chr = 'X';
	while (option_chr < '1' || option_chr > '5') {
		printf("Option: ");
		
		do {
			option_chr = fgetc(stdin);
		} while (option_chr <= ' ');
	}

	int option = option_chr - '0';

	switch (option) {
		case 1:
			if (account.speed_upgrades >= MAX_LEVEL) {
				printf("Speed Upgrade already maxed out\n");
				return;
			}
			buy(1, account.speed_upgrades + 1, speed_cost, account.bits);
			break;
		case 2:
			if (account.bonus_upgrades >= MAX_LEVEL) {
				printf("Bonus Upgrade already maxed out\n");
				return;
			}
			buy(2, account.bonus_upgrades + 1, bonus_cost, account.bits);
			break;
		case 3:
			if (account.bonus_chance_upgrades >= MAX_LEVEL) {
				printf("Bonus Change Upgrade already maxed out\n");
				return;
			}
			buy(3, account.bonus_chance_upgrades + 1, bonus_chance_cost, account.bits);
			break;
		case 4:
			buy(4, 0, FLAG_PRICE, account.bits);
			break;
		case 5:
			return;
	}
}

void buy(int item, int level, unsigned long price, unsigned long bits) {
	if (price > bits) {
		printf("You don't have enough money for this item\n");
		return;
	}

	char option_chr = 'X';
	while (option_chr != 'y' && option_chr != 'n') {
		printf("Confirm purchase (y / n): ");
	
		do {
			option_chr = fgetc(stdin);
		} while (option_chr <= ' ');
	} 

	if (option_chr == 'n') {
		return;
	}

	Account account = storage_get_account(username);

	switch (item) {
		case 1:
			account.speed_upgrades = level;
			break;
		case 2:
			account.bonus_upgrades = level;
			break;
		case 3:
			account.bonus_chance_upgrades = level;
			break;
		case 4:
			printf("Flag: %s\n", FLAG);
			break;
	}

	account.bits -= price;

	storage_save_account(username, account);
}

void mine() {
	Account account = storage_get_account(username);
	int mine_time = (300000 * (10 + account.speed_upgrades) / (1 + account.speed_upgrades)) / 5;
	int bonus_amount = 2 + account.bonus_upgrades * 2;
	double bonus_chance = (double)(1 + account.bonus_chance_upgrades) / (double)(6 + account.bonus_chance_upgrades);

	printf("Mining");

	for (int i = 0; i < 5; i++) {
		printf(".");
		usleep(mine_time);
	}
	printf("\n");

	bool got_bonus = ((double)rand() / (double)RAND_MAX) <= bonus_chance;

	if (got_bonus) {
		printf("Bonus! +%d bits\n", bonus_amount);
		account.bits += bonus_amount;
	} else {
		printf("+1 bit\n\n");
		account.bits++;
	}

	storage_save_account(username, account);
}
