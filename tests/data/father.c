#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
	char *args[] = {
		"child",
		NULL,
	};
	int status;
	pid_t pid;

	if (argc != 2) {
		fprintf(stderr, "Usage: father <path to child program>\n");
		return 1;
	}

	printf("I am the High-Father\n");

	pid = fork();

	switch (pid) {

	case 0:
		if (execv(argv[1], args) == -1) {
			perror("Failed to execute child");
			exit(255);
		}
		break;

	case -1:
		perror("Error trying to fork");
		return 2;
		break;

	default:
		if (wait(&status) == -1) {
			perror("Error waiting for child");
			return 3;
		}

		if (WIFEXITED(status)) {
			printf("Child exited with code %d\n",
			       WEXITSTATUS(status));
		}

		if (WIFSIGNALED(status)) {
			printf("Child terminated by signal %d\n",
			       WTERMSIG(status));
		}
		break;
	}

	return 0;
}
