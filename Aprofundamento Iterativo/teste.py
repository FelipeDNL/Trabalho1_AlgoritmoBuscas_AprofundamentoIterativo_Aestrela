# Defina o depósito como uma lista de listas
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

# Função para verificar se uma posição é válida no depósito
def is_valid_position(row, col):
    return 0 <= row < len(deposito) and 0 <= col < len(deposito[0]) and deposito[row][col] == 0

# Função para criar o grafo a partir do depósito
def create_graph(deposito):
    graph = {}
    rows, cols = len(deposito), len(deposito[0])

    for row in range(rows):
        for col in range(cols):
            if deposito[row][col] > 0:
                node = (row, col)
                neighbors = []
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    r, c = row + dr, col + dc
                    if is_valid_position(r, c):
                        neighbors.append((r, c))
                graph[node] = neighbors

    return graph

print(type(create_graph(deposito)))

# Função de busca em profundidade iterativa (IDDFS)
def iddfs(graph, start, goal, depth):
    if start == goal:
        return [start]

    if depth <= 0:
        return None

    for neighbor in graph[start]:
        result = iddfs(graph, neighbor, goal, depth - 1)
        if result is not None:
            return [start] + result

    return None

# Encontre o caminho do robô para uma estante
start_node = (1, 2)  # Posição inicial do robô
goal_node = (1, 12)  # Posição da estante

graph = create_graph(deposito)
max_depth = len(deposito) * len(deposito[0])

for depth in range(max_depth):
    path = iddfs(graph, start_node, goal_node, depth)
    if path is not None:
        print("Caminho encontrado:", path)
        break

if path is None:
    print("Caminho não encontrado.")