# forest_fire_vs_fireman
Experimento da tarefa 5.2 de Computação Experimental 2021/2

    Gabriel Rocha Fontenele
    Matrícula: 15/0126760

# Modelo
O modelo escolhido consiste no modelo de exemplo para o framework MESA padrão referente a simulação forest_fire. A modificação feita nesta tarefa consiste em manipular a densidade de um novo tipo de agente presente na floresta: o bombeiro.

A adição foi pensada para responder a seguinte pergunta: "o que acontece se houver um agente inibidor do fenômeno fogo?"

## Hipótese levantada: 
Aumentando-se a quantidade de agentes inibidores de fogo, bombeiros, consequentemente maior será a quantidade desse tipo de agente presente na floresta e maior a probabilidade de o fogo cessar ou pelo menos reduzir os danos causados à vegetação por uma queimada.

## Alterações e justificativas:

***server.py:***
Foi adicionado o parâmetro manipulável de quantidade de grupos de bombeiros. Assim, é possível que o usuário controle a quantidade de agentes bombeiros que atuarão durante a simulação. O parâmetro pode ser modificado mediante a interface web. As árvores salvas pelos bombeiros assumem a cor azul, através de uma chave que foi adicionada às cores que representam os estados das árvores na grade de ocupação.

***model.py:***
No modelo, durante a criação dos agentes do tipo árvore, as ávores próximas aos bombeiros tem dispersão de 1 célula para as diagonais e alcance de até 8 células à direito de um bombeiro. As árvores compreendidas nessa área possuem maior probalidade de não serem afetadas pelo fogo. A probabilidade distribuída de que uma árvore, a partir do agente inibidor até a última árvore compreendida pelo alcance, pegue fogo vai de 2%, 6%, 14%, 30% até 60% a medida que vai se afastando para a direita. Quanto maior o grupo de bombeiros, maior o alcance de árvores que eles conseguem salvar do fogo.

***agent.py:***
Durante uma queimada, a medida que o fogo se aproxima de uma árvore próxima a um bombeiro, a intensidade do fogo é atribuída através de uma variável randômica, que pode ultrapassar ou não a resistência que a árvore apresenta. Quando mais próxima de um grupo de bombeiros ela estiver menor será a chance de que ela seja queimada. A variável que representa essa probabilidade foi chamada de strength no código.

## Como usar o simulador:
A partir do diretório raiz do framework mesa, rode o comando

    mesa runserver <caminho da pasta>/forest_fire_vs_fireman

A partir da interface web, pode se modificar os valores das densidades, tanto das ávores quanto dos bombeiros, através dos seus respectivos sliders, com clique e arraste. Quando maior for o valor de cada densidade, maior será o número de agentes presentes na grade de ocupação e consequentemente participantes da simulação após o início da simulação.

A simulação acaba quando não houver mais fogo atuando na simulação ou se interrompida pelo usuário através do botão de parada.

## Coleta de dados:
Após o fim de uma simulação, dois arquivos de extensão .csv são gerados, cada um contendo dados relevantes referentes a observação do experimento, sendo eles:

***agent_data:*** contendo valores assumidos pelas variáveis a nível de agente durante toda a execução da simulação, em forma de tabela.
* A primeira coluna mostra a iteração e funciona como se fosse o decorrer do tempo durante a observação de um fenômeno real.
* A segunda coluna mostra a quantidade de árvores que até a enésima iteração não foram afetadas pela propagação do fogo.
* A terceira coluna mostra a quantidade de árvores em chamas. 
* A quarta representa a quantidade de árvores danificadas pelo fogo.
* A quinta coluna mostra a quantidade de árvores nas quais o fogo foi rapidamente apagado, evitando a propagação do incêndio, até a enésima iteração.

***model_data:*** esse arquivo apresenta, a partir da segunda coluna, duas colunas com o valor dos parâmetros escolhido pelo usuário, sendo eles a densidade da floresta e a quantidade de grupos de bombeiros atuantes no combate às chamas. As próximas três colunas mostram no final da simulação, respectivamente:
* a quantidade de árvores não afetadas pelas chamas e árvores não afetadas pelo fogo, em termos de porcentagem, e esse valor pode ter recebido influência indireta da ação dos bombeiros \(porque as chamas foram impedidas de chegar a algumas árvores\);
* a quantidade de árvores cujo fogo foi rapidamente apagado pela ação dos bombeiros, em porcentagem, impedindo a propagação das chamas sobre ávores ainda não afetadas;
* e por fim a quantidade, em porcentagem, de vegetação queimada;

fornecendo assim uma idéia geral sobre a eficácia da ação dos agentes inibidores.
