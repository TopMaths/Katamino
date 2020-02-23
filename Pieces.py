class piece:
    def __init__(self, array, color):
        self.color=color
        A=array
        orientations=[]
        for i in range(4):
            orientations.append(A)
            A=piece.rotation(A)
        A=piece.symetrie(A)
        for i in range(4):
            orientations.append(A)
            A=piece.rotation(A)
        self.orientations=list(frozenset(set(piece.tuplesToInt(T) for T in orientations)))
        self.dimensions=[]
        for p in range(len(self.orientations)):
            self.dimensions.append(self.dim(p))
        self.hautmin=min([d[1] for d in self.dimensions]) # hauteur minimale de la pièce
        self.reinit()
           
    def dim(self, p):
        larg=1
        while (self.orientations[p]>>larg)  & piece.Borddroit!=0: larg+=1
        haut=1
        while (self.orientations[p]>> (5*haut))  & piece.BordBas!=0:haut+=1
        dx=0
        while (1<<dx) & self.orientations[p] ==0: dx+=1
        return (larg,haut,dx)
        
    def CasesOccupees(self,dec):
        CO=[]
        L,H,dx=self.dimensions[self.p]
        DX,DY=(dec-dx)%5, (dec-dx)//5
        val=self.orientations[self.p]
        for l in range(L):
            for h in range(H):
                if (1<<(l+5*h)) & val:
                    CO.append((l+DX, h+DY))
        return CO
    
    def reinit(self):
        self.p=0 # numéro de l'orientation de la piece
    @staticmethod
    def tuplesToInt(T):
        A=0
        for lg,t in enumerate(T):
            for cl,x in enumerate(t):
                A+= x<<(cl+5*lg)
        return A
    @staticmethod 
    def rotation(A): # rotation du tableau
        B=tuple(zip(*A))
        return piece.symetrie(B)
    @staticmethod
    def symetrie(A): # renverse les lignes
        C=list(A)
        C.reverse()
        return tuple(C)
    def __str__(self):
        S="orientation :{}:\n".format(str(self.p))
        q=self.orientations[self.p]
        L=[]
        while(q!=0):
            L.append( bin((q%2**5))[2:].rjust(5,'0')+"\n")
            q=q//2**5
        L.reverse()
        for s in L:
            t=s.replace('0',' ')
            S+=t
        return S
        
    def next(self):
        self.p = (self.p+1)%len(self.orientations)
        return self.p!=0
        
    BordBas=2**5-1
    BordHaut=BordBas*2**55
    Borddroit=sum(2**(5*k) for k in range(0,12))
    BordGauche=Borddroit<<4
    
    P=[( ((1,1,1,1,1),), "#6495ED"), 
       (((0,0,0,1),(1,1,1,1)), "#FF8C00"),
       (((0,0,1,0),(1,1,1,1)), "#A0522D"),
       (((1,0,1),(1,1,1)),  "#FFFF00"),
       (((1,1,1,0),(0,0,1,1)), "#483D8B"),
       (((0,1,1),(1,1,1)),  "#BA55D3"),
       (((0,0,1),(1,1,1), (0,1,0)), "#778899"),
       (((0,0,1),(1,1,1), (0,0,1)), "#228B22"),
       (((0,1,0),(1,1,1), (0,1,0)), "#FF0000"),
       (((0,0,1),(1,1,1), (1,0,0)), "#00BFFF"),
       (((1,1,1),(0,0,1), (0,0,1)), "#1E90FF"),
       (((1,0,0),(1,1,0), (0,1,1)), "#9ACD32"),]


Pieces=[piece(*p) for p in piece.P]


