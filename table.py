from tkinter import *  
from tkinter import ttk
from etudeSimilarite import *


def detection():
    dialogBoite = Tk()
    label = Label(dialogBoite, text="Choisissez entre la méthode de similarité de Cosinus ou celui de Livenshtein \n")
    label.grid(row=0, column=1, padx=5)
    bouton1 = Button(dialogBoite, text='similarité cosinus')
    bouton1.pack(padx=100, side=LEFT)

    bouton2 = Button(dialogBoite, text='similarité livenshtein', command=dialogBoite.destroy)
    bouton2.pack(padx=10, side=LEFT)

    dialogBoite.mainloop()

class Table:
    def __init__(self, window, canvas,textOriginel , donnees, typeSimilarity):
        self.window = window
        self.canvas = canvas
        #frame.grid_forget()
        """self.canvas = Canvas(self.canvas, width=1240, height=5000, confine=FALSE, bd=0,highlightthickness=0)
        self.canvas.place(x=0, y=0)"""
        self.textOriginel = textOriginel
        self.donnees = donnees
        self.typeSimilarity = typeSimilarity
        self.item0 = '1er item de chaque ligne'
        self.item1 = '2ème item de chaque ligne'
        self.entete = 'en tete de la table'

    def create_table(self):
        content = Frame(self.canvas, bg='#1DB786')
        self.canvas.create_window((0,630), window=content, anchor='nw')

        entete = Frame(content, bg='#1DB786')
        entete.grid(row=0, column=0)
        self.item0 = Text(entete, width=73, height=15, bd=0, bg='#1DB786')
        self.item0.grid(row=0, column=0)
        self.item0.insert(1.0, ' ')
        self.item0.config(state='disabled')
        self.item1 = Text(entete, width=68, height=15, bg='#fff')
        self.item1.grid(row=0, column=1, ipadx=2)
        self.item1.insert(1.0, self.textOriginel)
        self.item1.config(state='disabled')
        scrollbar = ttk.Scrollbar(entete, orient='vertical', command=self.item1.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.item1['yscrollcommand'] = scrollbar.set

        self.canvas.config(scrollregion=(0,0, 1162, 630+243))
        
        i = 1 
        for donnee in self.donnees:
            frame = Frame(content)
            frame.grid(row=i, column=0)
            
            self.item0 = Text(frame, width=72, height=15)
            self.item0.grid(row=0, column=0)
            self.item0.insert(1.0, donnee[0])
            self.item0.config(state='disabled')
            scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.item0.yview)
            scrollbar.grid(row=0, column=1, sticky='ns')
            self.item0['yscrollcommand'] = scrollbar.set
            self.item1 = Text(frame, width=71, height=15)
            self.item1.grid(row=0, column=2)
            if(self.typeSimilarity == 'cosinus'):
                self.item1.insert(5.0, 'Le pourcentage de Cosinus entre ces deux textes est de: {}'.format(donnee[1]))
            if(self.typeSimilarity == 'livenshtein'):
                self.item1.insert(5.0, 'La distance de Livenshtein entre ces deux textes est de: {}'.format(donnee[1]))
            self.item1.config(state='disabled')
            
            self.canvas.config(scrollregion=(0,0, 1162, 630+(i+1)*243))
            
            if(i%2 != 0):
                self.item0.config(bg="#729fcf")
                self.item1.config(bg="#729fcf")
            else:
                self.item0.config(bg="#babdb6")
                self.item1.config(bg="#babdb6")
            i += 1

'''window = Tk()
window.geometry("1240x650")
window.minsize(480,360)
texte = ['Projet De Fin De Cycle Projet De Fin De Cycle ' + 'Projet De Fin De Cycle Projet De Fin De Cycle ' +
    'Projet De Fin De Cycle Projet De Fin De Cycle ' + 'Projet De Fin De Cycle Projet De Fin De Cycle '+
    'Projet De Fin De Cycle Projet De Fin De Cycle ' + 'Projet De Fin De Cycle Projet De Fin De Cycle '+
    'Projet De Fin De Cycle Projet De Fin De Cycle '+ 'Projet De Fin De CycleP rojet De Fin De Cycle']
data_liste = [texte, texte, texte, texte]
table = Table(window, texte, data_liste)
table.create_table()

window.mainloop()'''

"""
    def detection():
    dialogBoite = Tk()
    label = Label(dialogBoite, text="Choisissez entre la méthode de similarité de Cosinus ou celui de Livenshtein \n")
    label.grid(row=0, column=1, padx=5)
    bouton1 = Button(dialogBoite, text='similarité cosinus')
    bouton1.pack(padx=100, side=LEFT)

    bouton2 = Button(dialogBoite, text='similarité livenshtein', command=dialogBoite.destroy)
    bouton2.pack(padx=10, side=LEFT)

    dialogBoite.mainloop()

    def create_table(self):
        frame = Frame(self.canvas, relief=GROOVE, bg='#1DB786')
        frame.grid(row=14, column=0, rowspan=5 , columnspan=3, padx=5)
        self.item0 = Label(frame, text=self.textOriginel, bg='#fff')
        self.item0.pack(side =LEFT, padx=8)
        for donnee in self.donnees:
            i = 1
            for j in range(1,3):

                secondFrame = Frame(self.canvas)
                secondFrame.grid(row=i+24, column=0, rowspan=5 , columnspan=6, padx=5)

                self.item0 = Label(secondFrame, text= donnee, width=150)
                self.item0.pack(side =LEFT, pady=5)
               
                self.item1 = Label(secondFrame, text= donnee, width=100)
                self.item1.pack(side =LEFT, pady=5, padx=8)
                if(i%2 != 0):
                    self.item0.config(bg="#729fcf")
                    self.item1.config(bg="#729fcf")
                else:
                    self.item0.config(bg="#babdb6")
                    self.item1.config(bg="#babdb6")
                i += 5

"""