#include <iostream>
#include <algorithm>
#include <queue>
#include <chrono>
#include <format>
#include <string>
#include <algorithm>
#include <vector>

struct Piece {
    int width;
    int height;

    bool operator>(const Piece& other) const {
        return width * height > other.width * other.height;
    }

    std::string toString() const {
        return std::format("{} by {}", width, height);
    }
};

struct Edge {
    int xPos;
    int yPos;
    int length;

    bool operator<(const Edge& other) const {
        if (yPos == other.yPos) {
            return xPos > other.xPos;
        }
        return yPos > other.yPos;
    }
};

struct SolutionPart {
    int xPos;
    int yPos;
    Piece piece;

    std::string toString() const {
        return std::format("{} at {}, {}", piece.toString(), xPos, yPos);
    }
};

// The board size and pieces corresponding to the Calibron 12 puzzle. 
// To solve a different puzzle, simply modify these three values 
constexpr int BOARD_WIDTH {56};
constexpr int BOARD_HEIGHT {56};
std::vector<Piece> pieces {
    Piece{28,14},
    Piece{28,6},
    Piece{21,18},
    Piece{21,18},
    Piece{10,7},
    Piece{14,4},
    Piece{17,14},
    Piece{32,10},
    Piece{32,11},
    Piece{28,7},
    Piece{21,14},
    Piece{21,14},
};
std::vector<SolutionPart> solution {};

bool place(Piece& piece, std::priority_queue<Edge>& edges) {
    Edge edgeToInsertOn = edges.top();
    if (piece.height + edgeToInsertOn.yPos > BOARD_HEIGHT) {
        return false;
    }
    edges.pop();
    if (edges.size() > 0) {
        Edge nextEdge = edges.top();
        while (nextEdge.yPos == edgeToInsertOn.yPos && nextEdge.xPos == edgeToInsertOn.xPos + edgeToInsertOn.length) {
            edges.pop();
            edgeToInsertOn = Edge(edgeToInsertOn.xPos, edgeToInsertOn.yPos, edgeToInsertOn.length + nextEdge.length);
            if (edges.size() < 1) {
                break;
            }
            nextEdge = edges.top();
        }
    }
    if (piece.width > edgeToInsertOn.length) {
        edges.push(edgeToInsertOn);
        return false;
    }
    solution.push_back(SolutionPart{edgeToInsertOn.xPos, edgeToInsertOn.yPos, piece});
    if (edgeToInsertOn.length == piece.width) {
        edges.push(Edge{edgeToInsertOn.xPos, edgeToInsertOn.yPos + piece.height, piece.width});
    }
    else {
        edges.push(Edge{edgeToInsertOn.xPos, edgeToInsertOn.yPos + piece.height, piece.width});
        edges.push(Edge{edgeToInsertOn.xPos + piece.width, edgeToInsertOn.yPos, edgeToInsertOn.length - piece.width});
    }
    return true;
}

bool solve(std::vector<Piece> pieces, std::priority_queue<Edge> edges) {
    if (pieces.size() < 1) {
        return true;
    }
    for (size_t i {0}; i < pieces.size(); i++) {
        Piece curPiece = pieces[i];
        for (bool rotate : {false, true}) {
            if (rotate) {
                curPiece = Piece{curPiece.height, curPiece.width};
            }
            std::priority_queue<Edge> edgesCopy = edges;
            if (place(curPiece, edgesCopy)) {
                // Optimizing out this copy resulted in marginal speed gains and way uglier code, so keeping the copy in
                std::vector<Piece> newPieces;
                newPieces.resize(pieces.size() - 1);
                std::copy(pieces.begin(), pieces.begin() + i, newPieces.begin());
                std::copy(pieces.begin() + i + 1, pieces.end(), newPieces.begin() + i);
                if (solve(newPieces, edgesCopy)) {
                    return true;
                }
                solution.pop_back();
            }
        }
    }
    return false;
}

int main() {
    std::sort(pieces.begin(), pieces.end(), std::greater<Piece>());
    std::vector<Edge> starting_edge {Edge{0,0, BOARD_WIDTH}};
    std::priority_queue<Edge> edges {starting_edge.begin(), starting_edge.end()};
    auto start = std::chrono::steady_clock::now();
    bool solved = solve(pieces, edges);
    auto end = std::chrono::steady_clock::now();
    if (solved) {
        std::cout << std::format("Solution found in {}:", std::chrono::duration_cast<std::chrono::milliseconds>(end - start)) << "\n";
        for (const auto& solutionPart : solution) {
            std::cout << solutionPart.toString() << "\n";
        }
    }
    else {
        std::cout << std::format("No solution found exists, all possibilities eliminated in {}", std::chrono::duration_cast<std::chrono::milliseconds>(end - start));
    }
}