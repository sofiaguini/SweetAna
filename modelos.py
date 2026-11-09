class Receita:
    def __init__(self, nome, categoria, tempo, dificuldade, rendimento,
                 ingredientes, modo_preparo, foto="", favorita=False):
        self.nome = nome
        self.categoria = categoria
        self.tempo = tempo
        self.dificuldade = dificuldade
        self.rendimento = rendimento
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo
        self.foto = foto
        self.favorita = favorita

    def adicionar_aos_favoritos(self):
        self.favorita = True

    def remover_dos_favoritos(self):
        self.favorita = False

    def exibir_detalhes(self):
        return {
            "nome": self.nome,
            "categoria": self.categoria,
            "tempo": self.tempo,
            "dificuldade": self.dificuldade,
            "rendimento": self.rendimento,
            "ingredientes": self.ingredientes,
            "modo_preparo": self.modo_preparo,
            "foto": self.foto
        }


class Preparo:
    def __init__(self, nome, tipo, ingredientes, modo_preparo, foto="",
                 compatibilidades=None):
        self.nome = nome
        self.tipo = tipo
        self.ingredientes = ingredientes
        self.modo_preparo = modo_preparo
        self.foto = foto
        self.compatibilidades = compatibilidades or []

    def exibir_detalhes(self):
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "ingredientes": self.ingredientes,
            "modo_preparo": self.modo_preparo,
            "foto": self.foto,
            "compatibilidades": self.compatibilidades
        }

    def combina_com(self, nome_preparo):
        for nome in self.compatibilidades:
            if nome.lower() == nome_preparo.lower():
                return True
        return False


class CadernoReceitas:
    def __init__(self):
        self.receitas = []
        self.preparos = []

    def adicionar_receita(self, receita):
        self.receitas.append(receita)

    def buscar_receita(self, nome):
        for receita in self.receitas:
            if receita.nome.lower() == nome.lower():
                return receita
        return None

    def filtrar_por_categoria(self, categoria):
        resultado = []
        for receita in self.receitas:
            if receita.categoria.lower() == categoria.lower():
                resultado.append(receita)
        return resultado

    def filtrar_por_dificuldade(self, dificuldade):
        resultado = []
        for receita in self.receitas:
            if receita.dificuldade.lower() == dificuldade.lower():
                resultado.append(receita)
        return resultado

    def listar_favoritas(self):
        favoritas = []
        for receita in self.receitas:
            if receita.favorita:
                favoritas.append(receita)
        return favoritas

    def adicionar_preparo(self, preparo):
        self.preparos.append(preparo)

    def buscar_preparo(self, nome):
        for preparo in self.preparos:
            if preparo.nome.lower() == nome.lower():
                return preparo
        return None

    def filtrar_preparos_por_tipo(self, tipo):
        resultado = []

        # "creme" funciona como categoria de recheios na interface.
        # Assim, cremes, brigadeiros e geleias podem aparecer juntos.
        if tipo.lower() == "creme":
            tipos_recheio = ["creme", "brigadeiro", "geleia"]

            for preparo in self.preparos:
                if preparo.tipo.lower() in tipos_recheio:
                    resultado.append(preparo)

            return resultado

        for preparo in self.preparos:
            if preparo.tipo.lower() == tipo.lower():
                resultado.append(preparo)

        return resultado

    def buscar_por_ingredientes(self, ingredientes_disponiveis):
        resultado = []

        ingredientes_disponiveis = [
            ingrediente.lower().strip()
            for ingrediente in ingredientes_disponiveis
        ]

        for receita in self.receitas:
            ingredientes_faltantes = []
            encontrados = []

            for ingrediente in receita.ingredientes:
                ingrediente_lower = ingrediente.lower()

                encontrado = False

                for disponivel in ingredientes_disponiveis:
                    if disponivel in ingrediente_lower or ingrediente_lower in disponivel:
                        encontrado = True
                        break

                if encontrado:
                    encontrados.append(ingrediente)
                else:
                    ingredientes_faltantes.append(ingrediente)

            resultado.append({
                "receita": receita,
                "encontrados": encontrados,
                "faltantes": ingredientes_faltantes
            })

        return resultado

    def verificar_compatibilidade(self, nome1, nome2):
        preparo1 = self.buscar_preparo(nome1)
        preparo2 = self.buscar_preparo(nome2)

        if preparo1 is None or preparo2 is None:
            return False

        if preparo1.combina_com(nome2):
            return True

        if preparo2.combina_com(nome1):
            return True

        return False

    def verificar_combinacao_completa(self, base, recheio, complemento):
        base_recheio = self.verificar_compatibilidade(base, recheio)
        recheio_complemento = self.verificar_compatibilidade(recheio, complemento)

        return base_recheio and recheio_complemento

    def gerar_combinacoes(self, base, recheio, complemento):
        resultado = []

        if self.verificar_combinacao_completa(base, recheio, complemento):
            resultado.append(
                f"{base} + {recheio} + {complemento}"
            )

        return resultado
