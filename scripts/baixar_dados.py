from pathlib import Path
from urllib.request import Request, urlopen

periodos = [
    (2025, 1),
    (2025, 2),
    (2025, 3),
    (2025, 4),
    (2026, 1),
    (2026, 2),
]

pasta = Path(__file__).resolve().parents[1] / "dados" / "raw"
pasta.mkdir(parents=True, exist_ok=True)

for ano, trimestre in periodos:
    url = (
        "https://www3.bcb.gov.br/rdrweb/rest/ext/ranking/arquivo"
        f"?ano={ano}&periodicidade=TRIMESTRAL&periodo={trimestre}"
        "&tipo=Bancos+e+financeiras"
    )

    nome = f"ranking_bcb_{ano}_T{trimestre}.csv"
    destino = pasta / nome

    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as resposta:
        destino.write_bytes(resposta.read())

    print(f"Salvo: {destino.name}")
