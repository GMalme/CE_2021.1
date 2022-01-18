#!/usr/bin/python
# -*- coding: utf-8 -*-

# Esta classe modela uma pirâmide populacional humana ou pirâmide etária, presente em um território.
# A pirâmide é definida pela população de homens e mulheres nos estratos, bem como pelas suas taxas de mortalidade para homens e mulheres em faixas correspondentes,
# e também pela taxa de fecundidade das mulheres em idades férteis, conforme os indicadores do IBGE e RIPSA (MInistério da Saúde)
# Dada uma pirâmide populacional, essa classe impementa alguns métodos que permitem ajustá-la, e que são:
# ## change_pyramid (self, rate): modifica os valores de população  da pirâmide populacional por uma taxa, que varia de ]-1:infinito]
# ## change_total_fecundity_rate(self, rate): modifica a taxa de fecundidade do território por uma taxa que varia de ]-1:infinito]
# ## step_to_next_year(self): Atualiza a pirâmide populacional com um ano à frente
# ## to_string(self): retorna uma string com uma representação da pirâmide na forma de caracteres
# 
brazilian_pyramid_2019 = [{'age':'0-4', 'pop_m':7454197, 'pop_f':7117753},{'age':'5-9', 'pop_m':7469798, 'pop_f':7146432},{'age':'10-14', 'pop_m':7727130, 'pop_f':7424459},{'age':'15-19', 'pop_m':8383635, 'pop_f':8097851},{'age':'20-24', 'pop_m':8711984, 'pop_f':8494800},{'age':'25-29', 'pop_m':8542090, 'pop_f':8432526},{'age':'30-34', 'pop_m':8623220, 'pop_f':8639595},{'age':'35-39', 'pop_m':8511655, 'pop_f':8661714},{'age':'40-44', 'pop_m':7523486, 'pop_f':7780880},{'age':'45-49', 'pop_m':6616618, 'pop_f':6981933},{'age':'50-54', 'pop_m':6107921, 'pop_f':6593438},{'age':'55-59', 'pop_m':5376802, 'pop_f':5948447},{'age':'60-64', 'pop_m':4275622, 'pop_f':4880012},{'age':'65-69', 'pop_m':3261073, 'pop_f':3875478},{'age':'70-74', 'pop_m':2234841, 'pop_f':2810744},{'age':'75-79', 'pop_m':1422037, 'pop_f':1933468},{'age':'80-120', 'pop_m':1491051, 'pop_f':2496829}]
brazilian_life_table_male_2019 = [{ 'age':'0', 'mortality_rate':12.8462639943163},{ 'age':'1', 'mortality_rate':0.883489095999415},{ 'age':'2', 'mortality_rate':0.58008551784518},{ 'age':'3', 'mortality_rate':0.446318204562048},{ 'age':'4', 'mortality_rate':0.368874480549932},{ 'age':'5', 'mortality_rate':0.318380552750016},{ 'age':'6', 'mortality_rate':0.283764944193442},{ 'age':'7', 'mortality_rate':0.260263634350933},{ 'age':'8', 'mortality_rate':0.246075944725574},{ 'age':'9', 'mortality_rate':0.241325001600603},{ 'age':'10', 'mortality_rate':0.247906105411946},{ 'age':'11', 'mortality_rate':0.269867141963506},{ 'age':'12', 'mortality_rate':0.314303481627565},{ 'age':'13', 'mortality_rate':0.392930985500808},{ 'age':'14', 'mortality_rate':0.524673801822737},{ 'age':'15', 'mortality_rate':1.00747065783449},{ 'age':'16', 'mortality_rate':1.28577644825805},{ 'age':'17', 'mortality_rate':1.53906296289327},{ 'age':'18', 'mortality_rate':1.74693721201502},{ 'age':'19', 'mortality_rate':1.91490369583366},{ 'age':'20', 'mortality_rate':2.08339227077179},{ 'age':'21', 'mortality_rate':2.24607379325321},{ 'age':'22', 'mortality_rate':2.35233713228415},{ 'age':'23', 'mortality_rate':2.3869070650462},{ 'age':'24', 'mortality_rate':2.36828223556178},{ 'age':'25', 'mortality_rate':2.32531428752774},{ 'age':'26', 'mortality_rate':2.28886671984236},{ 'age':'27', 'mortality_rate':2.26944811662656},{ 'age':'28', 'mortality_rate':2.28229156322926},{ 'age':'29', 'mortality_rate':2.32098968521618},{ 'age':'30', 'mortality_rate':2.36558210614458},{ 'age':'31', 'mortality_rate':2.40724407126899},{ 'age':'32', 'mortality_rate':2.45760349964083},{ 'age':'33', 'mortality_rate':2.51714729538079},{ 'age':'34', 'mortality_rate':2.58732440776891},{ 'age':'35', 'mortality_rate':2.67130018863137},{ 'age':'36', 'mortality_rate':2.76982543086086},{ 'age':'37', 'mortality_rate':2.88162313204848},{ 'age':'38', 'mortality_rate':3.00722351044491},{ 'age':'39', 'mortality_rate':3.14920461267206},{ 'age':'40', 'mortality_rate':3.30917987494992},{ 'age':'41', 'mortality_rate':3.4918118858802},{ 'age':'42', 'mortality_rate':3.70233286011052},{ 'age':'43', 'mortality_rate':3.9444393512407},{ 'age':'44', 'mortality_rate':4.21759339097582},{ 'age':'45', 'mortality_rate':4.51728620130142},{ 'age':'46', 'mortality_rate':4.84363777013538},{ 'age':'47', 'mortality_rate':5.20237194756635},{ 'age':'48', 'mortality_rate':5.59556519774784},{ 'age':'49', 'mortality_rate':6.02313862353107},{ 'age':'50', 'mortality_rate':6.48469724843163},{ 'age':'51', 'mortality_rate':6.97937359523313},{ 'age':'52', 'mortality_rate':7.50755160638651},{ 'age':'53', 'mortality_rate':8.06975827209771},{ 'age':'54', 'mortality_rate':8.66870024363334},{ 'age':'55', 'mortality_rate':9.31620796804766},{ 'age':'56', 'mortality_rate':10.0101211735115},{ 'age':'57', 'mortality_rate':10.7384149986331},{ 'age':'58', 'mortality_rate':11.4989931418949},{ 'age':'59', 'mortality_rate':12.3043716979625},{ 'age':'60', 'mortality_rate':13.1721989343957},{ 'age':'61', 'mortality_rate':14.1225726943139},{ 'age':'62', 'mortality_rate':15.1683871576871},{ 'age':'63', 'mortality_rate':16.3258901217277},{ 'age':'64', 'mortality_rate':17.6030314635237},{ 'age':'65', 'mortality_rate':18.9717484185606},{ 'age':'66', 'mortality_rate':20.4639560388485},{ 'age':'67', 'mortality_rate':22.15923713843},{ 'age':'68', 'mortality_rate':24.1023035143931},{ 'age':'69', 'mortality_rate':26.2831535184789},{ 'age':'70', 'mortality_rate':28.6396950427661},{ 'age':'71', 'mortality_rate':31.1626070576964},{ 'age':'72', 'mortality_rate':33.9210803771399},{ 'age':'73', 'mortality_rate':36.9429833932693},{ 'age':'74', 'mortality_rate':40.2366043798849},{ 'age':'75', 'mortality_rate':43.7860956838437},{ 'age':'76', 'mortality_rate':47.6061288934392},{ 'age':'77', 'mortality_rate':51.753775667653},{ 'age':'78', 'mortality_rate':56.2693697810927},{ 'age':'79', 'mortality_rate':61.1806113322994},{ 'age':'80-120', 'mortality_rate':1000}]
brazilian_life_table_female_2019 = [{ 'age':'0', 'mortality_rate':10.9783474575967},{ 'age':'1', 'mortality_rate':0.715517167634885},{ 'age':'2', 'mortality_rate':0.45656457694397},{ 'age':'3', 'mortality_rate':0.345277105955909},{ 'age':'4', 'mortality_rate':0.281766289092076},{ 'age':'5', 'mortality_rate':0.240667771613115},{ 'age':'6', 'mortality_rate':0.21245379524276},{ 'age':'7', 'mortality_rate':0.192904980994365},{ 'age':'8', 'mortality_rate':0.180158061996648},{ 'age':'9', 'mortality_rate':0.173707978857523},{ 'age':'10', 'mortality_rate':0.174098611184226},{ 'age':'11', 'mortality_rate':0.182945906131136},{ 'age':'12', 'mortality_rate':0.213345123535331},{ 'age':'13', 'mortality_rate':0.249829320391188},{ 'age':'14', 'mortality_rate':0.279655161645724},{ 'age':'15', 'mortality_rate':0.335843333235637},{ 'age':'16', 'mortality_rate':0.385090287970736},{ 'age':'17', 'mortality_rate':0.423916551829262},{ 'age':'18', 'mortality_rate':0.446740786446787},{ 'age':'19', 'mortality_rate':0.457984534066168},{ 'age':'20', 'mortality_rate':0.467798052448822},{ 'age':'21', 'mortality_rate':0.481971615143928},{ 'age':'22', 'mortality_rate':0.497397183526681},{ 'age':'23', 'mortality_rate':0.515557118824353},{ 'age':'24', 'mortality_rate':0.536650957899273},{ 'age':'25', 'mortality_rate':0.558824211744362},{ 'age':'26', 'mortality_rate':0.58312894077064},{ 'age':'27', 'mortality_rate':0.613136085949031},{ 'age':'28', 'mortality_rate':0.650270079533075},{ 'age':'29', 'mortality_rate':0.693676611311056},{ 'age':'30', 'mortality_rate':0.743275347749975},{ 'age':'31', 'mortality_rate':0.796288669273788},{ 'age':'32', 'mortality_rate':0.849805219823153},{ 'age':'33', 'mortality_rate':0.902323618004811},{ 'age':'34', 'mortality_rate':0.956493609924594},{ 'age':'35', 'mortality_rate':1.01722425209943},{ 'age':'36', 'mortality_rate':1.0878588860208},{ 'age':'37', 'mortality_rate':1.16819236139907},{ 'age':'38', 'mortality_rate':1.25978483929699},{ 'age':'39', 'mortality_rate':1.36343951056854},{ 'age':'40', 'mortality_rate':1.47633520340871},{ 'age':'41', 'mortality_rate':1.60167411061081},{ 'age':'42', 'mortality_rate':1.74671197084762},{ 'age':'43', 'mortality_rate':1.9146194874645},{ 'age':'44', 'mortality_rate':2.10276566066094},{ 'age':'45', 'mortality_rate':2.30894523165112},{ 'age':'46', 'mortality_rate':2.52682159924295},{ 'age':'47', 'mortality_rate':2.75132740099312},{ 'age':'48', 'mortality_rate':2.97913762779502},{ 'age':'49', 'mortality_rate':3.21470304632575},{ 'age':'50', 'mortality_rate':3.46935948647886},{ 'age':'51', 'mortality_rate':3.74705930700422},{ 'age':'52', 'mortality_rate':4.04242489727898},{ 'age':'53', 'mortality_rate':4.35645315062877},{ 'age':'54', 'mortality_rate':4.69357639288883},{ 'age':'55', 'mortality_rate':5.0641054118488},{ 'age':'56', 'mortality_rate':5.47042585682894},{ 'age':'57', 'mortality_rate':5.90808997027961},{ 'age':'58', 'mortality_rate':6.37878549717116},{ 'age':'59', 'mortality_rate':6.89110871572159},{ 'age':'60', 'mortality_rate':7.45416224025537},{ 'age':'61', 'mortality_rate':8.08138695238606},{ 'age':'62', 'mortality_rate':8.78489539964976},{ 'age':'63', 'mortality_rate':9.57625410697781},{ 'age':'64', 'mortality_rate':10.4598684267795},{ 'age':'65', 'mortality_rate':11.4264701043444},{ 'age':'66', 'mortality_rate':12.4881037695086},{ 'age':'67', 'mortality_rate':13.6760706756855},{ 'age':'68', 'mortality_rate':15.0086606407373},{ 'age':'69', 'mortality_rate':16.4887345009009},{ 'age':'70', 'mortality_rate':18.0903835162949},{ 'age':'71', 'mortality_rate':19.8309999098716},{ 'age':'72', 'mortality_rate':21.7692017621311},{ 'age':'73', 'mortality_rate':23.9374915042678},{ 'age':'74', 'mortality_rate':26.3368777872463},{ 'age':'75', 'mortality_rate':28.916154916289},{ 'age':'76', 'mortality_rate':31.6965225119559},{ 'age':'77', 'mortality_rate':34.7767186869365},{ 'age':'78', 'mortality_rate':38.2121363227138},{ 'age':'79', 'mortality_rate':42.0077933689101},{ 'age':'80-120', 'mortality_rate':1000}]
brazilian_total_fecundity_rate = 1.76 

