#include "TGraph.h"
#include "TLegend.h"

void spec_plots()
{
	// load function for making plots
	// cannot load another macro in this macro

	// .L make_spect_graph.C; // need to load this in root first

	TLegend* legend = new TLegend(0.78, 0.7, 0.93, 0.93); // y1 = 0.56, 0.7

	TGraph* g0 = make_spect_graph("sept15_test/File_170915_113656_lux_pmt.txt");
	// TGraph* g1 = make_spect_graph("sept22_test/");
	TGraph* g2 = make_spect_graph("sept29_test/File_170929_111256_lux_pmt.txt");
	TGraph* g3 = make_spect_graph("oct13_test/File_171013_111254_lux_pmt.txt");
	TGraph* g4 = make_spect_graph("oct20_test/File_171020_121831_lux_pmt.txt");
	TGraph* g5 = make_spect_graph("oct27_test/File_171027_123246_lux_pmt.txt");
	// TGraph* g6 = make_spect_graph("nov03_test/");
	// TGraph* g7 = make_spect_graph("");
	
	g0->SetTitle("LUX PMT");
	// g1->SetLineColor(kRed);
	g2->SetLineColor(kBlue);
	g3->SetLineColor(kGreen);
	g4->SetLineColor(kMagenta);
	g5->SetLineColor(kCyan);
	// g6->SetLineColor(kViolet-3);
	// g7->SetLineColor(kOrange);

	legend->AddEntry(g0, "2017-09-15", "l");
	// legend->AddEntry(g1, "2017-09-22", "l");
	legend->AddEntry(g2, "2017-09-29", "l");
	legend->AddEntry(g3, "2017-10-13", "l");
	legend->AddEntry(g4, "2017-10-20", "l");
	legend->AddEntry(g5, "2017-10-27", "l");
	// legend->AddEntry(g6, "2017-11-03", "l");
	// legend->AddEntry(g7, "17-08-25", "l");

	
	g0->Draw();
	// g1->Draw("same");
	g2->Draw("same");
	g3->Draw("same");
	g4->Draw("same");
	g5->Draw("same");
	// g6->Draw("same");
	// g7->Draw("same");
	legend->Draw();

}

int main()
{
	spec_plots();
	return 0;
}
