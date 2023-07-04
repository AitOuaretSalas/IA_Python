from __future__ import annotations
from typing import TypeVar, Generic, List, Deque, Optional

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self.container

    def push(self, item: T) -> None:
        self.container.append(item)

    def pop(self) -> T:
        return self.container.pop()

    def __repr__(self) -> str:
        return repr(self.container)

class Node(Generic[T]):
    def __init__(self, etat: T, parent: Optional[Node], cout: float = 0.0, heuristique: float = 0.0) -> None:
        self.etat: T = etat
        self.parent: Optional[Node] = parent
        self.cout: float = cout
        self.heuristique: float = heuristique

    def __lt__(self, other: Node) -> bool:
        return (self.cout + self.heuristique) < (other.cout + other.heuristique)


def node_to_path(node: Node[T]) -> List[T]:
        chemin: List[T] = [node.etat]
        while node.parent is not None:
            node = node.parent
            chemin.append(node.etat)
        chemin.reverse()
        return chemin

class Queue(Generic[T]):
    def __init__(self) -> None:
        self.container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self.container

    def push(self, item: T) -> None:
        self.container.append(item)

    def pop(self) -> T:
        return self.container.popleft()

    def __repr__(self) -> str:
        return repr(self.container)