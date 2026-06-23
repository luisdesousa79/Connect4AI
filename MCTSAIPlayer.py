from Player import Player
from Connect4Board import Connect4Board
import random
import math


class MCTSAIPlayer(Player): 

    #Inicializamos a classe
    def __init__(self, piece, max_iterations=1000):
        
        super().__init__(piece)
        
        # Vai representar o Nó Atual
        self.root = None 
        self.max_depth = max_iterations
        self.iterations = max_iterations
        self.ConstanteC = math.sqrt(2)


    #Fechado
    def search(self):
        #Aqui vamos fazer as iterações , no fim das iterações iremos, em teoria, obter a melhor jogada possivel.
        for _ in range(self.iterations): 

            # Fase de seleção -> Aqui vamos selecionar o nós a ser explorado    
            node = self.select(self.root) 
            # Fase de simulação
            reward = self.simulate(node)
            # Fase de retropropagação 
            self.backpropagate(node, reward) 

        # Melhor jogada (mais visitada)
        return self.root.best_child(c=0) 
    
    #Fechado
    #Selecionamos aqui o nó a explorar
    def select(self, node): 
        
        #Enquanto o nó não for terminal, isto é, enquando pudermos jogar.
        while not self.is_terminal(node.state): 

            # se o nó não tiver sido totalmente expandido, expande
            if not node.is_fully_expanded():
                return self.expand(node)


            node = node.best_child(self.ConstanteC)
        
        return node
    
    # Vemos se a procura está terminada ou não. 
    # os casos são: alguem já ganhou, ou houve empate (board full).
    def is_terminal(self, state): 
        return state.check_winner(1) or state.check_winner(2 )or state.is_board_full()
     

    # Método que vai atualizar as estatísticas dos nós no caminho.
    def backpropagate(self, node, reward):
        # Enquanto não chegarmos ao Nó Inicial(o escolhido no expand) não paramos até atualizar as estatisticas dos nós.
        while node is not None:
            # Atualizamos o visits do nó atual
            node.visits += 1
            # Atualizamos o número de "wins"
            node.wins += reward
            #vamos para o parent -> Node passa a ser o pai do Node Atual.
            node = node.parent 

            
    def simulate(self, node):
        # Seleciona um nó não totalmente expandido ou terminal
        estado_atual = node.getstate().copy()

        # Aqui será a jogada do adversário -> Já trocamos no expand para o jogador atual
        pecaAtual = node.player 

        while True:

            if estado_atual.check_winner(self.piece):
                return 1 #caso que a nossa peça ganha o jogo
            if estado_atual.check_winner(self.GetOpponente(self.piece)):
                return 0 #caso que a peça adversaria ganha o jogo
            if estado_atual.is_board_full():
                return 0.5 #Caso empate
            
            movimentos_validos = estado_atual.get_valid_moves() # Obtemos os movimentos validos
            next_movimento = random.choice(movimentos_validos) # escolha aleatoria da movimentaçao a fazer.
            estado_atual.drop_piece(next_movimento, pecaAtual) # Fazemos a jogada
            pecaAtual = self.GetOpponente(pecaAtual) #Trocamos de jogador 
        
    
    def expand(self, node):
        # Preenchimento dos nós já "explorados" -> Jogadas já exploradas
        # controla os nós filhos que já foram explorados
        movimentos_tentados = [] 

        # Percorremos os nós filhos
        for child in node.getChildreans():
            #Fazemos append(adicionar) à lista de movimentos_tentados(equivalente a disser nós visitados)
            movimentos_tentados.append(child.getMove()) 
        
        # Possíveis moves -> Lista com movimentos possiveis dados pela Board
        possible_moves = node.state.get_valid_moves() 

        # Aqui iremos ter basicamente os "nós que ainda podem ser explorados, vamos associar cada jogada possiveis a um nó"
        movimentod_naoTentados = [] 

        # Aqui vmaos percorrer as jogadas possíveis no tabuleiro e ver quais ainda não foram exploradas
        for move in possible_moves:
            if move not in movimentos_tentados:
                movimentod_naoTentados.append(move)

        # Realizamos uma escolha de nó de forma random (nó a explorar)
        move_choose = random.choice(movimentod_naoTentados) 
        
        # Passamos agora a "criar" um novo nó filho, correspondente à move escolhida
        # este nó será o proximo nó simulado
        
        # Obtenção da board
        new_board = node.state.copy() 
        # Possíveis moves -> Lista com movimentos possiveis dados pela Board
        # Realizamos jogada de modo a obter basicamente o novo estado (o nó realmente)
        new_board.drop_piece(move_choose, node.player) 
        # Criação do nó filho a ser explorado, o player passa a ser o próximo jogador.
        child = Node(new_board, parent= node , moves = move_choose , player = self.GetOpponente(node.player)) 

        # Alocaçao do nó filho ao node atual
        node.children.append(child) 

        return child

    
    def get_move(self, board):
        self.root = Node(board.copy(), self.piece) # Estado Atual
        best_node = self.search() # Vamos à procura da melhor jogada
        return best_node.moves # Melhor jogada a fazer , ou seja um Inteiro que indica me que coluna "despejar" a peça
    

    def GetOpponente(self, piece): # Obtemos a peça do oponente
        if piece == 1:
            return 2
        return 1
        


#Classes Auxiliares

class Node:

    def __init__(self, state,  player , parent=None , moves = None):
        self.state = state # Estado do jogo (ex: tabuleiro)
        self.parent = parent # Nó pai
        self.children = [] # Lista de nós filhos
        self.wins = 0 # Vitórias acumuladas
        self.visits = 0 # Número de visitas
        self.moves = moves
        self.player = player


    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_valid_moves())  # Verifica se todos os movimentos possíveis foram explorados
    
    def best_child(self, c=1.414): # c = sqrt(2)
        # Seleciona o filho com o maior valor UCB
        return max(self.children, key=lambda child: child.ucb(c))
    
    def getstate(self):
        return self.state
    
    def getMove(self):
        return self.moves
    
    def getChildreans(self):
        return self.children
        
    # Fórmula UCB1 (Upper Confidence Bound)
    def ucb(self, c):
        # Dá prioridade a nós nunca visitados
        if self.visits == 0:
            return float('inf')

        exploitation = self.wins / self.visits ## Termo Exploitation -> Mede a taxa de sucesso do nó

        exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits) # Termo Exploration: -> Incentiva explorar nós menos visitados

        return exploitation + exploration #Valor da USB para o proprio nó
    

    


        




        



    