#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

constexpr double PEAK_VOLTAGE = 0.050; // V
constexpr double IMPEDANCE = 50.; // Ohms
constexpr double dT = 2.E-9; // s ; fixed sampling interval

// Each event will have 7 rows of header info
// We can get the record length from the first row
constexpr size_t REC_LEN_ROW = 0;

void get_data(const char* filename)
{
    std::ifstream in_file(filename);
    
}
