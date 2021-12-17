from os import path
import pickle
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class Tirage(BaseModel):
    N1: int
    N2: int
    N3: int
    N4: int
    N5: int
    E1: int
    E2: int
    win: int


# Data cleaning

data = pd.read_csv('datasource/EuroMillions_numbers.csv', sep=";")
dict = data.to_dict()


def randomNotN(n: int, maximum: int) -> int:
    """creates a random between 1 and maximum+1 different from n

    Args:
        n (int): arg value
        maximum (int): arg value

    Returns:
        int: the return value
    """
    r = np.random.randint(1, maximum+1)
    while r == n:
        r = np.random.randint(1, maximum+1)
    return r


newdata = []
for i in dict["Date"]:
    for i in range(4):
        newdata.append({
            "N1": randomNotN(dict["N1"][i], 50),
            "N2": randomNotN(dict["N2"][i], 50),
            "N3": randomNotN(dict["N3"][i], 50),
            "N4": randomNotN(dict["N4"][i], 50),
            "N5": randomNotN(dict["N5"][i], 50),
            "E1": randomNotN(dict["E1"][i], 12),
            "E2": randomNotN(dict["E2"][i], 12),
            "Win": 0
        })
newdata = pd.DataFrame(newdata)
data["Win"] = 1
inputData = pd.concat([newdata, data[["N1", "N2", "N3", "N4", "N5", "E1", "E2", "Win"]]], ignore_index=True)



def trainTest():
    """separates training and test data

    Returns:
        tuple[Sequence | Any | list,Sequence | Any | list,Sequence | Any | list]: the return value
    """
    X_train, X_test, y_train, y_test = train_test_split(inputData.drop("Win", axis=1), inputData["Win"])
    return X_train, X_test, y_train, y_test

def trainModel(dataFrame):
    """Model training

    Args:
        dataFrame (Any): Arg value

    Returns:
        tuple[RandomForestCLassifier,tuple[Sequence | Any | list, Sequence | Any | list, Sequence | Any | list, Sequence | Any | list]]: 
        train is return to keep informations about test variables and use it later
    """
    train = trainTest()
    X_train = train[0]
    X_test = train[1]
    y_train = train[2]
    y_test = train[3]
    model = RandomForestClassifier(n_estimators=1000)
    model.fit(X_train, y_train)
    return model, train

# Model creation or loading if it already exist

if not path.exists("save.p"):
    model = trainModel(inputData)
    pickle.dump(model,open("save.p","wb"))
else:
    model = pickle.load(open("save.p","rb"))


def generateGrid(threshold=0.1):
    """generates a random draw with a chance of winning greater than threshold

    Args:
        threshold (float, optional): Defaults to 0.1.

    Returns:
        dict[str, Any]: The return value
    """
    grid = {
        "N1": np.random.randint(1, 51),
        "N2": np.random.randint(1, 51),
        "N3": np.random.randint(1, 51),
        "N4": np.random.randint(1, 51),
        "N5": np.random.randint(1, 51),
        "E1": np.random.randint(1, 13),
        "E2": np.random.randint(1, 13),
    }
    prediction = model[0].predict_proba(pd.DataFrame([grid]))
    while prediction[0][1] < threshold:
        grid = {
            "N1": np.random.randint(1, 51),
            "N2": np.random.randint(1, 51),
            "N3": np.random.randint(1, 51),
            "N4": np.random.randint(1, 51),
            "N5": np.random.randint(1, 51),
            "E1": np.random.randint(1, 13),
            "E2": np.random.randint(1, 13),
        }
        prediction = model[0].predict_proba(pd.DataFrame([grid]))
    return grid
