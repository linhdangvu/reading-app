from flask import Flask, jsonify, render_template,request
from flask_cors import CORS, cross_origin
# import logging
from tableIndex import getTableIndex
from getBooksApi import getBooksData, getBooksThread
from cosine import cosineSearchWord, getMatrixCloseness
from jaccard import jaccardSimilarity
import time, concurrent.futures, json, requests, re
from threading import Lock

##########################################
# ---------- INITIAL VARIABLE ---------- #
##########################################
# logging.basicConfig(level=logging.INFO)
# listBooks = [49345,56667,1,2,3,4,5,40,48]
listBooks = [l for l in range(1,200)] + [49345,56667]
books_10 = [listBooks[x:x+10] for x in range(0, len(listBooks), 10)]
historyWords = dict()
clickedBooks = dict()
suggestionObject = dict({"data": [],"status" : True})
rankingObject = dict({"data": [],"status" : True})
mostReadObject = dict({"data": [],"status" : True})
booksInfoObject = dict({"data": [],"status" : True})
allBooksoObject = dict({"data": [],"status" : True})
closenessDataObject = dict({"data": [],"status" : True})
tableIndexDataObject =   dict({"data": dict(),"status" : True})
loadingBack = dict({"status": True})

def loadingData():
    if loadingBack['status']:
        print('START LOADING DATA')
        loading_time = time.time()
        count = 1
        print('We will load {} time for {} books'.format(len(books_10), len(listBooks)))
        for book in books_10:
            print('Times --> {}'.format(count))
            count += 1
            print(book)
            bookInfo = []
            allBooks = []
            tableIndexDataObject['data'], bookInfo, allBooks = getTableIndex(book,  tableIndexDataObject['data'])
            booksInfoObject['data'] += bookInfo
            allBooksoObject['data'] += allBooks

        # tableIndexDataObject['data'], booksInfoObject['data'], allBooksoObject['data'] = getTableIndex(listBooks)
        tableIndexDataObject['status'] = False
        booksInfoObject['status'] = False
        allBooksoObject['status'] = False
        closenessDataObject['data'] = getMatrixCloseness(tableIndexDataObject['data'])
        closenessDataObject['status'] = False
        loadingBack['status'] = False
        print('END LOADING DATA ----------> {}'.format(time.time() - loading_time))

