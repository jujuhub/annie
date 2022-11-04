#include "TGraph.h"
#include "TLegend.h"

void att_plots_liner()
{
    TLegend* legend = new TLegend(0.78, 0.7, 0.93, 0.93);

    TGraph* g0 = plot_spec_att("sept15_test/File_170915_111436_liner.txt");
    legend->AddEntry(g0, "2017 Sep 15", "l");

//    TGraph* g1 = plot_spec_att("sept22_test/File_170922_113626_liner.txt");
//    legend->AddEntry(g1, "2017 Sep 22", "l");

//    TGraph* g2 = plot_spec_att("sept29_test/File_170929_120424_liner.txt");
//    legend->AddEntry(g2, "2017 Sep 29", "l");

    TGraph* g3 = plot_spec_att("oct13_test/File_171013_104255_liner.txt");
    legend->AddEntry(g3, "2017 Oct 13", "l");

//    TGraph* g4 = plot_spec_att("oct20_test/File_171020_124020_liner.txt");
//    legend->AddEntry(g4, "2017 Oct 20", "l");

//    TGraph* g5 = plot_spec_att("oct27_test/File_171027_113837_liner.txt");
//    legend->AddEntry(g5, "2017 Oct 27", "l");

//    TGraph* g6 = plot_spec_att("nov03_test/File_171103_103322_liner.txt");
//    legend->AddEntry(g6, "2017 Nov 3", "l");

//    TGraph* g7 = plot_spec_att("nov10_test/File_171110_111441_liner.txt");
//    legend->AddEntry(g7, "2017 Nov 10", "l");

    TGraph* g8 = plot_spec_att("nov17_test/File_171117_123332_liner.txt");
    legend->AddEntry(g8, "2017 Nov 17", "l");

    g0->SetTitle("liner");
//    g1->SetLineColor(kRed);
//    g2->SetLineColor(kBlue);
    g3->SetLineColor(kGreen);
//    g4->SetLineColor(kMagenta);
//    g5->SetLineColor(kCyan);
//    g6->SetLineColor(kViolet-3);
//    g7->SetLineColor(kOrange);
    g8->SetLineColor(kYellow);

    g0->Draw();
//    g1->Draw("same");
//    g2->Draw("same");
    g3->Draw("same");
//    g4->Draw("same");
//    g5->Draw("same");
//    g6->Draw("same");
//    g7->Draw("same");
    g8->Draw("same");

    legend->Draw();

}

int main()
{
    att_plots_liner();
    return 0;
}
