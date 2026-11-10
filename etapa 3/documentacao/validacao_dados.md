# Validação da análise

## Base utilizada

Foram considerados os seis arquivos trimestrais disponíveis no repositório:

- 2025 T1
- 2025 T2
- 2025 T3
- 2025 T4
- 2026 T1
- 2026 T2

A consolidação da Etapa 2 contém 1.130 registros. O Banco do Brasil aparece nos arquivos como `BB (conglomerado)` e possui uma observação em cada trimestre.

## Resultados conferidos para o Banco do Brasil

| Período | Índice | Respondidas | Procedentes | Procedentes extrapoladas | Clientes BCB (CCS + SCR) |
|---|---:|---:|---:|---:|---:|
| 2025 T1 | 20,55 | 13.364 | 154 | 1.617 | 78.676.764 |
| 2025 T2 | 22,20 | 18.965 | 119 | 1.776 | 79.972.615 |
| 2025 T3 | 25,85 | 22.802 | 93 | 2.091 | 80.883.474 |
| 2025 T4 | 16,22 | 25.122 | 51 | 1.330 | 81.983.236 |
| 2026 T1 | 19,36 | 23.611 | 64 | 1.608 | 82.994.859 |
| 2026 T2 | 32,68 | 25.764 | 108 | 2.748 | 84.086.146 |

Para o índice do BB: média 22,81; mediana 21,375; mínimo 16,22; máximo 32,68; desvio padrão amostral 5,78738.

## Pontos metodológicos

O índice do ranking atual utiliza a quantidade extrapolada de reclamações procedentes. A extrapolação é feita a partir da amostra de reclamações analisadas pelo Banco Central.

A quantidade de clientes do ranking é formada pela base conjugada CCS + SCR. Por isso, ela não deve ser comparada como se fosse o mesmo conceito do total de clientes divulgado pelo Banco do Brasil em apresentações corporativas.

Valores ausentes no campo `Índice` não são preenchidos artificialmente. As análises do indicador utilizam os valores efetivamente publicados.

Os outliers da base geral foram identificados pelo critério do IQR apenas para exploração. Eles não foram removidos automaticamente, pois a base reúne instituições de portes muito diferentes.
