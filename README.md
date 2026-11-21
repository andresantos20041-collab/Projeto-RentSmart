# RentSmart — Sistema de Orçamento de Locação

Projeto acadêmico desenvolvido em Python para a disciplina **Algorithmic Thinking & Introduction to Object-Oriented Programming**.

## Objetivo
Automatizar o orçamento mensal de locação da R.M Imóveis, aplicando valores-base, adicionais, desconto para apartamentos e taxa contratual.

## Regras implementadas
- Apartamento: aluguel-base de R$ 700,00.
- Casa: aluguel-base de R$ 900,00.
- Estúdio: aluguel-base de R$ 1.200,00.
- Apartamento com 2 quartos: adicional de R$ 200,00.
- Casa com 2 quartos: adicional de R$ 250,00.
- Casa/apartamento com vaga: adicional mensal de R$ 300,00.
- Estúdio: sem estacionamento = R$ 0,00; pacote de até 2 vagas = R$ 250,00; cada vaga acima de 2 = R$ 60,00.
- Apartamento sem crianças: desconto de 5% sobre o valor do aluguel após os adicionais.
- Taxa contratual: R$ 2.000,00, parcelável em até 5 vezes.
- CSV: projeção de 12 meses; a parcela da taxa aparece nos primeiros meses conforme o parcelamento escolhido.

## Requisitos
- Python 3.9 ou superior.
- Não exige instalação de bibliotecas externas.

## Como executar
1. Baixe ou clone este repositório.
2. Abra a pasta do projeto no VS Code.
3. Abra o terminal integrado.
4. Execute:

```bash
python main.py
```

No Windows, se o comando acima não funcionar, tente:

```bash
py main.py
```

5. Responda às perguntas exibidas no terminal.
6. Ao final, o arquivo `projecao_12_meses.csv` será criado na mesma pasta do programa.

## Organização do projeto
```text
RentSmart/
├── main.py
├── README.md
└── documentacao/
    └── relatorio_teorico.pdf
```

## Programação Orientada a Objetos
O projeto utiliza a classe abstrata `Imovel` e as classes `Apartamento`, `Casa` e `Estudio`, que especializam suas regras. A classe `Orcamento` coordena os cálculos e a apresentação, enquanto `ResultadoOrcamento` armazena os valores calculados.

## Observação sobre a regra do estúdio
O enunciado informa que o pacote inicial de duas vagas custa R$ 250,00 e que vagas adicionais custam R$ 60,00 cada. A implementação considera que, ao contratar estacionamento, o pacote de R$ 250,00 cobre até duas vagas; a partir da terceira vaga, soma-se R$ 60,00 por vaga extra. A opção zero significa que o cliente não contrata estacionamento.
