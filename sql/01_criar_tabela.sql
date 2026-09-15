-- Estrutura inicial para a base do Ranking de Reclamações do BCB.
-- Os nomes podem ser ajustados na hora da importação para acompanhar o cabeçalho do CSV.

CREATE TABLE ranking_reclamacoes (
    ano INTEGER,
    trimestre INTEGER,
    categoria VARCHAR(100),
    tipo VARCHAR(100),
    cnpj_if VARCHAR(20),
    instituicao_financeira VARCHAR(255),
    indice DECIMAL(18,6),
    reclamacoes_reguladas_procedentes INTEGER,
    reclamacoes_reguladas_outras INTEGER,
    reclamacoes_nao_reguladas INTEGER,
    total_reclamacoes INTEGER,
    total_clientes BIGINT
);
