import timeit
import heapq
import copy

class Piece:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    # Pieces are ordered by area
    def __lt__(self, other):
        return self.width * self.height < other.width * other.height
    
    def __str__(self):
        return f"{self.width} by {self.height}"
        
class Edge:
    def __init__(self, x, y, length):
        self.xPos = x
        self.yPos = y
        self.length = length

    # Edges are ordered by position - the top-left most edge is considered the "smallest" for our min heap 
    def __lt__(self, other):
        if self.yPos == other.yPos:
            return self.xPos < other.xPos
        return self.yPos < other.yPos

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
    if (piece.height + edgeToInsertOn.yPos > BOARD_HEIGHT):
        return False, -1, -1
    
    # Merge edges that are connected before checking if the piece fits horizontally
    nextEdge: Edge = None
    if len(edges) > 0:
        nextEdge: Edge = edges[0]
        while nextEdge.yPos == edgeToInsertOn.yPos and nextEdge.xPos == edgeToInsertOn.xPos + edgeToInsertOn.length:
            heapq.heappop(edges)
            edgeToInsertOn = Edge(edgeToInsertOn.xPos, edgeToInsertOn.yPos, edgeToInsertOn.length + nextEdge.length)
            if (len(edges) < 1):
                break
            nextEdge = edges[0]

    # Check if piece fits horizontally
    if (piece.width > edgeToInsertOn.length):
        return False, -1, -1
    
    # Update the edges min heap to reflect the new piece, adding one or two edges as appropriate
    if (edgeToInsertOn.length == piece.width):
        heapq.heappush(edges, Edge(edgeToInsertOn.xPos, edgeToInsertOn.yPos + piece.height , piece.width))
    else:
        heapq.heappush(edges, Edge(edgeToInsertOn.xPos, edgeToInsertOn.yPos + piece.height, piece.width))
        heapq.heappush(edges, Edge(edgeToInsertOn.xPos + piece.width, edgeToInsertOn.yPos, edgeToInsertOn.length - piece.width))
    return True, edgeToInsertOn.xPos, edgeToInsertOn.yPos

def solve(pieces: list[Piece], edges: list[Edge]):
    if (len(pieces) < 1):
        return True
    for idx, piece in enumerate(pieces):
        for rotate in (False, True):
            if (rotate):
                piece = Piece(piece.height, piece.width)
            edgesCopy = copy.deepcopy(edges)
            fits, xPos, yPos = place(piece, edgesCopy)
            if fits:
                solution.append(SolutionPart(piece, xPos, yPos))
                newPieces = pieces[:idx] + pieces[idx+1:] # Copying is inefficient
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
pieces.sort(reverse = True)

# Measure execution time
execution_time = timeit.timeit(
    stmt="solve(pieces, edges)",
    setup="from __main__ import solve, pieces, edges",
    number=1
) * 1000

print(f"Solution found in {execution_time:.0f} milliseconds")

for solutionPart in solution:
    print(str(solutionPart))