from modelos import Receita, Preparo, CadernoReceitas

caderno = CadernoReceitas()

# =========================
# MASSAS E BASES DOCES
# =========================

massas = [
    Preparo(
        "Massa Branca", "massa",
        [
            "220 g ovo", "170 g iogurte natural integral", "155 g óleo",
            "270 g açúcar refinado", "270 g farinha de trigo", "15 g fermento químico"
        ],
        """Pré-aqueça o forno a 165 °C.
Quebre um ovo de cada vez sobre um pote pequeno e transfira para uma tigela média.
Junte o iogurte e o óleo e bata com o fouet até ficar homogêneo.
Peneire os secos, abra um buraco no centro e despeje os líquidos.
Misture começando do centro, incorporando os secos das laterais.
Divida a massa entre as fôrmas e leve ao forno preaquecido por 20 min.""",
        "imagens/Biscoitos Dourados em Ambiente Aconchegante.png",
        ["Brigadeiro de Leite Ninho", "Creme de Baunilha", "Geleia de Frutas Vermelhas"]
    ),

    Preparo(
        "Massa Branca Chiffon", "massa",
        [
            "275 g ovo", "100 g açúcar refinado (1)", "125 g água filtrada",
            "100 g óleo de girassol", "100 g açúcar refinado (2)",
            "200 g farinha de trigo", "25 g amido de milho", "12 g fermento químico"
        ],
        """Unte apenas o fundo de três fôrmas de 21 cm. Preaqueça a 165 °C.
Bata as gemas, açúcar (1), óleo e água até formar um creme claro e volumoso.
Peneire farinha, amido e fermento. Incorpore a farinha em três etapas.
Bata as claras com o açúcar (2) até picos médios.
Agregue o merengue ao creme de gemas em três etapas.
Distribua nas fôrmas e asse por cerca de 15 minutos.
Para desenformar, passe delicadamente uma faca sem ponta rente à fôrma.""",
        "imagens/Bolo dourado em camadas com flores.png",
        ["Brigadeiro de Leite Ninho", "Creme de Baunilha", "Geleia de Frutas Vermelhas"]
    ),

    Preparo(
        "Massa Cenoura", "massa",
        [
            "150 g ovo", "180 g cenoura", "135 g óleo de girassol",
            "240 g açúcar refinado", "175 g farinha de trigo", "3 g fermento",
            "Pitada de sal"
        ],
        """Preaqueça o forno a 165 °C e unte o fundo de duas fôrmas de 21 cm.
Descasque e corte as cenouras. Bata no liquidificador com as gemas,
açúcar e óleo até homogeneizar.
Despeje numa tigela e peneire farinha, fermento e sal.
Bata as claras até começar a montar picos e incorpore à massa.
Divida em duas partes iguais e asse por 15 minutos.""",
        "imagens/Bolo dourado com lim#U00f5es e flores.png",
        ["Brigadeiro Tradicional"]
    ),

    Preparo(
        "Massa Chocolate", "massa",
        [
            "160 g leite", "20 g suco de limão", "70 g ovo",
            "70 g óleo de girassol", "240 g açúcar refinado",
            "160 g farinha de trigo", "50 g cacau 50% em pó",
            "7 g bicarbonato de sódio", "3 g fermento", "Pitada de sal",
            "160 g água filtrada"
        ],
        """Preaqueça o forno a 165 °C e unte o fundo de duas fôrmas.
Misture o leite com o suco de limão.
Peneire farinha e cacau e misture os demais secos.
Em outra tigela misture os líquidos.
Despeje os líquidos nos secos e misture até homogeneizar.
Aqueça a água por 1 minuto no micro-ondas e misture na massa.
Divida em duas partes e asse por 22 minutos.""",
        "imagens/Bolo de chocolate com recheio cremoso.png",
        ["Brigadeiro Tradicional", "Geleia de Frutas Vermelhas"]
    ),

    Preparo(
        "Massa Red Velvet", "massa",
        [
            "240 g de leite integral", "45 g de suco de limão", "110 g de ovo",
            "210 g de óleo de girassol", "10 g de corante em gel vermelho",
            "240 g de açúcar refinado", "300 g de farinha de trigo",
            "20 g de cacau 50% em pó", "5 g de bicarbonato de sódio",
            "Pitada de sal"
        ],
        """Preaqueça o forno a 165 °C e unte o fundo de três fôrmas.
Misture o leite com o suco de limão.
Peneire farinha e cacau e misture os demais secos.
Em outra tigela misture os líquidos.
Despeje os líquidos nos secos e misture até homogeneizar.
Divida em três partes e asse por 15 minutos.""",
        "imagens/Redvelvet.png",
        ["Creme de Limão Siciliano", "Geleia de Frutas Vermelhas"]
    )
]

