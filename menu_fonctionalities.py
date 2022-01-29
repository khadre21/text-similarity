from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import *
from pretraitement import *
from etudeSimilarite import *
from table import *
import sqlite3


def comparaison_by_cosinus(window, canvas, texte_a_comparer, seuil):
    data_liste = []
    conn = sqlite3.connect('data_base.db')
    curseur = conn.cursor()
    curseur.execute('''SELECT texteOriginale, texteModifiee FROM documents''')
    resultats = curseur.fetchall()
    i = 0
    while i < len(resultats)-1:
        s = Similarite(texte_a_comparer, resultats[i][1])
        if(s.sim_cosinus()*100 >= int(seuil)):
            data_liste.append([resultats[i][0], s.sim_cosinus()*100])
        i += 1
    table = Table(window, canvas, texte_a_comparer, data_liste, 'cosinus')
    table.create_table()
    conn.close()

def comparaison_by_livenshtein(window, canvas, texte_a_comparer, seuil):
    data_liste = []
    conn = sqlite3.connect('data_base.db')
    curseur = conn.cursor()
    curseur.execute('''SELECT texteOriginale, texteModifiee FROM documents''')
    resultats = curseur.fetchall()
    i = 0
    while i < len(resultats)-1:
        s = Similarite(texte_a_comparer, resultats[i][1])
        if(s.sim_cosinus()*100 >= int(seuil)):
                data_liste.append([resultats[i][0], s.sim_livenshtein()])
        i += 1
    table = Table(window, canvas, texte_a_comparer, data_liste, 'livenshtein')
    table.create_table()
    conn.close()       
    

def when_seuil_is_defined(window, canvas, frame_content, textOrigine, seuil):

    label3 = Label(frame_content, text='Veuiller choisir entre les deux méthodes de calcul de similarité',
                    font =("Ubuntu Condensed",11), bg='#1DB786', fg="white")
    label3.grid(row=11, column=0, columnspan=3, padx=3, pady=3, sticky=W)

    similarite_cos_btn = Button(frame_content, text='Similarité Cosinus', 
                                command = lambda: comparaison_by_cosinus(window, canvas, textOrigine, seuil))
    similarite_cos_btn.grid(row=12, column=1, ipadx=20, pady=5, sticky=E)

    similarite_lev_btn = Button(frame_content, text='Similarité Levenshtein',
                                command = lambda: comparaison_by_livenshtein(window, canvas, textOrigine, seuil))
    similarite_lev_btn.grid(row=12, column=2, columnspan=2, pady=5, ipadx=5, sticky=E)

def verifier(window, canvas, text):
    pretraitement = PreTraitement(text)
    hash = pretraitement.hashage()
    
    conn = sqlite3.connect('data_base.db')
    curseur = conn.cursor()
    curseur.execute('''SELECT date FROM documents
                                 WHERE hash=?''', (hash, ))
    result = curseur.fetchone()
    conn.close()

    if(result):
        messagebox.showwarning('Alerte', "ce texte s'agit bien d'une fake news! Il a déjà été publié le "+ str(result[0]))
    else:
        content = Frame(canvas, bg="#1DB786")
        canvas.create_window((0,475), window=content, anchor='nw')
        label1 = Label(content, text="Veuillez définir une seuil de confiance pour vérifier s'il exite déjà " +
                                    "dans la base de données", font =("Ubuntu Condensed",11), bg='#1DB786', fg="white")
        label1.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=W)
        label2 = Label(content, text="des textes trés similaire à ce texte:", font =("Ubuntu Condensed",11),
                       bg='#1DB786', fg="white")
        label2.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        seuil = Entry(content)
        seuil.insert(0, '0')
        seuil.grid(row=1, column=2, padx=6, pady=5, sticky=W)
        seuil_btn = Button(content, text='Aplliquer', command = lambda: when_seuil_is_defined(window, canvas, content, text, seuil.get()))
        seuil_btn.grid(row=1, column=3, ipadx=17, pady=3, sticky=E)

        pretraitement.stockage()
    
