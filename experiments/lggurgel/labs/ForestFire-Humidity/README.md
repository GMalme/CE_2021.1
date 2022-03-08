# Forest Fire - Mesa Model

## Introdução

[Forest fire model](http://en.wikipedia.org/wiki/Forest-fire_model) é um simples modelo que simula o avanço do fogo em uma floresta. A floresta é representada por uma grade de células, cada uma podendo conter árvore ou vazio. Árvores podem estar bem, em chamas ou queimadas. Esse modelo apresenta a umidade relativa do ar como uma nova variável dinâmica extra. Ou seja, tanto **densidade** quanto essa nova variável **umidade relativa** influenciarão no alastramento das chamas.

## Como executar a simulação

### Configuração do ambiente

Criação e inicialização do ambiente virtual.

```
    $ python3 -m venv venv
    $ source venv/bin/activate
```

Instalação das dependências.

```
    $ pip install -r requirements.txt
```

### Execução da simulação

Na pasta raiz do projeto, execute:

```
   (venv) $ mesa runserver
```

A simulação está disponível no endereço local: [http://127.0.0.1:8521/](http://127.0.0.1:8521/)


## Nova variável dinâmica: **relative_humidity**

A umidade relativa foi inserida no modelo para ser alternativa de impacto da simulação.

Essa nova variável representa o que seria a quantidade de umidade presente na floresta, variando entre 1 à 100.
Esse valor será representado inicialmente em porcentage e, para fins matemáticos, será transformada em unidade probabilistica, variando de 0.1 à 1, para indicar se alguma árvore é suscetível ao fogo se possuir valor booleano para essa probabilidade simples.

### Simulação exemplo: densidade fixa em **0.65**


#### Relative Humidity: 10%
![Relative Humidity: 10%](https://i.ibb.co/nz6Ckqg/Screenshot-from-2022-03-08-19-46-24.png)


#### Relative Humidity: 50%
![Relative Humidity: 50%](https://i.ibb.co/rf790VK/Screenshot-from-2022-03-08-19-45-23.png)

#### Relative Humidity: 70%
![Relative Humidity: 70%](https://i.ibb.co/DpD1zMV/Screenshot-from-2022-03-08-19-45-51.png)

As demais simulações com o experimento completo está no arquivo **.csv** do projeto.