for preparo in massas:
    caderno.adicionar_preparo(preparo)


# =========================
# CREMES, RECHEIOS E COBERTURAS
# =========================

cremes = [
    Preparo(
        "Creme de Baunilha", "creme",
        [
            "230 g de leite integral", "70 g de creme de leite fresco 35% gordura",
            "170 g de leite condensado", "20 g de amido do milho",
            "30 g pasta de baunilha", "90 g de chocolate branco em gotas ou picado fino"
        ],
        """Coloque o chocolate branco numa tigela.
Misture numa panela o leite condensado e o amido.
Junte leite, creme de leite e pasta de baunilha.
Cozinhe em fogo médio, mexendo até ferver e engrossar.
Despeje sobre o chocolate branco e misture.
Coloque plástico filme em contato e deixe na geladeira.""",
        "imagens/Colherada de Baunilha Cremosa.png",
        ["Massa Branca", "Massa Branca Chiffon", "Morangos", "Frutas Vermelhas"]
    ),

    Preparo(
        "Creme de Limão Siciliano", "creme",
        [
            "230 g de leite integral", "70 g de creme de leite fresco 35% gordura",
            "170 g de leite condensado", "20 g de amido do milho",
            "40 g de suco de limão siciliano + raspas de 1 limão siciliano",
            "90 g de chocolate branco em gotas ou picado fino"
        ],
        """Coloque o chocolate branco numa tigela.
Misture numa panela o leite condensado e o amido.
Junte leite, creme de leite e raspas. Cozinhe em fogo médio até engrossar.
Despeje sobre o chocolate branco e misture.
Espere esfriar um pouco e junte o suco de limão.
Coloque plástico filme em contato e leve à geladeira.""",
        "imagens/Creme Cremoso em Tigela Azul R#U00fastica.png",
        ["Massa Red Velvet", "Morangos", "Frutas Vermelhas", "Cream Cheese"]
    ),

    Preparo(
        "Brigadeiro de Leite Ninho", "brigadeiro",
        [
            "395 g leite condensado", "50 g leite", "50 g creme de leite fresco 35% gordura",
            "15 g manteiga sem sal", "20 g leite ninho"
        ],
        """Peneire o leite ninho no leite condensado dentro da panela e misture.
Adicione os demais ingredientes e mexa em fogo médio-baixo até atingir
o ponto de bico. Despeje num recipiente e cubra com plástico filme em contato.""",
        "imagens/Creme de baunilha com baunilha natural.png",
        ["Massa Branca", "Massa Branca Chiffon", "Morangos", "Frutas Vermelhas"]
    ),

    Preparo(
        "Brigadeiro Tradicional", "brigadeiro",
        [
            "395 g leite condensado", "50 g leite", "50 g creme de leite fresco 35% gordura",
            "15 g manteiga sem sal", "15 g cacau 50% em pó"
        ],
        """Peneire o cacau no leite condensado dentro da panela e misture.
Adicione os demais ingredientes e mexa em fogo médio-baixo até atingir
o ponto de bico. Despeje num recipiente e cubra com plástico filme em contato.""",
        "imagens/Sobremesa de Chocolate em Lou#U00e7a R#U00fastica.png",
        ["Massa Cenoura", "Massa Chocolate", "Morangos", "Framboesas"]
    ),

    Preparo(
        "Geleia de Frutas Vermelhas", "geleia",
        [
            "500 g de frutas vermelhas (apenas um ou um mix de preferência)",
            "80 g de açúcar refinado (para uma geleia mais doce colocar 100 g)"
        ],
        """Junte todos os ingredientes na panela.
Cozinhe por 10 a 20 minutos, mexendo com frequência para não queimar,
mas com cuidado para não desfazer os pedaços.
Remova a espuma que se formar na superfície.
Quanto mais cozinhar, mais reduzida fica a geleia.""",
        "imagens/Geleia Artesanal de Frutas Vermelhas.png",
        ["Massa Branca", "Massa Branca Chiffon", "Massa Chocolate",
         "Massa Red Velvet", "Cheesecake", "Morangos", "Framboesas",
         "Frutas Vermelhas"]
    )
]

