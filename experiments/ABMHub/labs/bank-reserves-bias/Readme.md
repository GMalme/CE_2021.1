# bank_reserves_bias

O modelo presente nesse repositório é uma variação do modelo "bank_reserves", encontrado dentre os exemplos padrões da biblioteca MESA, para Python. O modelo original simula pessoas que, andando randomicamente por um espaço, fazem trocas financeiras com outras pessoas que encontrarem, tendo 50% de chance de trocar 0 dinheiros (ou seja, não troca nada), e 25% para tanto 5 quando 2 dinheiros.

O modelo aqui proposto é levemente diferente: agora, temos um fator "trade_threshold", que é uma variável que ilustra o preconceito entre diferentes classes econômicas. Ou seja, pessoas ricas tendem a não fazer negócios com pessoas pobres, e vice versa.

Se a diferença do dinheiro entre duas pessoas é maior que o threshold, então elas têm 90% de chance de não realizar nenhuma troca. Além disso, para diferenciar o impacto entre realizar uma transação entre pessoas de diferentes classes econômicas, outra alteração foi feita: quando alguém vai fazer uma transação, há 50% de chance dessa pessoa trocar 2 dinheiros, e 50% de trocar 5 + 10% de todo seu dinheiro. Ou seja, pessoas mais ricas usam mais dinheiro em suas transações.

A ideia por trás dessas alterações era que o modelo anterior é, de certa forma, baseado em sorte. Ascenção econômica (entre pobre, classe média e ricos) poderia ocorrer randomicamente, já que todos trocam a mesma quantidade de dinheiros, e todos trocam entre si sem critérios. A nova proposta traz uma segregação econômica muito maior.

Ou seja, nossa **hipótese causal** para justificar essas mudanças é: a partir do momento em que ricos raramente fazem trocas com pessoas com menos condições econômicas que eles, e cada pessoa faz trocas de acordo com sua capacidade financeira, temos, teoricamente uma tendência a muito dinheiro em poucas mãos.

Para testar todas essas hipóteses levantadas, tiramos alguns dados: 8 arquivos csv que variam as seguintes variáveis: quantidade de pessoas no modelo, e a variável proposta, trade_threshold. Extraímos, também, dados no ponto de vista do modelo, e dados no ponto de vista dos agentes:

Dados de agente extraídos

- Rich (quantidade de ricos)
- Poor (quantidade de pobres)
- Middle Class (quantidade de classe média)
- AgentId (id da pessoa)
- Wealth (qtd de dinheiro que determinada pessoa tem, especificada pelo AgentID)

Dados de modelo extraídos

- Savings (dinheiro total guardado por toda população)
- Wallets (dinheiro total disponível na carteira de toda população)
- Money (dinheiro total, savings + wallets)
- Loans (dinheiro total emprestado, ou seja, devendo)
- Mean Money (dinheiro médio da população, média do savings)
- Standart Deviation Money (desvio padrão do dinheiro da população)

Todos esses dados são importantes para alguma análise. Mas, como queremos ver a segregação econômica, então o "Standart Deviation Money" é o mais imporante. Esse parâmetro foi introduzido nesse repositório justamente com o intuito de medir a segregação econômica com a introdução do "trade_threshold".

Podemos observar que, realmente, nos testes realizados, o aumento do "trade_threshold" aumenta a segregação econômica. Se compararmos a execução com  pessoas:25 e trade_threshold:0, com pessoas:25 e trade_threshold:15, o desvio padrão é bem maior. Mesma coisa se fizermos a mesma comparação com os arquivos com a variável pessoas:100.

Portanto, comprovamos que o incremento da variável trade_threshold, juntamente com a alteração que "cada pessoa faz transações de acordo com sua conta bancária", realmente aumenta a desigualdade econômica no modelo.
