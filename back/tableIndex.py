import requests, re, concurrent.futures, time
from thread import baseThreadPool
from getBooksApi import getListBooks
from threading import Lock

# list of words not consider as keyword, there are a lot more but we don't have enough data
letters_3 = ['the', 'and', 'are', 'for', 'not', 'but', 'had', 'has', 'was', 
                'all', 'any', 'one', 'man', 'out', 'you', 'his', 'her', 'can', 
                'did', 'get', 'him', 'its', 'let', 'per', 'run', 'set', 'who', 'say']
letters_4 = ['that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'into', 'each','also', 'than', 'most', 'here', 'tell', 'know',
                'want', 'been', 'much', 'some', 'very', 'what', 'does', 'when', "whom",'them','after', 'even','both',
                'were', 'more', 'many', 'upon', 'read', 'quit', 'none', 'like', 'once', 'make', 'just']
letters_5 = ['there', 'which', 'these', 'other', 'where', 'about', 'above', 'among', 'bring', 'could', 'every', 'their', 'while', 'since',
            'along', 'across', 'front', 'could', 'twice', 'again', 'might' ,'thank', 'grand', 'ebook']
letters = ['before', 'behind', 'because', 'owning', 'without', 'inside', 'around', 'should', 'itself','thanks', 'something', 'someone',"project",'gutenberg','welcome',
            'things', 'tells', 'means', 'those', 'named','email','print']
commonWords = letters_3 + letters_4 + letters_5 + letters

# get table index for all book and each book
def getTableIndex(listBooks, tableIndex):
    print('RUNNING function getTableIndex')
    threaded_start = time.time()
    # tableIndex = dict()
    booksInfo = []
    listBooksData, allBooks = getListBooks(listBooks)

    # This function read each book content to get table index
    def readBook(book):
        response_API = requests.get(book['text_url'])
        data = response_API.text
        lock = Lock()

        #### Option 1: Prendre seulement des mots avec carateres de 4 à 10
        words = re.findall(r"[A-Za-z]{3,20}\w+", data)
        occurentCounts = dict()

        def filterBooks(word):
            lock.acquire()
            w = word.lower()
            # Count for table index all books
            if w not in commonWords:
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