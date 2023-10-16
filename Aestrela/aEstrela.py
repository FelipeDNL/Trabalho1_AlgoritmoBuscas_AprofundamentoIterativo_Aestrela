import heapq

class Robo:
    def __init__(self, nome, posicao_inicial):
        self.nome = nome
        self.posicao = posicao_inicial
        self.acoes_executadas = []

    def mover_para(self, destino, deposito, robos):
        rota = astar(deposito, self.posicao, destino)

        if rota:
            for acao in rota:
                self.executar_acao(acao)
            self.posicao = destino
            self.acoes_executadas.extend(rota)
            imprimir_deposito(deposito, robos)

    def executar_acao(self, acao):
        self.acoes_executadas.append(acao)

class Estante:
    def __init__(self, codigo, posicao):
        self.codigo = codigo
        self.posicao = posicao

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

def astar(deposito, start, end):
    def heuristica(ponto1, ponto2):
        return abs(ponto1[0] - ponto2[0]) + abs(ponto1[1] - ponto2[1])

    movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimentos possíveis: direita, esquerda, baixo, cima
    direcoes = ["Direita", "Esquerda", "Baixo", "Cima"]  # Direções correspondentes

    open_set = []
    closed_set = set()

    start_node = Node(start)
    start_node.g = start_node.h = start_node.f = 0
    open_set.append(start_node)

    while open_set:
        open_set.sort(key=lambda x: x.f)  # Ordena pelo valor f do nó
        atual = open_set.pop(0)
        closed_set.add(atual.position)

        if atual.position != end:
            vizinhos = []
            for movimento in movimentos:
                vizinho_posicao = (atual.position[0] + movimento[0], atual.position[1] + movimento[1])

                if (
                    0 <= vizinho_posicao[0] < len(deposito)
                    and 0 <= vizinho_posicao[1] < len(deposito[0])
                    and deposito[vizinho_posicao[0]][vizinho_posicao[1]] == 0
                ):
                    vizinho = Node(vizinho_posicao, parent=atual)
                    vizinho.g = atual.g + 1
                    vizinho.h = heuristica(vizinho.position, end)
                    vizinho.f = vizinho.g + vizinho.h

                    if vizinho.position not in closed_set:
                        vizinhos.append(vizinho)

            for vizinho in vizinhos:
                if vizinho not in open_set:
                    open_set.append(vizinho)

    caminho = []
    direcoes_caminho = []  # Rastreia direções
    while atual.parent is not None:
        caminho.append(atual)
        atual = atual.parent

    direcoes_caminho = []
    for i in range(len(caminho) - 1, 0, -1):
        direcao_index = movimentos.index((caminho[i].position[0] - caminho[i - 1].position[0], caminho[i].position[1] - caminho[i - 1].position[1]))
        direcoes_caminho.append(direcoes[direcao_index])

    direcoes_caminho.reverse()
    return caminho[::-1], direcoes_caminho  # Retorna o caminho reverso e as direções

def encontrar_posicao_estante_por_codigo(codigo_estante, deposito):
    for row in range(len(deposito)):
        for col in range(len(deposito[row])):
            if deposito[row][col] == codigo_estante:
                return (row, col)
    return None

def encontrar_robo_mais_proximo(robos, estante):
    def distancia_entre_pontos(ponto1, ponto2):
        return abs(ponto1[0] - ponto2[0]) + abs(ponto1[1] - ponto2[1])

    robo_mais_proximo = None
    menor_distancia = float('inf')

    for robo in robos:
        distancia = distancia_entre_pontos(robo.posicao, estante)
        if distancia < menor_distancia:
            robo_mais_proximo = robo
            menor_distancia = distancia

    return robo_mais_proximo

def imprimir_deposito(deposito, robos):
    deposito_com_robos = [list(row) for row in deposito]
    for robo in robos:
        deposito_com_robos[robo.posicao[0]][robo.posicao[1]] = -3

    for row in deposito_com_robos:
        for cell in row:
            if cell == 0:
                print(".", end=" ")  # Célula vazia
            elif cell == -1:
                print("X", end=" ")  # Célula com o valor -1 (posição final)
            elif cell == -3:
                print("R", end=" ")  # Célula com o valor -3 (posição atual do robô)
            else:
                print(cell, end=" ")  # Outros valores no depósito
        print()  # Nova linha após cada linha da matriz

