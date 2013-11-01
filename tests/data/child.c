#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
	printf("I am the child\n");
	sleep(1);
	return 0;
}
