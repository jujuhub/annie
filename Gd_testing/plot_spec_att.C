#include <fstream>
#include <sstream>
#include <string>

TGraph* plot_spec_att(const char* filename)
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
    axis_labels.push_back(dummy);

  while (std::getline(infile, line))
  {
    // get the x and y values from the current line
    std::istringstream iss(line);
    double x = 0.;
    double y = 0.;
    bool stored_x = false;
    bool stored_y = false;
    double num = 0.;
    while(std::getline(iss, dummy, ',') && std::istringstream(dummy) >> num) {
      if (!stored_x) { x = num; stored_x = true; }
      else if (!stored_y) { y = num; stored_y = true; }
    }

    if (stored_x && stored_y) {
      xs.push_back(x);
      ys.push_back(y);
    }
  }

  TGraph* tg = new TGraph(xs.size(), &(xs.front()), &(ys.front()));
  tg->SetNameTitle("mydata", (title + ";" + axis_labels.at(0)
    + ";" + axis_labels.at(1)).c_str());

  for (size_t i = 0; i < xs.size(); ++i){
      if (ys.at(i) > 0){
        tg->SetPoint(i, xs.at(i), 0.1/TMath::Log(TMath::Power(10, ys.at(i))));
      } else {
        tg->SetPoint(i, xs.at(i), 0);
      }
  }

  tg->GetXaxis()->SetTitle("wavelength (nm)");
  tg->GetYaxis()->SetTitle("attenuation length (m)");

  return tg;
}

std::vector<TGraph*> make_spect_graphs() {

  std::vector<TGraph*> result;

  // Parse every ".txt" file in the current directory, making a TGraph for each.
  // Skip files for which the absorption at 200 nm is small (probably just
  // distilled water calibration runs)
  TSystemDirectory dir(gSystem->pwd(), gSystem->pwd());
  for (size_t i = 0; i < dir.GetListOfFiles()->GetEntries(); ++i) {
    std::string filename = (dynamic_cast<TSystemFile*>(dir.GetListOfFiles()
      ->At(i)))->GetName();
    if (filename.length() > 4 &&
      filename.substr(filename.length() - 4) == ".txt")
    {
      TGraph* tg = plot_spec_att(filename.c_str());
      if (tg->Eval(200.) > 0.1) result.push_back(tg);
    }
  }

  return result;
}
