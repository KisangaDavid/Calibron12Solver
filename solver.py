import heapq
import copy

class Piece:
    def __init__(self, width, height):
        self.x = width
        self.y = height
    
    # Pieces are ordered by area
    def __lt__(self, other):
        return self.x * self.y < other.x * other.y
    
    def __str__(self):
        return f"{self.x} by {self.y}"
        
class Edge:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length

    # Edges are ordered by position - the top-left most edge is considered the "smallest" for our min heap 
    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

class SolutionPart:
    def __init__(self, piece, xPos, yPos):
        self.piece = piece
        self.xPos = xPos
        self.yPos = yPos

    def __str__(self):
        return f"{str(self.piece)} at xPos {self.xPos}, yPos {self.yPos}"

def place(piece: Piece, edges: list[Edge]):
    edgeToInsertOn = heapq.heappop(edges)
    # Check if piece fits vertically
    if (piece.y + edgeToInsertOn.y > BOARD_HEIGHT):
        return False, -1, -1
    
    # Merge edges that are connected before checking if the piece fits horizontally
    nextEdge: Edge = None
    if len(edges) > 0:
        nextEdge: Edge = edges[0]
        while nextEdge.y == edgeToInsertOn.y and nextEdge.x == edgeToInsertOn.x + edgeToInsertOn.length:
            heapq.heappop(edges)
            edgeToInsertOn = Edge(edgeToInsertOn.x, edgeToInsertOn.y, edgeToInsertOn.length + nextEdge.length)
            if (len(edges) < 1):
                break
            nextEdge = edges[0]

    # Check if piece fits horizontally
    if (piece.x > edgeToInsertOn.length):
        return False, -1, -1
    
    # Update the edges min heap to reflect the new piece, adding one or two edges as appropriate
    if (edgeToInsertOn.length == piece.x):
        heapq.heappush(edges, Edge(edgeToInsertOn.x, edgeToInsertOn.y + piece.y , piece.x))
    else:
        heapq.heappush(edges, Edge(edgeToInsertOn.x, edgeToInsertOn.y + piece.y, piece.x))
        heapq.heappush(edges, Edge(edgeToInsertOn.x + piece.x, edgeToInsertOn.y, edgeToInsertOn.length - piece.x))
    return True, edgeToInsertOn.x, edgeToInsertOn.y

def solve(pieces: list[Piece], edges: list[Edge]):
    if (len(pieces) < 1):
        for solutionPart in solution:
            print(str(solutionPart))
        return True
    for idx, piece in enumerate(pieces):
        for rotate in (False, True):
            if (rotate):
                piece = Piece(piece.y, piece.x)
            edgesCopy = copy.deepcopy(edges)
            fits, xPos, yPos = place(piece, edgesCopy)
            if fits:
                solution.append(SolutionPart(piece, xPos, yPos))
                newPieces = pieces[:idx] + pieces[idx+1:]
                if solve(newPieces, edgesCopy):
                    return True
                solution.pop()
    return False

# The board size and pieces corresponding to the Calibron 12 puzzle. To solve a different puzzle, simply modify these three values 
BOARD_WIDTH = 56
BOARD_HEIGHT = 56
pieces = [
    Piece(28,14),
    Piece(28,6),
    Piece(21,18),
    Piece(21,18),
    Piece(10,7),
    Piece(14,4),
    Piece(17,14),
    Piece(32,11),
    Piece(32,10),
    Piece(28,7),
    Piece(21,14),
    Piece(21,14),
]

solution = []
edges = [Edge(0,0,BOARD_WIDTH)]

pieces.sort(reverse = True) # Using bigger pieces at the beginning leads to more pruning
solve(pieces, edges)