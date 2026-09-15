# Banco do Brasil + ODS 8

Base escolhida para o projeto de Data Storytelling.

## Tema

Análise das reclamações relacionadas ao Banco do Brasil usando o Ranking de Instituições por Índice de Reclamações do Banco Central do Brasil.

O recorte vai do 1º trimestre de 2025 ao 2º trimestre de 2026. São seis trimestres, o suficiente para acompanhar a evolução do Banco do Brasil e fazer comparações pontuais com outras instituições.

## Fonte dos dados

Banco Central do Brasil

Dataset: Ranking de Instituições por Índice de Reclamações

Portal:
https://dadosabertos.bcb.gov.br/dataset/ranking-de-instituicoes-por-indice-de-reclamacoes

Histórico dos arquivos:
https://www3.bcb.gov.br/ranking/historico.do

## Estrutura da pasta

```text
Banco_do_Brasil_Dados_BCB/
├── README.md
├── dados/
│   ├── raw/
│   │   ├── README.md
│   │   └── fontes_periodos.csv
│   └── processed/
│       └── README.md
├── documentacao/
│   ├── metadados.xlsx
│   └── fontes.txt
├── scripts/
│   └── baixar_dados.py
└── sql/
    ├── 01_criar_tabela.sql
    └── 02_consultas.sql
```

## Como os dados serão usados

Os CSVs do Banco Central ficam em `dados/raw` sem edição. Quando começarem os filtros e ajustes, os resultados podem ser salvos em `dados/processed`.

A ideia é carregar os arquivos no banco de dados e trabalhar com SQL. O arquivo `01_criar_tabela.sql` traz uma estrutura inicial de tabela e o `02_consultas.sql` deixa duas consultas básicas para começar a análise.

## Campos principais

Para o projeto, os campos mais importantes são:

- ano
- trimestre
- instituição financeira
- índice de reclamações
- reclamações reguladas procedentes
- reclamações reguladas outras
- reclamações não reguladas
- total de reclamações
- quantidade de clientes

A planilha `documentacao/metadados.xlsx` reúne as definições, o recorte, as limitações e as fontes usadas.

## Cuidados

O ranking reúne reclamações recebidas, analisadas e encerradas pelo Banco Central no período de referência. Por isso, ele não representa todas as reclamações feitas contra o banco em todos os canais.

O índice também não deve ser tratado como uma pesquisa de satisfação. Ele relaciona as reclamações reguladas procedentes com a base de clientes usada pelo Banco Central.

Os arquivos brutos devem ser preservados. Qualquer limpeza ou filtro fica em uma cópia separada.
