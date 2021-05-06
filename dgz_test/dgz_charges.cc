#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>

void get_charges(const char* filename) {
	// read in data
	std::ifstream in_file(filename);
	if (!in_file.good()) return;
	else std::cout << "Reading file...\n";

	double dT = 2E-10;
}

int main(int argc, char* argv[]) {
	if (argc <= 1) { return 1; } // check num of args when exec
	else { get_charges(argv[1]); } // call func to calc charges

	return 0;
}
