"""
RentSmart - Sistema de Orçamento de Locação
Projeto acadêmico em Python com Programação Orientada a Objetos.

Execução:
    python main.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
import csv


TAXA_CONTRATUAL = 2000.00
LIMITE_PARCELAS = 5


def moeda(valor: float) -> str:
    """Formata um valor no padrão monetário brasileiro."""
    texto = f"R$ {valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def ler_opcao(mensagem: str, opcoes: tuple[str, ...]) -> str:
    """Lê uma opção até que o usuário informe um dos valores permitidos."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in opcoes:
            return resposta
        print(f"Opção inválida. Escolha: {', '.join(opcoes)}.")


def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    """Lê um número inteiro dentro de um intervalo."""
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Informe um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


class Imovel(ABC):
    """Classe-base que representa um imóvel disponível para locação."""

    def __init__(self, quartos: int):
        self.quartos = quartos

    @property
    @abstractmethod
    def aluguel_base(self) -> float:
        pass

    @abstractmethod
    def descricao(self) -> str:
        pass

    def calcular_adicionais(self, possui_garagem: bool = False) -> float:
        """Calcula adicionais comuns de imóvel. Subclasses podem especializar."""
        return 300.00 if possui_garagem else 0.00


class Apartamento(Imovel):
    """Apartamento de um ou dois quartos."""

    def __init__(self, quartos: int, possui_garagem: bool, sem_criancas: bool):
        super().__init__(quartos)
        self.possui_garagem = possui_garagem
        self.sem_criancas = sem_criancas

    @property
    def aluguel_base(self) -> float:
        return 700.00

    def descricao(self) -> str:
        return f"Apartamento - {self.quartos} quarto(s)"

    def calcular_adicionais(self, possui_garagem: bool = False) -> float:
        adicional_quartos = 200.00 if self.quartos == 2 else 0.00
        adicional_garagem = 300.00 if self.possui_garagem else 0.00
        return adicional_quartos + adicional_garagem

    def calcular_desconto(self, valor_com_adicionais: float) -> float:
        return valor_com_adicionais * 0.05 if self.sem_criancas else 0.00


class Casa(Imovel):
    """Casa de um ou dois quartos."""

    def __init__(self, quartos: int, possui_garagem: bool):
        super().__init__(quartos)
        self.possui_garagem = possui_garagem

    @property
    def aluguel_base(self) -> float:
        return 900.00

    def descricao(self) -> str:
        return f"Casa - {self.quartos} quarto(s)"

    def calcular_adicionais(self, possui_garagem: bool = False) -> float:
        adicional_quartos = 250.00 if self.quartos == 2 else 0.00
        adicional_garagem = 300.00 if self.possui_garagem else 0.00
        return adicional_quartos + adicional_garagem


class Estudio(Imovel):
    """Estúdio com pacote inicial de duas vagas e vagas extras opcionais."""

    def __init__(self, quantidade_vagas: int):
        super().__init__(quartos=0)
        self.quantidade_vagas = quantidade_vagas

    @property
    def aluguel_base(self) -> float:
        return 1200.00

    def descricao(self) -> str:
        return "Estúdio"

    def calcular_adicionais(self, possui_garagem: bool = False) -> float:
        if self.quantidade_vagas == 0:
            return 0.00
        # O pacote de estacionamento inclui até duas vagas por R$ 250,00.
        extras = max(0, self.quantidade_vagas - 2)
        return 250.00 + (extras * 60.00)


@dataclass
class ResultadoOrcamento:
    """Armazena os valores calculados para a locação."""

    aluguel_base: float
    adicionais: float
    desconto: float
    aluguel_mensal: float

    taxa_contratual: float
    quantidade_parcelas: int

    @property
    def valor_parcela_contrato(self) -> float:
        return self.taxa_contratual / self.quantidade_parcelas


