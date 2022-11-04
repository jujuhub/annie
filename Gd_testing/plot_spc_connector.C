#include "TGraph.h"
#include "TLegend.h"

void plot_spc_connector()
{
	TLegend *legend = new TLegend(0.78, 0.70, 0.93, 0.93);

	TGraph *g0 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/File_190523_115210_1pct_normal_Gd.txt");
	legend->AddEntry(g0, "initial 1% Gd", "l"); 

	TGraph *g1 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/File_190523_115948_MA_connector_1pct_Gd.txt");
	legend->AddEntry(g1, "~10min", "l"); 

	TGraph *g2 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/File_190524_144151_MA_connector_1pct_Gd.txt");
	legend->AddEntry(g2, "1 day", "l"); 

	TGraph *g3 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/File_190528_112623_MA_connector_1pct_Gd.txt");
	legend->AddEntry(g3, "5 days", "l"); 

//	TGraph *g4 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/2018-12-27/File_181227_114852_nylon_rope_1pct_Gd.txt");
//	legend->AddEntry(g4, "~1.25 month", "l"); 

//	TGraph *g5 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/2018-10-19/File_181019_164505_1x19_316SS_1pct_Gd.txt");
//	legend->AddEntry(g5, "~2 months", "l"); 

//	TGraph *g6 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/2018-11-20/File_181120_153359_1x19_316SS_1pct_Gd.txt");
//	legend->AddEntry(g6, "~3 months", "l");

//	TGraph *g7 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/2018-12-18/File_181219_131528_1x19_316SS_1pct_Gd.txt");
//	legend->AddEntry(g7, "~4 months", "l");

//	TGraph *g8 = make_spect_graph_log("/home/juhe/ANNIE/Gd_testing/2019-01-03/File_190103_115104_1x19_316SS_1pct_Gd.txt");
//	legend->AddEntry(g8, "~5 months", "l");

	g0->SetTitle("MacArtney connector sample [connector only]");
	g1->SetLineColor(2);
    g2->SetLineColor(4);
    g3->SetLineColor(3);
//    g4->SetLineColor(6);
//    g5->SetLineColor(7);
//    g6->SetLineColor(9);
//    g7->SetLineColor(kOrange);
//    g8->SetLineColor(5);

	g0->Draw();
	g1->Draw("same");
	g2->Draw("same");
	g3->Draw("same");
//	g4->Draw("same");
//	g5->Draw("same");
//	g6->Draw("same");
//	g7->Draw("same");
//	g8->Draw("same");

	legend->Draw();

}

int main()
{
	plot_spc_connector();
	return 0;
}
