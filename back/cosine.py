from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import networkx as nx
import time, concurrent.futures

from thread import baseThreadPool

# this function use cosine similarity
def cosineSearchWord(historyWords, tableIndexData):
    print("RUNNING function cosineSearchWord")
    threaded_start = time.time()
    # Init variable
    result = dict()
    booksData = dict({'history':historyWords})
    for word in historyWords.keys():
        if word in tableIndexData:
            for b in tableIndexData[word].keys(): 
                if b in booksData:
                    booksData[b].update(dict({word:tableIndexData[word][b]}))
                else:
                    booksData.update(dict({b: dict({word:tableIndexData[word][b]})}))
    bookDF = pd.DataFrame(booksData.values(),
        index=booksData.keys()).fillna(0)
    for cs in list(booksData.keys())[1:]:
        result[cs] = cosine_similarity(bookDF.loc["history":"history"],bookDF.loc[cs:cs])[0][0]

    sortedBooks = dict(sorted(result.items(),key=lambda x:x[1], reverse=True))

    print("END function cosineSearchWord -----> {}".format(time.time() - threaded_start))
    return sortedBooks

def getMatrixCloseness(tableIndexData):
    print("RUNNING function getMatrixCloseness")
    threaded_start = time.time()
    # Init variable
    booksData = dict()
    def transformTableCloseness(word):
        for b in tableIndexData[word].keys(): 
            if b in booksData:
                booksData[b].update(dict({word:tableIndexData[word][b]}))
            else:
                booksData.update(dict({b: dict({word:tableIndexData[word][b]})}))
    baseThreadPool(tableIndexData, transformTableCloseness)

    bookDF = pd.DataFrame(booksData.values(),
        index=booksData.keys()).fillna(0)

    matrixCloseness = []

    def getCloseness(b1,b2):
        if b1 != b2:
            res = cosine_similarity(bookDF.loc[b1:b1],bookDF.loc[b2:b2])[0][0]
            if res*100 > 50: # > 50% -> add edge
                matrixCloseness.append((b1,b2))

    # Loop 1 thread
    def closenessThread1(b1):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for b2 in list(booksData.keys()):
                futures.append(executor.submit(getCloseness, b1,b2))
    baseThreadPool(list(booksData.keys()), closenessThread1)

    # Create the graph representing the reading app
    G = nx.Graph()
    G.add_edges_from(matrixCloseness)
    closenessData = []

    # Compute the closeness centrality of each node in the graph
    closeness_centrality = nx.closeness_centrality(G)

    # Print the closeness centrality of each node
    for node, closeness in closeness_centrality.items():
        closenessData.append({"bookId": node, "closeness":closeness })

    sortedClosenessData = sorted(closenessData, key=lambda d: d['closeness'], reverse=True) 
    print("END function getMatrixCloseness -----> {}".format(time.time() - threaded_start))
    return sortedClosenessData