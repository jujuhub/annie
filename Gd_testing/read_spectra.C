#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TMath.h>
#include <TCanvas.h>
#include <TLeaf.h>
#include <Rtypes.h>
#include <TROOT.h>
#include <TRandom3.h>
#include <TH2.h>
#include <TPad.h>
#include <TVector3.h>
#include <TString.h>
#include <TPRegexp.h>
#include <TGraph.h>
#include <TSystemDirectory.h>
#include <TSystemFile.h>
#include <TSystem.h>

#include <sys/stat.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <string>
#include <vector>

////////////////////////////////////////////////////////////////////////
/////////////////////// TGraph creating part ///////////////////////////
////////////////////////////////////////////////////////////////////////
/////////////////////////   ABSORBANCE   /////////////////////////////

TGraph* make_spect_graph_abs(const char* filename) {
  
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
  
  TGraph* tg_abs = new TGraph(xs.size(), xs.data(), ys.data());
  tg_abs->SetNameTitle(TString(title), (title + ";" + axis_labels.at(0) + ";" + axis_labels.at(1)).c_str());
  
  for (size_t i = 0; i < xs.size(); ++i){
    tg_abs->SetPoint(i, xs.at(i), ys.at(i));
  }
  
  tg_abs->GetXaxis()->SetTitle("Wavelength [nm]");
  tg_abs->GetYaxis()->SetTitle("Absorption [a.u.]");
  
  return tg_abs;
  
}

////////////////////////////////////////////////////////////////////////
/////////////////////// TGraph creating part ///////////////////////////
////////////////////////////////////////////////////////////////////////
/////////////////////////   ATT LENGTH   /////////////////////////////

TGraph* make_spect_graph_att(const char* filename) {
  
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
  
  TGraph* tg_att = new TGraph(xs.size(), xs.data(), ys.data());
  tg_att->SetNameTitle(TString(title) + "_att_length", (title + ";" + axis_labels.at(0) + ";" + axis_labels.at(1)).c_str());
  
  for (size_t i = 0; i < xs.size(); ++i){
    if (ys.at(i) > 0){ //Avoid inf/nan at 0
      tg_att->SetPoint(i, xs.at(i), 0.1/TMath::Log(TMath::Power(10,ys.at(i))));
    } else {
      tg_att->SetPoint(i, xs.at(i), 0);
    }
  }
  
  tg_att->GetXaxis()->SetTitle("Wavelength [nm]");
  tg_att->GetYaxis()->SetTitle("Attenuation length [m]");
  
  return tg_att;
  
}

////////////////////////////////////////////////////////////////////////
/////////////////////// TH1D creating part ///////////////////////////
////////////////////////////////////////////////////////////////////////
/////////////////////////   ABSORBANCE   /////////////////////////////

TH1D* make_spect_hist_abs(const char* filename, int hist_nb) {
  
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
  
  TH1D *h_abs = new TH1D(Form("h%i",hist_nb),TString(title),xs.size(),xs.at(0),xs.at(xs.size()-1));
  
  for (size_t i = 0; i < xs.size(); ++i){
    h_abs->Fill(xs.at(i),ys.at(i));
  }
  
  h_abs->GetXaxis()->SetTitle("Wavelength [nm]");
  h_abs->GetYaxis()->SetTitle("Absorption [a.u.]");
  
  return h_abs;
  
}

////////////////////////////////////////////////////////////////////////
/////////////////////// TH1D creating part ///////////////////////////
////////////////////////////////////////////////////////////////////////
/////////////////////////   ATT LENGTH   /////////////////////////////

TH1D* make_spect_hist_att(const char* filename, int hist_nb) {
  
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
  
  TH1D *h_att = new TH1D(Form("h%i_att_length",hist_nb),TString(title),xs.size(),xs.at(0),xs.at(xs.size()-1));
  
  for (size_t i = 0; i < xs.size(); ++i){
    if (ys.at(i) > 0){ //Avoid inf/nan at 0
      h_att->Fill(xs.at(i),0.1/TMath::Log(TMath::Power(10,ys.at(i))));
    } else {
      h_att->Fill(xs.at(i),0);
    }
  }
  
  h_att->GetXaxis()->SetTitle("Wavelength [nm]");
  h_att->GetYaxis()->SetTitle("Attenuation length [m]");
  
  return h_att;
  
}

////////////////////////////////////////////////////////////////////////
//////////////////////////// Main part /////////////////////////////////
////////////////////////////////////////////////////////////////////////

void read_spectra() {
  
  TFile g("ALL_SPECTRA.root","RECREATE");
  int valid_files_counter = 0;
  int color_counter = 0;
  
  // Parse every ".txt" file in the current directory, making a TGraph/Hist for each.
  TSystemDirectory dir(gSystem->pwd(), gSystem->pwd());
  for (Int_t i = 0; i < dir.GetListOfFiles()->GetEntries(); ++i) {
    std::string filename = (dynamic_cast<TSystemFile*>(dir.GetListOfFiles()->At(i)))->GetName();
    if (filename.length() > 4 &&
      filename.substr(filename.length() - 4) == ".txt")
    {
      valid_files_counter++;
      TGraph* tg_abs = make_spect_graph_abs(filename.c_str());
      TGraph* tg_att = make_spect_graph_att(filename.c_str());
      TH1D* h_abs = make_spect_hist_abs(filename.c_str(), valid_files_counter);
      TH1D* h_att = make_spect_hist_att(filename.c_str(), valid_files_counter);
      //       tg->SetLineColor(i+6);
      //       h1->SetLineColor(i+6);
      //       tg->Draw("AL");
      if (valid_files_counter != 10 && valid_files_counter != 0 ) { // let's avoid having a white histogram (color codes 0 and 10) on a white backgroud...
	color_counter = valid_files_counter;
      } else {
	color_counter = valid_files_counter + 51;
      }
      tg_abs->SetLineColor(color_counter);
      tg_att->SetLineColor(color_counter);
      h_abs->SetLineColor(color_counter);
      h_att->SetLineColor(color_counter);
      
      tg_abs->Write();
      tg_att->Write();
      h_abs->Write();
      h_att->Write();
    }
  }
  
  g.Close();
}