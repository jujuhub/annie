#include <fstream>
#include <sstream>
#include <string>

Double_t grab_abs(const char* filename, double wavelength)
{
  std::ifstream infile(filename);

  std::string line, title;
  std::vector<double> xs;
  std::vector<double> ys;

  // Use the first line as the TGraph title
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
    // get the x and y values from the current line
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

  TGraph* tg = new TGraph(xs.size(), &(xs.front()), &(ys.front()));
  tg->SetNameTitle(TString(title), (title + ";" + axis_labels.at(0) + ";" + axis_labels.at(1)).c_str());

  for (size_t i = 0; i < xs.size(); ++i) {
    tg->SetPoint(i, xs.at(i), ys.at(i));
  }

  tg->GetXaxis()->SetTitle("wavelength [nm]");
  tg->GetYaxis()->SetTitle("absorption");

  Double_t abs = tg->Eval(wavelength);

  return abs;
}

TGraph* abs_v_t()
{
  // Parses every ".txt" file in current directory, making plot of abs over time
  TSystemDirectory dir(gSystem->pwd(), gSystem->pwd());

  TGraph* ag = new TGraph(dir.GetListOfFiles()->GetEntries());

  for (size_t i = 0; i < dir.GetListOfFiles()->GetEntries(); ++i)
  {
    std::string filename = (dynamic_cast<TSystemFile*>(dir.GetListOfFiles()->At(i)))->GetName();
    if (filename.length() > 4 && filename.substr(filename.length() - 9) == "liner.txt")
    {
      ag->SetPoint(i, i, grab_abs(filename.c_str(), 300.00));
      ag->SetPoint(i, i, grab_abs(filename.c_str(), 300.00));
    }
  }

  ag->SetTitle("Absorption over time at 300.00nm");
  ag->SetTitle("Absorption over time at 300.00nm");

  return ag;
}
