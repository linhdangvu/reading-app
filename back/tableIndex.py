import requests, re
from getBooksApi import getListBooks

# get table index for all book and each book
def getTableIndex(listBooks):
    tableIndex = dict()
    booksInfo = []
    listBooksData = getListBooks(listBooks)

    for book in listBooksData:
        response_API = requests.get(book['text_url'])
        data = response_API.text
        #### Option 1: Prendre seulement des mots avec carateres de 4 à 10
        words = re.findall(r"[A-Za-z]{4,10}\w+", data)
        occurentCounts = dict()

        for word in words:
            w = word.lower()

            # Count for table index all books
            if w in tableIndex:
                if book['id'] in tableIndex[w]:
                    tableIndex[w][book['id']] += 1
                else:
                    tableIndex[w][book['id']] = 1
            else:
                tableIndex[w] = dict({book['id']: 1})

            # Count for table index for each book
            if w in occurentCounts:
                occurentCounts[w] += 1
            else:
                occurentCounts[w] = 1

        booksInfo.append({
            "bookId": book['id'],
            "words": occurentCounts,
            "totalWords": len(words),
            "totalWordsWithOccur": len(occurentCounts)
        })    
    return tableIndex, booksInfo

