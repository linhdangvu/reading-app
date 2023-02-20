from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import networkx as nx

# this function use cosine similarity
def cosineSearchWord(historyWords, tableIndexData):
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
    return result

def getMatrixCloseness(tableIndexData):
    # Init variable
    booksData = dict()
    for word in tableIndexData:
        for b in tableIndexData[word].keys(): 
            if b in booksData:
                booksData[b].update(dict({word:tableIndexData[word][b]}))
            else:
                booksData.update(dict({b: dict({word:tableIndexData[word][b]})}))
    bookDF = pd.DataFrame(booksData.values(),
        index=booksData.keys()).fillna(0)
    # print(bookDF)
    matrixCloseness = []
    for c1, b1 in enumerate(list(booksData.keys())):
        for c2,b2 in enumerate(list(booksData.keys())):
            if b1 != b2:
                res = cosine_similarity(bookDF.loc[b1:b1],bookDF.loc[b2:b2])[0][0]
                if res*100 > 50: # > 50% -> add edge
                    matrixCloseness.append((b1,b2))
    

    # Create the graph representing the reading app
    G = nx.Graph()
    G.add_edges_from(matrixCloseness)
    closenessData = []

    # Compute the closeness centrality of each node in the graph
    closeness_centrality = nx.closeness_centrality(G)

    # Print the closeness centrality of each node
    for node, closeness in closeness_centrality.items():
        print(f"Node {node}: Closeness centrality = {closeness}")
        closenessData.append({"bookId": node, "closeness":closeness })
    return closenessData