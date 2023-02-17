from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import logging
import re

logging.basicConfig(level=logging.INFO)

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

listBooks = [49345,56667,1,2,3,4,5,6,7]
counts = dict()
word2letters = dict()
word3letters = dict()
tableIndex = dict()



# get table index
def getTableIndex(listBooks, counts, word2letters,word3letters,tableIndex):
    for book in listBooks:
        response_API = requests.get('https://www.gutenberg.org/files/{bookId}/{bookId}-0.txt'.format(bookId=book))
        data = response_API.text
        #### Option 1
        words = re.findall(r"[A-Za-z]{4,10}", data)
        for word in words:
            w = word.lower()
            if w in tableIndex:
                if book not in tableIndex[w]:
                    tableIndex[w] += [book]
            else:
                tableIndex[w] = [book]

        #### Option 2
        # words = re.findall(r"[A-Za-z]+", data) 
            # if len(w) <= 2:
            #     if w in word2letters:
            #         word2letters[w] += 1
            #     else:
            #         word2letters[w] = 1
            # elif len(w) == 3:
            #     if w in word3letters:
            #         word3letters[w] += 1
            #     else:
            #         word3letters[w] = 1
            # else:
            #     if w in counts:
            #         counts[w] += 1
            #     else:
            #         counts[w] = 1
            #     if w in tableIndex:
            #         if book not in tableIndex[w]:
            #             tableIndex[w] += [book]
            #     else:
            #         tableIndex[w] = [book]

    # print("Book ID: ", book)
    # print("Total word different: ", len(counts))
    # #print("sargon: " , counts["sargon"])
    # print("List 2 lettres: ",len(word2letters))
    # print("List 3 lettres: ",len(word3letters))
    # print(tableIndex)
    return tableIndex

tableIndexData = getTableIndex(listBooks, counts, word2letters,word3letters,tableIndex)

def getBooksData(listBooks):
    booksData = []
    for book in listBooks:
        response_API = requests.get('https://gutendex.com/books/{}'.format(book))
        #print(response_API.status_code)
        data = response_API.text
        parse_json = json.loads(data)
        booksData.append(parse_json)
    return booksData

# try to get only 10 book
@app.route('/getbooks', methods=['GET'])
def get_books():
    data = getBooksData(listBooks)
    return jsonify(data)

@app.route('/searchbook/<word>', methods=['GET'])
def search_books(word):
    # tableIndexData = getTableIndex(listBooks, counts, word2letters,word3letters,tableIndex)
    if tableIndexData.get(word)!=None:
        print(jsonify(tableIndexData[word]))
        bookData =  getBooksData(tableIndexData[word])
        return jsonify(bookData)
    else:
        return "NOT_FOUND"


@app.route('/tests/<bookId>/<word>', methods=['GET'])
def tests(bookId, word):
    print(id)
    return jsonify(bookId, word)

if __name__ == '__main__':
    app.run()