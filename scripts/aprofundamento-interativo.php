<?php
class Robo
{
    private $nome;
    private $posicao;
    private $acoesExecutadas;

    public function __construct($nome, $posicaoInicial)
    {
        // Inicializa um objeto Robo com um nome e uma posição inicial
        $this->nome = $nome;
        $this->posicao = $posicaoInicial;
        $this->acoesExecutadas = array();
    }

    public function moverPara($destino, $deposito, $robos)
    {
        // Move o robô para o destino no depósito usando o algoritmo A*
        $rota = aprofundamentoIterativo($deposito, $this->posicao, $destino);

        if ($rota) {
            foreach ($rota as $acao) {
                $this->executarAcao($acao);
            }
            $this->posicao = $destino;
            $this->acoesExecutadas = array_merge($this->acoesExecutadas, $rota);
            imprimirDeposito($deposito, $robos);
        }
    }

    // Método para executar uma ação e adicioná-la à lista de ações executadas
    public function executarAcao($acao)
    {
        $this->acoesExecutadas[] = $acao;
    }

    // Setter para $posicao
    public function setPosicao($posicao)
    {
        $this->posicao = $posicao;
    }

    // Getter para $posicao
    public function getPosicao()
    {
        return $this->posicao;
    }

    // Getter para $posicao
    public function getNome()
    {
        return $this->nome;
    }

    // Getter para $posicao
    public function getAcoesExecutadas()
    {
        return $this->acoesExecutadas;
    }
}

class Estante
{
    private $codigo;
    private $posicao;

    public function __construct($codigo, $posicao)
    {
        $this->codigo = $codigo;
        $this->posicao = $posicao;
    }

    // Setter para $codigo
    public function setCodigo($codigo)
    {
        $this->codigo = $codigo;
    }

    // Getter para $codigo
    public function getCodigo()
    {
        return $this->codigo;
    }

    // Setter para $posicao
    public function setPosicao($posicao)
    {
        $this->posicao = $posicao;
    }

    // Getter para $posicao
    public function getPosicao()
    {
        return $this->posicao;
    }
}

class Node
{
    private $position;
    private $parent;
    private $g;
    private $h;
    private $f;

    public function __construct($position, $parent = null)
    {
        $this->position = $position;
        $this->parent = $parent;
        $this->g = 0;
        $this->h = 0;
        $this->f = 0;
    }

    public function __lt($other)
    {
        return ($this->g + $this->h) < ($other->g + $other->h);
    }

    public function setPosition($value)
    {
        $this->position = $value;
    } // Define a posição
    public function setParent($value)
    {
        $this->parent = $value;
    } // Define o parente
    public function setG($value)
    {
        $this->g = $value;
    } // Define o g
    public function setH($value)
    {
        $this->h = $value;
    } // Define o h
    public function setF($value)
    {
        $this->f = $value;
    } // Define o f

    public function getPosition()
    {
        return $this->position;
    } // Retorna a posição
    public function getParent()
    {
        return $this->parent;
    } // Retorna o parent
    public function getG()
    {
        return $this->g;
    } // Retorna o g
    public function getH()
    {
        return $this->h;
    } // Retorna o h
    public function getF()
    {
        return $this->f;
    } // Retorna o f
}

function heuristica($ponto1, $ponto2)
{
    // Função heurística que estima o custo restante (heurístico) entre dois pontos
    return abs($ponto1[0] - $ponto2[0]) + abs($ponto1[1] - $ponto2[1]);
}

function aprofundamentoIterativo($deposito, $start, $end)
{
    $moves = [[1, 0], [-1, 0], [0, 1], [0, -1]];

    $dfsLimitado = function ($node, $depth, $limit) use ($deposito, $end, $moves, &$dfsLimitado) {
        if ($depth > $limit) {
            return null;
        }

        if ($node->getPosition() === $end) {
            return [$node->getPosition()];
        }

        if ($depth < $limit) {
            foreach ($moves as $move) {
                $newX = $node->getPosition()[0] + $move[0];
                $newY = $node->getPosition()[1] + $move[1];

                if (
                    $newX >= 0 && $newX < count($deposito) &&
                    $newY >= 0 && $newY < count($deposito[0]) &&
                    $deposito[$newX][$newY] == 0
                ) {
                    $childNode = new Node([$newX, $newY], $node, $depth + 1);
                    $result = $dfsLimitado($childNode, $depth + 1, $limit);
                    if ($result) {
                        $result[] = $node->getPosition();
                        return $result;
                    }
                }
            }
        }
    };

    $startNode = new Node($start);

    for ($limit = 1; $limit < count($deposito) * count($deposito[0]); $limit++) {
        echo "Nível da árvore: " . $limit . PHP_EOL;
        $result = $dfsLimitado($startNode, 0, $limit);
        if ($result) {
            return array_reverse($result);
        }
    }

    return null;
}


// Função q encontra a posição de uma estante no depósito com base no seu código
function encontrarPosicaoEstantePorCodigo($codigo_estante, $deposito)
{
    for ($row = 0; $row < count($deposito); $row++) {
        for ($col = 0; $col < count($deposito[$row]); $col++) {
            if ($deposito[$row][$col] == $codigo_estante) {
                return [$row, $col];
            }
        }
    }
    return null;
}

