# forest_fire_skin_resistence
Python mesa example forest_fire modificado<br />
Original disponível em https://github.com/projectmesa/mesa/tree/main/examples/forest_fire#forest_fireserverpy

## Hipótese

A modificação consiste na adição de uma nova variável (Tree skin thickness) que representa a resistência ao fogo da casaca da árvore. Quanto maior a resistência menor a chance de uma árvore pegar fogo, ogo menor a chence das chamas se espalharem. Com essa nova variável, podemos definir a resistência das árvore (número inteiro de 0 a 10) armazenada no atributo "skin". Com esse atributo, modificamos a função "step" em "agent.py" para que a propagação do fogo não só dependa da proximidade entre uma árvore e outra, mas também leva em consideração a possibilidade do fogo não ser capaz de queimar uma árvore mesmo ela estando perto o sufucuente.

## Sumário

Modelo que simula a propagação de um incêndio em uma floresta. O esquema apresenta a dorma de grid of cells, cada célula pode ter ou não uma árvore. Cada árvore está não queimada (Fine), queimando (On Fire) ou queimada (Burned Out). O fogo se espalha de uma árvore que está em chamas (On Fire) para uma árvore que esteja intacta (Fine) somente se vencer a resistência da casaca da árvore intacta (número randômico maior ou igual ao valor de resistência (skin) ); as árvores que pegam fogo eventualmente são totalmente consumidas (On Fire -> Burned Out). O processo continua até todas as árvores em chamas (On Fire) se transformarem em totalmente queimadas (Burned Out).

## Como rodar

No diretório forest_fire, utilize o comando:<br />
    `$ mesa runserver`<br />
Abra o browser em http://127.0.0.1:8521/.<br />
Defina os valores das variáveis "Tree skin thickness" e "Tree density", precione "Reset" e em seguida "Start".

## Arquivos CSV

O progrma gera dois arquivos .csv, "agent_var.csv" e "model_var.csv".<br />
"agent_var.csv" armazena o estado dos agentes (Fine, On Fire ou Burned Out) a cada iteração.<br />
"model_var.csv" armazena a porcentagem das árvores que sobreviveram e impediram o aumento da queimada porque sua resistência a protegeu.
