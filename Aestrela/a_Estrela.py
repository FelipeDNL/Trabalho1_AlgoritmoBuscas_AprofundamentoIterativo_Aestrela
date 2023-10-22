import heapq

class Robo:
    def __init__(self, nome, posicao_inicial):
        #inicializa um objeto Robo com um nome e uma posição inicial
        self.nome = nome
        self.posicao = posicao_inicial
        self.acoes_executadas = []

    def mover_para(self, destino, deposito, robos):
        #move o robô para o destino no depósito usando o algoritmo A*
        rota = astar(deposito, self.posicao, destino)

        if rota:
            #rxecuta as ações na rota para chegar ao destino
            for acao in rota:
                self.executar_acao(acao)
            self.posicao = destino
            self.acoes_executadas.extend(rota)
            imprimir_deposito(deposito, robos) #atualiza a representação do depósito após a movimentação

    def executar_acao(self, acao):
        #executa uma ação e a adiciona à lista de ações executadas pelo robô
        self.acoes_executadas.append(acao)

class Estante:
    def __init__(self, codigo, posicao):
        #inicializa um objeto de estante com um código e uma posição
        self.codigo = codigo
        self.posicao = posicao

class Node:
    def __init__(self, position, parent=None):
        #representa um nó na busca A* com uma posição e um nó pai
        self.position = position
        self.parent = parent
        self.g = 0  #custo acumulado do início até este nó
        self.h = 0  #custo heurístico estimado do nó até o destino
        self.f = 0  #custo total f (f = g + h)

    def __lt__(self, other):
        #método para comparar nós com base em seus valores f
        return (self.g + self.h) < (other.g + other.h)

def astar(deposito, start, end):
    #a função A* encontra o caminho mais curto de 'start' para 'end' em um depósito

    def heuristica(ponto1, ponto2):
        #função heurística que estima o custo restante (heurístico) entre dois pontos
        return abs(ponto1[0] - ponto2[0]) + abs(ponto1[1] - ponto2[1])

    movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  #movimentos possíveis: direita, esquerda, baixo, cima
    direcoes = ["Direita", "Esquerda", "Baixo", "Cima"]  #direções correspondentes

    open_set = []  #lista de nós a serem explorados
    closed_set = set()  #conjunto de nós já explorados


    start_node = Node(start) #nó inicial
    start_node.g = start_node.h = start_node.f = 0 #inicializa os valores de custo g, heurístico h e custo total f
    open_set.append(start_node) #adiciona o nó inicial à lista de nós abertos

    while open_set:
        open_set.sort(key=lambda x: x.f)  #ordena pelo valor f do nó
        atual = open_set.pop(0) #remove o nó com menor custo f da lista
        closed_set.add(atual.position) #adiciona o nó atual ao conjunto de nós fechados

        if atual.position != end:
            vizinhos = []
            for movimento in movimentos:
                vizinho_posicao = (atual.position[0] + movimento[0], atual.position[1] + movimento[1])

                if (
                    0 <= vizinho_posicao[0] < len(deposito)
                    and 0 <= vizinho_posicao[1] < len(deposito[0])
                    and deposito[vizinho_posicao[0]][vizinho_posicao[1]] == 0
                ):
                    vizinho = Node(vizinho_posicao, parent=atual)  #cria um novo nó vizinho
                    vizinho.g = atual.g + 1  #custo g é a distância até o vizinho
                    vizinho.h = heuristica(vizinho.position, end)  #custo heurístico h estimado
                    vizinho.f = vizinho.g + vizinho.h  #custo total f

                    if vizinho.position not in closed_set:
                        vizinhos.append(vizinho)

            for vizinho in vizinhos:
                if vizinho not in open_set:
                    open_set.append(vizinho)  #adiciona vizinhos à lista de nós abertos se ainda não estiverem lá

    caminho = []  #lista para armazenar o caminho
    direcoes_caminho = []  #lista para rastrear direções

    while atual.parent is not None:
        caminho.append(atual)  #adiciona o nó atual ao caminho
        atual = atual.parent  #move-se para o nó pai

    direcoes_caminho = []
    for i in range(len(caminho) - 1, 0, -1):
        #calcula as direções entre os nós no caminho
        direcao_index = movimentos.index((caminho[i].position[0] - caminho[i - 1].position[0], caminho[i].position[1] - caminho[i - 1].position[1]))
        direcoes_caminho.append(direcoes[direcao_index])

    direcoes_caminho.reverse()  #inverte a lista de direções
    return caminho[::-1], direcoes_caminho  #retorna o caminho reverso e as direções

#função q encontra a posição de uma estante no depósito com base no seu código
def encontrar_posicao_estante_por_codigo(codigo_estante, deposito):
    for row in range(len(deposito)):
        for col in range(len(deposito[row])):
            if deposito[row][col] == codigo_estante:
                return (row, col)
    return None

#encontra o robô mais próximo de uma determinada estante
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

#imprime o depósito com as posições dos robôs marcadas
def imprimir_deposito(deposito, robos):
    deposito_com_robos = [list(row) for row in deposito]
    for robo in robos:
        deposito_com_robos[robo.posicao[0]][robo.posicao[1]] = -3

    for row in deposito_com_robos:
        for cell in row:
            if cell == 0:
                print(".", end=" ")  #célula vazia
            elif cell == -1:
                print("X", end=" ")  #célula com o valor -1 (posição final)
            elif cell == -3:
                print("R", end=" ")  #célula com o valor -3 (posição atual do robô)
            else:
                print(cell, end=" ")  #outros valores no depósito
        print()  #nova linha após cada linha da matriz

def mover_robo_para_estante_e_retornar(robo, estante, deposito):
    rota_estante_x, direcoes_estante_x = astar(deposito, robo.posicao, estante)

    if rota_estante_x:
        #inicialize a direção do primeiro movimento como "Desconhecida"
        direcao_anterior = "Desconhecida"

        for i in range(len(direcoes_estante_x)):
            direcao_atual = direcoes_estante_x[i]

            #se a direção atual não for a mesma que a anterior, execute a ação
            if direcao_atual != direcao_anterior:
                robo.acoes_executadas.append(direcao_atual)

            direcao_anterior = direcao_atual

            #atualize a posição do robô no depósito
            deposito[robo.posicao[0]][robo.posicao[1]] = 0
            robo.mover_para(rota_estante_x[i].position, deposito, robos)
            deposito[robo.posicao[0]][robo.posicao[1]] = -3

        #retornar à estante
        rota_retorno, direcoes_retorno = astar(deposito, robo.posicao, estante)

        for i in range(len(direcoes_retorno)):
            direcao_atual = direcoes_retorno[i]

            #se a direção atual não for a mesma que a anterior, execute a ação
            if direcao_atual != direcao_anterior:
                robo.acoes_executadas.append(direcao_atual)

            direcao_anterior = direcao_atual

            #atualize a posição do robô no depósito
            deposito[robo.posicao[0]][robo.posicao[1]] = 0
            robo.mover_para(rota_retorno[i].position, deposito, robos)
            deposito[robo.posicao[0]][robo.posicao[1]] = -3

        #exibir todas as ações do robô
        #print(f"Ações do Robô {robo.nome}: {robo.acoes_executadas}")
    else:
        print(f"Não foi possível encontrar um caminho para a estante.")

#definir depósito
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

#definir robôs
robos = [Robo("R1", (12, 0)), Robo("R2", (12, 1)), Robo("R3", (12, 2)), Robo("R4", (12, 3)), Robo("R5", (12, 4))]

#loop para realizar tarefas sequencialmente
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
