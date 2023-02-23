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
listBooks = [49345,56667,1,2,3,4,5,6,7]
# listBooks = [l for l in range(1,20)]
historyWords = dict()
clickedBooks = dict()
lastSearchWord = dict({"word": ""})
# tableIndexData, booksInfo, allBooks = getTableIndex(listBooks)
# closenessData = getMatrixCloseness(tableIndexData)
suggestionObject = dict({"data": [],"status" : True})
lastSearchObject = dict({"data": [],"status" : True})
rankingObject = dict({"data": [],"status" : True})
mostReadObject = dict({"data": [],"status" : True})
booksInfoObject = dict({"data": [],"status" : True})
allBooksoObject = dict({"data": [],"status" : True})
closenessDataObject = dict({"data": [],"status" : True})
tableIndexDataObject =   dict({"data": dict(),"status" : True})
loadingBack = dict({"status": True})
lastReadingBook = dict({"bookId": None, "data": "", "link": ""})


def create_app(debug=True):

    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['JSON_SORT_KEYS'] = False

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['CORS_HEADERS'] = 'Content-Type'


    #############################
    # ---------- GET ---------- #
    #############################

    @app.route("/")
    def index():
        if loadingBack['status']:
            print('START LOADING DATA')
            tableIndexDataObject['data'], booksInfoObject['data'], allBooksoObject['data'] = getTableIndex(listBooks)
            tableIndexDataObject['status'] = False
            booksInfoObject['status'] = False
            allBooksoObject['status'] = False
            closenessDataObject['data'] = getMatrixCloseness(tableIndexDataObject['data'])
            closenessDataObject['status'] = False
            loadingBack['status'] = False
            print('END LOADING DATA')
        return render_template("index.html")

    # try to get only 10 book
    @app.route('/getbooks', methods=['GET'])
    def get_books():
        print("Running get_books")
        # data = getBooksData(listBooks)
        return jsonify(allBooksoObject['data'])


        
    # get table index
    @app.route('/tableindex', methods=['GET'])
    def table_index():
        return jsonify(list(tableIndexDataObject['data'].keys()))
    
    # Use Cosine to have suggestion & ranking
    @app.route('/cosine', methods=['GET'])
    def cosine():
        print("Running cosine")
        if rankingObject["status"] and not tableIndexDataObject['status']:
            ranking = []
            booksData = cosineSearchWord(historyWords, tableIndexDataObject['data'])
            for id,val in enumerate(list(booksData)):
                if id > 10:
                    break
                else:
                    ranking.append(getBooksThread(val))
            rankingObject["data"] = ranking
            rankingObject["status"] = False
        return jsonify(rankingObject["data"])
    
    # get most read by compare clicked book
    @app.route('/mostread', methods=['GET'])
    def most_read():
        if mostReadObject['status']:
            sortedClickedBooks = dict(sorted(clickedBooks.items(),key=lambda x:x[1], reverse=True) )
            ranking = []
            for id,val in enumerate(list(sortedClickedBooks.keys())):
                if id > 10:
                    break
                else:
                    ranking.append(getBooksThread(val))
            mostReadObject["data"] = ranking
            mostReadObject["status"] = False
        return jsonify(mostReadObject['data'])


    @app.route('/lastsearch', methods=['GET'])
    def last_search():
        print('Running last search')
        if lastSearchObject["status"]:
            lastSearch = lastSearchWord["word"]
            sortedBooks = dict()
            if tableIndexDataObject['data'].get(lastSearch)!=None and lastSearch != "":
                # print(jsonify(tableIndexData[word]))
                sortedBooks = dict(sorted(tableIndexDataObject['data'][lastSearch].items(),key=lambda x:x[1], reverse=True))
            lastSearchObject["data"] = getBooksData(list(sortedBooks.keys()))
            lastSearchObject["status"] = False
        return jsonify(lastSearchObject["data"])

    @app.route('/suggestion', methods=['GET'])
    def suggestion():
        print('RUN ROUTE suggestion')
        if suggestionObject["status"] and not tableIndexDataObject['status'] and not closenessDataObject['status']:
            # Init variable
            lastSearch = lastSearchWord["word"]
            sortedBooks = dict()
            suggestionBooks = []
            lock = Lock()
            
            print("Last search" , lastSearch)
            if tableIndexDataObject['data'].get(lastSearch)!=None and lastSearch != "":
                # print(jsonify(tableIndexData[word]))
                sortedBooks = dict(sorted(tableIndexDataObject['data'][lastSearch].items(),key=lambda x:x[1], reverse=True))

            def checkCloseness(closenessPos, suggestionBooks, sortedBooks):
                return closenessPos not in suggestionBooks and closenessPos not in list(sortedBooks.keys())

            def getSuggestion(id,closeData):
                lock.acquire()
                if closeData['bookId'] in list(sortedBooks.keys()):
                    if id==0:
                        if checkCloseness(closenessDataObject['data'][id+1]['bookId'] , suggestionBooks, sortedBooks):
                            suggestionBooks.append(closenessDataObject['data'][id+1]['bookId']) 
                    elif id==len(closenessDataObject['data'])-1:
                        if checkCloseness(closenessDataObject['data'][id-1]['bookId'] , suggestionBooks, sortedBooks):
                            suggestionBooks.append(closenessDataObject['data'][id-1]['bookId']) 
                    else:
                        if checkCloseness(closenessDataObject['data'][id+1]['bookId'] , suggestionBooks, sortedBooks):
                            suggestionBooks.append(closenessDataObject['data'][id+1]['bookId']) 
                        if checkCloseness(closenessDataObject['data'][id-1]['bookId'] , suggestionBooks, sortedBooks):
                            suggestionBooks.append(closenessDataObject['data'][id-1]['bookId']) 
                lock.release()

            print("START thread getSuggestion")
            threaded_start = time.time()
            # booksData = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for id,closeData in enumerate(closenessDataObject['data']):
                    futures.append(executor.submit(getSuggestion, id,closeData))
            print("END thread getSuggestion", time.time() - threaded_start)

            suggestionObject["data"] = getBooksData(suggestionBooks)     
            suggestionObject["status"] = False
        print('END ROUTE suggestion')
        return jsonify(suggestionObject["data"])
    
    #############################################
    # ---------- GET WITH PARAMETERS ---------- #
    #############################################

    # find book with keyword
    @app.route('/searchbook/<word>', methods=['GET'])
    def search_books(word):
        print("Running search_books POST")
        if not tableIndexDataObject['status']:
            if tableIndexDataObject['data'].get(word)!=None:
                # print(jsonify(tableIndexData[word]))
                sortedBooks = dict(sorted(tableIndexDataObject['data'][word].items(),key=lambda x:x[1], reverse=True))
                bookData =  getBooksData(sortedBooks.keys())
                return jsonify(bookData)
            else:
                return "NOT_FOUND"
        return "NO TABLE INDEX AVAILABLE"
    
    @app.route('/readbookcontent/<bookId>')
    def read_book_content(bookId):
        print("RUN ROUTE readbookcontent")
        if lastReadingBook['bookId'] != bookId:
            book_data = getBooksThread(bookId)
            for format in book_data['formats'].keys():
                if '.htm' in book_data['formats'][format]:
                    lastReadingBook['link'] = book_data['formats'][format]
                    response_API = requests.get(book_data['formats'][format])
                    lastReadingBook['data'] = response_API.text
                elif '.html.images' in book_data['formats'][format]:
                    lastReadingBook['link'] = book_data['formats'][format]
                    response_API = requests.get(book_data['formats'][format])
                    lastReadingBook['data'] = response_API.text
                    
            lastReadingBook['bookId'] = bookId

        pattern = re.compile(r'<body>(.*?)</body>', re.DOTALL)
        result = re.search(pattern, lastReadingBook['data'])

        if result:
            body_content = result.group(1)
            replace_image = body_content.replace('images/', 'https://www.gutenberg.org/cache/epub/{}/images/'.format(bookId))
            # print(body_content)
            lastReadingBook['data'] = replace_image
        print("END ROUTE readbookcontent")
        return jsonify({ "link": lastReadingBook['link'],'textHtml' : lastReadingBook['data']})
        


    ##############################
    # ---------- POST ---------- #
    ##############################
    # send search data
    @app.route('/searchdata', methods=['POST', 'GET'])
    @cross_origin(origin='*',headers=['content-type'])
    def search_data():
        print("Running search_data with keyword")
        if request.method == 'POST':
            word = request.json['word']
            lowerWord = word.lower()
            lastSearchWord["word"] = lowerWord
            if lowerWord in historyWords:
                historyWords[lowerWord] += 1
            else:
                historyWords[lowerWord] = 1
            lastSearchObject["status"] = True
            suggestionObject["status"] = True
            rankingObject["status"] = True
        return jsonify(historyWords)
    
    @app.route('/clickedbooks', methods=['POST','GET'])
    @cross_origin(origin='*',headers=['content-type'])
    def clicked_books():
        print("RUN ROUTE clicked_books")
        if request.method == 'POST':
            bookId = request.json['bookId']
            # lastSearchWord["word"] = lowerWord
            if bookId in clickedBooks:
                clickedBooks[bookId] += 1
            else:
                clickedBooks[bookId] = 1
            mostReadObject["status"] = True
        print("END ROUTE clicked_books")
        return jsonify(clickedBooks)
    
    #################################################
    # ---------- SHOW SOME DATA TO CHECK ---------- #
    #################################################

    # get all list of index
    @app.route('/tindex', methods=['GET'])
    def tindex():
        return jsonify(tableIndexDataObject['data'])
    

    ###########################################
    # ---------- NOT USING FOR NOW ---------- #
    ###########################################

    # get table index for each book
    @app.route('/itbook', methods=['GET'])
    def itbook():
        return jsonify(booksInfoObject['data'])

    # Use Jaccard to have list of book suggestion and order it
    @app.route('/jaccard', methods=['GET'])
    def jaccard():
        booksData = jaccardSimilarity(historyWords,booksInfoObject['data'])

        # sortedBooks = sorted(booksData, key=lambda d: d['jaccard'], reverse=True) 
        sendBookId = []
        for sb in booksData:
            if sb['jaccard'] > 0:
                sendBookId.append(sb['bookId'])
        top5 = sendBookId.slice(0,5)  if len(sendBookId) > 5 else sendBookId
        ranking = getBooksData(top5)
        # print(booksData)
        return jsonify(ranking)
        # return jsonify(sendBookId, booksData, historyWords)
            
    return app

app = create_app(debug=True)
if __name__ == "__main__" :
    app.run()