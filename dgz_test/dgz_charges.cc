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
    if (!in_file.good()) return;
    else std::cout << "Reading file...\n";

//    std::string string_dummy;
//    for (size_t i = 0; i < 7; ++i)
//    {
//        if (i == 0)
//        {
//            std::getline(in_file, string_dummy, ' ');
//        }
//    }

    size_t record_length = 1030;

    std::cout << "Integrating pulses...\n";

    // initialize variables
    std::vector<double> charges; // Coulombs
    std::vector<double> voltages; // V
    double voltage = 0.;
    size_t frame_counter = 0;
    double voltage_sum = 0.;

    while (in_file >> voltage)
    {
        
    }
}
