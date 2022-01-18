# Modelando o surgimento dos territórios para um sistema de simulação da ciência mundial
# Por Jorge H C Fernandes (jhcf@unb.br)
# Este script apresenta uma modelagem e análise inicial de uma rede de territórios, a ser usada
# 	em um simulador do processo científico mundial. é baseada nos dados de dependências econômicas entre
# 	os municípios do Brasil, gerados a partir da pesquisa REGIC2018 do IBGE.
# O script é composto por sete seções:
# 	1. Baixando e desempacotando os dados
# 	2. Lê as planilhas e cria os dataframes com dados relativos a arestas (ligações entre municípios) e vértices (atratividade dos municípios)
# 	3. declarando uma função que cria dois dataframes (arestas e vértices) para geração de um grafo no igraph, com
# 		base no corte de municípios de pequena população, 
# 			bem como no corte de dependências (influências) fracas entre os municípios
# 	4. declarando uma função que cria um grafo igraph com base nos dataframes (arestas e vértices), sem vértices isolados
# 	5. declarando uma função que cria, a partir de um grafo igraph, dois dataframes (arestas e vértices) que podem ser usados no visNetwork
# 	6. Cria alguns grafos e visualizações para explorar as propriedades dos mesmos
# 	7. gera as famílias de grafos variando os limites de população e dependências,
#    		sumariza e captura as propriedades básicas de cada grafo

## 1. Baixando os arquivos do IBGE sobre as regioes de influencoa das cidades brasileiras

url <- "https://geoftp.ibge.gov.br/organizacao_do_territorio/divisao_regional/regioes_de_influencia_das_cidades/Regioes_de_influencia_das_cidades_2018_Resultados_definitivos/base_tabular/REGIC2018_Municipios_Ligacoes_e_atracao_xlsx.zip"
temp <- tempfile()
temp2 <- tempfile()
download.file(url, temp)
unzip(zipfile = temp, exdir = temp2)

## 2. Lendo as planilhas na forma de datasets
# 	Lê as planilhas e cria os dataframes com dados relativos a arestas (ligações entre municípios) e vértices (atratividade dos municípios)
#install.packages("readxl")
library(readxl)
REGIC2018_Quest_Ligacoes_entre_Municipios <- read_xlsx(file.path(temp2, "REGIC2018_Quest_Ligacoes_entre_Municipios.xlsx"))
REGIC2018_Quest_Atracao_Municipios <- read_xlsx(file.path(temp2, "REGIC2018_Quest_Atracao_Municipios.xlsx"))
View(REGIC2018_Quest_Atracao_Municipios)
View(REGIC2018_Quest_Ligacoes_entre_Municipios)


# 	3. declarando uma função que cria dois dataframes (arestas e vértices) em formato próprio para geração de um grafo no igraph, com
# 		base no corte de 
# 			municípios de pequena população, 
# 			dependências (influências) fracas entre os municípios
gerar_datasets_grafo <- function(df_ligacoes, df_municipios, limite_inferior_dependência_fluxos, limite_inferior_populacao) {
	#### Estabelece um limite mínimo de dependência de from para to, para manter as conexões no grafo
	# limite_inferior_dependência_fluxos <- 0.85
	
	#### Estabelece um limite mínimo de população, para manter as conexões no grafo
	#limite_inferior_populacao <- 20000
	
	# filtrando as arestas conforme os limites de população
	regic2018_arestas <- 
		df_ligacoes[
			df_ligacoes$PERC_LIG>=limite_inferior_dependência_fluxos &
			df_ligacoes$POP2018_O>=limite_inferior_populacao &
			df_ligacoes$POP2018_D>=limite_inferior_populacao 
		,]

	### 3.2 Selecionando os dados relevantes das arestas
	#### coloca nos registros de arestas os dados essenciais e opcionais para a geração  e análise do grafo
	regic2018_arestas <- regic2018_arestas[,c("MUN_ORIGEM","MUN_DESTINO","PERC_LIG","IA","IA_Q1","IA_Q2","IA_Q3","IA_Q4","IA_Q5","IA_Q6","IA_Q7","IA_Q8","IA_Q9","IA_Q10")]

	### 3.3 - Organizando os vértices
	#### Identificando os municípios registrados e seus principais atributos
	regic2018_vertices <- df_municipios[,c("CODMUN","NOME_MUN","POP2018","IA","HIERAR_CID","NOME_HIERAR_CID")]
	#### Renomeando os atributos dos vértices e arestas para adaptação a visualização no visNetwork
	names(regic2018_arestas) <- c("FROM","TO",names(regic2018_arestas)[3:14])
	#### Renomeando aS primeiraS colunas do dataframe de vértices ajustado para adaptação a visualização no visNetwork
	names(regic2018_vertices) <- c("ID","LABEL",names(regic2018_vertices)[3:6])
	#### Removendo as arestas cujos identificadores não estão presentes na tabela dos municípios 
	regic2018_arestas <- regic2018_arestas[regic2018_arestas$FROM %in% regic2018_vertices$ID,]
	regic2018_arestas <- regic2018_arestas[regic2018_arestas$TO %in% regic2018_vertices$ID,]

	#### Remove registros de arestas com valores NA
	regic2018_arestas <- na.omit(regic2018_arestas)
	#### Remove registros de vértices com valores NA
	regic2018_vertices <- na.omit(regic2018_vertices)

	return (list(regic2018_arestas, regic2018_vertices))
}


