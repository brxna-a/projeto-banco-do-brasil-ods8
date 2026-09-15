-- Evolução do Banco do Brasil
SELECT
    ano,
    trimestre,
    instituicao_financeira,
    indice,
    reclamacoes_reguladas_procedentes,
    total_reclamacoes,
    total_clientes
FROM ranking_reclamacoes
WHERE UPPER(instituicao_financeira) LIKE '%BANCO DO BRASIL%'
ORDER BY ano, trimestre;

-- Comparação do período mais recente do recorte
SELECT
    instituicao_financeira,
    indice,
    reclamacoes_reguladas_procedentes,
    total_reclamacoes,
    total_clientes
FROM ranking_reclamacoes
WHERE ano = 2026
  AND trimestre = 2
ORDER BY indice DESC;
