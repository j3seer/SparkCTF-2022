#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

void x(char* s, char k) {
	int i;
	int n;

	n = strlen(s);

	for (i = 0; i < n; i++) {
		s[i] ^= k;
	}
}

int main() {
	char k;
	char data[64];

	setbuf(stdout, NULL);
	srand(time(0));

	for (;;) {
		k = (char) rand() & 0xff;
		printf("Encrypt using key 0x%x: ", k & 0xff);
		read(0, data, 0x64);

		x(data, k);

		if (strcmp(data, "quit") == 0) {
			break;
		}
	
		printf("Result: %s\n", data);
	}

	return 0;
}
