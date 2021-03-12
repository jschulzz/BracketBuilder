import train
import keras
import os
import numpy as np

from ComparisonFunctions.CompareFunction import CompareFunction
from ComparisonFunctions.utils import getStarters

def compareTeams(team1name, team2name, data):
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    t1 = data[team1name]
    t2 = data[team2name]
    input_list = train.createInputList(t1) + train.createInputList(t2)
    keras.backend.clear_session()
    model = train.createModel(len(input_list))

    model.load_weights("best.hdf5")
    prediction = model.predict(np.expand_dims(input_list, axis=0))[0][0]
    keras.backend.clear_session()
    if prediction > 0.5:
        return 0, 1, round(max(prediction, 1 - prediction) * 1000) / 1000
    return 1, 0, round(max(prediction, 1 - prediction) * 1000) / 1000


comparison = CompareFunction(wantHighest=True, comparison=compareTeams)
