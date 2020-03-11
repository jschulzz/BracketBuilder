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


def createInputList(team_stats):
    output_current = []
    output_current.append(len(team_stats["wins"]) / team_stats["g"])
    # field goal percentage
    output_current.append(team_stats["fg_pct"])
    # field goal attempts per game
    output_current.append(team_stats["fga"] / team_stats["g"])
    # 2's percentage
    output_current.append(team_stats["fg2_pct"])
    # 2's attempts per game
    output_current.append(team_stats["fg2a"] / team_stats["g"])
    # 3's percentage
    output_current.append(team_stats["fg3_pct"])
    # 3's attempts per game
    output_current.append(team_stats["fg3a"] / team_stats["g"])
    # Freethrow percentage
    output_current.append(team_stats["ft_pct"])
    # Freethrow attempts per game
    output_current.append(team_stats["fta"] / team_stats["g"])
    # offensive rebounds per game
    output_current.append(team_stats["orb"] / team_stats["g"])
    # defensive rebounds per game
    output_current.append(team_stats["drb"] / team_stats["g"])
    # assists per game
    output_current.append(team_stats["ast"] / team_stats["g"])
    # steals per game
    output_current.append(team_stats["stl"] / team_stats["g"])
    # blocks per game
    output_current.append(team_stats["blk"] / team_stats["g"])
    # turnovers per game
    output_current.append(team_stats["tov"] / team_stats["g"])
    # fouls per game
    output_current.append(team_stats["pf"] / team_stats["g"])
    # points per game
    output_current.append(team_stats["pts_per_g"] / 100)
    # strength of schedule
    output_current.append(team_stats["points_against"] / 100)
    # strength of schedule
    output_current.append(team_stats["sos"] / 13)
    # offensive efficincy
    output_current.append(team_stats["offensive"] / 100)
    # defensive efficiency
    output_current.append(team_stats["defensive"] / 100)
    players = sorted(team_stats["players"], key=lambda x: x["minutes"], reverse=True)
    for p in players[:5]:
        output_current.append(p["minutes"] / 40)
        output_current.append(p["fga"] / 10)
        output_current.append(p["fg"] / 10)
        output_current.append(p["fg2a"] / 10)
        output_current.append(p["fg2"] / 10)
        output_current.append(p["fg3a"] / 10)
        output_current.append(p["fg3"] / 10)
        output_current.append(p["fta"] / 10)
        output_current.append(p["ft"] / 10)
        output_current.append(p["orb"] / 10)
        output_current.append(p["drb"] / 10)
        output_current.append(p["ast"] / 10)
        output_current.append(p["stl"] / 10)
        output_current.append(p["blk"] / 10)
        output_current.append(p["tov"] / 10)
        output_current.append(p["pf"] / 5)
        output_current.append(p["pts"] / 20)

    # starter's points
    # output_current.append(sum(team_stats["player_pts"][5:]) / 100)
    # starter's point weight
    # output_current.append(sum(team_stats["player_pts"][5:]) / team_stats["pts_per_g"])
    return output_current


def getData():

    data = {}
    with open("stats.json") as file:
        data = json.load(file)
    input_list = []
    output_list = []
    data = data["team_stats"]
    for winner_team_name in data:
        for loser_team_name in data[winner_team_name]["wins"]:
            if loser_team_name not in data:
                # skip wins over untracked teams
                continue
            t1name = winner_team_name
            t2name = loser_team_name
            t1 = data[t1name]
            t2 = data[t2name]
            if t1["wins"] == None or t2["wins"] == None:
                # don't track games with missing data
                continue
            input_current = createInputList(t1) + createInputList(t2)
            input_list.append(input_current)
            output_list.append(0)
            input_current = createInputList(t2) + createInputList(t1)
            input_list.append(input_current)
            output_list.append(1)
    return input_list, output_list


def createModel(input_length):
    model = Sequential()
    # model.add(Dropout(0.3))
    model.add(
        Dense(
            30,
            activation="relu",
            kernel_initializer="normal",
            input_shape=(input_length,),
        )
    )
    # model.add(Dropout(0.1))
    model.add(Dense(75, activation="relu"))
    model.add(Dropout(0.1))
    # model.add(Dense(10, activation="relu", kernel_initializer="normal"))
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
        epochs=500,
        batch_size=32,
        callbacks=callbacks_list,
        validation_split=0.2,
    )
