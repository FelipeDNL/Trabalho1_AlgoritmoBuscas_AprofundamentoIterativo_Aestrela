<?php
class Robo
{
    private $nome;
    private $posicao;
    private $acoesExecutadas;

    public function __construct($nome, $posicaoInicial)
    {
        $this->nome = $nome;
        $this->posicao = $posicaoInicial;
        $this->acoesExecutadas = array();
    }

    public function moverPara($destino, $deposito, $robos)
    {
        $rota = AStar::findPath($deposito, $this->posicao, $destino);

        if ($rota) {
            foreach ($rota as $acao) {
                $this->executarAcao($acao);
            }
            $this->posicao = $destino;
            $this->acoesExecutadas = array_merge($this->acoesExecutadas, $rota);
            Deposito::imprimirDeposito($deposito, $robos);
        }
    }

    public function executarAcao($acao)
    {
        $this->acoesExecutadas[] = $acao;
    }

    public function setPosicao($posicao)
    {
        $this->posicao = $posicao;
    }

    public function getPosicao()
    {
        return $this->posicao;
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

    public function setCodigo($codigo)
    {
        $this->codigo = $codigo;
    }

    public function getCodigo()
    {
        return $this->codigo;
    }

    public function setPosicao($posicao)
    {
        $this->posicao = $posicao;
    }

    public function getPosicao()
    {
        return $this->posicao;
    }
}

class AStar
{
    public static function findPath($deposito, $start, $goal)
    {
        $movimentos = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        $direcoes = ["Direita", "Esquerda", "Baixo", "Cima"];
        $openSet = [];
        $cameFrom = [];
        $gScore = [];
        $fScore = [];
        $gScore[$start] = 0;
        $fScore[$start] = self::heuristica($start, $goal);
        $openSet[] = $start;

        while (!empty($openSet)) {
            $current = self::getLowestFScoreNode($openSet, $fScore);
            if ($current == $goal) {
                return self::reconstructPath($cameFrom, $current);
            }

            $key = array_search($current, $openSet);
            unset($openSet[$key]);

            foreach ($movimentos as $movimento) {
                $neighbor = [$current[0] + $movimento[0], $current[1] + $movimento[1]];

                if (self::isValidMove($neighbor, $deposito)) {
                    $tentativeGScore = $gScore[$current] + 1;

                    if (!array_key_exists($neighbor, $gScore) || $tentativeGScore < $gScore[$neighbor]) {
                        $cameFrom[$neighbor] = $current;
                        $gScore[$neighbor] = $tentativeGScore;
                        $fScore[$neighbor] = $gScore[$neighbor] + self::heuristica($neighbor, $goal);

                        if (!in_array($neighbor, $openSet)) {
                            $openSet[] = $neighbor;
                        }
                    }
                }
            }
        }

        return null;
    }

    private static function getLowestFScoreNode($openSet, $fScore)
    {
        $lowestF = PHP_INT_MAX;
        $lowestNode = null;

        foreach ($openSet as $node) {
            if ($fScore[$node] < $lowestF) {
                $lowestF = $fScore[$node];
                $lowestNode = $node;
            }
        }

        return $lowestNode;
    }

    private static function reconstructPath($cameFrom, $current)
    {
        $totalPath = [$current];
        while (array_key_exists($current, $cameFrom)) {
            $current = $cameFrom[$current];
            array_unshift($totalPath, $current);
        }
        return $totalPath;
    }

    private static function isValidMove($position, $deposito)
    {
        $row = $position[0];
        $col = $position[1];
        return $row >= 0 && $row < count($deposito) && $col >= 0 && $col < count($deposito[0]) && $deposito[$row][$col] === 0;
    }

    private static function heuristica($ponto1, $ponto2)
    {
        return abs($ponto1[0] - $ponto2[0]) + abs($ponto1[1] - $ponto2[1]);
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

    public function setPosition($value)
    {
        $this->position = $value;
    }

    public function setParent($value)
    {
        $this->parent = $value;
    }

    public function setG($value)
    {
        $this->g = $value;
    }

    public function setH($value)
    {
        $this->h = $value;
    }

    public function setF($value)
    {
        $this->f = $value;
    }

    public function getPosition()
    {
        return $this->position;
    }

    public function getParent()
    {
        return $this->parent;
    }

    public function getG()
    {
        return $this->g;
    }

    public function getH()
    {
        return $this->h;
    }

    public function getF()
    {
        return $this->f;
    }
}

class Deposito
{
    public static function imprimirDeposito($deposito, $robos)
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
}

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

function moverRoboParaEstanteERetornar($robo, $estante, $deposito, $robos)
{
    list($rotaEstanteX, $direcoesEstanteX) = AStar::findPath($deposito, $robo->getPosicao(), $estante);

    if ($rotaEstanteX) {
        $direcaoAnterior = "Desconhecida";

        for ($i = 0; $i < count($direcoesEstanteX); $i++) {
            $direcaoAtual = $direcoesEstanteX[$i];

            if ($direcaoAtual !== $direcaoAnterior) {
                $robo->executarAcao($direcaoAtual);
            }

            $direcaoAnterior = $direcaoAtual;

            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = 0;
            $robo->moverPara($rotaEstanteX[$i], $deposito, $robos);
            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = -3;
        }

        list($rotaRetorno, $direcoesRetorno) = AStar::findPath($deposito, $robo->getPosicao(), $estante);

        for ($i = 0; $i < count($direcoesRetorno); $i++) {
            $direcaoAtual = $direcoesRetorno[$i];

            if ($direcaoAtual !== $direcaoAnterior) {
                $robo->executarAcao($direcaoAtual);
            }

            $direcaoAnterior = $direcaoAtual;

            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = 0;
            $robo->moverPara($rotaRetorno[$i], $deposito, $robos);
            $deposito[$robo->getPosicao()[0]][$robo->getPosicao()[1]] = -3;
        }
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
    new Robo("R3", array(
12, 2)),
    new Robo("R4", array(12, 3)),
    new Robo("R5", array(12, 4))
);

while (true) {
    $codigoEstanteDesejada = readline("Digite o código da estante desejada (ou -1 para sair): ");

    if ($codigoEstanteDesejada == -1) {
        echo "Loop encerrado a pedido do usuário.";
        break;
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
}
