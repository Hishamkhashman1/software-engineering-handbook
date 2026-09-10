#include <stdio.h>

// // this is a global variable
// int global_variable = 26;
//
// int main() {
// 	{
// 	printf("Hello, World!"); // making a one liner comment
// 	int programmer_age = 39; // loacl variable
//
// 	printf("\n%d\n", programmer_age);
//
// 	char programmer_name[] = "Hisham";
//
//
// 	printf("\n%s\n", programmer_name);
//
// 	long id_number = 1980003456;
//
// 	printf("\n%ld\n", id_number);
//
// 	float pi_var = 3.14159265358979;
//
// 	printf("\n%f\n", pi_var);
//
// 	char gender = 'M';
//
// 	printf("\n%c\n", gender);
//
// 	_Bool is_active_programmer = 1; // bool is obviously true or false from boolean .. but truthy and falsy are binary lol 0 false 1 true treated as %d
//
// 	printf("\n%d\n", is_active_programmer);
// 	return 0; /* making a multiliner
// 		     comment */
// 	}

int main() {
	 int nums[6];
	 nums[0] = 1;
	 nums[1] = 1;
	 nums[2] = 1;
	 nums[3] = 4;
	 nums[4] = 2;
	 nums[5] = 2;

	 for (int i = 0; i < 6; i++) {
		 printf("nums[%d] = %d\n",i, nums[i]);
	 }
	 return 0;

}
