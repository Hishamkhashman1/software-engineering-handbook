#include <stdio.h>

int main() {
	printf("Hello, World!"); // making a one liner comment
	int programmer_age = 39;

	printf("\n%d\n", programmer_age);

	char programmer_name[] = "Hisham";


	printf("\n%s\n", programmer_name);

	long id_number = 1980003456;

	printf("\n%ld\n", id_number);

	float pi_var = 3.14159265358979;

	printf("\n%f\n", pi_var);

	char gender = 'M';

	printf("\n%c\n", gender);

	_Bool is_active_programmer = 1; // bool is obviously true or false from boolean .. but truthy and falsy are binary lol 0 false 1 true treated as %d

	printf("\n%d\n", is_active_programmer);
	return 0; /* making a multiliner
		     comment */
}
