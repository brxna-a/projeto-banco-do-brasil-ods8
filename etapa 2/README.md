# Banco do Brasil + ODS 8 - Etapa 2

A Etapa 2 contém a proposta analítica, análise exploratória dos seis CSVs oficiais do Banco Central, notebook Jupyter, script Python, tabelas e gráficos.

## Estrutura

```text
etapa_2/
├── README.md
├── requirements.txt
├── src/
│   └── analise_exploratoria.py
├── notebooks/
│   └── analise_exploratoria.ipynb
├── documentacao/
│   ├── proposta_analitica.md
│   └── metadados_e_governanca.md
└── outputs/
    ├── tabelas/
    └── graficos/
```

## Execução

Na raiz do repositório:

```powershell
python -m pip install -r .\etapa_2\requirements.txt
python .\etapa_2\src\analise_exploratoria.py
```

Os arquivos brutos devem continuar em `dados/raw`.

## Resultados principais

A base consolidada contém 1.130 registros provenientes de seis trimestres. O Banco do Brasil aparece como `BB (conglomerado)` e possui seis observações no recorte.

O índice do BB variou entre 16,22 e 32,68, com média de 22,81 e mediana de 21,38. O maior valor ocorreu em 2026 T2 e o menor em 2025 T4.

A interpretação deve considerar a metodologia do Banco Central e as diferenças de porte entre as instituições.
