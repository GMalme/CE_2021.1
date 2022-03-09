# Forest Fire Model

## Novo Modelo

O modelo Forest Fire Point and Resistance é um modelo de simulação de incêndios, baseado no exemplo "Forest Fire", fornecido no repositório do [framework MESA](https://github.com/projectmesa/mesa-examples). O modelo original é um simples simulador de incêndios que tem como variável do ambiente a densidade de árvores. O novo modelo, no entanto, apresenta duas variáveis que atribuem questões mais realistas a simulação: A intensidade e a localização do início do incêndio.

## Descrição da hipótese

Observando a execução do modelo, nota-se que o incêndio é gerado em todos os pontos com árvores localizadas na primeira coluna da matriz, exibindo apenas a dispersão do fogo entre as árvores, mas sem contar com fatores como a intensidade do fogo, que varia de acordo com o gerador do incêndio, e a localização do início do incêndio. A partir dessas adições, é possível observar casos de árvores que pela sua estrutura ou tipo, não são atingidas pelo fogo.

## Mudanças realizadas

### Variável "Fire Intensity"

De acordo com a expansão do fogo e sua intensidade, uma árvore é incendiada ou não de acordo com a probabilidade definida por essa variável.

### Posição do ponto inicial do incêndio

Definindo a posição inicial do incêndio, o modelo permite que sejam observados a expansão pontual do incêndio, assim como casos onde o incêndio não ocorre, visto que o ponto inicial não é incendiável por falta de vegetação na área.

## Como executar
No diretório forest_fire_point_and_resistance, execute o comando ``mesa runserver``.

Aguarde o modelo ser aberto no seu navegador. (Caso não seja aberto, acesse o link [http://127.0.0.1:8521](http://127.0.0.1:8521)); Logo após, clique em Reset e depois em Run.


## Os arquivos CSV's

- **Fine**: Árvores que não foram atingidas pelo fogo.
- **On Fire**: Árvores que estão em chamas.
- **Burned Out**: Árvores que foram queimadas pelo fogo.
- **Escaped the Fire**: Árvores que o fogo alcançou, mas não foram incendiadas.