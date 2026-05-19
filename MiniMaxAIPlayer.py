from Player import Player
from Connect4Board import Connect4Board
import random

# MinimaxAIPlayer herda de Player
class MinimaxAIPlayer(Player):

    def __init__(self, piece, max_depth=3):

        # inicializa construtor de Player
        super().__init__(piece)
        self.max_depth = max_depth

    # função alphabeta pruning
    def alphabeta(self, board, depth, alpha, beta, current_piece):
        
        #   guardar os valores das pieces que correspondem ao jogador de AI e ao seu adversário
        if current_piece == 1:
            opponent_piece = 2
        else:
            opponent_piece = 1

        # variável para guardar a melhor jogada
        best_move = None

        # caso base da recursão da função alphabeta
        if (depth == 0
            or board.check_winner(current_piece) 
            or board.check_winner(opponent_piece) 
            or board.is_board_full()
        ):
           
            return self.evaluate_board(board, self), None
        
        # vai devolver todas as jogadas válidas
        # devolve todas as colunas que têm uma posição livre
        # ou seja, colunas para onde se pode jogar
        valid_moves = board.get_valid_moves()

        # este trecho trata do caso em que é o jogador max a jogar
        if current_piece == self.piece:

            # variável para guardar o melhor resultado
            best_score = float('-inf')

            for move in valid_moves:
                new_board = board.copy()
                new_board.drop_piece(move, current_piece)
                score = self.alphabeta(new_board, depth-1, alpha, beta, opponent_piece)[0]
                if score > best_score:
                    best_move = move
                    best_score = score
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
            # devolve o par de melhor resultado e a jogada correspondente
            return best_score, best_move
                
        
        # este trata do caso em que é o jogador min a jogar
        else:

            # variável para guardar o melhor resultado
            best_score = float('inf')

            for move in valid_moves:
                new_board = board.copy()
                new_board.drop_piece(move, current_piece)
                score = self.alphabeta(new_board, depth-1, alpha, beta, opponent_piece)[0]
                if score < best_score:
                    best_move = move
                    best_score = score
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
        
            # devolve o par de melhor resultado e a jogada correspondente
            return best_score, best_move
              

    # função que vai procurar e retornar a melhor jogada de entre
    # as jogadas válidas usando MiniMax
    def get_move(self, board):

        # retorna escolha da jogada beaseada no Alpha-Beta Pruning
        # alphabeta(node, max_depth, alpha, beta, piece)
        score, move = self.alphabeta(board, self.max_depth, float('-inf'), float('inf'), self.piece)
        return move 
   
   # função heurística que vai atribuir valores (scores) a diferentes estados do jogo
   # incompleta
    def evaluate_board(self, game, player):

        # guardar os números de piece do jogador e do adversário
        if player.piece == 1:
            opponent_piece = 2
        else:
            opponent_piece = 1

        if game.check_winner(player.piece):
            return 1
        
        elif game.check_winner(opponent_piece):
            return -1
        
        elif game.is_board_full():
            return 0

        # aqui tenho de tratar dos casos em que se avalia o jogo sem este ter terminado
        # isto é, os casos do dois em linhas, do três em linhas, das ameaças e do centro 
        else:
            return 0

    
