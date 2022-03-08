# charts_moreRandom_moreMoney
Repositório para a atividade 5.2 de Computação Experimental
Esta tarefa utiliza os arquivos disponibilizados no repositório: https://github.com/projectmesa/mesa

Foi escolhido o exemplo 'Charts' que nada mais é do que uma versão com mais dados visíveis do exemplo bank_reserves, onde cada pessoa se move por um espaço, tendo a chance de encontrar com outra pessoa e, novamente, tendo a chance de trocar dinheiro com essa outra pessoa. Todas as probabilidades desse teste, com exceção dos encontros, são de 50%.

 O teste também separa as pessoas em três classes: Ricos, Classe Média e Pobres. Todos começam como Classe Média e eventualmente, dependendo das devidas probabilidades, assumem a classe Rica ou Pobre. Em cima deste fator, a hipótese causal utilizada neste experimento assume que: a diminuição dos valores das probabilidades de encontros e trocas, adicionada com o aumento da quantidade de empréstimos que um indivíduo pode fazer antes de ser considerado de classe Pobre, pode gerar uma situação onde nunca existirão pessoas de classe Pobre ou que este número seja mínimo, comparado com as pessoas de classe Rica e Média.
 
 Estas alterações foram feitas nos arquivos 'model.py' e 'agents.py', ambos se encontram na pasta mesa\examples\charts.
 
 Primeiramente, na classe 'agents.py', nas linhas 75 e 77, a função 'randint' foi trocada de 0 , 1 (50%) para 0 , 4 (25%). Simbolizando a diminuição das probabilidades de trocas.
 
 Na classe 'model.py', nas linhas 38 e 48, os valores de empréstimos para a pessoa ser considerada de classe Pobre ou Média foram alterados de 10 para 20, permitindo que eles possam fazer mais empréstimos e conseguirem uma situação mais estável antes de entrarem na classe Pobre.
