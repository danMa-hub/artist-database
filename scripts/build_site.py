"""Genera le pagine dei tag, l'indice degli artisti e rende cliccabili i tag.

Gira nella copia di lavoro di GitHub Actions prima di Jekyll: i file delle
schede nel repo non vengono modificati, cambia solo il sito pubblicato.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
ESCLUSE = {"README", "tags", "00-lista-artisti", "index"}
RIGHE_TAG = [("tecnica", "**Tag tecnica/formato:**"), ("tema", "**Tag tema:**")]


def slug_tag(tag):
    return re.sub(r"[^a-z0-9-]+", "-", tag.lower()).strip("-")


schede = []
for f in sorted(ROOT.glob("*.md")):
    if f.stem in ESCLUSE:
        continue
    testo = f.read_text(encoding="utf-8")
    titolo = re.match(r"# (.+)", testo)
    nome = titolo.group(1).strip() if titolo else f.stem
    tag = {"tecnica": [], "tema": []}
    righe = testo.split("\n")
    for i, riga in enumerate(righe[:15]):
        for chiave, prefisso in RIGHE_TAG:
            if riga.startswith(prefisso):
                trovati = re.findall(r"`([^`]+)`", riga)
                tag[chiave] = trovati
                righe[i] = prefisso + " " + " ".join(
                    f"[`{t}`](tag/{slug_tag(t)}.html)" for t in trovati
                )
    f.write_text("\n".join(righe), encoding="utf-8")
    schede.append({"slug": f.stem, "nome": nome, "tag": tag})

per_tag = {"tecnica": {}, "tema": {}}
for s in schede:
    for chiave in per_tag:
        for t in s["tag"][chiave]:
            per_tag[chiave].setdefault(t, []).append(s)

cartella = ROOT / "tag"
cartella.mkdir(exist_ok=True)
for chiave, mappa in per_tag.items():
    for t, elenco in mappa.items():
        righe = [
            "---", f"title: {t}", "---", "",
            f"# Tag: {t}", "",
            f"[Tutti i tag](index.html) · [Elenco degli artisti](../index.html)", "",
            f"{len(elenco)} schede ({'tecnica/formato' if chiave == 'tecnica' else 'tema'}):", "",
        ]
        for s in sorted(elenco, key=lambda x: x["nome"].lower()):
            righe.append(f"- [{s['nome']}](../{s['slug']}.html)")
        (cartella / f"{slug_tag(t)}.md").write_text("\n".join(righe) + "\n", encoding="utf-8")

indice_tag = ["---", "title: Tag", "---", "", "# Tag", "",
              "[Elenco degli artisti](../index.html) · [Vocabolario dei tag](../tags.html)", ""]
for chiave, titolo in (("tecnica", "Tecnica e formato"), ("tema", "Tema")):
    indice_tag += [f"## {titolo}", ""]
    for t, elenco in sorted(per_tag[chiave].items()):
        indice_tag.append(f"- [{t}]({slug_tag(t)}.html) ({len(elenco)})")
    indice_tag.append("")
(cartella / "index.md").write_text("\n".join(indice_tag), encoding="utf-8")

voci = []
for s in sorted(schede, key=lambda x: x["nome"].lower()):
    tutti = s["tag"]["tecnica"] + s["tag"]["tema"]
    chiave = html.escape((s["nome"] + " " + " ".join(tutti)).lower(), quote=True)
    badge = " ".join(
        f'<a href="tag/{slug_tag(t)}.html"><code>{html.escape(t)}</code></a>' for t in tutti
    )
    voci.append(
        f'<li data-s="{chiave}"><a href="{s["slug"]}.html">{html.escape(s["nome"])}</a> {badge}</li>'
    )

index = f"""---
title: Artist Database
---

# Artist Database

{len(schede)} schede di artisti e riferimenti critici su new media, modellazione 3D, mondi virtuali e IA applicata all'arte. Materiale didattico dell'Accademia di Belle Arti G. Carrara di Bergamo.

[Tutti i tag](tag/index.html) · [Vocabolario dei tag](tags.html) · [Come contribuire](README.html)

<input id="cerca" type="search" placeholder="Cerca un artista o un tag" style="width:100%;padding:6px">

<ul id="elenco" style="list-style:none;padding:0">
{chr(10).join(voci)}
</ul>

<script>
document.getElementById('cerca').addEventListener('input', function (e) {{
  var q = e.target.value.toLowerCase().trim();
  document.querySelectorAll('#elenco li').forEach(function (li) {{
    li.style.display = li.dataset.s.indexOf(q) === -1 ? 'none' : '';
  }});
}});
</script>
"""
(ROOT / "index.md").write_text(index, encoding="utf-8")
print(f"{len(schede)} schede, {sum(len(m) for m in per_tag.values())} tag")
