#include <stdio.h>

int main() {
	char FLAG[] = "DalCTF{test}";
	


	float fflag[sizeof(FLAG)];
	long lflag[sizeof(fflag)];

	int x = sizeof(FLAG);

	for(int i=0;i<x;i++){
	fflag[i] = (float) FLAG[i];
	fflag[i] = fflag[i] * fflag[i];
	// man I forgot what line needs to go here... Maybe I should play some quake to think about it
	}

	x = x - 1;

	for(int i=0;i<x;i++){
	printf("\n%d", lflag[i]);
	};

	return 0;
}
