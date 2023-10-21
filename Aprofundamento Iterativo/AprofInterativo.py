class Robo:
    def __init__(self, nome, posicao_inicial):
        self.nome = nome
        self.posicao = posicao_inicial
        self.acoes_executadas = []

    def mover_para(self, destino, deposito):
        rota = aprofundamento_iterativo(deposito, self.posicao, destino)

        if rota:
            for acao in rota:
                self.executar_acao(acao)
            self.posicao = destino
            self.acoes_executadas.extend(rota)

            # Armazene a rota original
            self.rota_original = rota

    def executar_acao(self, acao):
        self.acoes_executadas.append(acao)

    def retornar_ao_ponto_inicial(self, deposito):
        if hasattr(self, 'rota_original'):
            rota_retorno = list(reversed(self.rota_original))
            for destino in rota_retorno:
                self.mover_para(destino, deposito)

class Node:
    def __init__(self, position, parent=None, depth=0):
        self.position = position
        self.parent = parent
        self.depth = depth

    def path(self):
        path = []
        current = self
        while current is not None:
            path.append(current.position)
            current = current.parent
        return list(reversed(path))


# Função aprofundamento_iterativo implementa busca em profundidade iterativa
def aprofundamento_iterativo(deposito, start, end):
    def dfs_limitado(node, depth, limit, visited):
        if depth > limit:
            return None

        if node.position == end:
            return [node.position]

        if depth < limit:
            for move in moves:
                new_x, new_y = node.position[0] + move[0], node.position[1] + move[1]
                if 0 <= new_x < len(deposito) and 0 <= new_y < len(deposito[0]) and deposito[new_x][new_y] == 0:
                    child_node = Node((new_x, new_y), parent=node, depth=depth + 1)
                    # Verifique se o nó já foi visitado
                    if child_node.position not in visited:
                        visited.add(child_node.position)
                        result = dfs_limitado(child_node, depth + 1, limit, visited)
                        if result:
                            result.append(node.position)
                            return result

    # Possíveis movimentos no depósito (cima, baixo, esquerda, direita)
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start_node = Node(start)

    visited = set()  # Conjunto para manter o controle dos nós visitados
    visited.add(start_node.position)

    for limit in range(1, len(deposito) * len(deposito[0])):
        print(f"Nível da árvore: {limit}")
        result = dfs_limitado(start_node, 0, limit, visited)
        if result:
            return list(reversed(result))

    return None


def acoes_possiveis(posicao, deposito):
    movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    acoes = []
    for movimento in movimentos:
        nova_posicao = (posicao[0] + movimento[0], posicao[1] + movimento[1])
        if 0 <= nova_posicao[0] < len(deposito) and 0 <= nova_posicao[1] < len(deposito[0]) and deposito[nova_posicao[0]][nova_posicao[1]] == 0:
            acoes.append(nova_posicao)
    return acoes


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
                print(".", end=" ")
            elif cell == -1:
                print("X", end=" ")
            elif cell == -3:
                print("R", end=" ")
            else:
                print(cell, end=" ")
        print()


def mover_robo_para_estante_e_retornar(robo, estante, deposito):
    rota_estante = aprofundamento_iterativo(deposito, robo.posicao, estante)

    if rota_estante:
        for destino in rota_estante:
            robo.mover_para(destino, deposito)
            imprimir_deposito(deposito, robos)

        # Inverter a rota para retornar
        rota_retorno = list(reversed(rota_estante))

        for destino in rota_retorno:
            robo.mover_para(destino, deposito)
            imprimir_deposito(deposito, robos)

        # Exibir todas as ações do robô
        print(f"Ações do Robô {robo.nome}: {robo.acoes_executadas}")
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
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 101],
        [102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116]
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