def create_app(debug=True):

    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['JSON_SORT_KEYS'] = False

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['CORS_HEADERS'] = 'Content-Type'


    #################################################
    # ---------- SHOW SOME DATA TO CHECK ---------- #
    #################################################

    # SHOW FULL TABLE INDEX
    @app.route('/tindex', methods=['GET'])
    def tindex():
        loadingData()
        return jsonify(tableIndexDataObject['data'])
    
    # SHOW FULL CLOSENESS
    @app.route('/closeness', methods=['GET'])
    def closeness():
        loadingData()
        return jsonify(closenessDataObject['data'])
    
    # get table index for each book
    @app.route('/itbook', methods=['GET'])
    def itbook():
        loadingData()
        return jsonify(booksInfoObject['data'])



    #############################
    # ---------- GET ---------- #
    #############################

    # homeage for back end
    @app.route("/")
    def index():
        loadingData()
        return render_template("index.html")

    # try to get only 10 books first
    @app.route('/getbooks', methods=['GET'])
    def get_books():
        loadingData()
        return jsonify(allBooksoObject['data'])
    
    # SHOW get keys of table index
    @app.route('/tableindex', methods=['GET'])
    def table_index():
        loadingData()
        return jsonify(list(tableIndexDataObject['data'].keys()))
        
    # Use Cosine to have suggestion & ranking
    @app.route('/cosine', methods=['GET'])
    def cosine():
        print("RUN ROUTE /cosine")
        loadingData()
        time_start = time.time()
        # if rankingObject["status"]:
        ranking = []
        booksData = cosineSearchWord(historyWords, tableIndexDataObject['data'])
        for id,val in enumerate(list(booksData)):
            if id > 10:
                break
            else:
                ranking.append(getBooksThread(val))
        rankingObject["data"] = ranking
        # rankingObject["status"] = False
        print('END ROUTE /cosine ----------> {}'.format(time.time() - time_start))
        return jsonify(rankingObject["data"])
    
    # get most read by compare clicked book
    @app.route('/mostread', methods=['GET'])
    def most_read():
        print("RUN ROUTE /mostread")
        loadingData()
        time_start = time.time()
        # if mostReadObject['status']:
        sortedClickedBooks = dict(sorted(clickedBooks.items(),key=lambda x:x[1], reverse=True) )
        ranking = []
        for id,val in enumerate(list(sortedClickedBooks.keys())):
            if id > 10:
                break
            else:
                ranking.append(getBooksThread(val))
        mostReadObject["data"] = ranking
        # mostReadObject["status"] = False
        print('END ROUTE /mostread ----------> {}'.format(time.time() - time_start))
        return jsonify(mostReadObject['data'])



    
    #############################################
    # ---------- GET WITH PARAMETERS ---------- #
    #############################################

    # This route for find books with <word> in table index
    @app.route('/searchbook/<word>', methods=['GET'])
    def search_books(word):
        print("RUN ROUTE /searchbook/<word>")
        loadingData()
        time_start = time.time()
        # if not tableIndexDataObject['status']:
        if tableIndexDataObject['data'].get(word)!=None:
            # print(jsonify(tableIndexData[word]))
            sortedBooks = dict(sorted(tableIndexDataObject['data'][word].items(),key=lambda x:x[1], reverse=True))
            bookData =  getBooksData(list(sortedBooks.keys()))
            print("END ROUTE /searchbook/<word> ----------> {}".format(time.time() - time_start))
            return jsonify(bookData)
        else:
            print("END ROUTE /searchbook/<word> ----------> {}".format(time.time() - time_start))
            return "NOT_FOUND"
        
        # return "NO TABLE INDEX AVAILABLE"
    
    ##############################
    # ---------- POST ---------- #
    ##############################
    # send search data
    @app.route('/searchdata', methods=['POST', 'GET'])
    @cross_origin(origin='*',headers=['content-type'])
    def search_data():
        print("RUN ROUTE /searchdata")
        loadingData()
        time_start = time.time()
        if request.method == 'POST':
            word = request.json['word']
            lowerWord = word.lower()
            if lowerWord in historyWords:
                historyWords[lowerWord] += 1
            else:
                historyWords[lowerWord] = 1
            # suggestionObject["status"] = True
            # rankingObject["status"] = True
        print("END ROUTE /searchdata ----------> {}".format(time.time() - time_start))
        return jsonify(historyWords)
    
    @app.route('/clickedbooks', methods=['POST','GET'])
    @cross_origin(origin='*',headers=['content-type'])
    def clicked_books():
        print("RUN ROUTE /clickedbooks")
        loadingData()
        time_start = time.time()
        if request.method == 'POST':
            bookId = request.json['bookId']
            if bookId in clickedBooks:
                clickedBooks[bookId] += 1
            else:
                clickedBooks[bookId] = 1
            # mostReadObject["status"] = True
        print("END ROUTE /clickedbooks ----------> {}".format(time.time() - time_start))
        return jsonify(clickedBooks)
    
    # This route for suggest data from the last search keyword from local storage
    @app.route('/suggestion', methods=['POST'])
    @cross_origin(origin='*',headers=['content-type'])
    def suggestion():
        print('RUN ROUTE /suggestion')
        loadingData()

        # Init variable
        threaded_start = time.time()
        lastSearch = request.json['last_search']
        sortedBooks = dict()
        suggestionBooks = []
        lock = Lock()
        
        if tableIndexDataObject['data'].get(lastSearch)!=None and lastSearch != "":
            sortedBooks = dict(sorted(tableIndexDataObject['data'][lastSearch].items(),key=lambda x:x[1], reverse=True))

        def checkCloseness(closenessPos, suggestionBooks):
            return closenessPos not in suggestionBooks

        def getSuggestion(id,closeData):
            lock.acquire()
            if closeData['bookId'] in list(sortedBooks.keys()):
                if id==0:
                    if checkCloseness(closenessDataObject['data'][id+1]['bookId'] , suggestionBooks):
                        suggestionBooks.append(closenessDataObject['data'][id+1]['bookId']) 
                elif id==len(closenessDataObject['data'])-1:
                    if checkCloseness(closenessDataObject['data'][id-1]['bookId'] , suggestionBooks):
                        suggestionBooks.append(closenessDataObject['data'][id-1]['bookId']) 
                else:
                    if checkCloseness(closenessDataObject['data'][id+1]['bookId'] , suggestionBooks):
                        suggestionBooks.append(closenessDataObject['data'][id+1]['bookId']) 
                    if checkCloseness(closenessDataObject['data'][id-1]['bookId'] , suggestionBooks):
                        suggestionBooks.append(closenessDataObject['data'][id-1]['bookId']) 
            lock.release()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for id,closeData in enumerate(closenessDataObject['data']):
                futures.append(executor.submit(getSuggestion, id,closeData))
        
        top10Suggestion = suggestionBooks[0:10] if len(suggestionBooks) > 11 else suggestionBooks

        suggestionObject["data"] = getBooksData(top10Suggestion)
        # suggestionObject["status"] = False
        print('END ROUTE /suggestion ----------> {}'.format(time.time() - threaded_start))
        return jsonify(suggestionObject["data"])
    
    # This route for reading book from book id <bookId>
    @app.route('/readbookcontent', methods=['POST'])
    @cross_origin(origin='*',headers=['content-type'])
    def read_book_content():
        print("RUN ROUTE /readbookcontent")
        loadingData()
        time_start = time.time()
        # if lastReadingBook['bookId'] != bookId:
        bookId = request.json['bookId']
        bookLink = ""
        bookContent = ""
        book_data = getBooksThread(bookId)
        for format in book_data['formats'].keys():
            if '.htm' in book_data['formats'][format] or '.html.images' in book_data['formats'][format]:
                bookLink = book_data['formats'][format]
                response_API = requests.get(book_data['formats'][format])
                bookContent = response_API.text 

        # take string of words from <body> ... </body> by RegEx
        pattern = re.compile(r'<body>(.*?)</body>', re.DOTALL)
        result = re.search(pattern, bookContent)

        if result:
            body_content = result.group(1)
            bookContent = body_content.replace('images/', 'https://www.gutenberg.org/cache/epub/{}/images/'.format(bookId))
        print("END ROUTE /readbookcontent----------> {}".format(time.time() - time_start))
        return jsonify({ "link": bookLink,'textHtml' : bookContent})


    ###########################################
    # ---------- NOT USING FOR NOW ---------- #
    ###########################################

    # # Use Jaccard to have list of book suggestion and order it
    # @app.route('/jaccard', methods=['GET'])
    # def jaccard():
    #     booksData = jaccardSimilarity(historyWords,booksInfoObject['data'])

    #     # sortedBooks = sorted(booksData, key=lambda d: d['jaccard'], reverse=True) 
    #     sendBookId = []
    #     for sb in booksData:
    #         if sb['jaccard'] > 0:
    #             sendBookId.append(sb['bookId'])
    #     top5 = sendBookId.slice(0,5)  if len(sendBookId) > 5 else sendBookId
    #     ranking = getBooksData(top5)
    #     # print(booksData)
    #     return jsonify(ranking)
    #     # return jsonify(sendBookId, booksData, historyWords)
    return app

app = create_app(debug=True)
if __name__ == "__main__" :
    app.run(host='0.0.0.0', port=5000)