# Fonction métier du premier onglet du menu principal
def detection_fakeNews(window,canvas_acceuil, canvas_of_menu1, canvas_of_menu2, canvas_of_menu3):
    # Dactivation du contenu des frame des autres éléments de menu qui ne sont pas indéxés
    canvas_acceuil.place_forget()
    canvas_of_menu2.grid_forget()
    canvas_of_menu3.grid_forget()

    canvas_of_menu1.grid(row=0, column=0, sticky='ew')
    scrollbar = ttk.Scrollbar(window, orient='vertical', command=canvas_of_menu1.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    canvas_of_menu1.config(scrollregion=(0,0, 1162, 670))
    canvas_of_menu1['yscrollcommand'] = scrollbar.set
    
    frameInputText = Frame(canvas_of_menu1, bg="#1DB786")
    canvas_of_menu1.create_window((0,0), window=frameInputText, anchor='nw')
    
    label = Label(frameInputText, text='Veuillez saisir ici le texte à vérifier :',
                  font =("Ubuntu Condensed",11), bg='#1DB786', fg='white')
    label.grid(row=0, column=0, columnspan=2, pady=8, sticky=W)              
    text = Text(frameInputText)
    text.grid(row=1, column=0, rowspan=5, columnspan=5, padx=5, ipadx=15, pady=5, sticky=W)
    
    btn_verification = Button(frameInputText, text='Vérifier',
                               command = lambda: verifier(window, canvas_of_menu1, text.get(1.0, END)))
    btn_verification.grid(row=6, column=4, pady=5, ipadx=25, sticky=E)
    

def etude_similarite(frame, texte1, texte2, similarity_type):
    s = Similarite(texte1, texte2)
    if(similarity_type == 'cosinus'):
        sim = s.sim_cosinus() * 100
    if(similarity_type == 'livenshtein'):
        sim = 100 - s.sim_livenshtein()
    label3 = Label(frame, text="Le pourcrntage de similarité entre ces deux textes est de {} %".format(sim),
                   font =("Ubuntu Condensed",11), bg='#1DB786', fg='white')
    label3.grid(row=5, column=0, pady=8, sticky='w')

# Fonction métier du deuxième onglet du menu principal
def similarite_cosinus(window,canvas_acceuil, canvas_of_menu1, canvas_of_menu2, canvas_of_menu3):
    # Dactivation du contenu des frame des autres éléments de menu qui ne sont pas indéxés
    canvas_acceuil.place_forget()
    canvas_of_menu1.grid_forget()
    canvas_of_menu3.grid_forget()

    canvas_of_menu2.grid(row=0, column=0, sticky='ew')
    scrollbar = ttk.Scrollbar(window, orient='vertical', command=canvas_of_menu2.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    canvas_of_menu2.config(scrollregion=(0,0, 1162, 1000))
    canvas_of_menu2['yscrollcommand'] = scrollbar.set

    frame = Frame(canvas_of_menu2, bg="#1DB786")
    canvas_of_menu2.create_window((0,0), window=frame, anchor='nw')
    label1 = Label(frame, text='Veuillez saisir ici le premier texte:',
                   font =("Ubuntu Condensed",11), bg='#1DB786', fg='white')
    label1.grid(row=0, column=0, pady=8, sticky='w')
    texte1 = Text(frame)
    texte1.grid(row=1, column=0, padx=11)
    label2 = Label(frame, text='Veuillez saisir ici le premier texte:',
                   font =("Ubuntu Condensed",11), bg='#1DB786', fg='white')
    label2.grid(row=2, column=0, pady=15, sticky='w')
    texte2 = Text(frame)
    texte2.grid(row=3, column=0, padx=11)

    btn = Button(frame, text='Etude Similarité', command= lambda: etude_similarite(frame, texte1.get(1.0, END),
                                                                                   texte2.get(1.0, END), 'cosinus'))
    btn.grid(row=4, column=0, pady=5, sticky='e')


def similarite_livenshtein(window,canvas_acceuil, canvas_of_menu1, canvas_of_menu2, canvas_of_menu3):
    # Dactivation du contenu des frame des autres éléments de menu qui ne sont pas indéxés
    canvas_acceuil.place_forget()
    canvas_of_menu1.grid_forget()
    canvas_of_menu2.grid_forget()

    canvas_of_menu3.grid(row=0, column=0, sticky='ew')
    scrollbar = ttk.Scrollbar(window, orient='vertical', command=canvas_of_menu3.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    canvas_of_menu3.config(scrollregion=(0,0, 1162, 1000))
    canvas_of_menu3['yscrollcommand'] = scrollbar.set

    frame = Frame(canvas_of_menu3, bg="#1DB786")
    canvas_of_menu3.create_window((0,0), window=frame, anchor='nw')
    label1 = Label(frame, text='Veuillez saisir ici le premier texte:',
                   font =("Ubuntu Condensed",11), bg='#1DB786', fg='white')
    label1.grid(row=0, column=0, pady=8, sticky='w')
    texte1 = Text(frame)
    texte1.grid(row=1, column=0, padx=11)
    label2 = Label(frame, text='Veuillez saisir ici le premier texte:',
                   font =("Ubuntu Condensed",11), bg='#1DB786', fg='white')
    label2.grid(row=2, column=0, pady=15, sticky='w')
    texte2 = Text(frame)
    texte2.grid(row=3, column=0, padx=11)

    btn = Button(frame, text='Etude Similarité', command= lambda: etude_similarite(frame, texte1.get(1.0, END),
                                                                                   texte2.get(1.0, END), 'livenshtein'))
    btn.grid(row=4, column=0, pady=5, sticky='e')

"""window = Tk()
window.geometry("1180x680")
window.minsize(480,360)
canvas_of_menu2 = Canvas(window, bd=0, highlightthickness=0, width=1162, height=633, bg='#1DB786')
similarite_livenshtein(window, 1, 2, 3, canvas_of_menu2)
window.mainloop()"""
