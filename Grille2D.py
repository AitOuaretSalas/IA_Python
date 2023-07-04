from collections import namedtuple
from enum import Enum
import random
from typing import  List, NamedTuple, TypeVar, Set
from tkinter import *
from tkinter.ttk import *
from Structures import Stack, Queue, node_to_path, Node


T = TypeVar('T')


class Case(str, Enum):
    VIDE = " "
    OBSTACLE = "X"
    DEPART ="D"
    ARRIVEE = "A"
    CHEMIN = "*"
    EXPLOREE = "E"
    COURANTE = "C"
    FRONTIERE = "F"


class Emplacement(NamedTuple):
    ligne : int
    colonne : int

class Grille2D:
    def __init__(self, lignes : int = 10, colonnes : int = 10, occurencesObstacles : float = 0.2, depart : Emplacement = Emplacement(0,0), arrivee : Emplacement = Emplacement(9,9)) -> None:

        self._lignes = lignes
        self._colonnes = colonnes
        self._depart = depart
        self._arrivee = arrivee

        self._grille : List[List[Case]] = [[Case.VIDE for c in range(colonnes)] for l in range(lignes)]
        self._genererObstacles(lignes, colonnes, occurencesObstacles)

        self._grille[depart.ligne][depart.colonne] = Case.DEPART
        self._grille[arrivee.ligne][arrivee.colonne] = Case.ARRIVEE
        self._GUI()

    def _GUI(self):
        self.root : Tk = Tk()
        self.root.title("Strategies de recherche")
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight = 1)

        frame: Frame = Frame(self.root)
        frame.grid(column=0, row=0, sticky=N + S + E + W)

        style : Style = Style()
        style.theme_use('classic')
        style.configure("BG.TLabel", foreground="black", font=('Helvetica', 26))
        style.configure("BG.TButton", foreground="black", font=('Helvetica', 26))
        style.configure("BG.TListbox", foreground="black", font=('Helvetica', 26))
        style.configure("BG.TCombobox", foreground="black", font=('Helvetica', 26))
        style.configure(" ", foreground="black", background="white")

        style.configure(Case.VIDE.value + ".TLabel", foreground="black", background="white", font=('Helvetica', 26))
        style.configure(Case.OBSTACLE.value + ".TLabel", foreground="white", background="black", font=('Helvetica', 26))
        style.configure(Case.DEPART.value + ".TLabel", foreground="black", background="green", font=('Helvetica', 26))
        style.configure(Case.ARRIVEE.value + ".TLabel", foreground="black", background="red", font=('Helvetica', 26))
        style.configure(Case.CHEMIN.value + ".TLabel", foreground="black", background="yellow", font=('Helvetica', 26))
        style.configure(Case.EXPLOREE.value + ".TLabel", foreground="black", background="cyan", font=('Helvetica', 26))
        style.configure(Case.COURANTE.value + ".TLabel", foreground="black", background="blue", font=('Helvetica', 26))
        style.configure(Case.FRONTIERE.value + ".TLabel", foreground="black", background="orange", font=('Helvetica', 26))


        for ligne in range(self._lignes):
            Grid.rowconfigure(frame, ligne, weight=1)
            ligne_label: Label = Label(frame, text=str(ligne), style="BG.TLabel", anchor="center")
            ligne_label.grid(row=ligne, column=0, sticky=N + S + E + W)
            Grid.rowconfigure(frame, ligne, weight=1)
            Grid.grid_columnconfigure(frame, 0, weight=1)

        for colonne in range(self._colonnes):
            Grid.columnconfigure(frame, colonne, weight=1)
            colonne_label: Label = Label(frame, text=str(colonne), style="BG.TLabel", anchor="center")
            colonne_label.grid(row=self._lignes, column=colonne + 1, sticky=N + S + E + W)
            Grid.rowconfigure(frame, self._lignes, weight=1)
            Grid.columnconfigure(frame, colonne + 1, weight=1)

        self._case_labels: List[List[Label]] = [[Label(frame, anchor="center") for c in range(self._colonnes)] for r in range(self._lignes)]
        for ligne in range(self._lignes):
            for colonne in range(self._colonnes):
                case_label: Label = self._case_labels[ligne][colonne]
                Grid.columnconfigure(frame, colonne + 1, weight=1)
                Grid.rowconfigure(frame, ligne, weight=1)
                case_label.grid(row=ligne, column=colonne + 1, sticky=N + S + E + W)
        self._display_grid()

        dfs_button: Button = Button(frame, style="BG.TButton", text="DFS", command=self.dfs)
        dfs_button.grid(row=self._lignes + 2, column=1, columnspan=3, sticky=N + S + E + W)
        bfs_button: Button = Button(frame, style="BG.TButton", text="BFS", command=self.bfs)
        bfs_button.grid(row=self._lignes + 3, column=1, columnspan=3, sticky=N + S + E + W)
        #idfs_button: Button = Button(frame, style="BG.TButton", text="IDFS", command=self.idfs)
        #idfs_button.grid(row=self._lignes + 4, column=1, columnspan=3, sticky=N + S + E + W)
        #aStar_button: Button = Button(frame, style="BG.TButton", text="A*", command=self.aStar)
        #aStar_button.grid(row=self._lignes + 5, column=1, columnspan=3, sticky=N + S + E + W)
        Grid.rowconfigure(frame, self._lignes + 2, weight=1)
        Grid.rowconfigure(frame, self._lignes + 3, weight=1)
        #Grid.rowconfigure(frame, self._lignes + 4, weight=1)
        #Grid.rowconfigure(frame, self._lignes + 5, weight=1)

        frame.pack(fill="both", expand=True)
        self.root.mainloop()



    def _genererObstacles(self, lignes : int, colonnes : int, occurence : float):
        for ligne in range(lignes):
            for colonne in range(colonnes):
                if random.uniform(0, 1.0) < occurence :
                    self._grille[ligne][colonne] = Case.OBSTACLE

    def _display_grid(self):
        self._grille[self._depart.ligne][self._depart.colonne] = Case.DEPART
        self._grille[self._arrivee.ligne][self._arrivee.colonne] = Case.ARRIVEE
        for ligne in range (self._lignes):
            for colonne in range (self._colonnes):
                case : Case = self._grille[ligne][colonne]
                case_label : Label = self._case_labels[ligne][colonne]
                case_label.configure(style= case.value + ".TLabel")

                
    def pas(self, frontiere, exploree, nodePrecedent):
        if not frontiere.empty:
            nodeCourrant : Node[T] = frontiere.pop()
            etatCourrant : T = nodeCourrant.etat
            self._grille[etatCourrant.ligne][etatCourrant.colonne] = Case.COURANTE

        if self.testArrivee(etatCourrant):
            chemin = node_to_path(nodeCourrant)
            self.mark(chemin)
            self._display_grid()
            return

        for child in self.successors(etatCourrant):
            if child in exploree:
                continue
            exploree.add(child)
            
            frontiere.push(Node(child, nodeCourrant))

        self._display_grid()
        self.root.after(50, self.pas, frontiere, exploree, nodeCourrant)

    def dfs(self):
        self.clear()
        self._display_grid()
        
        frontier: Stack[Node[T]] = Stack()
        frontier.push(Node(self._depart, None))
        
        explored: Set[T] = {self._depart}
        self.pas(frontier, explored, None)

    def bfs(self):
        self.clear()
        self._display_grid()
        
        frontier: Queue[Node[T]] = Queue()
        frontier.push(Node(self._depart, None))
        
        explored: Set[T] = {self._depart}
        self.pas(frontier, explored, None)

    def __str__(self) -> str:
        output: str = ""
        for ligne in self._grille:
            output += "".join([c.value for c in ligne]) + "\n"
        return output

    def testArrivee(self, ml: Emplacement) -> bool:
        return ml == self._arrivee

    def successors(self, ml: Emplacement) -> List[Emplacement]:
        emplacements: List[Emplacement] = []
        if ml.ligne + 1 < self._lignes and self._grille[ml.ligne + 1][ml.colonne] != Case.OBSTACLE:
            emplacements.append(Emplacement(ml.ligne + 1, ml.colonne))
        if ml.ligne - 1 >= 0 and self._grille[ml.ligne - 1][ml.colonne] != Case.OBSTACLE:
            emplacements.append(Emplacement(ml.ligne - 1, ml.colonne))
        if ml.colonne + 1 < self._colonnes and self._grille[ml.ligne][ml.colonne + 1] != Case.OBSTACLE:
            emplacements.append(Emplacement(ml.ligne, ml.colonne + 1))
        if ml.colonne - 1 >= 0 and self._grille[ml.ligne][ml.colonne - 1] != Case.OBSTACLE:
            emplacements.append(Emplacement(ml.ligne, ml.colonne - 1))
        return emplacements

    def mark(self, chemin: List[Emplacement]):
        for emplacement in chemin:
            self._grille[emplacement.ligne][emplacement.colonne] = Case.CHEMIN
        self._grille[self._depart.ligne][self._depart.colonne] = Case.DEPART
        self._grille[self._arrivee.ligne][self._arrivee.colonne] = Case.ARRIVEE

    def clear(self):
        for ligne in range(self._lignes):
            for colonne in range(self._colonnes):
                if self._grille[ligne][colonne] != Case.OBSTACLE:
                    self._grille[ligne][colonne] = Case.VIDE
        self._grille[self._depart.ligne][self._depart.colonne] = Case.DEPART
        self._grille[self._arrivee.ligne][self._arrivee.colonne] = Case.ARRIVEE

if __name__ == "__main__":
    m: Grille2D = Grille2D()