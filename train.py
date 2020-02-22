import os
import json
import random
from statistics import mean
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import metrics, optimizers
import numpy as np
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

# TODO: To be honest, this is pretty clean and straightforward. Maybe still toy with more training ideas?


def clearOldNetworks():
    for file in os.listdir(os.curdir):
        if file.startswith("weights-improvement"):
            os.remove(file)


def createInputList(t1, t2):
    output_current = []
    output_current.append(len(t1["wins"]) / 35)
    output_current.append(t1["fg_pct"])  # field goal percentage
    # field goal attempts per game
    output_current.append(t1["fga"] / t1["mp"])
    output_current.append(t1["fg2_pct"])  # 2's percentage
    output_current.append(t1["fg2a"] / t1["mp"])  # 2's attempts per game
    output_current.append(t1["fg3_pct"])  # 3's percentage
    output_current.append(t1["fg3a"] / t1["mp"])  # 3's attempts per game
    output_current.append(t1["ft_pct"])  # Freethrow percentage
    output_current.append(t1["fta"] / t1["mp"])  # Freethrow attempts per game
    output_current.append(t1["orb"] / t1["mp"])  # offensive rebounds per game
    output_current.append(t1["drb"] / t1["mp"])  # defensive rebounds per game
    output_current.append(t1["ast"] / t1["mp"])  # assists per game
    output_current.append(t1["stl"] / t1["mp"])  # steals per game
    output_current.append(t1["blk"] / t1["mp"])  # blocks per game
    output_current.append(t1["tov"] / t1["mp"])  # turnovers per game
    output_current.append(t1["pf"] / t1["mp"])  # fouls per game
    output_current.append(t1["pts_per_g"] / 100)  # points per game
    output_current.append(t1["points_against"] / 100)  # strength of schedule
    output_current.append(t1["sos"] / 13)  # strength of schedule
    output_current.append(mean(t1["heights"]) / 80)  # average height
    output_current.append(mean(t1["weights"]) / 280)  # average weight
    # average height of starters
    output_current.append(mean(t1["heights"][:5]) / 80)
    # average weight of starters
    output_current.append(mean(t1["weights"][:5]) / 280)
    output_current.append(sum(t1["player_pts"][5:]) / 100)  # average jersey number
    output_current.append(sum(t1["player_pts"][:5]) / 100)  # average jersey number
    output_current.append(
        sum(t1["player_pts"][5:]) / t1["pts_per_g"]
    )  # average jersey number
    output_current.append(
        sum(t1["player_pts"][:5]) / t1["pts_per_g"]
    )  # average jersey number
    output_current.append(mean(t1["jersey_nums"]) / 36)  # average jersey number
    output_current.append(t1["offensive"] / 100)  # offensive efficincy
    output_current.append(t1["defensive"] / 100)  # defensive efficiency

    # field goal percentage
    output_current.append(len(t2["wins"]) / 35)
    output_current.append(t2["fg_pct"])  # field goal percentage
    # field goal attempts per game
    output_current.append(t2["fga"] / t2["mp"])
    output_current.append(t2["fg2_pct"])  # 2's percentage
    output_current.append(t2["fg2a"] / t2["mp"])  # 2's attempts per game
    output_current.append(t2["fg3_pct"])  # 3's percentage
    output_current.append(t2["fg3a"] / t2["mp"])  # 3's attempts per game
    output_current.append(t2["ft_pct"])  # Freethrow percentage
    output_current.append(t2["fta"] / t2["mp"])  # Freethrow attempts per game
    output_current.append(t2["orb"] / t2["mp"])  # offensive rebounds per game
    output_current.append(t2["drb"] / t2["mp"])  # defensive rebounds per game
    output_current.append(t2["ast"] / t2["mp"])  # assists per game
    output_current.append(t2["stl"] / t2["mp"])  # steals per game
    output_current.append(t2["blk"] / t2["mp"])  # blocks per game
    output_current.append(t2["tov"] / t2["mp"])  # turnovers per game
    output_current.append(t2["pf"] / t2["mp"])  # fouls per game
    output_current.append(t2["pts_per_g"] / 100)  # points per game
    output_current.append(t2["points_against"] / 100)  # strength of schedule
    output_current.append(t2["sos"] / 13)  # strength of schedule
    output_current.append(mean(t2["heights"]) / 80)  # average height
    output_current.append(mean(t2["weights"]) / 290)  # average weight

    output_current.append(sum(t2["player_pts"][5:]) / 100)  # average jersey number
    output_current.append(sum(t2["player_pts"][:5]) / 100)  # average jersey number
    output_current.append(
        sum(t2["player_pts"][5:]) / t2["pts_per_g"]
    )  # average jersey number
    output_current.append(
        sum(t2["player_pts"][:5]) / t2["pts_per_g"]
    )  # average jersey number
    # average height of starters
    output_current.append(mean(t2["heights"][:5]) / 80)
    # average weight of starters
    output_current.append(mean(t2["weights"][:5]) / 280)
    output_current.append(mean(t2["jersey_nums"]) / 36)  # average jersey number
    output_current.append(t2["offensive"] / 100)  # offensive efficincy
    output_current.append(t2["defensive"] / 100)  # defensive efficiency
    # output_current.append(random.random())
    return output_current


