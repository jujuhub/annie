#include "TFile.h"
#include "TTree.h"
#include "TH2I.h"
#include "TCanvas.h"
#include "TText.h"
#include "TChain.h"
#include "TObjArray.h"
#include "TIterator.h"
#include "TChainElement.h"

// v1

void pmt_hits_v1() {
	// load stuff
	gSystem->Load("lib/MainLoop.so");

	TChain* ch = new TChain("mrd_tree");
	ch->Add("V*.root"); // add files in dir to chain

	// histograms
	TH2I* hfacc = new TH2I("hfacc", "FACC", 2, 14, 16, 13, 1, 14);
	TH2I* hmrd2 = new TH2I("hmrd2", "MRD2", 2, 16, 18, 13, 1, 14);
	TH2I* hmrd3 = new TH2I("hmrd3", "MRD3", 2, 18, 20, 15, 1, 16);

	// define pointers
	TTree* t = NULL;
	Mrd* mrd = NULL;

	TObjArray* fileElements = ch->GetListOfFiles();
	TIter next(fileElements);
	TChainElement* chEl = 0;
	
	while (chEl = (TChainElement*)next()) {
		TFile f(chEl->GetTitle());
		f.GetObject("mrd_tree", t);
		t->SetBranchAddress("mrd", &mrd);

		for (int i = 0; i < t->GetEntries(); ++i) {
			t->GetEntry(i);
			// t->Show();

			for (int j = 0; j < mrd->Cards().size(); ++j) {
			// hcol->Fill(mrd->Cards().at(j).Slot(), mrd->Cards().at(j).Channel());

				if (mrd->Cards().at(j).Slot() == 14) {
					if (mrd->Cards().at(j).Channel() > 13) {
						hfacc->Fill(mrd->Cards().at(j).Slot()+1, mrd->Cards().at(j).Channel()-13);
					} // move paddles to the right
					else {
					hfacc->Fill(mrd->Cards().at(j).Slot(), mrd->Cards().at(j).Channel());
					}
				} // FACC

				else if (mrd->Cards().at(j).Slot() == 17) {
					if (mrd->Cards().at(j).Channel() > 13) {
						hmrd2->Fill(mrd->Cards().at(j).Slot()-1, mrd->Cards().at(j).Channel()-13);
					} // move paddles to the left
					else {
						hmrd2->Fill(mrd->Cards().at(j).Slot(), mrd->Cards().at(j).Channel());
					}
				} // MRD2

				else {
					if (mrd->Cards().at(j).Channel() > 15) {
						hmrd3->Fill(mrd->Cards().at(j).Slot()+1, mrd->Cards().at(j).Channel()-15);
					} // move paddles to the right
					else {
						hmrd3->Fill(mrd->Cards().at(j).Slot(), mrd->Cards().at(j).Channel()-1);
					}
				} // MRD3
			}
		}
	} // loops over ea file

	TCanvas* c1 = new TCanvas;
	// c1->Divide(3,1);
	TText* txt = new TText();
	txt->SetTextFont(43);
	txt->SetTextSize(20);

	c1->SetGrid();
	hfacc->Draw("COLZ");

	for (int i = 1; i < 27; ++i) {
		if (i > 13) {
			txt->DrawText(15.4, i-13+0.25, Form("14-%d", i));
		}
		else {
			txt->DrawText(14.4, i+0.25, Form("14-%d", i));
		}
	}

	TCanvas* c2 = new TCanvas;
	c2->cd();
	c2->SetGrid();
	hmrd2->Draw("COLZ");

	for (int i = 1; i < 27; ++i) {
		if (i > 13) {
			txt->DrawText(16.4, i-13+0.25, Form("17-%d", i));
		}
		else {
			txt->DrawText(17.4, i+0.25, Form("17-%d", i));
		}
	}
	
	TCanvas* c3 = new TCanvas;
	c3->cd();
	c3->SetGrid();
	hmrd3->Draw("COLZ");

	for (int i = 1; i < 30; ++i) {
		if (i > 14) {
			txt->DrawText(19.4, i-14+0.25, Form("18-%d", i));
		}
		else {
			txt->DrawText(18.4, i+0.25, Form("18-%d", i));
		}
	}

	// f->Close(); // won't plot if included
}

int main() {
	pmt_hits_v1();
	return 0;
}