# 	4. declarando uma função que cria um grafo igraph com base nos dataframes (arestas e vértices), removendo os vértices isolados
#install.packages("igraph")
library(igraph)

cria_grafo_componentes <- function(regic2018_arestas, regic2018_vertices, removeIsolados=TRUE) {
	
	### 3.4 - Criando a rede
	#install.packages("igraph")
	library(igraph)
	#
	rede_municipios <- graph_from_data_frame(regic2018_arestas,regic2018_vertices, directed = TRUE)
	#
	if (removeIsolados) {
		# identificando os vértices isolados
		isolados <- which(degree(rede_municipios)==0)
		# removendo os vértices isolados
		rede_municipios <- delete.vertices(rede_municipios,isolados)
	}
	#### Plotando do grafo da rede com componentes maiores que 1
	#plot(rede_municipios_componentes,vertex.label=V(rede_municipios_componentes)$LABEL)
	return (rede_municipios)
}


# 	5. declarando uma função que cria, a partir de um grafo igraph, dois dataframes (arestas e vértices) que podem ser usados no visNetwork
gera_vis_dataframes_from_igraph <- function(grafo) {

	# gera um dataframe global correspondente ao igraph
	grafo_dataframe <-  as_long_data_frame(grafo)

	# obtém um novo dataframe apenas com os dados das arestas
	edges<-data.frame(cbind(
		grafo_dataframe[,c("from")],
		grafo_dataframe[,c("to")],
		grafo_dataframe[,c("PERC_LIG")]*grafo_dataframe[,c("from_POP2018")],
		grafo_dataframe[,c("PERC_LIG")],
		grafo_dataframe[,c("from_name")],
		grafo_dataframe[,c("to_name")],
		grafo_dataframe[,c("from_LABEL")],
		grafo_dataframe[,c("to_LABEL")],
		grafo_dataframe[,c("from_POP2018")],
		grafo_dataframe[,c("to_POP2018")],
		grafo_dataframe[,c("from_IA")],
		grafo_dataframe[,c("to_IA")]
	))
	# renomeia as colunas do dataframe de arestas
	names(edges)<-c("from","to","value","perc_lig","from_name","to_name","from_LABEL","to_LABEL","from_POP2018","to_POP2018","from_IA","to_IA")
	
	# obtém um novo dataframe apenas com os dados dos vértices
	nodes<-data.frame(cbind(
		c(edges$from,edges$to),
		c(edges$from_name,edges$to_name),
		c(edges$from_LABEL,edges$to_LABEL),
		as.numeric(c(edges$from_POP2018,edges$to_POP2018)),
		as.numeric(c(edges$from_IA,edges$to_IA))
	)
	)
	# elimina os vértices duplicados
	nodes<-unique(nodes)
	# renomeia as colunas do dataframe de vértices
	names(nodes)<-c("id","COD_IBGE","label","value","IA")
	
	# retorna os dois dataframes em uma lista
	return (list(nodes, edges))	
}

# 6. Cria alguns grafos e visualizações para explorar as propriedades dos mesmos

# 6.1 declara uma função que filtra e apresenta visualização dos grafos
library(visNetwork)
visualiza_dataset <- function(dataset_list,plot=FALSE,vis=TRUE,removeIsolados=TRUE) {

	# cria o grafo, eliminado componentes isolados
	grafo_componentes <- cria_grafo_componentes(dataset_list[[1]], dataset_list[[2]], removeIsolados)
	
	# apresenta sumário das propriedades do grafo
	grafo_componentes

	# plota o grafo de forma simples
	if (plot) {
		plot(grafo_componentes, vertex.label=NA)
	}

	#plota o grafo com um visualizador avançado
	#install.packages("visNetwork"")

	if (vis) {
		dataframes_visNetwork <- gera_vis_dataframes_from_igraph(grafo_componentes)

		visNetwork(dataframes_visNetwork[[1]],dataframes_visNetwork[[2]])  %>% visEdges(arrows = 'to')  %>%
  			visPhysics(stabilization = FALSE) %>%
  			visEdges(smooth = FALSE) 
	}
}

