import requests, re, concurrent.futures, time
from thread import baseThreadPool
from getBooksApi import getListBooks
from threading import Lock

# get table index for all book and each book
def getTableIndex(listBooks):
    print('RUNNING function getTableIndex')
    threaded_start = time.time()
    tableIndex = dict()
    booksInfo = []
    listBooksData, allBooks = getListBooks(listBooks)

    def readBook(book):
        response_API = requests.get(book['text_url'])
        data = response_API.text
        lock = Lock()

        #### Option 1: Prendre seulement des mots avec carateres de 4 à 10
        words = re.findall(r"[A-Za-z]{4,10}\w+", data)
        occurentCounts = dict()

        def filterBooks(word):
            lock.acquire()
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
            lock.release()

        baseThreadPool(words, filterBooks, False)

        return {
            "bookId": book['id'],
            "words": occurentCounts,
            "totalWords": len(words),
            "totalWordsWithOccur": len(occurentCounts)
        }
    booksInfo = baseThreadPool(listBooksData, readBook, True)

    print('END function getTableIndex -----> {}'.format(time.time() - threaded_start))
    return tableIndex, booksInfo, allBooks