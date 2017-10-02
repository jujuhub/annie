#include "TGraph.h"
#include "TLegend.h"

void spec_plots()
{
	// load function for making plots; cannot load another macro in this macro
	// .L make_spect_graph.C;

	TLegend* legend = new TLegend(0.78, 0.7, 0.93, 0.93); // y1 = 0.56, 0.7

	// TGraph* g0 = make_spect_graph("jul07_test/");
	// TGraph* g1 = make_spect_graph("jul14_test/");
	// TGraph* g2 = make_spect_graph("jul21_test/");
	// TGraph* g3 = make_spect_graph("jul28_test/");
	TGraph* g4 = make_spect_graph("aug04_test/File_170804_123603_lux_pmt.txt");
	TGraph* g5 = make_spect_graph("aug11_test/File_170811_120857_lux_pmt.txt");
	TGraph* g6 = make_spect_graph("aug18_test/File_170818_114937_2ndtrial_lux_pmt.txt");
	TGraph* g7 = make_spect_graph("aug25_test/File_170825_124202_lux_pmt.txt");
	
	g4->SetTitle("LUX PMT");
	// g1->SetLineColor(kRed);
	// g2->SetLineColor(kBlue);
	// g3->SetLineColor(kGreen);
	g4->SetLineColor(kMagenta);
	g5->SetLineColor(kCyan);
	g6->SetLineColor(kViolet-3);
	g7->SetLineColor(kOrange);

	// legend->AddEntry(g0, "17-07-07", "l");
	// legend->AddEntry(g1, "17-07-14", "l");
	// legend->AddEntry(g2, "17-07-21", "l");
	// legend->AddEntry(g3, "17-07-28", "l");
	legend->AddEntry(g4, "17-08-04", "l");
	legend->AddEntry(g5, "17-08-11", "l");
	legend->AddEntry(g6, "17-08-18", "l");
	legend->AddEntry(g7, "17-08-25", "l");

	
	// g0->Draw();
	// g1->Draw();
	// g2->Draw("same");
	// g3->Draw("same");
	g4->Draw();
	g5->Draw("same");
	g6->Draw("same");
	g7->Draw("same");
	legend->Draw();

}

int main()
{
	spec_plots();
	return 0;
}