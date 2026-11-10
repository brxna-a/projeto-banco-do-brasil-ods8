from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# A pasta etapa_3 deve ficar na raiz do repositório.
ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "dados" / "raw"
OUT = ROOT / "etapa_3" / "outputs"
TABELAS = OUT / "tabelas"
GRAFICOS = OUT / "graficos"

for pasta in (TABELAS, GRAFICOS):
    pasta.mkdir(parents=True, exist_ok=True)

arquivos = sorted(RAW.glob("ranking_bcb_20*_T*.csv"))
if len(arquivos) != 6:
    raise FileNotFoundError(
        f"Foram encontrados {len(arquivos)} CSVs. O projeto usa 6 arquivos, de 2025 T1 a 2026 T2."
    )

def numero_br(valor):
    if pd.isna(valor):
        return np.nan
    texto = str(valor).strip()
    if not texto:
        return np.nan
    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")
    texto = re.sub(r"[^0-9.\-]", "", texto)
    try:
        return float(texto)
    except ValueError:
        return np.nan

quadros = []
for arquivo in arquivos:
    df = pd.read_csv(arquivo, sep=";", encoding="utf-8-sig", dtype=str)
    # Alguns arquivos possuem uma coluna vazia no fim do cabeçalho.
    df = df.loc[:, [c for c in df.columns if str(c).strip()]]
    df["arquivo_origem"] = arquivo.name
    quadros.append(df)

base = pd.concat(quadros, ignore_index=True, sort=False)

colunas_numericas = [
    "Índice",
    "Quantidade total de reclamações respondidas",
    "Quantidade de reclamações procedentes",
    "Quantidade de reclamações procedentes extrapoladas",
    "Quantidade total de reclamações analisadas",
    "Quantidade total de clientes – CCS e SCR",
    "Quantidade de clientes – CCS",
    "Quantidade de clientes – SCR",
]

for coluna in colunas_numericas:
    if coluna not in base.columns:
        raise KeyError(f"Coluna esperada não encontrada: {coluna}")
    base[coluna] = base[coluna].map(numero_br)

base["Ano"] = pd.to_numeric(base["Ano"], errors="raise").astype(int)
base["Trimestre_num"] = base["Trimestre"].astype(str).str.extract(r"([1-4])")[0].astype(int)
base["Periodo"] = base["Ano"].astype(str) + " T" + base["Trimestre_num"].astype(str)

# Qualidade dos dados
metadados = []
for coluna in base.columns:
    s = base[coluna]
    metadados.append({
        "coluna": coluna,
        "tipo": str(s.dtype),
        "registros": len(s),
        "nulos": int(s.isna().sum()),
        "percentual_nulos": round(float(s.isna().mean() * 100), 2),
        "valores_distintos": int(s.nunique(dropna=True)),
    })
pd.DataFrame(metadados).to_csv(
    TABELAS / "metadados_colunas.csv", index=False, encoding="utf-8-sig"
)

# Recorte do Banco do Brasil
bb = base[base["Instituição financeira"].eq("BB (conglomerado)")].copy()
bb = bb.sort_values(["Ano", "Trimestre_num"])
if len(bb) != 6:
    raise ValueError(f"Esperados 6 registros do BB; encontrados {len(bb)}.")

def moda_informativa(s):
    s = s.dropna()
    if s.empty or s.value_counts().max() == 1:
        return np.nan
    return s.mode().iloc[0]

def estatisticas(df, colunas):
    linhas = []
    for coluna in colunas:
        s = pd.to_numeric(df[coluna], errors="coerce").dropna()
        q1, q3 = s.quantile(.25), s.quantile(.75)
        linhas.append({
            "variavel": coluna,
            "n": int(s.count()),
            "media": s.mean(),
            "mediana": s.median(),
            "moda": moda_informativa(s),
            "minimo": s.min(),
            "q1": q1,
            "q3": q3,
            "maximo": s.max(),
            "iqr": q3 - q1,
            "variancia": s.var(ddof=1),
            "desvio_padrao": s.std(ddof=1),
        })
    return pd.DataFrame(linhas)

estatisticas(bb, colunas_numericas).to_csv(
    TABELAS / "estatisticas_descritivas_bb.csv", index=False, encoding="utf-8-sig"
)

# Outliers da base completa pelo critério do IQR.
resumo_outliers = []
for coluna in colunas_numericas:
    s = base[coluna].dropna()
    q1, q3 = s.quantile(.25), s.quantile(.75)
    iqr = q3 - q1
    li, ls = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    mask = (base[coluna] < li) | (base[coluna] > ls)
    resumo_outliers.append({
        "variavel": coluna,
        "outliers_iqr": int(mask.sum()),
        "limite_inferior": li,
        "limite_superior": ls,
    })
