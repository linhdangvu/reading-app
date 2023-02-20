def jaccardSimilarity(historyWords,booksInfo):
    booksData = []
    for book in booksInfo:
        count = 0
        for w in historyWords.keys():
            if w in book['words']:
                count += 1
        booksData.append({
            "bookId": book['bookId'],
            "jaccard": (count/book['totalWordsWithOccur'])
        })
    return booksData