# cria e visualiza os datasets filtrados
visualiza_dataset (gerar_datasets_grafo(
	REGIC2018_Quest_Ligacoes_entre_Municipios,
	REGIC2018_Quest_Atracao_Municipios,
	0.10, #limite_inferior_dependência_fluxos 
	10000) #limite_inferior_populacao
)

# cria e visualiza os datasets filtrados
visualiza_dataset (gerar_datasets_grafo(
	REGIC2018_Quest_Ligacoes_entre_Municipios,
	REGIC2018_Quest_Atracao_Municipios,
	0.40, #limite_inferior_dependência_fluxos 
	90000) #limite_inferior_populacao
)

# cria e visualiza os datasets filtrados
visualiza_dataset (gerar_datasets_grafo(
	REGIC2018_Quest_Ligacoes_entre_Municipios,
	REGIC2018_Quest_Atracao_Municipios,
	0.80, #limite_inferior_dependência_fluxos 
	200000) #limite_inferior_populacao
)

# 7. gera as famílias de grafos variando os limites de população e dependências,
#    sumariza e captura as propriedades básicas de cada grafo
#

# 7.1 gera um sumário com as propriedades do grafo
sumariza_grafo <- function(lf, lp, grafo) {
	return(list(
                        limite_fluxos=lf,
                        limite_populacao=lp,
			# guarda os grafos originais, para flexibilizar análises
                        grafo=grafo,
                        componentes=components(grafo)$no,
                        vertices=length(V(grafo)),
                        arestas=length(E(grafo)),
                        diametro=diameter(grafo),
                        triangulos=sum(count_triangles(grafo))
                ))
}


# define as faixas de valores a explorar, na geração das famílias de grafos
limites_fluxos <- seq(from = 0.95, to = 0.05, by = -0.05)
limites_populacao <- seq(from=500000, to=5000, by = -5000)

# cria as famílias de grafos
familias_de_grafos <- list()
for (lf in limites_fluxos) {
	for (lp in limites_populacao) {
		datasets <- gerar_datasets_grafo(
        		REGIC2018_Quest_Ligacoes_entre_Municipios,
        		REGIC2018_Quest_Atracao_Municipios,
        		lf,
        		lp)
		grafo <- cria_grafo_componentes(datasets[[1]], datasets[[2]])

		sumario_de_metricas_do_grafo <- sumariza_grafo(lf, lf, grafo)

		familias_de_grafos <- append(familias_de_grafos, list(sumario_de_metricas_do_grafo))
	}
}
# Informa quantos grafos foram gerados, sendo que cada grafo apresenta um conjunto de N pontos em N gráficos diferentes
length(familias_de_grafos)

# 8. Cria as curvas para cada família de pontos dentro de um mesmo parâmetro
# um gráfico tem um conjunto de curvas, cada curva referente à variação de uma propriedade do grafo em função da variação da população miníma, 
# mantendo-se fixo um limite inferior dos fluxos que relacionam os habitantes de um território dependendo de produtos e serviços ofertados pelo outro território
#
# Cria cinco gráficos, cada um com uma família de curvas para uma mesma métrica do grafo
GraficoComponentesXPopulacao <- list()
GraficoArestasXPopulacao <- list()
GraficoDiametroXPopulacao <- list()
GraficoVerticesXPopulacao <- list()
GraficoTriangulosXPopulacao <- list()

i<-1
# guarda os limites máximos de cada métrica, para definir o tamanho do eixo Y durante a plotagem
maxComponentes <- 0
maxArestas <- 0
maxDiametro <- 0
maxVertices <- 0
maxTriangulos <- 0

