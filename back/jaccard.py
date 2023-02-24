# ----- THIS FUNCTION IS NOT WORKING FOR NOW ----- #

def jaccardSimilarity(historyWords,booksInfo):
    booksData = []
    for book in booksInfo:
        count = 0
        for w in historyWords.keys():
            if w in book['words']:
                count += historyWords[w]
        booksData.append({
            "bookId": book['bookId'],
            "jaccard": (count/book['totalWords'])
        })
    sortedBooks = sorted(booksData, key=lambda d: d['jaccard'], reverse=True) 
    return sortedBooks