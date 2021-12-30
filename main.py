import os
import pandas as pd
import psutil
from Node.Node import Node
from StarCube.StarCube import StarCube
import seaborn as sns
import numpy as np
import time
from Tree.Tree import Tree
import math

def discretize(dataFrame, NumDims, PartitionNone):

    maxim = [0] * len(dataFrame.columns)
    mini = [0] * len(dataFrame.columns)
    dX = [0] * len(dataFrame.columns)

    for j in NumDims:
        MaxofCol = dataFrame.iloc[0, j]
        MinofCol = dataFrame.iloc[0, j]
        for i in range(len(dataFrame)):
            if dataFrame.iloc[i, j] < MinofCol:
                MinofCol = dataFrame.iloc[i, j]
            if dataFrame.iloc[i, j] > MaxofCol:
                MaxofCol = dataFrame.iloc[i, j]
        maxim[j] = MaxofCol
        mini[j] = MinofCol
        dX[j] = (maxim[j] - mini[j]) / (--PartitionNone)

    for j in NumDims:
        for i in range(len(dataFrame)):
            dataFrame.iloc[i, j] = math.floor((dataFrame.iloc[i, j] - mini[j]) / dX[j])
    return dataFrame.astype(int)



def startable_gen(dataFrame):
    restore = 0
    if dataFrame.keys()[0] == 0:
        dataFrame = dataFrame.rename(columns={0: 'A'})
        restore = 1

    unique = []
    numCounts = []
    for i in range(len(dataFrame.columns)):
        unique = np.unique(dataFrame.iloc[:, i])
        numCounts.append([])
        for j in range(len(unique)):
            count = len(dataFrame.iloc[:, i][dataFrame.iloc[:, i] == unique[j]])
            numCounts[i].append(count)
            if threshold > count:
                dataFrame.iloc[:, i][dataFrame.iloc[:, i] == unique[j]] = -1

    dataFrame = dataFrame.groupby(dataFrame.columns.tolist()).size().reset_index().rename(columns={0: 'count'})

    if restore == 1:
        dataFrame = dataFrame.rename(columns={'A': 0})
    return dataFrame

def decode(startable):
    sep1 = '_'
    sep2 = ';'
    for i in range(len(startable)):
        for j in range(len(startable.columns) - 1):
            startable.iloc[i, j] = sep1.join(
                [sep2.join([chr(97 + math.floor(j / 26)) * (math.floor(j / 26)), chr(97 + (j % 26))]),
                 str(startable.iloc[i, j])])
    return startable


if __name__ == '__main__':
    start_time = time.time()
    p1 = psutil.Process(os.getpid())
    f = open("../output.txt", "w+")



    f1 = "data/Algerian_forest_fires_dataset_UPDATE.csv"
    print('input file: ', f1)
    dataFrame = pd.read_csv(f1, sep=";")


    print('Attempting to discretize the imported dataset...')
    # dataFrame = discretize(dataFrame, NumDims, PartitionNone)
    print('Proceeding to star-cubing algorithm...')
    threshold = 100
    startable = startable_gen(dataFrame)
    startable = decode(startable)

    root = Node(data='root', count=sum(startable.iloc[:, len(startable.columns) - 1]), depth=0)
    startree = Tree(root, threshold)
    startree.generate(startable)

    starcube = StarCube(threshold, startree)
    starcube.starcubing(startree, root)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Total Bytes Used: ", end='')
    print(p1.memory_info().rss)

    f.close()

    g = sns.PairGrid(dataFrame)
    g.map_diag(sns.stripplot)
    g.map_offdiag(sns.stripplot, jitter=True)

