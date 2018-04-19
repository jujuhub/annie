#include <TFile.h>
#include <TH1.h>
#include <TGraph.h>
#include <TSystemDirectory.h>
#include <TSystemFile.h>
#include <TSystem.h>

#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>
#include <vector>

TGraph* plot_spectrum(const char* filename)
{
  std::ifstream infile(filename);

  std::string line, title;
  std::vector<double> xs;
  std::vector<double> ys;

  // Use the first line as the TGraph title
  std::getline(infile, title);

  //Get the x and y axis labels
  std::getline(infile, line);
  std::istringstream iss(line);
  std::vector<std::string> axis_labels;
  std::string dummy;
  while (std::getline(iss, dummy, ','))
    axis_labels.push_back(dummy);

  while (std::getline(infile, line))
  {
    // get x and y values from the current line
    std::istringstream iss(line);
    double x = 0.;
    double y = 0.;
    bool stored_x = false;
    bool stored_y = false;
    double num = 0.;
    while (std::getline(iss, dummy, ',') && std::istringstream(dummy) >> num)
    {
      if (!stored_x) { x = num; stored_x = true; }
      else if (!stored_y) { y = num; stored_y = true; }
    }

    if (stored_x && stored_y) 
    {
      xs.push_back(x);
      ys.push_back(y);
    }
  }

  TGraph* tg = new TGraph(xs.size(), &(xs.front()), &(ys.front()));
  tg->SetNameTitle(TString(title), (title + ";" + axis_labels.at(0) + ";" + axis_labels.at(1)).c_str());

  for (size_t i = 0; i < xs.size(); ++i)
    { tg->SetPoint(i, xs.at(i), ys.at(i)); }

  tg->GetXaxis()->SetTitle("wavelength [nm]");
  tg->GetYaxis()->SetTitle("absorption");

  return tg;
}

double abs_at_wavelength(const char* filename, const double* wavelength)
{
  std::ifstream infile(filename);

  std::string line, title;
  std::vector<double> xs;
  std::vector<double> ys;

  // Use the first line as TGraph title
  std::getline(infile, title);

  // Get the x and y axis labels
  std::getline(infile, line);
  std::istringstream iss(line);
  std::vector<std::string> axis_labels;
  std::string dummy;
  while (std::getline(iss, dummy, ','))
    { axis_labels.push_back(dummy); }

  while (std::getline(infile, line))
  {
    // get x and y values from current line
    std::istringstream iss(line);
    double x = 0.;
    double y = 0.;
    bool stored_x = false;
    bool stored_y = false;
    double num = 0.;
    while (std::getline(iss, dummy, ',') && std::istringstream(dummy) >> num)
    {
      if (!stored_x) { x = num; stored_x = true; }
      else if (!stored_y) { y = num; stored_y = true; }
    }

    if (stored_x && stored_y) {
      xs.push_back(x);
      ys.push_back(y);
    }
  }

  // return absorption value at specified wavelength
  return tg->Eval(wavelength);
}

void abs_level()
{
  // pseudocode
  // look through all Gd_testing directories and finds ".txt" files matching
  // filename endings listed in another .txt file
  // for each ending:
  // load the file, call on abs_at_wavelength (need to ask for user input),
  // make a plot of all the abs values


  TFile g("ALL_SPECTRA.root", "RECREATE");
  int valid_files_counter = 0;
  int color_counter = 0;

  // Look for every ".txt" file in the weekly Gd testing directories, making a plot for each

  TSystemDirectory dir(gSystem->pwd(), gSystem->pwd());
  for (Int_t i = 0; dir.GetListOfFiles()->GetEntries(); ++i)
  {
    std::string filename = (dynamic_cast<TSystemFile*>(dir.GetListOfFiles()->At(i)))->GetName();
    if (filename.length() > 9 && filename.substr(filename.length() - 11) == "_liners.txt")
    {
      valid_files_counter++;
      TGraph* tg = plot_spectrum(filename.c_str());
      

      if (valid_files_counter != 10 && valid_files_counter != 0) {
        color_counter = valid_files_counter; }
      else { color_counter = valid_files_counter + 51; }

      tg->SetLineColor(color_counter);
      tg->Write();
    }
  }

  g.Close();
}
