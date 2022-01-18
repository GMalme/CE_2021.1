# Surgem os territórios

## Summary

Esse modelo de simulação utiliza um grafo para modelar o surgimento e crescimento de uma rede territórios, cada território com seus atributos
como população, complexidade econômica, fatores climáticos e ambientais, entre outros fatores, determinantes das trocas econômicas estabelecidas entre esses territórios. A realização das trocas, por sua vez, altera alguns dos fatores do próprio território,
além do fato da pirâmide populacional ser alterada ao longo do tempo, independentemente de trocas. 

O modelo é baseado em extensas modificações e acréscimos ao código do Virus Network do conjunto de exemplos do framework Python MESA, o qual por sua vez é baseado no NetLogo model "Virus on Network".

Para que o modelo funcione o framework MESA foi modificado para poder acomodar grafos dirigidos.
A versão modificada do framework mesa, necesssáriopara execução da simulação, pode ser obtida em https://github.com/jhcf/mesa

### Virus on Network

For more information about NetLogo model "Virus on Network", read the NetLogo's web page: http://ccl.northwestern.edu/netlogo/models/VirusonaNetwork.

The full tutorial describing how the Python MESA "Virus on Network" model is built can be found at:
http://mesa.readthedocs.io/en/master/tutorials/intro_tutorial.html

JavaScript library used in this example to render the network: [d3.js](https://d3js.org/).

#### Further Reading


[Stonedahl, F. and Wilensky, U. (2008). NetLogo Virus on a Network model](http://ccl.northwestern.edu/netlogo/models/VirusonaNetwork). 
Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.


[Wilensky, U. (1999). NetLogo](http://ccl.northwestern.edu/netlogo/)
Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

## Installation

To install the dependencies use pip3 and the requirements.txt in this directory. e.g.

```
    $ pip3 install git+https://github.com/jhcf/mesa.git 
    $ pip3 install networkx
```

## How to Run

To run the model interactively, run ``pyhton3 run_server.py`` in this directory. e.g.

```
    $ python3 run_server.py
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/), adjust the parameters in the left panel, press Reset, and then Run.

## Files

* ``model.py``: Contains the model and agent classs, and specific model classes.
* ``BrazilianPopulationalPyramid.py``: Contains the model of the populational pyramid of Brazil in 2019
* ``server.py``: Defines classes for visualizing the model (network layout) in the browser via Mesa's modular server, and instantiates a visualization server.
* ``run_server.py``: Launches a model visualization server.
* ``run_batch.py``: Launches a batch of simulations for exploring the properties of the model.
