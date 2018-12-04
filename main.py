#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 23:58:14 2018
Conectar ROOT con Tensorflow
@author: hernanca
"""

# from ROOT import TBranch, TTree, TFile, TChain, TBrowser
# from ROOT import gROOT
import uproot               # Se instala con pip3 install uproot [all]
import pandas as pd
import tensorflow as tf     # Se instala con pip3 install tensorflow[all]
import numpy as np

GammaOrMuon = ["gamma", "muon"]
Angle = ["00", "10", "20", "30", "40", "50", "60", "70", "80", "90"]
Rank = range(64)
OneOrTwo = {1: "1", 2: "2"}

data = pd.DataFrame()          # creación de DataFrame vacío
for k in GammaOrMuon:
    FilesToOpen = []
    for j in Rank:
        FilesToOpen.append("../data/" + Angle[4] + "deg/" + k
                           + "-rank" + str(Rank[j]).zfill(3) + "-CCD-"
                           + "*.fits.root")
    iterator = uproot.tree.iterate(FilesToOpen,   # ubicación de archivos .root
                                   "hitSumm",     # nombre del TTree a leer
                                   reportentries=False)
    for i in iterator:
        if k == "gamma":
            partial = pd.DataFrame.from_dict(i)
            partial["target"] = pd.Series(["gamma"] * len(i[list(i)[0]]))
            data = data.append(partial, ignore_index=True)
            del partial
        elif k == "muon":
            partial = pd.DataFrame.from_dict(i)
            partial["target"] = pd.Series(["muon"] * len(i[list(i)[0]]))
            data = data.append(partial, ignore_index=True)
            del partial
# rellenado del DataFrame: Recorre todos los archivos .root y los agrega al
# DataFrame. ignore_index evita que el índice se reinicie con cada archivo

data.drop([b"runID", b"ohdu", b"expoStart", b"nSat"], axis=1, inplace=True)
data = data.reindex(np.random.permutation(data.index))
print(data.describe(), "\n")
print(data["target"].describe())
