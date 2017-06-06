#include "TChain.h"
#include "TTree.h"
#include "TGraph2D.h"
#include <TMath.h>
#include <TRandom2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TF2.h>
#include <TH1.h>
#include <Math/Functor.h>
#include <TPolyLine3D.h>
#include <Math/Vector3D.h>
#include <Fit/Fitter.h>

using namespace ROOT::Math;

void mu_track()
{
	gSystem->Load("lib/MainLoop.so");

	Mrd* mrd = NULL;
	TChain* ch = new TChain("mrd_tree");
	ch->Add("V*.root");
	ch->SetBranchAddress("mrd", &mrd);

	TGraph2D* g = new TGraph2D();
	TGraph2D* f = new TGraph2D();

	// for (int i = 0; i < ch->GetEntries(); ++i)
	// {
	// 	ch->GetEntry(i);

	// 	for (int j = 0; j < mrd->Cards().size(); ++j) 
	// 	{
	// 		if (mrd->Cards().at(j).Channel() > 13)
	// 		{
	// 			g->SetPoint(i+j, mrd->Cards().at(j).Slot(), 1.5, mrd->Cards().at(j).Channel());
	// 		}
	// 		else
	// 		{
	// 			g->SetPoint(i+j, mrd->Cards().at(j).Slot(), 0.5, mrd->Cards().at(j).Channel());
	// 		} // generically plots events to left or right

	// 		// g->SetPoint(i+j, mrd->TimeStamp(), mrd->Cards().at(j).Slot(),mrd->Cards().at(j).Channel());
	// 	}
	// }

	for (int i = 0; i < 3; ++i)
	{
		ch->GetEntry(i);

		for (int j = 0; j < mrd->Cards().size(); ++j)
		{
			if (mrd->Cards().at(j).Channel() > 13)
			{
				g->SetPoint(i+j, mrd->Cards().at(j).Slot(), 1.5, mrd->Cards().at(j).Channel());
			}
			else
			{
				g->SetPoint(i+j, mrd->Cards().at(j).Slot(), 0.5, mrd->Cards().at(j).Channel());
			}
		}
	}

	// f->SetPoint();

	g->SetMarkerStyle(20);
	g->Draw("PCOL");
	g->GetXaxis()->SetRangeUser(12., 20.);
}