// Encontra o robô mais próximo de uma determinada estante
function encontrarRoboMaisProximo($robos, $estante)
{
    $distanciaEntrePontos = function ($ponto1, $ponto2) {
        return abs($ponto1[0] - $ponto2[0]) + abs($ponto1[1] - $ponto2[1]);
    };

    $robo_mais_proximo = null;
    $menor_distancia = INF;

    foreach ($robos as $robo) {
        $distancia = $distanciaEntrePontos($robo->getPosicao(), $estante);
        if ($distancia < $menor_distancia) {
            $robo_mais_proximo = $robo;
            $menor_distancia = $distancia;
        }
    }

    return $robo_mais_proximo;
}


function imprimirDeposito($deposito, $robos)
{
    $depositoComRobos = array_map(function ($row) {
        return $row;
    }, $deposito);

    foreach ($robos as $robo) {
        $posicaoRobo = $robo->getPosicao();
        $depositoComRobos[$posicaoRobo[0]][$posicaoRobo[1]] = -3;
    }

    foreach ($depositoComRobos as $row) {
        foreach ($row as $cell) {
            if ($cell == 0) {
                echo "-- ";
            } elseif ($cell == -1) {
                echo "XX ";
            } elseif ($cell == -2) {
                echo "   ";
            } elseif ($cell == -3) {
                echo "RR ";
            } elseif ($cell > 0 && $cell < 10) {
                echo "0" . $cell . " ";
            } else {
                echo $cell . " ";
            }
        }
        echo PHP_EOL;
    }
}


function moverRoboParaEstanteERetornar($robo, $estante, $deposito, $robos)
{
    list($rotaEstanteX, $direcoesEstanteX) = aprofundamentoIterativo($deposito, $robo->getPosicao(), $estante);

    if ($rotaEstanteX) {
        $direcaoAnterior = "Desconhecida";  // Inicialize a direção do primeiro movimento como "Desconhecida"

        for ($i = 0; $i < count($direcoesEstanteX); $i++) {
            $direcaoAtual = $direcoesEstanteX[$i];

            // Se a direção atual não for a mesma que a anterior, execute a ação
            if ($direcaoAtual !== $direcaoAnterior) {
                $robo->executarAcao($direcaoAtual);
            }

            $direcaoAnterior = $direcaoAtual;

            // Atualize a posição do robô no depósito
            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = 0;
            $robo->moverPara($rotaEstanteX[$i]->getPosition(), $deposito, $robos);
            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = -3;
        }

        // Retornar à estante
        list($rotaRetorno, $direcoesRetorno) = aprofundamentoIterativo($deposito, $robo->getPosicao(), $estante);

        for ($i = 0; $i < count($direcoesRetorno); $i++) {
            $direcaoAtual = $direcoesRetorno[$i];

            // Se a direção atual não for a mesma que a anterior, execute a ação
            if ($direcaoAtual !== $direcaoAnterior) {
                $robo->executarAcao($direcaoAtual);
            }

            $direcaoAnterior = $direcaoAtual;

            // Atualize a posição do robô no depósito
            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = 0;
            $robo->moverPara($rotaRetorno[$i]->getPosition(), $deposito, $robos);
            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = -3;
        }

        // Exiba todas as ações do robô
        // echo "Ações do Robô " . $robo->getNome() . ": " . implode(", ", $robo->getAcoesExecutadas()) . PHP_EOL;
    } else {
        echo "Não foi possível encontrar um caminho para a estante." . PHP_EOL;
    }
}


$deposito = array(
    array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    array(1, 0, 11, 21, 0, 31, 41, 0, 51, 61, 0, 71, 81, 0, 91),
    array(2, 0, 12, 22, 0, 32, 42, 0, 52, 62, 0, 72, 82, 0, 92),
    array(3, 0, 13, 23, 0, 33, 43, 0, 53, 63, 0, 72, 82, 0, 92),
    array(4, 0, 14, 24, 0, 34, 44, 0, 54, 64, 0, 73, 83, 0, 93),
    array(5, 0, 15, 25, 0, 35, 45, 0, 55, 65, 0, 75, 85, 0, 95),
    array(6, 0, 16, 26, 0, 36, 46, 0, 56, 66, 0, 76, 86, 0, 96),
    array(7, 0, 17, 27, 0, 37, 47, 0, 57, 67, 0, 77, 87, 0, 97),
    array(8, 0, 18, 28, 0, 38, 48, 0, 58, 68, 0, 78, 88, 0, 98),
    array(9, 0, 19, 29, 0, 39, 49, 0, 59, 69, 0, 79, 89, 0, 99),
    array(10, 0, 20, 30, 0, 40, 50, 0, 60, 70, 0, 80, 90, 0, 100),
    array(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1),
    array(-3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2)
);

$robos = array(
    new Robo("R1", array(12, 0)),
    new Robo("R2", array(12, 1)),
    new Robo("R3", array(12, 2)),
    new Robo("R4", array(12, 3)),
    new Robo("R5", array(12, 4))
);

if ($codigoEstanteDesejada == -1) {
    echo "Loop encerrado a pedido do usuário.";
}

$posicaoEstante = encontrarPosicaoEstantePorCodigo($codigoEstanteDesejada, $deposito);

if ($posicaoEstante !== null) {
    $estanteDesejada = $posicaoEstante;
    $roboDisponivel = encontrarRoboMaisProximo($robos, $estanteDesejada);

    if ($roboDisponivel !== null) {
        moverRoboParaEstanteERetornar($roboDisponivel, $estanteDesejada, $deposito, $robos);
    } else {
        echo "Nenhum robô disponível para a estante desejada.";
    }
} else {
    echo "Estante com código $codigoEstanteDesejada não encontrada no depósito.";
}
