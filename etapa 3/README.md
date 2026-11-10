# Etapa 3 - parte técnica

Esta pasta reúne a parte técnica da Etapa 3 do Projeto Aplicado I.

## Conteúdo

- `src/analise_exploratoria_etapa3.py`: script principal da análise.
- `notebooks/analise_exploratoria_etapa3.ipynb`: notebook organizado para consulta.
- `outputs/tabelas/`: tabelas usadas na conferência dos resultados.
- `outputs/graficos/`: gráficos usados no documento e no storytelling.
- `documentacao/`: notas de validação e orientação para integração ao repositório.

## Como colocar no repositório

Renomear esta pasta para `etapa_3` e colocá-la na raiz do projeto, no mesmo nível de `dados`, `documentacao` e `etapa 2`.

Os seis arquivos originais continuam em `dados/raw`. Não é necessário duplicá-los dentro da Etapa 3.

## Como executar

Na raiz do repositório:

```powershell
python -m pip install -r .\etapa_3\requirements.txt
python .\etapa_3\src\analise_exploratoria_etapa3.py
```

O script lê os seis CSVs de 2025 T1 a 2026 T2 e recria as tabelas e os gráficos.

## Observação sobre clientes

Nos resultados analíticos, `clientes_bcb_ccs_scr` corresponde à base usada pelo Banco Central no cálculo do ranking. Esse número não é o mesmo indicador corporativo de clientes divulgado pelo Banco do Brasil em seus materiais institucionais.
