#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define HOMEWORK_SIZE 80

char* homework;

void do_maths() {
	char number[8];
	int x, y;

	printf("Input number x? ");
	read(0, number, sizeof(number));
	x = atoi(number);

	puts("Let y = 1337");
	y = 1337;

	switch (rand() & 3) {
	case 0:
		printf("x + y = %d\n", x + y);
		break;
	case 1:
		printf("x - y = %d\n", x - y);
		break;
	case 2:
		printf("x * y = %d\n", x * y);
		break;
	case 3:
		printf("x ** y = %d\n", (int) pow(x, y));
		break;
	default:
		puts("Unknown operation");
	}
}

void do_history() {
	homework = (char*) malloc(HOMEWORK_SIZE);
	printf("What's your task about? ");
	read(0, homework, HOMEWORK_SIZE);
	puts("Interesting, so do you like it? [y/n]");

	switch (getchar()) {
	case 'y':
		puts("Alright");
		break;
	case 'n':
		puts("Then, let's forget about it");
		free(homework);
		break;
	default:
		puts("This is History, not Quantum Physics...");
		exit(1);
	}
}

void do_pwn() {
	puts("I hate history, let's have fun!");
	read(0, homework, HOMEWORK_SIZE);
	puts("That sounds great!");
}

int menu() {
	int option;

	setbuf(stdout, NULL);

	puts("What should I do?");
	puts("1. Maths\n2. History\n3. Pwn\n4. Exit");
	printf("> ");
	scanf("%d", &option);
	getchar();

	return option;
}

int main() {
	int i;

	srand(time(0));
	puts("Margot has a lot of homework to do, so I wrote a program to help her");

	for (;;) {
		switch (menu()) {
		case 1:
			do_maths();
			break;
		case 2:
			do_history();
			break;
		case 3:
			do_pwn();
			break;
		default:
			puts("Well done! You finished");
		}
	}

	return 0;
}