class Orcamento:
    """Coordena o cálculo e a apresentação do orçamento."""

    def __init__(self, imovel: Imovel, quantidade_parcelas: int):
        self.imovel = imovel
        self.quantidade_parcelas = quantidade_parcelas
        self.resultado = self.calcular()

    def calcular(self) -> ResultadoOrcamento:
        adicionais = self.imovel.calcular_adicionais()
        valor_com_adicionais = self.imovel.aluguel_base + adicionais

        desconto = 0.00
        if isinstance(self.imovel, Apartamento):
            desconto = self.imovel.calcular_desconto(valor_com_adicionais)

        aluguel_mensal = valor_com_adicionais - desconto

        return ResultadoOrcamento(
            aluguel_base=self.imovel.aluguel_base,
            adicionais=adicionais,
            desconto=desconto,
            aluguel_mensal=aluguel_mensal,
            taxa_contratual=TAXA_CONTRATUAL,
            quantidade_parcelas=self.quantidade_parcelas,
        )

    def exibir_resumo(self) -> None:
        r = self.resultado
        print("\n" + "=" * 48)
        print("             RESUMO DO ORÇAMENTO")
        print("=" * 48)
        print(f"Imóvel:                 {self.imovel.descricao()}")
        print(f"Aluguel-base:           {moeda(r.aluguel_base)}")
        print(f"Adicionais:             {moeda(r.adicionais)}")
        print(f"Desconto:              -{moeda(r.desconto)}")
        print("-" * 48)
        print(f"ALUGUEL MENSAL:         {moeda(r.aluguel_mensal)}")
        print()
        print(f"Taxa contratual:        {moeda(r.taxa_contratual)}")
        print(f"Parcelamento:           {r.quantidade_parcelas}x")
        print(f"Valor de cada parcela:  {moeda(r.valor_parcela_contrato)}")
        print("=" * 48)
        print("A taxa contratual é apresentada separadamente do aluguel.")
        print("O CSV mostrará as parcelas da taxa nos primeiros meses do contrato.")

    def gerar_csv(self, nome_arquivo: str = "projecao_12_meses.csv") -> str:
        """Gera a projeção de aluguel e taxa contratual para 12 meses."""
        r = self.resultado
        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow([
                "Mes", "Aluguel mensal (R$)", "Taxa contratual total (R$)",
                "Parcela da taxa no mes (R$)", "Total previsto no mes (R$)"
            ])

            for mes in range(1, 13):
                parcela = r.valor_parcela_contrato if mes <= r.quantidade_parcelas else 0.00
                total = r.aluguel_mensal + parcela
                escritor.writerow([
                    mes,
                    f"{r.aluguel_mensal:.2f}",
                    f"{r.taxa_contratual:.2f}" if mes == 1 else "0.00",
                    f"{parcela:.2f}",
                    f"{total:.2f}",
                ])
        return nome_arquivo


def coletar_imovel() -> Imovel:
    print("\nTIPO DE IMÓVEL")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    tipo = ler_opcao("Escolha (1/2/3): ", ("1", "2", "3"))

    if tipo == "1":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_opcao("Deseja uma vaga de garagem? (s/n): ", ("s", "n")) == "s"
        sem_criancas = ler_opcao(
            "O cliente informa que não possui crianças? (s/n): ", ("s", "n")
        ) == "s"
        return Apartamento(quartos, garagem, sem_criancas)

    if tipo == "2":
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_opcao("Deseja uma vaga de garagem? (s/n): ", ("s", "n")) == "s"
        return Casa(quartos, garagem)

    vagas = ler_inteiro(
        "Quantidade de vagas de estacionamento (0 para nenhuma): ", 0, 20
    )
    return Estudio(vagas)


def main() -> None:
    print("=" * 48)
    print("       RENTSMART - ORÇAMENTO DE LOCAÇÃO")
    print("=" * 48)

    imovel = coletar_imovel()
    parcelas = ler_inteiro(
        f"Em quantas parcelas deseja pagar a taxa contratual (1 a {LIMITE_PARCELAS})? ",
        1,
        LIMITE_PARCELAS,
    )

    orcamento = Orcamento(imovel, parcelas)
    orcamento.exibir_resumo()

    nome_csv = orcamento.gerar_csv()
    print(f"\nArquivo CSV gerado com sucesso: {nome_csv}")
    print("O arquivo foi salvo na mesma pasta do programa.")


if __name__ == "__main__":
    main()
