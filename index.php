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
                        <a class="nav-link" href="./scripts/a_Estrela.py">A*</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="./scripts/Aprofundamento_Interativo.py">Aprofundamento
                            Interativo</a>
                    </li>
                </ul>
            </div>
        </nav>
        <div class="alunos">
            <button class="btn btn-outline-dark alunos-botao" id="botao" onclick="mostrarAlunos()">Alunos</button>
            <span class="alunos-text" id="alunos">
                Artur Mihok Cunha <br>
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
            <div class="script-buttons">
                <a href="./scripts/a_Estrela.py" class="btn" download>A*</a>
                <a href="./scripts/Aprofundamento_Interativo.py" class="btn" download>Aprofundamento Interativo</a>
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