# Projeto de Computação Experimental, por Pedro de Torres Maschio

## Instruções
Para o modelo funcionar, é preciso instalar o Mesa da versão disponível no github, fazendo uso do seguinte comando:

```
pip install -e git+https://github.com/projectmesa/mesa#egg=mesa
```

Após a instalação, o modelo em modo gráfico pode ser executado com o comando:
```
mesa runserver
```
na raiz do diretório.

Para gerar as planilhas, foi utilizado a seguinte sequência de comandos:
```
python3
from wolf_sheep import model
model.roda()
```

## Descrição do modelo
O modelo escolhido foi o [wolf_sheep](https://github.com/projectmesa/mesa/tree/main/examples/wolf_sheep) que é uma simulação sobre um sistema predador-presa. As características dessa simulação são:
- Há três tipos de agentes: lobos, ovelhas e grama;
- Os lobos e ovelhas perambulam pelo grid, ambos gastam energia ao andar. Lobos recarregam a energia ao comer ovelha, ovelhas recarregam a energia ao comer grama;
- Lobos comem as ovelhas se estiverem na mesma célula.

## Descrição da hipótese e das modificações
Minha hipótese para a modificação da simulação foi adicionar a característica de probabilidade de "doença" no agente de Presa (na ovelha), de tal modo que um predador não vai querer comê-la. Quanto maior a probabilidade de estar doente, maior a probabilidade de esta ovelha não ser comida por um lobo. O limite
de probabilidade que vai definir se a ovelha vai ser comida ou não poderá ser definido pelo usuário na interface da simulação.

As modificações e suas justificativas foram:
- No modelo, foi adicionado a variável `diseaseLimiar`, que define um limiar de doença permitido para um lobo comer a ovelha. O valor mínimo é de 0.01, os passos são de 0.01 e o valor máximo é 1. 
- Para cada ovelha foi adicionada a variável `diseaseProbability`, um valor real gerado aleatoriamente entre [0, 1), que define a probabilidade de esta determinada ovelha estar doente.
- No comportamento do agente lobo, ficou definido que ele só vai comer a ovelha se sua `diseaseProbability` for inferior ou igual ao `diseaseLimiar` definido pelo usuário.

O que eu esperei ver com a mudança: quanto menor o valor do `diseaseLimiar`, maior a probabilidade de que as ovelhas vão prevalecer, pois os lobos só vão querer comer as ovelhas com o `diseaseProbability` muito baixo. Por outro lado, quanto maior o valor do `diseaseLimiar`, mais próximo esta simulação vai estar da simulação original, pois a verificação no agente do lobo vai se tornar irrelevante.

## Planilhas

Segue abaixo uma descrição de cada umas das colunas das planilhas:

- **RunId**: id da execução, número inteiro
- **iteration**: iteração atual.
- **Step**: passo atual.
- **width**: tamanho da grid.
- **height**: tamanho da grid.
- **sheep_reproduce**: probabilidade de casa ovelha reproduzir a cada passo.
- **wolf_reproduce**: probabilidade de cada lobo reproduzir a cada passo.
- **wolf_gain_from_food**: energia que os lobos ganham da grama.
- **grass**: se a grama está habilitada (inicialmente verdadeiro nas simulações).
- **grass_regrowth_time**:  quanto tempo a grama demora para crescer após ser comida.
- **sheep_gain_from_food**: energia que as ovelhas ganham da grama.
- **initial_sheep**: número de inicial de ovelhas.
- **initial_wolves**: número inicial de lobos.
- **diseaseLimiar**: limiar de doença, probabilidade.
- **Wolves**: número de lobos vivos.
- **Sheep**: número de ovelhas vivas.

## Experimentos

Foram executados três experimentos, com valores de `diseaseLimiar` variando nos valores 0, 0.25 e 0.50. Foram executadas 100 iterações, por no máximo 100 passos.