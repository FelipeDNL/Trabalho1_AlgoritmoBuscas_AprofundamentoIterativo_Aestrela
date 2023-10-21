from treelib import Node, Tree
from queue import LifoQueue

class Estado:
  def __init__(self, cidade, pai, nivel):
    self.cidade = cidade
    self.pai = pai
    self.nivel = nivel

import numpy as np

# Defina o depósito
deposito = np.array([
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
    [-3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]
], dtype=int)



class BuscaProfundidadeLimitada:

  def __init__(self):
    self.rotas = {'Porto Alegre': ['Florianópolis','São Paulo'],
                  'Florianópolis': ['Curitiba','Porto Alegre'],
                  'Curitiba': ['Florianópolis','São Paulo','Rio de Janeiro'],
                  'São Paulo':['Belo Horizonte', 'Curitiba', 'Porto Alegre', 'Salvador'],
                  'Rio de Janeiro':['Belo Horizonte','Cuiabá', 'Curitiba'],
                  'Belo Horizonte': ['Brasília','Cuiabá', 'São Paulo','Rio de Janeiro'],
                  'Brasília': ['Belo Horizonte','Fortaleza'],
                  'Salvador': ['Fortaleza','São Paulo'],
                  'Cuiabá': ['Belo Horizonte','Manaus','Rio de Janeiro'],
                  'Fortaleza': ['Manaus','Salvador','Brasília'],
                  'Manaus': ['Cuiabá','Fortaleza']
  }

  def realizaBusca(self, origem, destino, limite):
    fronteira = LifoQueue()
    resultado, qtdVisitados, qtdExpandidos, arvore = self.busca(origem, destino, limite, fronteira)
    self.mostraResultado(resultado, qtdVisitados, qtdExpandidos, arvore)

  def busca(self, origem, destino, limite, fronteira):
    atual = Estado(origem, None, 0)
    fronteira.put(atual)
    visitados = set()
    visitados.add(atual.cidade)
    qtdVisitados = 1
    qtdExpandidos = 0
    ##### As próximas linhas são desnecessárias caso não se deseje ver a árvore no final da execução
    #arvore = Tree()
    #arvore.create_node(atual.cidade, atual)
    #####
    resultado = None
    # A única diferença entre a busca em profundidade limitada e o controle do nível da árvore por meio da variável n que é um novo critério no while para continuar a busca
    while not fronteira.empty() and resultado == None:
      atual = fronteira.get()
      qtdExpandidos += 1
      resultado, fronteira, visitados, qtdVisitados, arvore = self.geraFilhos(atual, destino, fronteira, visitados, qtdVisitados, arvore, limite)
    return resultado, qtdVisitados, qtdExpandidos, arvore

#Implementação do método geraFilhos. Este método recebe um nodo da árvore como parâmetro e gera os filhos possíveis consultando a lista de adjacências.
#Ele também recebe como parâmetro a cidade de destino para saber se chegou ao resultado ou não e o limite para verificar se atingiu o limite estabelecido.
  def geraFilhos(self, atual,  destino, fronteira, visitados, qtdVisitados, arvore, limite):
    cidades = self.rotas.get(atual.cidade)
    for c in cidades:
      if (c==destino):
        qtdVisitados += 1
        novo = Estado(c, atual, atual.nivel+1)
        visitados.add(c)
        # Esta linha é desnecessária caso não se deseje ver a árvore no final da execução
        arvore.create_node(c, novo, parent=atual)
        return novo, fronteira, visitados, qtdVisitados, arvore
      else:
        # Se os dois ifs abaixo estiverem comentados, a busca vai gerar estados repetidos na árvore, inclusive filhos que serão iguais ao pai de um nó (avô).
        # Se o primeiro if estiver comentado e o segundo if não a busca não vai gerar nenhum estado repetido no árvore
        # Se o segundo if estiver comentando e o primeiro não, a busca vai gerar estados repetidos na árvore, mas não gerará filhos iguais ao avô.

        #if atual.pai == None or c != atual.pai.cidade:
        if c not in visitados:
          qtdVisitados += 1
          visitados.add(c)
          novo = Estado(c, atual, atual.nivel+1)
          # Esta linha é desnecessária caso não se deseje ver a árvore no final da execução
          arvore.create_node(c, novo, parent=atual)
          if atual.nivel + 1 < limite:
            fronteira.put(novo)
    return None, fronteira, visitados, qtdVisitados, arvore


#Implementação do método que apresenta os resultados da busca. O resultado está na ordem inversa pois ele é descoberto retornando do estado final até o estado inicial,
#consultando o atributo pai da classe Estado. Para apresentá-lo na ordem correta, basta inserir os estados em uma lista,
#em vez de mostrá-los diretamente e depois mostrar a lista na ordem inversa.
  def mostraResultado(self, resultado, qtdVisitados, qtdExpandidos, arvore):
    if (resultado==None):
      print('Solução não encontrada.')
    else:
      print('***Rota encontrada***')
      while (resultado != None):
        print(resultado.cidade)
        resultado = resultado.pai
    print('Estados visitados: ',qtdVisitados)
    print('Estados expandidos: ',qtdExpandidos)
    print('****Árvore gerada****')
    arvore.show()

class BuscaAprofundamentoIterativo(BuscaProfundidadeLimitada):

  def __init__(self):
    super().__init__()

  def realizaBusca(self, origem, destino):
    for i in range(1,10):
      fronteira = LifoQueue()
      print("****limite ",i," ***")
      resultado, qtdVisitados, qtdExpandidos, arvore = self.busca(origem, destino, i, fronteira)
      if resultado != None:
        self.mostraResultado(resultado, qtdVisitados, qtdExpandidos, arvore)
        break;

algbusca = BuscaAprofundamentoIterativo()
algbusca.realizaBusca('Porto Alegre','Manaus')