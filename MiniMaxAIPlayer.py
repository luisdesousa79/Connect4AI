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
           
            return self.evaluate_board(board, self.piece), None
        
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
                # chama recursivamente alphabeta e guarda o resultado obtido
                score = self.alphabeta(new_board, depth-1, alpha, beta, opponent_piece)[0]
                # se o resultado for superior ao melhor resultado obtido até agora guarda o resultado e a jogada.
                if score > best_score:
                    best_move = move
                    best_score = score
                # se o alpha for superior ao melhor resultado, fixa um novo alpha
                alpha = max(alpha, best_score)
                # se o alpha maior ou igual a beta, poda
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
                # compara o resultado com o melhor resultado, se for menor, guarda o novo melhor resultado
                if score < best_score:
                    best_move = move
                    best_score = score
                # se o melhor resultado é inferior ao beta, fixa um novo beta
                beta = min(beta, best_score)
                # se alpha maior ou igual  abeta, poda poder este ramo
                if alpha >= beta:
                    break
        
            # devolve o par de melhor resultado e a jogada correspondente
            return best_score, best_move
              

    # função que vai procurar e retornar a melhor jogada de entre
    # as jogadas válidas usando MiniMax
    def get_move(self, board):

        
        # alphabeta(node, max_depth, alpha, beta, piece)
        score, move = self.alphabeta(board, self.max_depth, float('-inf'), float('inf'), self.piece)

        # caso o alphabeta devolva None, faz jogada aleatória
        if move is None:
            valid_moves = board.get_valid_moves()

        
            if valid_moves:
                return random.choice(valid_moves)
        
        # caso contrário, retorna escolha da jogada beaseada no Alpha-Beta Pruning
        return move 


    # função heurística que vai atribuir valores (scores) a diferentes estados do jogo
    def evaluate_board(self, game, player):

        # guardar os números de piece do jogador e do adversário
        if player == 1:
            opponent = 2
        else:
            opponent = 1

        # caso de vitória
        if game.check_winner(player):
            return float('inf')
        
        # caso de derrota
        elif game.check_winner(opponent):
            return float('-inf')
        
        # caso de empate
        elif game.is_board_full():
            return 0
        
        # aqui tenho de tratar dos casos não terminais do jogo, isto é,
        # os casos do dois em linhas, do três em linhas, das ameaças e do centro 
        else:
            score = 0
            
            # horizontal 
            for row in range(game.rows):
                for col in range(game.cols - game.n_connect + 1):
                    # vamos considerar janelas de quatro de cada vez
                    window = [game.grid[row][col + i] for i in range(4)]
                    score += self.evaluate_window(window, player, opponent)
                    

            # vertical
            for col in range(game.cols):
                for row in range(game.rows - game.n_connect + 1):
                    # vamos considerar janelas de quatro de cada vez
                    window = [game.grid[row + i][col] for i in range(4)]
                    # avaliamos a janela
                    score += self.evaluate_window(window, player, opponent)
        
            # diagonal /
            for row in range(game.rows - 1, game.n_connect - 2, -1):
                for col in range(game.cols - game.n_connect + 1):
                    # vamos considerar janelas de quatro de cada vez
                    window = [game.grid[row - i][col + i] for i in range(4)]
                    # avaliamos a janela
                    score += self.evaluate_window(window, player, opponent)


            # diagonal \
            for row in range(game.rows - game.n_connect + 1):
                for col in range(game.cols - game.n_connect + 1):
                    # vamos considerar janelas de quatro de cada vez
                    window = [game.grid[row + i][col + i] for i in range(4)]
                    # avaliamos a janela
                    score += self.evaluate_window(window, player, opponent)
        
            # avaliação do centro do tabuleiro
            # considerámos a ocupação de uma das quatro posições centrais como vantajosa
            mid_row = game.rows // 2
            mid_col = game.cols // 2
        
            central_positions = [(mid_row - 1, mid_col - 1), (mid_row - 1, mid_col), (mid_row, mid_col - 1), 
                            (mid_row, mid_col)]


            for row, col in central_positions: 

                if game.grid[row][col] == player:
                    score += 15

                elif game.grid[row][col] == opponent:
                    score -= 15

        # devolvemos o valor acumulado 
        return score

    # função auxiliar para avaliar uma "janela" de quatro posições
    def evaluate_window(self, window, player_piece, opponent_piece):
        value = 0
        
        # caso três em linha do jogador
        if window.count(player_piece) == 3 and window.count(0) == 1:
            value += 75
        # caso dois em linha do jogador
        elif window.count(player_piece) == 2 and window.count(0) == 2:
            value += 50
        # caso três em linha do adversário
        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            value -= 75
        # caso dois em linha do adversário    
        elif window.count(opponent_piece) == 2 and window.count(0) == 2:
            value -= 50
        
        return value



        
