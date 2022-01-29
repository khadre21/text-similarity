import unidecode
import hashlib
import sqlite3
from datetime import *


conn = sqlite3.connect('data_base.db')
curseur = conn.cursor()
curseur.execute(
    """
    CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        hash VARCHAR(64),
        texteOriginale TEXT,
        texteModifiee TEXT,
        date DATE
    )
    """
)
conn.commit()
conn.close()

'''conn = sqlite3.connect('data_base.db')
curseur = conn.cursor()
curseur.execute(
    """
    DELETE FROM documents 
    WHERE id=?
    """, (47,)
)
conn.commit()
conn.close()'''

class PreTraitement:

    def __init__(self, doc):
        self.doc = doc
        self.textOriginel = doc
        self.textModifie = self.preTraitement()

    def deleteSmallWords(self):
        self.doc = self.doc.split(" ") if type(self.doc) != list else self. doc

        # Cette boucle est ajoutée pour supprimer les eventuels caractères \n de *retour à la ligne* présents
        # sur certaines chaines de caractères lors de la récupèration d'informations sur les bases de données
        for word in self.doc:
            indice = self.doc.index(word)
            word = word.split("\n")
            if len(word) == 2: 
                self.doc[indice] = word[0]
                    
        for word in self.doc:
            # Si un mot est en effet constitué d'une lettre et un autre mot séparés par une 
            # apostrophe alors on supprime cette lettre et on considère seulement le deuxième mot 
            indice = self.doc.index(word)
            word = word.split("'")
            if len(word) == 2: 
                self.doc[indice] = word[1]
        
        for word in self.doc:
            if(len(word) > 1):
                if(word[len(word)-1]==',' or word[len(word)-1]==':' or word[len(word)-1]=='.'
                        or word[len(word)-1]=='!' or word[len(word)-1]=='?'):
                    indice = self.doc.index(word)
                    self.doc[indice] = word[:len(word)-1]

        # Suppression des mots composés de moins de 3 lettres
        for word in self.doc:   
            if len(word) <= 3:
                indice = self.doc.index(word)
                del self.doc[indice]

        return self.doc


    # Elimination des caractères accentués
    # Laisser tous les mots en minuscule
    def unidecodeAndLowerCase(self):
        for word in self.deleteSmallWords():
            indice = self.doc.index(word)
            self.doc[indice] = unidecode.unidecode(self.doc[indice])

        for word in self.doc:
            indice = self.doc.index(word)
            self.doc[indice] = self.doc[indice].lower()  

    # Fonction à utiliser seulement pour le corpus ie l'ensemble des mots 
    # des deux textes et non pas pour chaque texte individuellement
    def deleteRepetedWords(self):
        self.unidecodeAndLowerCase()
        for word in self.doc:
            indice = self.doc.index(word)
            i = indice + 1
            while(i < len(self.doc)):
                if word == self.doc[i]:
                    del self.doc[i]
                else:
                    i += 1 

    # Suppresion des mots répétés plusieurs fois
    # Ordonner les mots
    def ordonnerLesMots(self):
        self.deleteRepetedWords()
        self.doc.sort() # Ordonnancement des mots


    def preTraitement(self):
        self.ordonnerLesMots()
        return ' '.join(self.doc)


    def hashage(self):
        h = hashlib.sha256(str(self.textModifie).encode('utf-8'))
        return h.hexdigest()


    def stockage(self):
        conn = sqlite3.connect('data_base.db')
        curseur = conn.cursor()
        document =(self.hashage(), self.textOriginel, self.textModifie, date.today())
        curseur.execute("""INSERT INTO documents( hash, texteOriginale, texteModifiee, date) 
                           VALUES(?, ?, ?, ?)""", document)
        conn.commit()
        conn.close()


    