class BrazilianPopulationalPyramid:
    def __init__(
        self,
        pyramid=brazilian_pyramid_2019,
        # https://www.ibge.gov.br/en/statistics/social/population/17117-complete-life-tables.html
        life_table_male=brazilian_life_table_male_2019,
        life_table_female=brazilian_life_table_female_2019, 
        # ibge https://www.ibge.gov.br/apps/populacao/projecao/index.html
        # sobre mulheres entre 15 e 49 anos - Numero medio de filhos nascidos vivos, 
        # tidos por uma mulher ao final do seu periodo reprodutivo, 
        # na populacao residente em determinado espaco geografico, 
        # no ano considerado
        total_fecundity_rate = brazilian_total_fecundity_rate
        # outros
        #infant_mortality_rate_male = 12.43,
        #infant_mortality_rate_female = 10.64,
        #total_mortality_rate = 6.56,
    ):
        if (len(pyramid) == 17):
            self.check_pyramid(pyramid)
            self.set_pyramid(pyramid)
        else:
            raise("Illegal populational pyramid data. Incorrect size")
        self.life_table_male = life_table_male
        self.life_table_female = life_table_female
        self.total_fecundity_rate = total_fecundity_rate

    def check_pyramid(self, pyramid):
        for layer in pyramid:
            if (layer["age"] == None or layer["pop_m"] == None or layer["pop_f"] == None):
                raise("Illegal populational pyramid data layer: age or pop_m or pop_f is null.")
        return self

    def set_pyramid(self, pyramid):
        self.check_pyramid(pyramid)
        self.pyramid = pyramid
        return self

    def set_life_table_male(self, life_table_male):
        self.life_table_male = life_table_male
        return self

    def set_life_table_female(self, life_table_female):
        self.life_table_female = life_table_female
        return self

    def set_total_fecundity_rate(self, total_fecundity_rate):
        self.total_fecundity_rate = total_fecundity_rate
        return self

    def change_total_fecundity_rate(self, rate):
        if (rate <= -1):
            raise("Ilegal rate (must be bigger that -1): "+str(rate))
        change_in_fecundity_rate = self.total_fecundity_rate * rate
        self.total_fecundity_rate = self.total_fecundity_rate + change_in_fecundity_rate
        return self

    def change_pyramid(self, rate):
        if (rate <= -1):
            raise("Ilegal rate (must be bigger that -1): "+str(rate))
        new_pyramid = []
        for layer in self.pyramid:
            pop_m = layer['pop_m']
            pop_f = layer['pop_f']
            age_layer_name = layer['age']
            change_pop_m = pop_m * rate
            change_pop_f = pop_f * rate
            pop_m = pop_m + change_pop_m
            pop_f = pop_f + change_pop_f
            new_layer = {"age":age_layer_name,"pop_m":pop_m,"pop_f":pop_f}
            new_pyramid.append(new_layer)
        self.set_pyramid(new_pyramid)
        return self

    def pop_total_m(self):
        return sum(item['pop_m'] for item in self.pyramid)

    def pop_total_f(self):
        return sum(item['pop_f'] for item in self.pyramid)

    def pop_total(self):
        return self.pop_total_f()+self.pop_total_m()
        
    def pop_total_fertile(self):
        return sum(item['pop_f'] 
            for item in self.pyramid 
                if item['age'] 
                    in {'15-19','20-24','25-29','30-34','35-39','40-44','45-49'})

    def pop_total_old_age(self):
        return sum(item['pop_m'] 
            for item in self.pyramid 
                if item['age'] 
                    in {'65-69','70-74','75-79','80-120'}) + sum(item['pop_f'] 
            for item in self.pyramid 
                if item['age'] 
                    in {'65-69','70-74','75-79','80-120'})

    def pop_total_children(self):
        return sum(item['pop_m'] 
            for item in self.pyramid 
                if item['age'] 
                    in {'0-4','5-9','10-15'}) + sum(item['pop_f'] 
            for item in self.pyramid 
                if item['age'] 
                    in {'0-4','5-9','10-15'})

    def age_list(self, layer_name):
        minus = layer_name.find('-',0,4)
        plus = layer_name.find('+',1,4)
        initial_age = -1
        final_age = -1
        if (minus > 0): # closed layers
            initial_age = int(layer_name[0:minus])
            final_age = int(layer_name[minus+1:])
        else: # final layer
            initial_age = int(layer_name[0:plus])
            final_age = 120
        return {str(i) for i in range(initial_age,final_age+1)}

    ## calcula a taxa de mortalidade média de uma faixa de idade presente na pirâmide
    def average_mortality_rate(self, life_table, layer_name):
        age_list = self.age_list(layer_name)
        sum_mortality_rate = sum(item['mortality_rate'] 
            for item 
                in life_table 
                    if item['age'] 
                        in age_list)
        qtd_years = len([item for item in life_table if item['age'] in age_list])
        if (qtd_years == 0):
            # chegamos ao final da tabela
            sum_mortality_rate = 1000 # todos irão morrer na última faixa
            qtd_years = len(age_list)
        average_mortality_rate =  sum_mortality_rate / qtd_years
        return average_mortality_rate

    # Executa um passo da simulação
    def step(self): 
        self.step_to_next_year()

    # Realiza o ciclo anual de evolucao da populacao, onde 20% da populacao da faixa inferior sobe para a faixa seguinte
    # Aplicam-se as taxas de mortalidade por faixa e de fecundidade global 
    def step_to_next_year(self): 
        new_pyramid = []
        pop_m_ant = 0
        pop_f_ant = 0
        age_layer_name_ant = None
        for layer in self.pyramid:
            pop_m = layer['pop_m']
            pop_f = layer['pop_f']
            age_layer_name = layer['age']
            #print("original layer : { 'age':'"+age_layer_name+"','pop_m':"+str(pop_m)+", 'pop_f':"+str(pop_f)+"}")

            age_incoming_m = 0
            age_incoming_f = 0
            if (age_layer_name_ant == None): # primeira faixa - aplicar a taxa de fertilidade
                qtd_anos_ferteis = 35
                age_incoming_m = self.pop_total_fertile()/qtd_anos_ferteis * self.total_fecundity_rate / 2
                age_incoming_f = self.pop_total_fertile()/qtd_anos_ferteis * self.total_fecundity_rate / 2
                age_layer_name_ant = age_layer_name 
            else: # faixas sucessoras - busca a populacao da faixa anterior   
                age_incoming_m = pop_m_ant * (0.20) # 1/5 da populacao do estrato inferior sobe para a próxima faixa de idade
                age_incoming_f = pop_f_ant * (0.20) # 1/5 da população do estrato inferior sobe para a próxima faixa de idade
            age_outgoing_m = pop_m * (0.20)
            age_outgoing_f = pop_f * (0.20)

            age_dying_m = pop_m/1000 * self.average_mortality_rate(self.life_table_male,age_layer_name)
            age_dying_f = pop_m/1000 * self.average_mortality_rate(self.life_table_female,age_layer_name)

            pop_m_ant = pop_m
            pop_f_ant = pop_f
            new_pop_m = pop_m + age_incoming_m - age_outgoing_m - age_dying_m
            new_pop_f = pop_f + age_incoming_f - age_outgoing_f - age_dying_f
            new_layer = {"age":age_layer_name,"pop_m":new_pop_m,"pop_f":new_pop_f}
            new_pyramid.append(new_layer)
            #print("new layer : { 'age':'"+age_layer_name+"','pop_m':"+str(new_pop_m)+", 'pop_f':"+str(new_pop_f)+"}")
        self.set_pyramid(new_pyramid)
        return self

    def to_string(self):
        total_pop_m = self.pop_total_m()
        total_pop_f = self.pop_total_f()
        total_pop = total_pop_m + total_pop_f
        total_perc_m_str = str(round(total_pop_m/total_pop*100,1))+"%"
        total_perc_f_str = str(round(total_pop_f/total_pop*100,1))+"%"
        text_layers = []
        max_perc_in_any_layer = 16
        head_male_layer = "          "+"        "+(" "*int(max_perc_in_any_layer/2-2))+"MALES"+(" "*int(max_perc_in_any_layer/2-4))
        head_female_layer = (" "*int(max_perc_in_any_layer/2-3))+"FEMALES"+(" "*int(max_perc_in_any_layer/2-4))+"         "
        head_layer = head_male_layer+"|"+head_female_layer
        bottom_male_layer = "        | "+total_perc_m_str+"      | "[len(total_perc_m_str):]+(" "*(max_perc_in_any_layer-1))
        bottom_female_layer = (" "*max_perc_in_any_layer)+"|"+"      "[len(total_perc_f_str):]+total_perc_f_str+" | "
        bottom_layer = bottom_male_layer+"|"+bottom_female_layer
        for layer in self.pyramid:
            pop_m = layer['pop_m']
            pop_f = layer['pop_f']
            age_layer_name = layer['age']
            perc_m = pop_m/total_pop_m
            perc_f = pop_f/total_pop_m
            perc_m_str = str(round(perc_m*100,1))+"%"
            perc_f_str = str(round(perc_f*100,1))+"%"
            asterisc_perc_m_str = "*"*round(perc_m*100)
            asterisc_perc_f_str = "*"*round(perc_f*100)
            text_layer_male = ( 
                "       "[len(age_layer_name):]+age_layer_name+" |"+
                "      "[len(perc_m_str):]+perc_m_str+" |"+
                (" "*max_perc_in_any_layer)[len(asterisc_perc_m_str):]+asterisc_perc_m_str
                )
            text_layer_female = ( 
                asterisc_perc_f_str+(" "*max_perc_in_any_layer)[len(asterisc_perc_f_str):]+"|"+
                "      "[len(perc_f_str):]+perc_f_str+" |"+
                "       "[len(age_layer_name):]+age_layer_name
                )
            text_layer = text_layer_male + "|" + text_layer_female
            text_layers.append(text_layer)
        text_layers.append(head_layer)
        text_layers.reverse()
        text_layers.append(bottom_layer)
        return text_layers
         
