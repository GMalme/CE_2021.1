# Human Wolf Sheep

## Apresentação do novo modelo

O modelo Human Wolf Sheep foi desenvolvido com base no exemplo "Wolf Sheep" fornecido no repositório do [framework MESA](https://github.com/projectmesa/mesa-examples). O modelo original tem por objetivo simular o ecossistema existente entre lobos e ovelhas. Por sua vez, o novo modelo "Human Wolf Sheep" visa simular as consequência da inserção de humanos nesse ecossistema.

## Descrição da hipótese

Ao rodar o modelo "Wolf Sheep" algumas vezes, notou-se que caso se tenha as ovelhas sejam extintas antes dos lobos, estes não sobrevivem por muito tempo, pois não se alimentam de grama. Caso contrário, as ovelhas sobrevivem bem melhor, pois mantiveram sua fonte de energia e não possuem a ameaça de serem comidas por lobos. Tendo isso em vista, 
foi criado um agente que representa um humano, o qual se alimenta de grama e ovelha, mas que também pode ser comido por lobos, a fim de se analisar a influência que este quarto
elemento exerce perante este ecossistema.

## Mudanças realizadas

### Agente "Human"
Uma das mudanças mais relevantes foi a adiçao do agente "Human", que representa o ser humano que se alimenta de grama e carne de ovelha, mas que também pode ser atacado por lobos.

Para tal, foi reproduzido o comportamento do lobo referente a ovelha para codificar o humano também comendo ovelha, o comportamento da ovelha comendo grama para codificar o humano também comendo grama e o comportamento do lobo ao se mexer foi alterado a fim de se incluir suas ações caso esteja no mesmo quadrado que um humano. Os comportamento referentes a reproducibilidade e quantidade de energia adiquirida a partir da alimentação também foram codificados com base nos comportamentos das ovelhas e dos lobos. 

    class Human(RandomWalker):
        """
        A human that walks around, reproduces (asexually) and eats sheep and grass, and gets eaten by wolf.
        """

        energy = None

        def __init__(self, unique_id, pos, model, moore, energy=None):
            super().__init__(unique_id, pos, model, moore=moore)
            self.energy = energy

        def step(self):
            self.random_move()
            self.energy -= 1

            # If there is grass available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                self.energy += self.model.human_gain_from_food
                grass_patch.fully_grown = False

            # If there are sheep present, eat one
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
            if len(sheep) > 0:
                sheep_to_eat = self.random.choice(sheep)
                self.energy += self.model.human_gain_from_food

                # Kill the sheep
                self.model.grid._remove_agent(self.pos, sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)

            # Death or reproduction
            if self.energy < 0:
                self.model.grid._remove_agent(self.pos, self)
                self.model.schedule.remove(self)
            else:
                if self.random.random() < self.model.human_reproduce:
                    # Create a new human baby
                    self.energy /= 2
                    baby = Human(
                        self.model.next_id(), self.pos, self.model, self.moore, self.energy
                    )
                    self.model.grid.place_agent(baby, baby.pos)
                    self.model.schedule.add(baby)
                    
### Ajustes gerais
- Foi adicionado o arquivo "mesa_file.py", pois o código não estava conseguindo importar "time" do módulo "mesa.time". Todo o conteúdo desse arquivo foi obtido a partir do repositório do [framework MESA, na pasta "./mesa/time"](https://github.com/projectmesa/mesa/blob/main/mesa/time.py)
- Além da definição da classe "Humans" no arquivo "agents.py", também foram realizadas mais algumas modificações necessárias para a execução correta do código, como por exemplo a adição do Agente "Human" nos arquivos "server.py" e "model.py". 
- Adicionou-se uma linha representando a quantidade de humanos em cada "step" na visualização presente na interface de interação com a simulação.

## Como usar o simulador

### Dependências
 
Para a execução correta do modelo deve-se instalar o pacote **mesa** e os outros listados em **requirements.txt**. Isso pode ser feito ao se executar o seguinte comando:

```
  $ pip install -r requirements.txt

```

### Execução

Para utilizar o simulador e rodar o novo modelo, basta executar o seguinte comando: 

```
    $ mesa runserver
```

## Descrição das variáveis armazenadas no arquivo CSV

O arquivo csv onde foram armazenados os dados dos experimentos possuem 4 variáveis. A primeira coluna indica o "step", a coluna "Wolves" indica a quantidade de lobos durante aquele instante, a coluna "Sheep" indica a quantidade de ovelhas durante aquele momento e por fim, a coluna "Human" indica a quantidade de humanos durante aquele "step". 

Foram realizados 3 experimentos iniciais, alterando a espécie que seria inicializada como sendo a maioria. A seguir estão os parâmetros que foram usados em cada experimentos: 

- Experimento 1: initial_sheep = 100, initial_wolves = 50, initial_humans = 50
- Experimento 2: initial_sheep = 50, initial_wolves = 100, initial_humans = 50
- Experimento 3: initial_sheep = 50, initial_wolves = 50, initial_humans = 100

O nome dos arquivos csv indicam qual a espécie começou como maioria e qual durou até o final. Por exemplo, em "model_init_sheep_end_wolves_08-03-2022_18-55.csv", as ovelhas começaram como maioria, mas quem sobreviveu por mais tempo foram os lobos. 

## Repositório onde foi desenvolvido o simulador: https://github.com/Tatianafp/human_wolf_sheep_simulation
