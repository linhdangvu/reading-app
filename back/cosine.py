from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# this function use cosine similarity but also add the number occurs of words search to have most searching list
def cosineSimilarity(historyWords, tableIndexData):
    if historyWords!=None:
        booksData = dict({'history':historyWords})
    else:
        booksData = dict()
    result = dict()

    for word in historyWords.keys():
        if word in tableIndexData:
            for b in tableIndexData[word].keys(): 
                if b in booksData:
                    booksData[b].update(dict({word:tableIndexData[word][b]}))
                else:
                    booksData.update(dict({b: dict({word:tableIndexData[word][b]})}))
    bookDF = pd.DataFrame(booksData.values(),
        index=booksData.keys()).fillna(0)
    if historyWords!=None:
        for cs in list(booksData.keys())[1:]:
            result[cs] = cosine_similarity(bookDF.loc["history":"history"],bookDF.loc[cs:cs])[0][0]
        return result
    else:
        # this part will have the cosine each document to each other
        print(bookDF)
        pass