def mover_robo_para_estante_e_retornar(robo, estante, deposito):
    rota_estante_x, direcoes_estante_x = astar(deposito, robo.posicao, estante)

    if rota_estante_x:
        # Inicialize a direção do primeiro movimento como "Desconhecida"
        direcao_anterior = "Desconhecida"

        for i in range(len(direcoes_estante_x)):
            direcao_atual = direcoes_estante_x[i]

            # Se a direção atual não for a mesma que a anterior, execute a ação
            if direcao_atual != direcao_anterior:
                robo.acoes_executadas.append(direcao_atual)

            direcao_anterior = direcao_atual

            # Atualize a posição do robô no depósito
            deposito[robo.posicao[0]][robo.posicao[1]] = 0
            robo.mover_para(rota_estante_x[i].position, deposito, robos)
            deposito[robo.posicao[0]][robo.posicao[1]] = -3

        # Retornar à estante
        rota_retorno, direcoes_retorno = astar(deposito, robo.posicao, estante)

        for i in range(len(direcoes_retorno)):
            direcao_atual = direcoes_retorno[i]

            # Se a direção atual não for a mesma que a anterior, execute a ação
            if direcao_atual != direcao_anterior:
                robo.acoes_executadas.append(direcao_atual)

            direcao_anterior = direcao_atual

            # Atualize a posição do robô no depósito
            deposito[robo.posicao[0]][robo.posicao[1]] = 0
            robo.mover_para(rota_retorno[i].position, deposito, robos)
            deposito[robo.posicao[0]][robo.posicao[1]] = -3

        # Exibir todas as ações do robô
        #print(f"Ações do Robô {robo.nome}: {robo.acoes_executadas}")
    else:
        print(f"Não foi possível encontrar um caminho para a estante.")

# Defina o depósito
deposito = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 11, 21, 0, 31, 41, 0, 51, 61, 0, 71, 81, 0, 91],
    [2, 0, 12, 22, 0, 32, 42, 0, 52, 62, 0, 72, 82, 0, 92],
    [3, 0, 13, 23, 0, 33, 43, 0, 53, 63, 0, 72, 82, 0, 92],
    [4, 0, 14, 24, 0, 34, 44, 0, 54, 64, 0, 73, 83, 0, 93],
    [5, 0, 15, 25, 0, 35, 45, 0, 55, 65, 0, 75, 85, 0, 95],
    [6, 0, 16, 26, 0, 36, 46, 0, 56, 66, 0, 76, 86, 0, 96],
    [7, 0, 17, 27, 0, 37, 47, 0, 57, 67, 0, 77, 87, 0, 97],
    [8, 0, 18, 28, 0, 38, 48, 0, 58, 68, 0, 78, 88, 0, 98],
    [9, 0, 19, 29, 0, 39, 49, 0, 59, 69, 0, 79, 89, 0, 99],
    [10, 0, 20, 30, 0, 40, 50, 0, 60, 70, 0, 80, 90, 0, 100],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [-3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]
]

# Defina os robôs
robos = [Robo("R1", (12, 0)), Robo("R2", (12, 1)), Robo("R3", (12, 2)), Robo("R4", (12, 3)), Robo("R5", (12, 4))]

# Loop para realizar tarefas sequencialmente
while True:
    codigo_estante_desejada = int(input("Digite o código da estante desejada (ou -1 para sair): "))

    if codigo_estante_desejada == -1:
        print("Loop encerrado a pedido do usuário.")
        break

    posicao_estante = encontrar_posicao_estante_por_codigo(codigo_estante_desejada, deposito)

    if posicao_estante:
        estante_desejada = posicao_estante
        robo_disponivel = encontrar_robo_mais_proximo(robos, estante_desejada)

        if robo_disponivel:
            mover_robo_para_estante_e_retornar(robo_disponivel, estante_desejada, deposito)
        else:
            print("Nenhum robô disponível para a estante desejada.")
    else:
        print(f"Estante com código {codigo_estante_desejada} não encontrada no depósito.")
