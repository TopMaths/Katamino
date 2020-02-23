from Pieces import Pieces

class Grille:
    def __init__(self, h):
        self.val=0
        self.dec=0 # premier emplacement libre dans la grille, à partir du coin en bas à droite de la grille      
        self.h=h # hauteur de la grille
        # seld.d=dict() # le graphe reliant les points de la grille
        self.pieceUtilisee=[False]*h
        
    def pose(self, piece):
        larg,haut,dx=piece.dimensions[piece.p]
        self.val^=(piece.orientations[piece.p]<<(self.dec-dx))
        self.calcDec()

    def enleve(self, piece,dec): # corrigé ?  : prendre l'ancien dec, qu'il faut enregistrer en même temps que test
        larg,haut,dx=piece.dimensions[piece.p]
        self.val^=(piece.orientations[piece.p]<<(dec-dx))
        self.dec=dec
        #self.calcDec()
                   
    def calcDec(self):
        S=bin(self.val)[2:].rjust(5*self.h, '0')
        L=list(S)
        L.reverse()
        S="".join(L)
        self.dec=S.find('0')

    def coords(self):
        x=self.dec%5
        y=self.dec//5
        return (x,y)
    
    def nextDispo(self, nb):
        while nb<self.h and self.pieceUtilisee[nb]:nb+=1
        return nb
    
    def compatible(self,piece): # teste si l'on peut poser la pièce sur la grille sur le premier emplacement disponible
        larg,haut,dx=piece.dimensions[piece.p]
        x=self.dec%5 # numero de la colonne du premier emplacement libre
        if x-dx <0 or x-dx+larg>5: return False # trop a droite ou trop à gauche)
        if self.dec//5+haut>self.h: return False # trop haut 
        return ((piece.orientations[piece.p]<<(self.dec-dx)&self.val)==0)

    def __str__(self):
        ch=bin(self.val)[2:].rjust(5*self.h,'0')
        L=[ch[5*k:5*k+5]+"\n" for k in range(self.h) ]
        S=""
        for s in L:
            S+=s
        return S

    
