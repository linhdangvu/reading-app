import re

# opening of 56667 or history of babylon
with open("history_of_babylon.txt",mode ="r",encoding = "utf_8") as babylon_file:

    # création d'un tableau de ligne de données
    t = []
    

    # conversion d'un fichier txt en str
    content = "\w".join([l.rstrip() for l in babylon_file])


    #-------------MARCHE PAS BIEN !-----------------------
    # extraction des données mots par mots
    # t1 = re.findall("[^A-Za-z]"'\w',content)
    # t2 = re.split("[^A-Za-z]"'\w',content)
    #-------------------------------------------------

    # affiche tt les mots avec des espaces (epsilon sur les automates) 
    # t = re.findall("[A-Za-z]*",content)
 
    # extraction de chaque mot du fichier txt dans un tableau
    t = re.findall("[A-Za-z]+",content) 
    

    # affichage de chaque mot
    #print(t)


    # affichage de chaque mot qui ont <=2 caractères alphabétiques

    for w  in t:

        match = re.search(r'[A-Z]', w)
        if match:
            print(w)
        else:
            print("not found")


        
    
        
        