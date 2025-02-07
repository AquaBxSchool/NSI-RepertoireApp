""" Répertoire téléphonique """

version = "1.3"

"""
Créé Par Tom Chauvel, 8 octobre 2019
Dernière Mise à jour le : 16 octobre 2019

Programme qui permet d'insérer les informations de contacts et les stocker dans un fichier (data.txt).




Une erreur peut survenir car le programme n'arrive pas à ouvrir l'icone de la fenêtre : les lignes 26 et 66 sont alors à supprimer
"""

#------------------------------------------------------ Imports --------------------------------------------------------

from tkinter import *
from tkinter.messagebox import *
import webbrowser

#-------------------------------------------------- Initialisation -----------------------------------------------------

window = Tk()
#window.iconbitmap("@rep.ico")
window.title('Répertoire : v'+version)
window.resizable(width=False,height=False)

frame=LabelFrame()
scrollbar = Scrollbar(frame)
list_boutons = Listbox(window, width=80,height=1, font='Courier')
affichage_rep = Listbox(frame, width=80,height=20, font='Courier',yscrollcommand=scrollbar.set) #Zone ou s'affiche le répertoire
scrollbar.config(command=affichage_rep.yview)
scrollbar.pack(side = RIGHT, fill=Y)
affichage_rep.pack(side=LEFT)
Label(window, text= "{:^15}|{:^15}|{:^15}|{:^32}".format("Nom","Prénom","Numéro","Adresse"), font='Courier').grid(row=0, column=0,padx=5, pady=5) #Zone ou s'affiche les catégories
frame.grid(row=1, column=0,padx=5, pady=0)
list_boutons.grid(row=2, column=0,padx=5, pady=5)

try:
    with open("data.txt"): pass #vérifie que le fichier existe
except:
    fichier = open("data.txt", "w") #sinon il le créé

with open("data.txt", "r") as fichier: #transforme le fichier en liste
    listes = fichier.read().split("/") #sépare les str entre des / pour les ajouter dans une liste
    if listes[0] == "" : #vérifie que le premier membre de la liste est vide (obligatoirement si le fichier est vide)
        del listes[0]
    repertoire = []
    if len(listes) != 0 : #vérifie que la liste n'est pas vide
        for item in listes: #pour chaque valeur dans "listes"
            repertoire.append(item.split(",")) #ajoute dans une liste dans repertoire les sous listes de "listes"

#----------------------------------------------------- Fonctions -------------------------------------------------------

def afficher_repertoire(): #affiche le répertoire
    affichage_rep.delete(0, END) #réinitialise la fenêtre
    if len(repertoire) != 0 : #vérifie que la liste comporte un élément
        for i in range(len(repertoire)): #pour chaque élément dans la liste
            affichage_rep.insert(END, "{:^15}|{:^15}|{:^15}|{:^32}".format(repertoire[i][0],repertoire[i][1],repertoire[i][2],repertoire[i][3])) #affiche en ligne les valeurs de la liste

