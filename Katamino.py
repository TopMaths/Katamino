# Ce programme est fourni par Top Maths
# sans aucune garantie de fonctionnement
# Vous pouvez l'utiliser à votre guise,
# mais ce serai sympa de me faire de la pub en échange...


from Pieces import Pieces
import tkinter as tk
from Graphe import Grille


# accès à Top Maths
def opentopmaths():
    webbrowser.open_new("https://www.youtube.com/channel/UCZ2eC0-Rwkewu8jD5p_JpLg")

    
    
class Katamino(tk.Tk):
    def DessineVide(self):
        """dessine le tableau vide avec la bonne hauteur"""
        self.Plateau.delete("surdessin")        
        dx,dy=self.Plateau.unit
        ox,oy=self.Plateau.origin
        h=self.nbPieces
        self.Plateau.create_rectangle(ox,oy,ox+5*dx, oy+13*dy, fill="#ccaaaa", tag="surdessin")
        # lignes au dessus de la barre
        for i in range(0,14-h):
            self.Plateau.create_line(ox, oy +  i* dy, ox+ 5 * dx  , oy +  i* dy, tag="surdessin")
        for i in range(0,6):
            self.Plateau.create_line(ox+i*dx, oy , ox+i*dx,  oy+(13-h)*dy, tag="surdessin")
        # la barre de séparation
        self.Plateau.create_rectangle(ox,oy+(12-h)*dy ,ox+5*dx, oy+(13-h)*dy, fill="#fccf99", tag="surdessin")
        # lignes au dessous de la barre
        for i in range(14-h,15):
            self.Plateau.create_line(ox, oy +  i* dy, ox+ 5 * dx  , oy +  i* dy, tags=("surdessin", "dessous"))
        for i in range(0,6):
            self.Plateau.create_line(ox+i*dx, oy+(13-h)*dy , ox+i*dx,  oy+13*dy, tags=("surdessin","dessous"))
        
    def DessineSolution(self):
        """dessine la solution trouvée"""
        dx,dy=self.Plateau.unit
        ox,oy=self.Plateau.origin
        h=self.nbPieces
        if self.coince:  # cas où il n'y a pas de solution
            self.Plateau.create_line(ox, oy+13*dy , ox+5*dx,  oy+(13-h)*dy, tag="surdessin", fill="red", width=5)
            self.Plateau.create_line(ox,  oy+(13-h)*dy , ox+5*dx, oy+13*dy, tag="surdessin", fill="red", width=5)
        else: # cas où il y a une solution
            self.Plateau.delete("dessous")
            self.nbsol+=1
            for test,dec in self.solution:
                forme=Pieces[self.ListePieces[test]]
                CO=forme.CasesOccupees(dec)
                for cox,coy in CO:
                    self.Plateau.create_rectangle(ox+(5-cox)*dx, oy+(13-coy)*dy,ox+(4-cox)*dx, oy+(12-coy)*dy, fill=forme.color, tag="surdessin", outline=forme.color)
        self.Nbsol.config(state=tk.NORMAL, text="Solution {}".format(self.nbsol))
            
    def Solve(self):        
        if self.posInit:
            self.posInit=False
            for p in self.ListePieces:
                Pieces[p].reinit()
            self.solution=[] # se souvenir du premier emplacement disponible
            self.grille=Grille(self.nbPieces)
        if not self.coince:
            while self.solution:
                test,dec=self.solution.pop()
                self.grille.pieceUtilisee[test]=False
                self.grille.enleve(Pieces[self.ListePieces[test]],dec)
                if(Pieces[self.ListePieces[test]].next()):break
            if not self.solution:
                test=0
            while not self.coince and len(self.solution)<self.nbPieces:
                # amélioration possible :
                # inutile de tester les dispositions symétriques 
                # essayer de placer la pièce 0, dans le cadre en bas à droite
                # et seulement après placer les autres pièces ??
                # maintenant ça tourne assez vite comme ça, pourquoi s'embeter ?

                if self.grille.compatible(Pieces[self.ListePieces[test]]):
                    self.solution.append((test, self.grille.dec))
                    self.grille.pose(Pieces[self.ListePieces[test]])
                    self.grille.pieceUtilisee[test]=True
                    test=self.grille.nextDispo(0)
                else:
                    while not Pieces[self.ListePieces[test]].next():
                        test=self.grille.nextDispo(test+1)
                        if test==self.nbPieces:
                            if not self.solution:
                                self.coince=True
                                break
                            test,dec=self.solution.pop()
                            self.grille.enleve(Pieces[self.ListePieces[test]],dec)
                            self.grille.pieceUtilisee[test]=False
                        else: break
            if self.coince: # inutile de proposer la sauvegarde s'il n'y a pas de solution
                self.save.config(state=tk.DISABLED)
            else:
                self.save.config(state=tk.ACTIVE)
            self.DessineSolution()

    def ActiveTout(self):
        for cb in self.Im:
            cb.select()
        self.ModifyListPieces()
        
    def DesactiveTout(self):
        for cb in self.Im:
            cb.deselect()
        self.ModifyListPieces()

    def Save(self):
        code=sum([2**k for k in self.ListePieces])
        np=len(self.ListePieces)
        page=("tmp_{}_{}.ps").format(code,self.nbsol)
        self.Plateau.postscript(file=page, colormode="color")


    def ModifyListPieces(self):
        self.save.config(state=tk.DISABLED)
        self.ListePieces=[x for x in range(12) if self.CL_Var[x].get()==1]
        self.nbPieces=len(self.ListePieces)
        self.DessineVide()
        self.posInit=self.nbPieces!=0
        self.coince=self.nbPieces==0 #inutile de lancer la résolution s'il n'y a pas de pièce
        self.nbsol=0
        self.Nbsol.config(state=tk.DISABLED, text="Solution {}".format(self.nbsol))
        
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)
        self.title("Katamino")
        self.posInit=True
        self.coince=True
        self.nbPieces=0
        self.grid()
        self.Plateau=tk.Canvas(self, bd=5, relief="groove")
        self.Plateau.grid(row=0, column=0)
        self.Plateau.unit=(60,60) # les unités du plateau de jeu
        self.Plateau.origin=(1,1)
        self.Plateau.config(width=2*self.Plateau.origin[0]+5* self.Plateau.unit[0] , height=2*self.Plateau.origin[1]+13* self.Plateau.unit[1])
        self.DessineVide()
        # les pieces disponibles
        self.contain=tk.Frame(self)
        self.contain.grid(row=0,column=1)
        self.CheckList=tk.Frame(self.contain, height=100, width=100, bd=5, relief="groove")
        self.CheckList.grid(row=0,column=1)
        self.Im=[]
        self.CL_Var=[]
        for image in range(12):
            self.CL_Var.append(tk.IntVar())
            img=tk.PhotoImage(file="piece{}.gif".format(image))
            self.Im.append(tk.Checkbutton(self.CheckList,image=img ,variable=self.CL_Var[-1], command=self.ModifyListPieces))
            self.Im[-1].img=img
            self.Im[-1].no_image=image
            self.Im[-1].grid(row=image, column=1)
        self.ListePieces=[]
        self.CheckList.update()
        self.nbsol=0
        self.Nbsol=tk.Label(self.contain, state=tk.DISABLED, text="Solution {}".format(self.nbsol),relief="ridge",height=2,padx=10,pady=10)
        self.Nbsol.grid(row=2,column=1)
        # les boutons
        self.Action=tk.Frame()
        self.Action.grid(row=2, column=0, columnspan=2)
        self.solve=tk.Button(self.Action, text="Résoudre", bd=5, relief="groove", command=self.Solve)
        self.solve.grid(row=2,column=0)
        self.toutes=tk.Button(self.Action, text="Tout", bd=5, relief="groove", command=self.ActiveTout)
        self.toutes.grid(row=2,column=1)
        self.reset=tk.Button(self.Action, text="Reset", bd=5, relief="groove", command=self.DesactiveTout)
        self.reset.grid(row=2,column=2)
        self.save=tk.Button(self.Action, text='Save', bd=5, relief="groove", command=self.Save, state=tk.DISABLED)
        self.save.grid(row=2, column=3)

        self.topmaths=tk.Button(self.Action, text='Top Maths', bd=5, relief="groove", command=opentopmaths)
        self.topmaths.grid(row=2, column=4)
        self.quit=tk.Button(self.Action, text="Quitter", bd=5, relief="groove", command=self.quit)
        self.quit.grid(row=2,column=5)
        
app=Katamino()
app.mainloop()


    




