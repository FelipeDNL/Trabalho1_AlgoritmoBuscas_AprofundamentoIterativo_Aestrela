<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>A* e Aprofundamento Interativo</title>
    <link rel="stylesheet" href="./assets/style.css">
    <link rel="stylesheet" href="./assets/bootstrap.css">
    <link rel="icon" type="image/jpg" href="./assets/ifsc.png" />
</head>

<body>
    <?php
    $estoque = "";
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
    ?>

    <header>
        <div class="header-logo">
            <a href="https://www.ifsc.edu.br/web/campus-lages" target="_blank">
                <img src="./assets/logo.png" alt="Logo do IFSC">
            </a>
        </div>
        <nav class="menu navbar navbar-expand-lg">
            <div class="collapse navbar-collapse" id="menu">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="#sobre">Sobre</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./scripts/a_Estrela.py" download>A*</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./scripts/Aprofundamento_Interativo.py" download>Aprofundamento
                            Interativo</a>
                    </li>
                </ul>
            </div>
        </nav>
        <div class="alunos">
            <button class="btn btn-outline-dark alunos-botao" id="botao" onclick="mostrarAlunos()">Alunos</button>
            <span class="alunos-text" id="alunos">
                Artur Mihok <br>
                Felipe Davi <br>
                Igor Minerva <br>
                Silvio Wienieski
            </span>
        </div>
    </header>

    <main>
        <div style="margin-top: 60px; position:absolute" id="sobre"></div>
        <div class="sobre">
            <div class="st-1">
                <h2>IA - Algoritmos de Busca</h2>
                <hr>
                <p>Imagine uma ferramenta online que ajuda você a encontrar o caminho mais eficiente em um
                    labirinto,
                    planejar uma viagem com múltiplos destinos ou até mesmo sugerir as melhores opções de rotas para
                    entregas. Este projeto utiliza duas técnicas poderosas chamadas "Aprofundamento Iterativo" e "A*
                    (A
                    Estrela)" para tornar essas tarefas mais simples e eficazes.</p>
                <p>Em resumo, este projeto combina a potência dos algoritmos de busca com a facilidade de uso de uma
                    aplicação web. Ele pode ser aplicado em uma variedade de situações, desde planejar férias até
                    otimizar operações logísticas. Tudo o que você precisa fazer é definir o seu problema, e o
                    sistema
                    fará o resto, encontrando a melhor solução para você.</p>
            </div>
            <div class="st-2">
                <h4>A* (A Estrela)</h4>
                <p>O algoritmo A* é como um navegador GPS inteligente. Ele usa uma heurística para estimar quão
                    longe estamos do nosso destino e, em seguida, prioriza as ações que parecem mais promissoras.
                    Isso ajuda a encontrar a rota mais rápida e eficiente, economizando tempo e recursos.</p>
                <h4>Aprofundamento Iterativo</h4>
                <p>O aprofundamento iterativo é como um explorador que mergulha cada vez mais fundo no problema até
                    encontrar a solução. Funciona como uma busca gradual e persistente. Se a solução não for
                    encontrada em uma tentativa, o sistema aprofunda a pesquisa, explorando novas possibilidades,
                    tornando-o altamente eficiente para encontrar soluções mesmo em problemas desafiadores.</p>
            </div>
        </div>

        <div class="scripts">
            <h2>Implementação</h2>
            <p>Centros de distribuição precisam de muita organização e sistemas informatizados para localização e
                despacho das mercadorias. A figura apresenta o mapa de um depósito fictício de 185m², com as
                seguintes características:</p>
            <ul>
                <li>Cada célula da matriz representa o espaço de um metro quadrado.</li>
                <li>As células numeradas indicam a existência de uma estante naquela localização e o número
                    representa o seu código identificador</li>
                <li>As células R1 a R5 representam as posições iniciais de cada um dos cinco robôs existentes neste
                    depósito no início do dia.</li>
                <li>A célula X indica o ponto onde os robôs devem levar a estante para que a mercadoria seja
                    retirada
                    pelo funcionário.</li>
                <li>As células em branco representam os espaços livres por onde os robôs podem se movimentar.
                <li>Os robôs podem se movimentar verticalmente e horizontalmente, mas não diagonalmente.</li>
                <li>Ao receber um pedido, representado pelo código identificador da estante que armazena o produto
                    desejado, o sistema deve verificar qual robô está mais perto dela e enviar uma mensagem com a
                    rota a ser seguida para que o robô chegue até a estante. Esta rota é uma sequência de ações que
                    indica os movimentos a serem feitos pelos robôs (Cima, Baixo, Esquerda, Direita)</li>
            </ul>
            <p><strong>Scripts em Python:</strong></p>
            <div class="script-buttons">
                <a href="./scripts/a_Estrela.py" class="btn" download>A*</a>
                <a href="./scripts/Aprofundamento_Interativo.py" class="btn" download>Aprofundamento Interativo</a>
            </div>
        </div>

        <div class="implementacao">
            <div class="algoritmos">
                <?php
                echo "<table class='estoque'>";
                if ($estoque === "") $estoque = $deposito;
                // Abre o loop para as linhas da tabela
                for ($i = 0; $i < count($estoque); $i++) {
                    $k = 1;
                    echo "<tr class='row'>"; // Abre uma nova linha na tabela

                    // Loop através das colunas na linha atual
                    for ($j = 0; $j < count($estoque[$i]); $j++) {
                        if ($estoque[$i][$j] == -3) {
                            echo "<td class='column bold'><strong>R$k</strong></td>"; // Adiciona o robô
                            $k += 1;
                        } elseif ($estoque[$i][$j] == 0) {
                            echo "<td class='column'> </td>"; // Adiciona o espaço em branco à coluna
                        } elseif ($estoque[$i][$j] == -2) {
                            echo "<td class='column bn'> </td>"; // Adiciona o espaço em branco dos robos
                        } elseif ($estoque[$i][$j] == -1) {
                            echo "<td class='column'>X</td>"; // Adiciona o X
                        } else {
                            echo "<td class='column'>" . $estoque[$i][$j] . "</td>"; // Adiciona o valor da célula à coluna
                        }
                    }

                    echo "</tr>"; // Fecha a linha da tabela
                }

                // Fecha a tabela HTML
                echo "</table>";
                ?>
            </div>
            <div class="insercao">
                <p><strong>Implementação em PHP:</strong></p>
                <form method="POST" action="<?php echo $_SERVER['PHP_SELF']; ?>">
                    <input type="text" name="estante" id="cod_estante" placeholder="Digite o código da estante desejada:">
                    <div class="script-buttons">
                        <input type="submit" name="astar" class="btn" value="A*" />
                        <input type="submit" name="apint" class="btn" value="Aprofundamento Interativo" />
                    </div>
                </form>
                <div class="resposta">
                    <pre>
                    <?php
                    if (isset($_POST['estante']) && isset($_POST['astar'])) {
                        include 'scripts/a-estrela.php';

                        $robos = array(
                            new Robo("R1", array(12, 0)),
                            new Robo("R2", array(12, 1)),
                            new Robo("R3", array(12, 2)),
                            new Robo("R4", array(12, 3)),
                            new Robo("R5", array(12, 4))
                        );

                        $codigoEstanteDesejada = $_POST['estante'];
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
                    } elseif (isset($_POST['estante']) && isset($_POST['apint'])) {
                        include 'scripts/aprofundamento-interativo.php';

                        $robos = array(
                            new Robo("R1", array(12, 0)),
                            new Robo("R2", array(12, 1)),
                            new Robo("R3", array(12, 2)),
                            new Robo("R4", array(12, 3)),
                            new Robo("R5", array(12, 4))
                        );

                        $codigoEstanteDesejada = $_POST['estante'];
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
                    } else {
                        echo "Digite o código de uma estante.";
                    }
                    ?>
                    </pre>
                </div>
            </div>
        </div>


    </main>

    <footer>
        <p><strong>Repositório do GitHub: <a href="https://github.com/FelipeDNL/Trabalho1_AlgoritmoBuscas_AprofundamentoIterativo_Aestrela/">Trabalho1_AlgoritmoBuscas_AprofundamentoIterativo_Aestrela</strong></a>
        </p>
        <p style="color:#34a344">
            Instituto Federal de Educação, Ciência e Tecnologia de Santa Catarina - IFSC<br>
            Rua Heitor Vila Lobos, 225, São Francisco, CEP: 88506-400, Lages-SC<br>
            Telefone: (49) 3221-4256 <br>
            CNPJ 11.402.887/0011-32
        </p>
        <p>O conteúdo publicado nesta página é de responsabilidade exclusiva do docente e não representa
            necessariamente a opinião do Instituto Federal de Santa Catarina (IFSC).</p>
    </footer>

    <script>
        function mostrarAlunos() {
            var botao = document.getElementById("botao");
            var popup = document.getElementById("alunos");
            botao.classList.toggle("fundo-verde");
            popup.classList.toggle("show");
        }
    </script>
</body>

</html>