for preparo in cremes:
    caderno.adicionar_preparo(preparo)


# =========================
# COMPLEMENTOS PARA COMBINAÇÕES
# =========================

complementos = [
    Preparo(
        "Morangos", "complemento",
        ["Morangos frescos"],
        """Lave e higienize os morangos. Seque bem e corte conforme a montagem.""",
        "imagens/Bolo_de_morango.png",
        ["Creme de Baunilha", "Brigadeiro de Leite Ninho",
         "Creme de Limão Siciliano", "Brigadeiro Tradicional"]
    ),

    Preparo(
        "Framboesas", "complemento",
        ["Framboesas frescas"],
        """Higienize as framboesas com cuidado e utilize-as frescas na montagem.""",
        "imagens/Bolo_chocolate_com_framboesa.png",
        ["Brigadeiro Tradicional", "Geleia de Frutas Vermelhas"]
    ),

    Preparo(
        "Frutas Vermelhas", "complemento",
        ["Frutas vermelhas frescas ou mix de frutas vermelhas"],
        """Higienize as frutas e utilize-as frescas na decoração ou montagem.""",
        "imagens/Geleia Artesanal de Frutas Vermelhas.png",
        ["Creme de Baunilha", "Brigadeiro de Leite Ninho",
         "Creme de Limão Siciliano", "Geleia de Frutas Vermelhas"]
    ),

    Preparo(
        "Cream Cheese", "complemento",
        ["Cream cheese"],
        """Utilize o cream cheese em temperatura adequada para misturar ou finalizar a preparação.""",
        "imagens/Redvelvet.png",
        ["Creme de Limão Siciliano"]
    )
]

for preparo in complementos:
    caderno.adicionar_preparo(preparo)


# =========================
# RECEITAS COMPLETAS
# =========================