# Varre as famílias de grafos e gera as curvas para cada tipo de grafo
for (lf in limites_fluxos) {
	curvaComponentes <- c() # cria uma curva para um determinado valor de lf
	curvaArestas <- c() # cria uma curva para um determinado valor de lf
	curvaDiametro <- c() # cria uma curva para um determinado valor de lf
	curvaVertices <- c() # cria uma curva para um determinado valor de lf
	curvaTriangulos <- c() # cria uma curva para um determinado valor de lf
	curvaLabel <- NULL 
        for (lp in limites_populacao) {
		rec <- familias_de_grafos[[i]] # recupera um dos registros, que vai gerar um ponto na curva 
		curvaComponentes<-c(curvaComponentes,rec$componentes)
		if (rec$componentes > maxComponentes) { maxComponentes <- rec$componentes }

		curvaArestas<-c(curvaArestas,rec$arestas)
		if (rec$arestas > maxArestas) { maxArestas <- rec$arestas } 

		curvaDiametro<-c(curvaDiametro,rec$diametro)
		if (rec$diametro > maxDiametro) { maxDiametro <- rec$diametro }

		curvaVertices<-c(curvaVertices,rec$vertices)
		if (rec$vertices > maxVertices) { maxVertices <- rec$vertices }

		curvaTriangulos<-c(curvaTriangulos,rec$triangulos)
		if (rec$triangulos > maxTriangulos) { maxTriangulos <- rec$triangulos }

		curvaLabel <- paste(as.character(rec$limite_fluxos),":",as.character(lf))
		i <- i + 1
        }
	curvaComponentesMaisLabel <- list(label=curvaLabel,curva=curvaComponentes,legend=limites_populacao)
	GraficoComponentesXPopulacao <-
		append(GraficoComponentesXPopulacao,list(curvaComponentesMaisLabel))
	#print(length(GraficoComponentesXPopulacao))
	curvaArestasMaisLabel <- list(label=curvaLabel,curva=curvaArestas,legend=limites_populacao)
	GraficoArestasXPopulacao <-
		append(GraficoArestasXPopulacao,list(curvaArestasMaisLabel))
	#print(length(GraficoComponentesXPopulacao))
	curvaDiametroMaisLabel <- list(label=curvaLabel,curva=curvaDiametro,legend=limites_populacao)
	GraficoDiametroXPopulacao <-
		append(GraficoDiametroXPopulacao,list(curvaDiametroMaisLabel))
	#print(length(GraficoComponentesXPopulacao))
	curvaVerticesMaisLabel <- list(label=curvaLabel,curva=curvaVertices,legend=limites_populacao)
	GraficoVerticesXPopulacao <-
		append(GraficoVerticesXPopulacao,list(curvaVerticesMaisLabel))
	#print(length(GraficoComponentesXPopulacao))
	curvaTriangulosMaisLabel <- list(label=curvaLabel,curva=curvaTriangulos,legend=limites_populacao)
	GraficoTriangulosXPopulacao <-
		append(GraficoTriangulosXPopulacao,list(curvaTriangulosMaisLabel))
	#print(length(GraficoComponentesXPopulacao))
}

# a função abaixo gera uma paleta de cores para plotar cada curva com uma cor específica
# o código da função foi gerado a partir do comando choose_palette()
#install.packages("colorspace")
library(colorspace)
pal <- choose_palette() # execute choose palette para gerar uma paleta de cores de boa qualidade


# imprime o gráfico que mostra a variação de componentes no grafo, em função do tamanho da população dos municipios de origem, conforme varia o limite inferior dos fluxos populacionais
c <- 1
cores <- pal(length(GraficoComponentesXPopulacao))
plot(main="Qtd componentes no grafo em função do limite inferior do fluxo populacional observado",
	xlab="População da cidade de origem",
	ylab="Quantidade de componentes no grafo", limites_populacao,GraficoComponentesXPopulacao[[1]]$curva, col=cores[c],pch=c, ylim = c(0, maxComponentes))
lines(limites_populacao,GraficoComponentesXPopulacao[[1]]$curva, col=cores[c],ylim = c(0, maxComponentes))
legend(x=mean(limites_populacao),y=maxComponentes,title="Limite inferior do fluxo populacional",legend=limites_fluxos,col=cores,pch=1:length(GraficoComponentesXPopulacao),cex = 0.7)
for (c in 2:length(GraficoComponentesXPopulacao)) {
	points(limites_populacao,GraficoComponentesXPopulacao[[c]]$curva, col=cores[c],pch=c)
	lines(limites_populacao,GraficoComponentesXPopulacao[[c]]$curva, col=cores[c])
}

# imprime o gráfico que mostra a variação de arestas no grafo, em função do tamanho da população dos municipios de origem, conforme varia o limite inferior dos fluxos populacionais
c <- 1
cores <- pal(length(GraficoArestasXPopulacao))
plot(main="Qtd arestas no grafo em função do limite inferior do fluxo populacional observado",
	xlab="População da cidade de origem",
	ylab="Quantidade de arestas no grafo", limites_populacao,GraficoArestasXPopulacao[[1]]$curva, col=cores[c],pch=c, ylim = c(0, maxArestas))
