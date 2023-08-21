#include <stdio.h>

// gcc -std=c99 -Wall -Wextra -Wpedantic example.c -o example && ./example

int main (int argc, char** argv) {
	(void)(argc); (void)(argv); // get rid of "unused" warning

	printf("<%d>\n", '*');
	char str[5] = {0x50,0x65,0x72,0x6C,0};
	printf("<%s>\n",str);

	return 0;
}