receitas = [
    Receita(
        "Bolo de Cenoura", "Bolos e sobremesas", "30 min", "Médio",
        "1 bolo de 21 cm de diâmetro",
        [
            "2 discos de massa de cenoura",
            "2 receitas de brigadeiro tradicional",
            "Confeitos e decorações da sua escolha"
        ],
        """Numa base, coloque um pouco de brigadeiro para “colar” a massa.
Coloque o brigadeiro no saco de confeitar.
Posicione o primeiro disco e faça o trabalho de bico, preenchendo o meio.
Repita na outra camada e decore conforme sua escolha.""",
        "imagens/Bolo_de_cenoura_com_brigadeiro.png"
    ),

    Receita(
        "Bolo de Chocolate com Framboesa", "Bolos e sobremesas", "30 min", "Médio",
        "1 bolo de 21 cm de diâmetro",
        [
            "2 discos de massa de chocolate",
            "2 receitas de brigadeiro tradicional",
            "160 g de geleia de framboesa",
            "Confeitos, frutas vermelhas e outras decorações da sua escolha"
        ],
        """Coloque um pouco de brigadeiro na base.
Faça a borda com brigadeiro e preencha o meio.
Adicione a geleia no centro.
Repita na outra camada e decore conforme sua escolha.
A receita também indica geleia de frutas vermelhas como excelente combinação.""",
        "imagens/Bolo_chocolate_com_framboesa.png"
    ),

    Receita(
        "Bolo de Morango", "Bolos e sobremesas", "30 min", "Médio",
        "1 bolo de 21 cm de diâmetro",
        [
            "3 discos de massa branca",
            "2 receitas de brigadeiro de leite ninho",
            "315 g de creme de baunilha",
            "Morangos cortados (200 g)",
            "Confeitos, morangos e outras decorações da sua escolha"
        ],
        """Coloque um pouco de brigadeiro na base.
Faça o trabalho de bico na borda e preencha com brigadeiro.
Preencha o meio com creme de baunilha e morango.
Repita nas demais camadas e decore conforme sua escolha.""",
        "imagens/Bolo_de_morango.png"
    ),

    Receita(
        "Bolo Red Velvet", "Bolos e sobremesas", "30 min", "Médio",
        "1 bolo de 21 cm de diâmetro",
        [
            "3 discos de massa red velvet",
            "1 receita de creme de limão siciliano + 300 g de cream cheese",
            "Morangos cortados (200 g)",
            "Confeitos, frutas vermelhas e outras decorações da sua escolha"
        ],
        """Junte o creme com o cream cheese e bata brevemente com o fouet.
Coloque um pouco de creme na base.
Posicione o primeiro disco e coloque cerca de 1/3 do creme.
Coloque os morangos cortados.
Repita nas demais camadas e decore conforme sua escolha.""",
        "imagens/Redvelvet.png"
    ),

    Receita(
        "Cheesecake", "Bolos e sobremesas", "2 horas", "Médio/Difícil",
        "6 cheesecakes de 8 cm de diâmetro",
        [
            "Base: 100 g farinha de trigo",
            "Base: 60 g manteiga sem sal (1)",
            "Base: 30 g açúcar de confeiteiro",
            "Base: pitada de sal",
            "Base: 10 g farinha de amêndoa",
            "Base: 20 g ovo",
            "Base: 25 g manteiga sem sal (2)",
            "Creme: 490 g cream cheese",
            "Creme: 140 g creme de leite fresco 35% gordura",
            "Creme: 140 g açúcar refinado",
            "Creme: 8 g essência de baunilha",
            "Creme: 150 g ovo",
            "Montagem: 330 g de geleia da sua preferência"
        ],
        """Base:
Preaqueça o forno a 150 °C.
No processador coloque a farinha, o açúcar de confeiteiro, o sal,
a farinha de amêndoa e a manteiga sem sal (1) que deve estar gelada.
Processe até formar uma farofa um pouco mais grossa.
Misture bem o ovo até tudo se juntar.
Corte dois pedaços de papel manteiga e abra a massa entre eles.
Asse por 12 minutos.
Quando esfriar, triture no processador.
Derreta a manteiga sem sal (2) e misture na bolacha até virar farelo.
Distribua cerca de 30 g nas 6 formas de fundo removível e aperte bem.
Reserve.

Creme:
Preaqueça o forno a 90 °C.
Bata o cream cheese, o creme de leite fresco, a essência de baunilha e o açúcar até ficar sem grumos.
Incorpore os ovos um a um, sem misturar muito.
Coloque 150 g em cada forma.
Asse por 1 hora. Assim que esfriar, cubra as forminhas com plástico filme e leve à geladeira por 12 horas.

Montagem:
Desenforme os cheesecakes depois das 12 horas de refrigeração.
Coloque cerca de 55 g de geleia em cada um e decore conforme a preferência.
Armazene refrigerado e, de preferência, tampado para evitar que resseque.""",
        "imagens/Cheesecake.png"
    ),

    Receita(
        "Pannacota de Cumaru", "Sobremesas", "30 min", "Médio", "",
        [
            "4 g folha de gelatina", "175 g de chocolate branco", "200 g leite",
            "300 g creme de leite fresco 35% gordura", "1 g fava de tonka/cumaru",
            "180 g morango", "60 g açúcar refinado"
        ],
        """Creme:
Hidrate as folhas de gelatina em água fria.
Derreta o chocolate branco no micro-ondas, de 30 em 30 segundos, mexendo entre os intervalos.
Ferva o leite e acrescente a gelatina escorrida.
Verta 1/3 da mistura fervente no chocolate e misture bem.
Repita esse processo mais duas vezes.
Acrescente o creme de leite e a fava de tonka/cumaru.
Emulsione com mixer.
Despeje em um recipiente único ou divida conforme o desejado. Cubra com plástico filme e leve à geladeira por 4 horas, ou até firmar.

Geleia:
Numa panela coloque os morangos com o açúcar e cozinhe em fogo médio-baixo, esmagando os morangos e mexendo até engrossar.
Depois de engrossar, processe no mixer para obter uma geleia lisa e sem pedaços.
Coloque a geleia em um pote e cubra com plástico filme em contato.
Leve à geladeira.

Montagem:
Cubra toda a superfície da pannacota com a geleia de morango e decore.""",
        "imagens/Pannacota_cumaru.png"
    ),

    Receita(
        "Pudim de Leite Condensado", "Sobremesas", "50 min", "Médio", "",
        [
            "Caramelo: 200 g açúcar refinado",
            "Caramelo: água para cobrir o açúcar",
            "Caramelo: 40 g água",
            "Creme: 260 g leite condensado",
            "Creme: 80 g gemas",
            "Creme: 220 g leite integral"
        ],
        """Caramelo:
Numa panela de bordas altas, adicione o açúcar.
Regue com água apenas até que o açúcar esteja coberto.
Em fogo médio, cozinhe até obter um tom âmbar escuro e aroma intenso de caramelo.
Desligue o fogo e despeje cuidadosamente a segunda quantidade de água.
Mexa até obter uma calda lisa.
Despeje o caramelo na forma e espalhe pelas laterais.

Pudim:
Preaqueça o forno a 120 °C.
Numa tigela grande, combine o leite condensado com as gemas.
Regue com o leite e misture apenas para incorporar.
Passe a mistura por uma peneira.
Coloque na forma caramelizada.
Cubra com papel alumínio e asse em banho-maria.
Leve à geladeira e mantenha refrigerado por no mínimo 6 horas antes de desenformar.""",
        "imagens/Pudim_tradicional.png"
    ),

    Receita(
        "Cookie Tradicional", "Biscoitos e Cookies", "20 min", "Fácil", "",
        [
            "110 g de manteiga sem sal", "125 g açúcar mascavo",
            "75 g açúcar refinado", "55 g ovo", "10 g pasta de baunilha",
            "165 g farinha de trigo", "4 g sal", "3 g bicarbonato de sódio",
            "110 g chocolate meio amargo", "110 g chocolate ao leite"
        ],
        """Preaqueça o forno a 180 °C.
Misture manteiga e açúcares até formar um creme.
Junte o ovo e a baunilha.
Misture farinha, sal e bicarbonato e incorpore sem mexer em excesso.
Junte os chocolates.
Modele bolinhas de 100 g, deixando distância entre elas.
Asse por cerca de 8 minutos e aguarde antes de servir.""",
        "imagens/Cookie_tradicional.png"
    ),

    Receita(
        "Brownie Tradicional", "Biscoitos e Cookies", "20 min", "Fácil", "",
        [
            "100 g manteiga sem sal", "85 g chocolate meio amargo",
            "110 g ovo", "55 g açúcar refinado", "85 g açúcar mascavo",
            "30 g farinha de trigo", "15 g cacau 50% em pó", "Pitada de sal",
            "55 g chocolate branco", "55 g chocolate ao leite"
        ],
        """Preaqueça o forno a 200 °C.
Derreta chocolate meio amargo com manteiga.
Bata ovos com os açúcares sem dar volume.
Misture o chocolate com os ovos.
Peneire farinha, cacau e sal e acrescente.
Junte 2/3 dos chocolates e coloque na forma.
Finalize com o restante do chocolate.
Asse por 16 minutos.""",
        "imagens/Brownie_tradiconal.png"
    ),

    Receita(
        "Brioche", "Pães e salgados", "30 min", "Fácil", "8 bolinhas de 75 g",
        [
            "300 g farinha de trigo", "5 g fermento biológico seco",
            "50 g açúcar refinado", "50 g ovo", "120 g leite",
            "90 g manteiga com sal", "6 g sal", "Ovo + leite para pincelar"
        ],
        """Junte farinha, fermento, açúcar, ovo e metade do leite.
Sove e vá adicionando o restante do leite.
Adicione a manteiga em temperatura ambiente e depois o sal.
Sove até atingir o ponto de véu.
Descanse por 20 minutos.
Modele oito bolinhas de 75 g e deixe crescer até dobrar.
Pincele ovo e leite.
Asse a 160 °C por 8 minutos, reduza para 150 °C e asse por mais 20 minutos.
Deixe amornar sobre uma grade.""",
        "imagens/Brioche.png"
    ),

    Receita(
        "Pão de Leite", "Pães e salgados", "30 min", "Fácil", "",
        [
            "300 g farinha de trigo", "5 g fermento biológico seco",
            "40 g açúcar refinado", "50 g ovo", "130 g leite",
            "60 g manteiga com sal", "5 g sal", "Ovo + leite para pincelar"
        ],
        """Junte farinha, fermento, açúcar, ovo e metade do leite.
Sove e adicione o restante do leite.
Adicione a manteiga em temperatura ambiente e depois o sal.
Sove até atingir o ponto de véu.
Descanse por 20 minutos e modele conforme sua escolha.
Deixe crescer até dobrar.
Pincele ovo e leite.
Asse a 160 °C por 8 minutos, reduza para 150 °C e asse por mais 20 minutos.
Deixe amornar sobre uma grade.""",
        "imagens/Pao_de_leite.png"
    )
]

for receita in receitas:
    caderno.adicionar_receita(receita)


def carregar_caderno():
    return caderno
