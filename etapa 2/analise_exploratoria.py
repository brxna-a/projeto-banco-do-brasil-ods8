"""
Etapa 2 - Analise Exploratoria
Projeto Banco do Brasil + ODS 8

Le os seis CSVs oficiais do Banco Central presentes em dados/raw,
consolida a base, calcula estatisticas descritivas e gera graficos.
"""

from pathlib import Path
import re
import unicodedata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "dados" / "raw"
PROCESSED = ROOT / "dados" / "processed"
OUT = ROOT / "etapa_2" / "outputs"
TABLES = OUT / "tabelas"
FIGS = OUT / "graficos"

for pasta in [PROCESSED, TABLES, FIGS]:
    pasta.mkdir(parents=True, exist_ok=True)

ARQUIVOS = sorted(RAW.glob("ranking_bcb_20*_T*.csv"))

def ler_csv(path):
    """Le os CSVs do BCB preservando o formato original."""
    return pd.read_csv(path, sep=";", encoding="utf-8-sig", dtype=str)

def numero_br(valor):
    """Converte numero com virgula decimal para float."""
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

def moda_informativa(serie):
    """Retorna moda somente quando existe repeticao real."""
    moda = serie.dropna().mode()
    if moda.empty:
        return np.nan
    freq = (serie == moda.iloc[0]).sum()
    return moda.iloc[0] if freq > 1 else np.nan

def estatisticas(df, colunas):
    linhas = []
    for coluna in colunas:
        s = pd.to_numeric(df[coluna], errors="coerce").dropna()
        if s.empty:
            continue
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
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
            "iqr": q3-q1,
            "variancia": s.var(ddof=1),
            "desvio_padrao": s.std(ddof=1),
        })
    return pd.DataFrame(linhas)

if len(ARQUIVOS) != 6:
    raise FileNotFoundError(
        f"Esperados 6 arquivos em dados/raw, mas foram encontrados {len(ARQUIVOS)}."
    )

quadros = []
for arquivo in ARQUIVOS:
    df = ler_csv(arquivo)
    # Alguns arquivos trazem uma coluna vazia no final. Ela nao contem dado analitico.
    df = df.loc[:, [c for c in df.columns if str(c).strip()]]
    df["arquivo_origem"] = arquivo.name
    quadros.append(df)

base = pd.concat(quadros, ignore_index=True, sort=False)

# Conversoes
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
    base[coluna] = base[coluna].map(numero_br)

base["Ano"] = pd.to_numeric(base["Ano"], errors="coerce").astype("Int64")
base["Trimestre_num"] = (
    base["Trimestre"].astype(str).str.extract(r"([1-4])")[0].astype("Int64")
)
base["Periodo"] = (
    base["Ano"].astype("string") + " T" + base["Trimestre_num"].astype("string")
)

base = base.sort_values(
    ["Ano", "Trimestre_num", "Instituição financeira"]
).reset_index(drop=True)

base.to_csv(
    PROCESSED / "ranking_bcb_consolidado.csv",
    index=False,
    encoding="utf-8-sig"
)

# Metadados e qualidade
metadados = []
for coluna in base.columns:
    s = base[coluna]
    metadados.append({
        "coluna": coluna,
        "tipo": str(s.dtype),
        "registros": len(s),
        "nao_nulos": int(s.notna().sum()),
        "nulos": int(s.isna().sum()),
        "percentual_nulos": round(s.isna().mean()*100, 2),
        "valores_distintos": int(s.nunique(dropna=True)),
    })

pd.DataFrame(metadados).to_csv(
    TABLES / "metadados_colunas.csv",
    index=False,
    encoding="utf-8-sig"
)

# Banco do Brasil aparece na base oficial como BB (conglomerado).
bb = base[base["Instituição financeira"].eq("BB (conglomerado)")].copy()

if len(bb) != 6:
    raise ValueError(
        f"Esperados 6 registros do BB, mas foram encontrados {len(bb)}."
    )

# Estatistica descritiva
estatisticas(base, colunas_numericas).to_csv(
    TABLES / "estatisticas_descritivas_geral.csv",
    index=False,
    encoding="utf-8-sig"
)
estatisticas(bb, colunas_numericas).to_csv(
    TABLES / "estatisticas_descritivas_bb.csv",
    index=False,
    encoding="utf-8-sig"
)

# Outliers por IQR
outliers = []
for coluna in colunas_numericas:
    s = base[coluna].dropna()
    q1 = s.quantile(.25)
    q3 = s.quantile(.75)
    iqr = q3-q1
    li = q1 - 1.5*iqr
    ls = q3 + 1.5*iqr
    mask = (base[coluna] < li) | (base[coluna] > ls)
    outliers.append({
        "variavel": coluna,
        "quantidade_outliers": int(mask.sum()),
        "limite_inferior": li,
        "limite_superior": ls,
    })

pd.DataFrame(outliers).to_csv(
    TABLES / "outliers_iqr_resumo.csv",
    index=False,
    encoding="utf-8-sig"
)

# Comparadores escolhidos por porte, considerando a mediana da base de clientes.
porte = (
    base.groupby("Instituição financeira")[
        "Quantidade total de clientes – CCS e SCR"
    ]
    .median()
    .sort_values(ascending=False)
)

comparadores = ["BB (conglomerado)"] + [
    nome for nome in porte.index
    if nome != "BB (conglomerado)"
][:4]

comparacao = base[
    base["Instituição financeira"].isin(comparadores)
].copy()

# Grafico 1
plt.figure(figsize=(9,5))
plt.plot(bb["Periodo"], bb["Índice"], marker="o")
plt.title("Evolucao do indice de reclamacoes do Banco do Brasil")
plt.xlabel("Periodo")
plt.ylabel("Indice de reclamacoes")
plt.grid(axis="y", alpha=.25)
plt.tight_layout()
plt.savefig(FIGS/"01_evolucao_indice_bb.png", dpi=180)
plt.close()

# Grafico 2
plt.figure(figsize=(10,6))
for nome, grupo in comparacao.groupby("Instituição financeira"):
    grupo = grupo.sort_values(["Ano","Trimestre_num"])
    plt.plot(grupo["Periodo"], grupo["Índice"], marker="o", label=nome)
plt.title("Indice de reclamacoes: BB e instituicoes comparadoras")
plt.xlabel("Periodo")
plt.ylabel("Indice de reclamacoes")
plt.legend(fontsize=8)
plt.grid(axis="y", alpha=.25)
plt.tight_layout()
plt.savefig(FIGS/"02_comparacao_indice.png", dpi=180)
plt.close()

# Grafico 3
plt.figure(figsize=(9,5))
plt.plot(
    bb["Periodo"],
    bb["Quantidade de reclamações procedentes extrapoladas"],
    marker="o"
)
plt.title("Reclamacoes procedentes extrapoladas - Banco do Brasil")
plt.xlabel("Periodo")
plt.ylabel("Quantidade extrapolada")
plt.grid(axis="y", alpha=.25)
plt.tight_layout()
plt.savefig(FIGS/"03_procedentes_extrapoladas_bb.png", dpi=180)
plt.close()

print("Analise exploratoria concluida.")
print(f"Base consolidada: {PROCESSED/'ranking_bcb_consolidado.csv'}")
print(f"Resultados: {OUT}")
