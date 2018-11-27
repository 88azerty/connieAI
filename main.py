#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 23:58:14 2018
Conectar ROOT con Tensorflow
@author: hernanca
"""

# from ROOT import TBranch, TTree, TFile, TChain, TBrowser
# from ROOT import gROOT
import uproot       # Se instala con pip3 install uproot [all]
import pandas as pd
import tensorflow as tf # Se instala con pip3 install tensorflow[all]

iterator = uproot.tree.iterate("../kcikel/10deg/*.root", "hitSumm", reportentries=False) # hitSumm es el nombre del TTree dentro del TFile
data = pd.DataFrame()

for i in iterator:
    data = data.append(pd.DataFrame.from_dict(i), ignore_index=True)
    print("Leyendo datos")

print(data.describe())