lines(limites_populacao,GraficoArestasXPopulacao[[1]]$curva, col=cores[c],ylim = c(0, maxArestas))
legend(x=mean(limites_populacao),y=maxArestas,title="Limite inferior do fluxo populacional",legend=limites_fluxos,col=cores,pch=1:length(GraficoArestasXPopulacao),cex = 0.7)
for (c in 2:length(GraficoArestasXPopulacao)) {
	points(limites_populacao,GraficoArestasXPopulacao[[c]]$curva, col=cores[c],pch=c)
	lines(limites_populacao,GraficoArestasXPopulacao[[c]]$curva, col=cores[c])
}

# imprime o gráfico que mostra a variação do diâmetro no grafo, em função do tamanho da população dos municipios de origem, conforme varia o limite inferior dos fluxos populacionais
c <- 1
cores <- pal(length(GraficoDiametroXPopulacao))
plot(main="Diâmetro do grafo em função do limite inferior do fluxo populacional observado",
	xlab="População da cidade de origem",
	ylab="Diâmetro do grafo", limites_populacao,GraficoDiametroXPopulacao[[1]]$curva, col=cores[c],pch=c, ylim = c(0, maxDiametro))
lines(limites_populacao,GraficoDiametroXPopulacao[[1]]$curva, col=cores[c],ylim = c(0, maxDiametro))
legend(x=mean(limites_populacao),y=maxDiametro,title="Limite inferior do fluxo populacional",legend=limites_fluxos,col=cores,pch=1:length(GraficoDiametroXPopulacao),cex = 0.7)
for (c in 2:length(GraficoDiametroXPopulacao)) {
	points(limites_populacao,GraficoDiametroXPopulacao[[c]]$curva, col=cores[c],pch=c)
	lines(limites_populacao,GraficoDiametroXPopulacao[[c]]$curva, col=cores[c])
}

# imprime o gráfico que mostra a variação do diâmetro no grafo, em função do tamanho da população dos municipios de origem, conforme varia o limite inferior dos fluxos populacionais
c <- 1
cores <- pal(length(GraficoVerticesXPopulacao))
plot(main="Vertices do grafo em função do limite inferior do fluxo populacional observado",
	xlab="População da cidade de origem",
	ylab="Vertices do grafo", limites_populacao,GraficoVerticesXPopulacao[[1]]$curva, col=cores[c],pch=c, ylim = c(0, maxVertices))
lines(limites_populacao,GraficoVerticesXPopulacao[[1]]$curva, col=cores[c],ylim = c(0, maxVertices))
legend(x=mean(limites_populacao),y=maxVertices,title="Limite inferior do fluxo populacional",legend=limites_fluxos,col=cores,pch=1:length(GraficoVerticesXPopulacao),cex = 0.7)
for (c in 2:length(GraficoVerticesXPopulacao)) {
	points(limites_populacao,GraficoVerticesXPopulacao[[c]]$curva, col=cores[c],pch=c)
	lines(limites_populacao,GraficoVerticesXPopulacao[[c]]$curva, col=cores[c])
}

# imprime o gráfico que mostra a variação do diâmetro no grafo, em função do tamanho da população dos municipios de origem, conforme varia o limite inferior dos fluxos populacionais
c <- 1
cores <- pal(length(GraficoTriangulosXPopulacao))
plot(main="Triangulos do grafo em função do limite inferior do fluxo populacional observado",
	xlab="População da cidade de origem",
	ylab="Triangulos do grafo", limites_populacao,GraficoTriangulosXPopulacao[[1]]$curva, col=cores[c],pch=c, ylim = c(0, maxTriangulos))
lines(limites_populacao,GraficoTriangulosXPopulacao[[1]]$curva, col=cores[c],ylim = c(0, maxTriangulos))
legend(x=mean(limites_populacao),y=maxTriangulos,title="Limite inferior do fluxo populacional",legend=limites_fluxos,col=cores,pch=1:length(GraficoTriangulosXPopulacao),cex = 0.7)
for (c in 2:length(GraficoTriangulosXPopulacao)) {
	points(limites_populacao,GraficoTriangulosXPopulacao[[c]]$curva, col=cores[c],pch=c)
	lines(limites_populacao,GraficoTriangulosXPopulacao[[c]]$curva, col=cores[c])
}