pd.DataFrame(resumo_outliers).to_csv(
    TABELAS / "outliers_iqr_resumo.csv", index=False, encoding="utf-8-sig"
)

# Comparadores de grande porte usados no trabalho.
comparadores = {
    "BB": "BB (conglomerado)",
    "CAIXA": "CAIXA ECONÔMICA FEDERAL (conglomerado)",
    "NU PAGAMENTOS": "NU PAGAMENTOS (conglomerado)",
    "BRADESCO": "BRADESCO (conglomerado)",
    "ITAU": "ITAU (conglomerado)",
}

series = []
for rotulo, nome in comparadores.items():
    recorte = base[base["Instituição financeira"].eq(nome)].copy()
    recorte = recorte.sort_values(["Ano", "Trimestre_num"])
    if len(recorte) != 6:
        raise ValueError(f"{rotulo}: esperados 6 registros; encontrados {len(recorte)}.")
    tmp = recorte[["Periodo", "Índice"]].rename(columns={"Índice": rotulo})
    series.append(tmp.set_index("Periodo"))

comparacao = pd.concat(series, axis=1).reset_index()
comparacao.to_csv(
    TABELAS / "comparacao_instituicoes.csv", index=False, encoding="utf-8-sig"
)

# Tabela do BB usada no relatório.
bb_saida = bb[[
    "Periodo", "Ano", "Trimestre_num", "Índice",
    "Quantidade total de reclamações respondidas",
    "Quantidade de reclamações procedentes",
    "Quantidade de reclamações procedentes extrapoladas",
    "Quantidade total de reclamações analisadas",
    "Quantidade total de clientes – CCS e SCR",
    "Quantidade de clientes – CCS",
    "Quantidade de clientes – SCR",
]].copy()
bb_saida.columns = [
    "periodo","ano","trimestre","indice","reclamacoes_respondidas",
    "reclamacoes_procedentes","reclamacoes_procedentes_extrapoladas",
    "reclamacoes_analisadas","clientes_bcb_ccs_scr","clientes_ccs","clientes_scr"
]
bb_saida.to_csv(
    TABELAS / "registros_banco_do_brasil.csv", index=False, encoding="utf-8-sig"
)

# Gráfico 1
plt.figure(figsize=(9,5))
plt.plot(bb["Periodo"], bb["Índice"], marker="o")
plt.title("Evolução do índice de reclamações do Banco do Brasil")
plt.xlabel("Período")
plt.ylabel("Índice de reclamações")
plt.grid(axis="y", alpha=.25)
plt.tight_layout()
plt.savefig(GRAFICOS / "01_evolucao_indice_bb.png", dpi=200)
plt.close()

# Gráfico 2
plt.figure(figsize=(10,6))
for coluna in comparacao.columns[1:]:
    plt.plot(comparacao["Periodo"], comparacao[coluna], marker="o", label=coluna)
plt.title("Índice de reclamações: BB e instituições comparadoras")
plt.xlabel("Período")
plt.ylabel("Índice de reclamações")
plt.legend(fontsize=8)
plt.grid(axis="y", alpha=.25)
plt.tight_layout()
plt.savefig(GRAFICOS / "02_comparacao_indice.png", dpi=200)
plt.close()

# Gráfico 3
plt.figure(figsize=(9,5))
plt.plot(
    bb["Periodo"],
    bb["Quantidade de reclamações procedentes extrapoladas"],
    marker="o"
)
plt.title("Reclamações procedentes extrapoladas - Banco do Brasil")
plt.xlabel("Período")
plt.ylabel("Quantidade")
plt.grid(axis="y", alpha=.25)
plt.tight_layout()
plt.savefig(GRAFICOS / "03_procedentes_extrapoladas_bb.png", dpi=200)
plt.close()

# Gráfico 4
plt.figure(figsize=(9,5))
plt.plot(
    bb["Periodo"],
    bb["Quantidade total de clientes – CCS e SCR"] / 1_000_000,
    marker="o"
)
plt.title("Base de clientes usada pelo BCB no índice do Banco do Brasil")
plt.xlabel("Período")
plt.ylabel("Clientes BCB - CCS + SCR (milhões)")
plt.grid(axis="y", alpha=.25)
plt.tight_layout()
plt.savefig(GRAFICOS / "04_clientes_bcb_bb.png", dpi=200)
plt.close()

print("Análise concluída.")
print(f"Registros consolidados: {len(base)}")
print(f"Registros do BB: {len(bb)}")
print(f"Resultados salvos em: {OUT}")