def mod_repertoire(): #ajoute ou modifie un contact
    winadd = Tk()
    winadd.resizable(width=False,height=False)
    #winadd.iconbitmap("@rep.ico")
    try:
        affichage_rep.curselection()[0] #test si une ligne est sélectionnée
        winadd.title('Modifier')
    except :
        winadd.title('Ajouter')
    def send(nom,prenom,numero,adresse): #fonction qui traite les données collecter
        try: #try qui regarde si c'est une modification
            id = affichage_rep.curselection()[0] #test si une ligne est sélectionnée
            if nom.get() != "": #si la case est vide il ne modifie pas
                repertoire[id][0] = nom.get()
            if prenom.get() != "": #si la case est vide il ne modifie pas
                repertoire[id][1] = prenom.get()
            if numero.get() != "": #si la case est vide il ne modifie pas
                repertoire[id][2] = numero.get()
            if adresse.get() != "": #si la case est vide il ne modifie pas
                repertoire[id][3] = adresse.get()
            rep_m() #modifie fichier
            winadd.destroy() #ferme la fenêtre
        except: #sinon c'est un ajout
            if nom.get() and prenom.get() != "" : #si nom et prénom remplis
                repertoire.append([nom.get(),prenom.get(),numero.get(),adresse.get()]) #ajout des valeurs à la liste
                rep_m() #modifie fichier
                winadd.destroy() #ferme la fenêtre
            else:
                showerror('Erreur', 'Veuillez remplir au moins le nom et le prénom du contact') #sinon erreur
                winadd.destroy()

    #contenu de la fenêtre
    Label(winadd, text="Nom du contact ").grid(row=0, column=0,padx=40, pady=5)
    nom = Entry(winadd)
    nom.grid(row=1, column=0,padx=40, pady=5)
    Label(winadd, text="Prenom du contact ").grid(row=2, column=0,padx=40, pady=5)
    prenom = Entry(winadd)
    prenom.grid(row=3, column=0,padx=40, pady=5)
    Label(winadd, text="Numero du contact ").grid(row=4, column=0,padx=40, pady=5)
    numero = Entry(winadd)
    numero.grid(row=5, column=0,padx=40, pady=5)
    Label(winadd, text="Adresse (ou coordonnées gps) du contact ").grid(row=6, column=0,padx=40, pady=5)
    adresse = Entry(winadd)
    adresse.grid(row=7, column=0,padx=40, pady=5)
    Button(winadd,text = "Envoyer", command=lambda : send(nom,prenom,numero,adresse)).grid(row=8, column=0,padx=40, pady=5) #bouton avec fonction send qui envoie les données
    winadd.mainloop()

def rep_m(): #fonction qui modifie le fichier
    with open("data.txt", "w") as fichier : #ouvre le fichier data et l'écrase
        j=1
        for item in repertoire: #pour chaque objet dans la liste
            i=0
            for objet in item: #for pour écrire dans le fichier sans qu'il ne rajoute une virgule à la fin et qu'il rajoute un str dans la liste : "bonjour", "je suis", "tom" / "bonjour", "je suis", "tom", ""
                if i < 3:
                    fichier.write(objet + ",")
                else :
                    fichier.write(objet)
                i+=1
            if len(repertoire) > j: #si le nombre d'objet dans la liste est supérieur à j il écrit un '/' : sinon il sortira une erreur
                fichier.write("/")
            j+=1

    afficher_repertoire() #réinitialise la fenêtre

def del_to_repertoire(): #fonction qui supprime un contact dans la liste
    try:
        line = affichage_rep.curselection()[0]
        del repertoire[line] #supprime dans la liste l'élement sélectionné
        rep_m() #sauvegarde dans le fichier
    except:
        print("erreur : pas de sélection")

def open_map():
    try:
        id = affichage_rep.curselection()[0] #vérifie si une ligne est sélectionnée
        if repertoire[id][3] != "": #vérifie qu'il y a une adresse
            webbrowser.open("http://google.com/maps?q=" + repertoire[id][3]) #ouvre une fenêtre du navigateur pour situer le domicile du contact
        else :
            showerror('Erreur', 'Veuillez ajouter l\'adresse de votre contact ') #sinon erreur
    except:
        print("erreur : pas de sélection")

#-------------------------------------------------- Code principal -----------------------------------------------------

#Boutons
button0 = Button(list_boutons,text = "Ajouter️/Modifier", command = lambda :  mod_repertoire()).grid(row=0, column=0)
button1 = Button(list_boutons,text = "Supprimer", command = lambda :  del_to_repertoire()).grid(row=0, column=1)
button2 = Button(list_boutons,text = "Maps", command = lambda :  open_map()).grid(row=0, column=2)
list_boutons.insert(END, button0,button1,button2)

afficher_repertoire() #affiche le répertoire

window.mainloop()
