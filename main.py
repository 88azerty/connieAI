#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 23:58:14 2018
Conectar ROOT con Tensorflow
@author: hernanca
"""

from ROOT import TBranch, TTree, TFile, TChain, TBrowser
from ROOT import gROOT
import uproot
import math
import pandas as pd
import tensorflow as tf

gROOT.Reset()
file1 = TFile("/home/hernanca/MEGAsync/Laboratorio/CONNIE/kcikel/10deg/muon-rank000-CCD-1.fits.root", "READ")
tree1 = file1.Get("hitSumm")
file1.Close()

# TODO Usar TChain para combinar múltiples archivos ROOT

nameBranches = []
data = {}

for n in range(tree1.GetNbranches()):
    nameBranches.append(tree1.GetListOfBranches()[n].GetName())    # Get the names of all the branches in the given tree and store them in an array

for name in nameBranches:
    data[name] = []         # Initialize dict with empty arrays

for event in tree1:
    for name in nameBranches:
        runtime = "event." + name
        print(runtime)
        data[name].append( event.id )

print(data)
