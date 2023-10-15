Centros de distribuição precisam de muita organização e sistemas informatizados para localização e despacho das mercadorias. A figura 1 apresenta o mapa de um depósito fictício de 185m², com as seguintes características:
- Cada célula da matriz representa o espaço de um metro quadrado.
- As células numeradas indicam a existência de uma estante naquela localização e o número representa o seu código identificador.
- As células R1 a R5 representam as posições iniciais de cada um dos cinco robôs existentes neste depósito no início do dia.
- A célula X indica o ponto onde os robôs devem levar a estante para que a mercadoria seja retirada pelo funcionário.
- As células em branco representam os espaços livres por onde os robôs podem se movimentar.
- Os robôs podem se movimentar verticalmente e horizontalmente, mas não diagonalmente.
- Ao receber um pedido, representado pelo código identificador da estante que armazena o produto desejado, o sistema deve verificar qual robô está mais perto dela e enviar uma mensagem com a rota a ser seguida para que o robô chegue até a estante. Esta rota é uma sequência de ações que indica os movimentos a serem feitos pelos robôs (Cima, Baixo, Esquerda, Direita).
- Ao chegar na estante, o robô a suspenderá e a levará até a posição X, seguindo um caminho fixo que consiste em andar para baixo pelo corredor onde está a estante, virar à direita na penúltima linha e seguir até a última coluna onde está a posição X. Em seguida, o robô deve fazer o mesmo caminho na volta para guardar a estante no local onde ela estava e ficar parado sob a estante aguardando um novo chamado.
