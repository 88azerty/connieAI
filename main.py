#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 23:58:14 2018
Conectar ROOT con Tensorflow
@author: hernanca
"""
import uproot               # Se instala con pip3 install uproot[all]
import pandas as pd
import tensorflow as tf     # Se instala con pip3 install tensorflow[all]
import numpy as np

GammaOrMuon = ["gamma", "muon"]
Angle = ["00", "10", "20", "30", "40", "50", "60", "70", "80", "90"]
Rank = range(64)

data = pd.DataFrame()          # creación de DataFrame vacío
for k in GammaOrMuon:
    FilesToOpen = []
    for j in Rank:
        FilesToOpen.append("../data/" + Angle[4] + "deg/" + k
                           + "-rank" + str(Rank[j]).zfill(3) + "-CCD-"
                           + "*.fits.root")       # * incluye archivos -1 y -2
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

data.drop([b"runID", b"ohdu", b"expoStart", b"nSat", b"flag", #metadatos
           b"xMin", b"xMax", b"yMin", b"yMax", #geometria del evento
           b"xPix", b"yPix", b"level", b"ePix", b"nSavedPix"], #datos cada pixel
          axis=1, inplace=True)
data = data.reindex(np.random.permutation(data.index))
# se remueven las Series del DataFrame que contienen datos redundantes
# y se aleatorizan los eventos para asegurar consistencia

print("Lectura de datos finalizada.")
print("Iniciando el motor de ML.")

MijnFeature = data[[b'E0', b'n0', b'xBary0', b'yBary0', b'xVar0', b'yVar0',
                    b'E1', b'n1', b'xBary1', b'yBary1', b'xVar1', b'yVar1',
                    b'E2', b'n2', b'xBary2', b'yBary2', b'xVar2', b'yVar2',
                    b'E3', b'n3', b'xBary3', b'yBary3', b'xVar3', b'yVar3']]

MijnTarget = data["target"]
MijnOptimizer = tf.train.GradientDescentOptimizer(learning_rate=0.000001)
MijnOptimizer = tf.contrib.estimator.clip_gradients_by_norm(MijnOptimizer, 5.0)

MijnEstimator = tf.estimator.LinearRegressor(feature_columns=MijnFeature)