def getData():

    data = {}
    bracket = {}
    with open("games.json") as file:
        data = json.load(file)
    with open("node_modules/bracket-data/data/ncaam/2019.json") as f:
        bracket = json.load(f)
    sortorder = [0, 15, 7, 8, 4, 11, 3, 12, 5, 10, 2, 13, 6, 9, 1, 14]

    east = list(np.array(bracket["teams"]["E"])[sortorder])
    midwest = list(np.array(bracket["teams"]["M"])[sortorder])
    west = list(np.array(bracket["teams"]["W"])[sortorder])
    south = list(np.array(bracket["teams"]["S"])[sortorder])

    bracket_list = east + west + south + midwest
    bracket_list = list(map(lambda x: x["team"], bracket_list))
    input_list = []
    output_list = []
    for winner_team_name in data:
        for loser_team_name in data[winner_team_name]["wins"]:
            # if loser_team_name not in data or (loser_team_name not in bracket_list and winner_team_name not in bracket_list) :
            if loser_team_name not in data:
                continue
            t1name = winner_team_name
            t2name = loser_team_name
            t1 = data[t1name]
            t2 = data[t2name]
            # input_current = [0, 0]
            # input_current[r] = 1
            # print(t1name, t2name, r)
            if t1["link"] == None or t2["link"] == None:
                continue
            input_current = createInputList(t1, t2)
            input_list.append(input_current)
            output_list.append(0)
            input_current = createInputList(t2, t1)
            input_list.append(input_current)
            output_list.append(1)
    return input_list, output_list


def createModel(input_length):
    model = Sequential()
    # model.add(Dropout(0.3))
    model.add(
        Dense(
            20,
            activation="relu",
            kernel_initializer="normal",
            input_shape=(input_length,),
        )
    )
    model.add(Dropout(0.1))
    # model.add(Dense(75, activation='relu'))
    # model.add(Dropout(0.1))
    model.add(Dense(10, activation="relu", kernel_initializer="normal"))
    # model.add(Dropout(0.1))
    model.add(Dense(1, activation="sigmoid", kernel_initializer="normal"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


if __name__ == "__main__":
    clearOldNetworks()
    input_list, output_list = getData()
    print("Training on {} games".format(len(input_list)))
    print("Data Organized. Building Model")

    # print(output_list)
    model = createModel(len(input_list[0]))

    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-{val_acc:.4f}.hdf5"
    checkpoint = ModelCheckpoint(
        filepath, monitor="loss", verbose=1, save_best_only=True, mode="min"
    )
    reduction = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.8,
        patience=10,
        mode="auto",
        cooldown=2,
        min_lr=0.00001,
    )
    stopper = EarlyStopping(
        monitor="val_loss", min_delta=0.0005, patience=30, mode="auto"
    )
    # callbacks_list = [checkpoint, reduction, stopper]
    callbacks_list = [checkpoint, reduction]
    print("Fitting Now")
    model.fit(
        np.asarray(input_list),
        np.asarray(output_list),
        epochs=100,
        batch_size=8,
        callbacks=callbacks_list,
        validation_split=0.2,
    )
