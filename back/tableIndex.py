import requests, re, concurrent.futures, time
from thread import baseThreadPool
from getBooksApi import getListBooks
from threading import Lock

# get table index for all book and each book
def getTableIndex(listBooks):
    print('RUNNING function getTableIndex')
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

        # print("START Thread filterBooks")
        # threaded_filter_book = time.time()
        baseThreadPool(words, filterBooks, False)
        # print("END Thread filterBooks:", time.time() - threaded_filter_book)

        return {
            "bookId": book['id'],
            "words": occurentCounts,
            "totalWords": len(words),
            "totalWordsWithOccur": len(occurentCounts)
        }
    
    print("START Thread readBook")
    threaded_start = time.time()

    booksInfo = baseThreadPool(listBooksData, readBook, True)
    print("END Thread readBook:", time.time() - threaded_start)

    print('END function getTableIndex')
    return tableIndex, booksInfo, allBooks