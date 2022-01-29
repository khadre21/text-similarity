#from cProfile import label
from tkinter import *
import menu_fonctionalities


#creer 1er fenetre
window = Tk()
#personnalisation
window.title("Anti_fake_news")
window.geometry("1180x650")
window.minsize(480,360)
window.resizable(False,False)
window.iconbitmap("fn.ico")
window.config(background="#1DB786")


acceuil_canvas = Canvas(window, bd=0, highlightthickness=0)
acceuil_canvas.place(x=0, y=0)
acceuil_canvas.config(background="#1DB786")
#creation de frame
frame =Frame(acceuil_canvas, bg='#1DB786')
#ajouter du text
Label_title = Label(frame, text="\n\nBIENVENUE SUR LE PLATEFORME ANTI-FAKE NEWS",
                    font =("Ubuntu Condensed",21),bg='#1DB786',fg="white")
Label_2title = Label(frame, text="plateforme conçu pour detecter les fake news en déterminant le pourcentage de simularité  " ,
                    font =("Ubuntu Condensed",11),bg='#1DB786',fg="white")
Label_title.pack()
Label_2title.pack()
#creation image
width = 250
height =250
image = PhotoImage(file="fn.png").zoom(20).subsample(50)
canvas = Canvas(acceuil_canvas,width=width,height=height,bg="#1DB786",bd=0,highlightthickness=0)
canvas.create_image(width/2,height/2,image=image)
#ajout des frames
frame.grid(row=1,column=0, ipadx=200, columnspan=4, pady=30, sticky=W+E+N+S)
canvas.grid(row=2,column=1, columnspan=2, padx=100, pady=20)

# Définition des différents canvas du menu:
canvas_of_menu1 = Canvas(window, bd=0, highlightthickness=0, width=1162, height=633, bg='#1DB786')
canvas_of_menu2 = Canvas(window, bd=0, highlightthickness=0, width=1162, height=633, bg='#1DB786')
canvas_of_menu3 = Canvas(window, bd=0, highlightthickness=0, width=1162, height=633, bg='#1DB786')

# Définirion des différentes fonctionnalités du menu
menu_bar = Menu(window)
menu_bar.add_command(label='Détection de fake news', command= lambda : menu_fonctionalities.detection_fakeNews(
                                                                            window, acceuil_canvas, canvas_of_menu1,
                                                                            canvas_of_menu2, canvas_of_menu3
                                                                        ))
menu_bar.add_command(label='Similarité Cosinus', command= lambda : menu_fonctionalities.similarite_cosinus(
                                                                            window, acceuil_canvas, canvas_of_menu1,
                                                                            canvas_of_menu2, canvas_of_menu3
                                                                        ))
menu_bar.add_command(label='Similarité Livenshtein',  command= lambda : menu_fonctionalities.similarite_livenshtein(
                                                                            window, acceuil_canvas, canvas_of_menu1,
                                                                            canvas_of_menu2, canvas_of_menu3
                                                                        ))
window.config(menu=menu_bar)

#affichage fenetre
window.mainloop()


