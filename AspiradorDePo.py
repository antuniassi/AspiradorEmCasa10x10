from aigyminsper.search.search_algorithms import AEstrela
from aigyminsper.search.graph import HeuristicState
import random
import time
import multiprocessing

TAMANHO = 10

class AspiradorDePo(HeuristicState):

    def __init__(self, op, mapa, lin, col):
        super().__init__(op)
        self.mapa = mapa
        self.lin = lin
        self.col = col

    def successors(self):
        successors = []

        # limpar
        if self.mapa[self.lin][self.col] == "sujo":
            novo_mapa = [linha[:] for linha in self.mapa]
            novo_mapa[self.lin][self.col] = "limpo"

            successors.append(
                AspiradorDePo("limpar", novo_mapa, self.lin, self.col)
            )

        # cima
        if self.lin > 0:
            successors.append(
                AspiradorDePo("cima", self.mapa, self.lin - 1, self.col)
            )

        # baixo
        if self.lin < TAMANHO - 1:
            successors.append(
                AspiradorDePo("baixo", self.mapa, self.lin + 1, self.col)
            )

        # esquerda
        if self.col > 0:
            successors.append(
                AspiradorDePo("esquerda", self.mapa, self.lin, self.col - 1)
            )

        # direita
        if self.col < TAMANHO - 1:
            successors.append(
                AspiradorDePo("direita", self.mapa, self.lin, self.col + 1)
            )

        return successors

    def is_goal(self):
        return all("sujo" not in linha for linha in self.mapa)

    def description(self):
        return "Aspirador de po em uma casa 10x10"

    def cost(self):
        return 1

    def env(self):
        return str((self.lin, self.col, tuple(map(tuple, self.mapa))))

    def distancia(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def custo_mst(self, pontos):
        if len(pontos) <= 1:
            return 0

        visitados = {pontos[0]}
        nao_visitados = set(pontos[1:])
        custo = 0

        while nao_visitados:
            menor_distancia = float("inf")
            proximo = None

            for a in visitados:
                for b in nao_visitados:
                    d = self.distancia(a, b)

                    if d < menor_distancia:
                        menor_distancia = d
                        proximo = b

            custo += menor_distancia
            visitados.add(proximo)
            nao_visitados.remove(proximo)

        return custo

    def h(self):
        sujas = []

        for lin in range(TAMANHO):
            for col in range(TAMANHO):
                if self.mapa[lin][col] == "sujo":
                    sujas.append((lin, col))

        if not sujas:
            return 0

        posicao = (self.lin, self.col)

        distancia_mais_proxima = min(
            self.distancia(posicao, sujeira)
            for sujeira in sujas
        )

        return (
            len(sujas)
            + distancia_mais_proxima
            + self.custo_mst(sujas)
        )


def criar_mapa():
    mapa = [["limpo" for _ in range(TAMANHO)] for _ in range(TAMANHO)]

    quantidade_sujas = (TAMANHO * TAMANHO) // 2 # 50% do mapa sujo

    posicoes = [
        (lin, col)
        for lin in range(TAMANHO)
        for col in range(TAMANHO)
    ]

    posicoes_sujas = random.sample(posicoes, quantidade_sujas)

    for lin, col in posicoes_sujas:
        mapa[lin][col] = "sujo"

    return mapa


def buscar(state):
    algorithm = AEstrela()
    algorithm.search(state, pruning="general")


def main():
    mapa = criar_mapa()

    print("Mapa gerado:")
    for linha in mapa:
        print(linha)

    state = AspiradorDePo("", mapa, 0, 0)

    inicio = time.perf_counter()

    processo = multiprocessing.Process(target=buscar, args=(state,))
    processo.start()
    processo.join(300)  # 5 minutos
    fim = time.perf_counter()

    if processo.is_alive():
        processo.terminate()
        processo.join()
        print("Timeout: busca excedeu 5 minutos")
    else:
        print("Achou!")
        print(f"Tempo para encontrar a solucao: {fim - inicio:.6f} segundos")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()