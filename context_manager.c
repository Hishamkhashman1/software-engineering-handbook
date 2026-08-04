#include <stdio.h>
#include <stdlib.h>

int main() {
	FILE *f = fopen("/home/hisham/Downloads/Profile.txt", "r"); // r becasue we only want reead mode and FILE *f means we can call the file by f later 

	if (f == NULL) {
		printf("Error: no se puede open dis file. \n");
		return 1; // return 1 because it means it failed
	}

	// now becasue the file is not NULL so here comes the fun part 
	// create a temporary storage (buffer) to hold each line of text
	char buffer[256] // creating storage for 255 chars + 1
	
	// this reads the file line by line fgets()  buffer and size of buffer in the file and not null then print it 
	while (fgets(buffer, sizeof(buffer), f) != NULL) {
		printf("%s", buffer);
	}
	
	// close up the file to free up system memeory (what with does in python) 
	fclose(f);

	return 0;

}