#                   MALE                           |               FEMALE                                   
#                                                  |                                                  
#                                                  |                                                  
#                                                  |                                                  
#                                                  |                                                  
#                                                  |                                                  
#                                                  |                                                  
#                                                  |                                                  
#                                                  |                                                  
#                                                  |                                                  
#    |                                             |                                                  
#    |                                             |                                                  
#    |                                             |                                                  
#    |                                             |                                                  
#    |                                                 |                                                  
#    |                                                 |                                                  
#5-9 |                                                 |                                                  
#0-4 |                                         xxxxxxxx|xxxxxxxx                                         0-4  
#    | 123000000 | XX% | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|xxxxxxxxxxxxxxxxxxxxxxxxxxx
def test():
    pp = BrazilianPopulationalPyramid()
    pp.change_pyramid(-0.99)
    pp.change_total_fecundity_rate(1)
    for i in range(2021,2100):
        print (i)
        pp.step()
        print ("Crianças:",pp.pop_total_children())
        print ("Ferteis:",pp.pop_total_fertile())
        print ("Homens:",pp.pop_total_m())
        print ("Mulheres:",pp.pop_total_f())
        print ("Idosos:",pp.pop_total_old_age())
        print ("Total:",pp.pop_total())
    print("".join([str(l)+"<br>" for l in pp.to_string()]))
