<<<<<<< HEAD
import string
import Levenshtein as lev
import book

from nltk.corpus import stopwords


user_article = '''
In the first volume of this work an account was given of the early
races of Babylonia from prehistoric times to the foundation of the
monarchy. It closed at the point when the city of Babylon was about
to secure the permanent leadership under her dynasty of West-Semitic
kings. The present volume describes the fortunes of Babylonia during
the whole of the dynastic period, and it completes the history of
the southern kingdom. Last autumn, in consequence of the war, it
was decided to postpone its publication; but, at the request of the
publishers, I have now finished it and seen it through the press. At
a time when British troops are in occupation of Southern Mesopotamia,
the appearance of a work upon its earlier history may perhaps not be
considered altogether inopportune.
'''

tags = ['Levenshtein distance']

def fetch_book_data(tags):
    '''
    The purpose of this function is to get the book data associated to a certain user
    input tag.
    
    params:
        tag (String) : The item you want to seach book for
        
    returns:
        This function will return the contents associated to the user specified tag
    
    example:
        tag = 'Levenshtein distance'
        fetch_book_data(tag)
        >> In information theory, linguistics, and computer science, the Levenshtein distance 
           is a string metric...
    '''
    content = {}
    for tag in tags:
        # get book data for the tag
        book_tag = book.search(tag)

        # get page info
        page = book.page(book_tag[0])

        # get page content
        content[tag] = page.content
    return content

tag_content = fetch_book_data(tags)


def remove_punctuations(txt, punct = string.punctuation):
    '''
    This function will remove punctuations from the input text
    '''
    return ''.join([c for c in txt if c not in punct])
  
def remove_stopwords(txt, sw = list(stopwords.words('english'))):
    '''
    This function will remove the stopwords from the input txt
    '''
    return ' '.join([b for b in txt.split() if b.lower() not in sw])

def clean_text(txt):
    '''
    This function will clean the text being passed by removing specific line feed characters
    like '\n', '\r', and '\'
    '''
    
    txt = txt.replace('\n', ' ').replace('\r', ' ').replace('\'', '')
    txt = remove_punctuations(txt)
    txt = remove_stopwords(txt)
    return txt.lower()
  
user_article = clean_text(user_article) 
for tag, content in tag_content.items():
    tag_content[tag] = clean_text(content)
    
def similarity(user_article, tag_content):
    '''
    This function will identify the similarities between the user_article and all the
    content within tag_content
    
    params:
        user_article (String) : The text submitted by the user
        tag_content (Dictionary) : Key is the tag and the value is the content you want 
                                   to compare with the user_article
    
    returns:
        This function will return a dictionary holding the Levenshtein assocaited to the 
        user_article with each tag_content
    '''
    
    distances = {}
    for tag,content in tag_content.items():
        dist = lev.distance(user_article, content)
        distances[tag] = dist
    return distances
  
distances = similarity(user_article, tag_content)

def is_plagiarism(user_article, tag_content, distances, th = 0.4):
    '''
    This function will identify if the user_article is considered plagiarized for each
    of the tag_content based on the distances observed.
    
    params:
        user_article (String) : The text submitted by the user
        tag_content (Dictionary) : Key is the tag and the value is the content you want 
                                   to compare with the user_article
        distances (Dictionary) : Key is the tag and the value is the Levenshtein distance 
        th (Float) : The plagiarism threshold
    
    returns:
        A dictionary associated to the plagiarism percentage for each tag
    '''
    ua_len = len(user_article)
    distances = {tag:[d, max(ua_len, len(tag_content[tag]))] for tag,d in distances.items()}
    
    for tag, d in distances.items():
        if d[0] <= d[1] * th:
            distances[tag] = 'Plagiarized'
        else:
            distances[tag] = 'Not Plagiarized'
    return distances
  
is_plagiarism(user_article, tag_content, distances)
=======
def levenshteinDistance(word1, word2):
    N, M = len(word1), len(word2)
    # Create an array of size NxM
    dp = [[0 for i in range(M + 1)] for j in range(N + 1)]

    # Fill 01234... to array
    for j in range(M + 1):
        dp[0][j] = j
    for i in range(N + 1):
        dp[i][0] = i
   
    # Transitions
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j], # Insertion
                    dp[i][j-1], # Deletion
                    dp[i-1][j-1] # Replacement
                )
    return dp[N][M]
>>>>>>> main
