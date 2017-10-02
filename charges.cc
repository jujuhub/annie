#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

constexpr double PEAK_VOLTAGE = 0.080; // V
constexpr double IMPEDANCE = 50.; // Ohms

// The oscilloscope waveform CSV files have 7 header rows.
// We'll extract the sampling time interval from one of them while
// skipping the other information.
constexpr size_t SKIP_ROWS = 7;
// Index of the row on which the sampling time interval is given as
// the second entry
constexpr size_t TIME_INTERVAL_ROW = 1;
// Initialize the sampling interval dT to something silly in case we fail to
// read it
constexpr double BOGUS_dT = -9999.;

void get_charges(const char* filename) {
  std::ifstream in_file(filename);
  if (!in_file.good()) return;
  else std::cout << "Reading file...\n";

  double dT = BOGUS_dT;

  char dummy; // used to skip commas in the CSV file
  std::string string_dummy; // used to skip header rows
  for (size_t i = 0; i < SKIP_ROWS; ++i) {
    if (i == TIME_INTERVAL_ROW) {
      // ignore the line up until the first comma
      std::getline(in_file, string_dummy, ',');
      // get the sampling interval from the next entry
      in_file >> dT;
      if (dT == BOGUS_dT) {
        std::cerr << "Data format error. Could not"
          << " read sampling time interval from CSV file. Aborting...\n";
        return;
      }
      else {
        std::cout << "Sampling interval = " << dT << " s\n";
      }

      // ignore the rest of the line
      std::getline(in_file, string_dummy);
    }
    else {
      // ignore the whole line
      std::getline(in_file, string_dummy);
    }
  }

  std::cout << "Creating charge distributions...\n";

  // initialize variables
  std::vector<double> charges; // Coulombs
  std::vector<double> pulse_heights; // V
  std::vector<double> voltages; // V
  double time = 0.;
  double voltage = 0.;
  double min_voltage = 1e30;
  size_t frame_counter = 0;

  double old_time = -1e30;
  double voltage_sum = 0.;

  while (in_file >> dummy >> dummy >> dummy >> time >> dummy >> voltage) {
    // If we're not at the end of the frame
    if (time > old_time) {
      voltage_sum += voltage; // add to the area of the frame
      voltages.push_back(voltage);
      if (voltage < min_voltage) min_voltage = voltage;
      old_time = time;
    }
    // We're at the end of the frame
    else {
      bool skip_frame = false; // initialize skip frame flag
      ++frame_counter;

      // sum pedestal over first 5% of the frame
      double pedestal = 0.;
      double DC = 0.;
      size_t num_pedestal_samples = voltages.size() / 20;
      for (size_t k = 0; k < num_pedestal_samples; ++k) {

        DC = (k*DC + voltages.at(k)) / (k + 1.);

        // Check for any voltages past threshold
        if (std::abs(voltages.at(k+1) - DC) > PEAK_VOLTAGE) {
          // Skip the entire frame
          skip_frame = true;
        }
        else {
          // If there are no peaks this early, add to the pedestal
          pedestal += voltages.at(k);
        }
      }

      // Scale pedestal to full frame width
      pedestal *= 20;
      // voltages.size() / static_cast<double>(num_pedestal_samples);

      if (skip_frame) {
        std::cout << "skipped frame: " << frame_counter + 1 << '\n';
      }
      else {
        // store the pulse's charge in Coulombs
        charges.push_back( (-(voltage_sum - pedestal) * dT) / IMPEDANCE);
      }

      // Prepare for the next frame
      old_time = time;
      voltages.clear();
      voltages.push_back(voltage);
      voltage_sum = 0.;

      pulse_heights.push_back(-min_voltage);
      min_voltage = 1e30;
    }
  }

  std::ofstream out_file("my_charges.txt");
  for (auto q : charges) out_file << q << '\n';
  out_file.close();

  std::ofstream out_file2("my_pulse_heights.txt");
  for (auto h : pulse_heights) out_file2 << h << '\n';
  out_file2.close();
}

int main(int argc, char* argv[]) {
  if (argc <= 1) return 1;
  else get_charges(argv[1]);
  return 0;
}
