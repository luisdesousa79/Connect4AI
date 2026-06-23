import time
from collections import defaultdict
from MinimaxAIPlayer import *
from Connect4Board import *
from Connect4Game import *
from MCTSAIPlayer import *

import pandas as pd

def to_dataframe(results): #Apenas para o caso de querermos passar para csv
    return pd.DataFrame(results)


def run_match(p1, p2, game_class, n_games=50):
    stats = {
        "games": 0,
        "p1_wins": 0,
        "p2_wins": 0,
        "draws": 0,
        "durations": []
    } #Dicionario

    for _ in range(n_games):
        game = game_class() #Inicializamos aqui o game (passamos por parametro o objeto de Jogo)
        start = time.time() #Tempos

        winner = game.run_game(p1, p2, headless=True) #Fim do jogo aqui

        duration = time.time() - start #Tempo Final

        stats["games"] += 1 #Adicionamos mais 1 jogo (até perfazer os 30)
        stats["durations"].append(duration)

        #Aqui Basicamente guardamos as estatisticas
        if winner == p1.piece:
            stats["p1_wins"] += 1
        elif winner == p2.piece:
            stats["p2_wins"] += 1
        else:
            stats["draws"] += 1

    return stats #Return dos estados


def summarize(stats):
    games = stats["games"]
    durations = stats["durations"]

    return {
        "Nº Jogos": games,
        "Vitórias Jogador 1": stats["p1_wins"],
        "Vitórias Jogador 2": stats["p2_wins"],
        "Empates": stats["draws"],
        "Taxa Vitória J1": stats["p1_wins"] / games,
        "Taxa Vitória J2": stats["p2_wins"] / games,
        "Duração Média": sum(durations) / games,
        "Duração Máxima": max(durations),
        "Duração Mínima": min(durations),
    }


def run_all_tests():
    results = [] #Vamos guardar os resultados aqui.

    tests = [
    ("Minimax vs Random",
     MinimaxAIPlayer(1, max_depth=3),
     RandomAIPlayer(2)),

    ("MCTS vs Random",
     MCTSAIPlayer(1, max_iterations=100),
     RandomAIPlayer(2)),

    ("1º comb Minimax vs MCTS",
     MinimaxAIPlayer(1, max_depth=3),
     MCTSAIPlayer(2, max_iterations=100)),

    ("2º comb Minimax vs MCTS",
     MinimaxAIPlayer(1, max_depth=4),
     MCTSAIPlayer(2, max_iterations=700)),

    ("3º comb Minimax vs MCTS",
     MinimaxAIPlayer(1, max_depth=5),
     MCTSAIPlayer(2, max_iterations=1200)),
    ]

    for name, p1, p2 in tests:
        print(f"Running: {name}")

        stats = run_match(p1, p2, Connect4Game, n_games=30) #Aqui que vamos realizar os 30 jogos
        summary = summarize(stats) #Guardamos os resultados #Aqui será um dicionario , associado ao dicionarios iremos ter basicamente

        summary["Comparação"] = name #Mais um dado pro summay(dicionario), vai representar o nome do jogo
        results.append(summary)

    return results


def print_table(results):
    for r in results:
        print("\n========================")
        print(r["Comparação"])
        for k, v in r.items():
            if k != "Comparação":
                print(f"{k}: {v}")


if __name__ == "__main__":
    results = run_all_tests()
    df = to_dataframe(results)

    print_table(results) #Aqui e em baixo fazemos a mesma coisa.

    print(df)

    # opcional: exportar
    #df.to_csv("connect4_benchmark.csv", index=False)




                