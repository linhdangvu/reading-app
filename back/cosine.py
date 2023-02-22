from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import networkx as nx
import time, concurrent.futures

from thread import baseThreadPool

# this function use cosine similarity
def cosineSearchWord(historyWords, tableIndexData):
    print("RUNNING function cosineSearchWord")
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
    print("End function cosineSearchWord")
    return sortedBooks

def getMatrixCloseness(tableIndexData):
    print("RUNNING function getMatrixCloseness")
    # Init variable
    booksData = dict()
    def transformTableCloseness(word):
        for b in tableIndexData[word].keys(): 
            if b in booksData:
                booksData[b].update(dict({word:tableIndexData[word][b]}))
            else:
                booksData.update(dict({b: dict({word:tableIndexData[word][b]})}))
    print("START thread transformTableCloseness")
    threaded_start = time.time()
    baseThreadPool(tableIndexData, transformTableCloseness)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = []
    #     for word in tableIndexData:
    #         futures.append(executor.submit(transformTableCloseness, word))

    print("End thread transformTableCloseness", time.time() - threaded_start)
    

    bookDF = pd.DataFrame(booksData.values(),
        index=booksData.keys()).fillna(0)
    # print(bookDF)
    matrixCloseness = []

    def getCloseness(b1,b2):
        if b1 != b2:
            res = cosine_similarity(bookDF.loc[b1:b1],bookDF.loc[b2:b2])[0][0]
            if res*100 > 50: # > 50% -> add edge
                matrixCloseness.append((b1,b2))

    # Loop 1 thread
    def closenessThread1(b1):
        # print("Running closenessThread1:")
        # threaded_closeness_1= time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for b2 in list(booksData.keys()):
                futures.append(executor.submit(getCloseness, b1,b2))
        # print("End closenessThread1", time.time() - threaded_closeness_1)



    print("START thread closenessThread1...")
   
    threaded_closeness_2= time.time()
    baseThreadPool(list(booksData.keys()), closenessThread1)
    
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = []
    #     for b1 in list(booksData.keys()):
    #         futures.append(executor.submit(closenessThread1, b1))
    print("End thread closenessThread1..", time.time() - threaded_closeness_2)


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
    print("END function getMatrixCloseness")
    return sortedClosenessData