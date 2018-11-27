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
import numpy as np

iterator = uproot.tree.iterate( "../kcikel/10deg/*.root",                       # ubicación de los archivos .root
                                "hitSumm",                                      # nombre del TTree a leer
                                reportentries=False)
data = pd.DataFrame()                                                           # creación de DataFrame vacío

for i in iterator:                                                              # rellenado del DataFrame: Recorre todos los archivos .root
    data = data.append(pd.DataFrame.from_dict(i), ignore_index=True)            # y los agrega al DataFrame

data = data.reindex(np.random.permutation(data.index))                          # aleatorización del orden de los eventos.
data.describe()
