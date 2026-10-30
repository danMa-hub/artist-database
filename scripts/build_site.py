"""Genera il sito: indice a griglia, pagine dei tag, pagina delle mostre, anteprime.

Gira nella copia di lavoro di GitHub Actions prima di Jekyll: i file delle
schede nel repo non vengono modificati, cambia solo il sito pubblicato.
"""
import html
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
ESCLUSE = {"README", "informazioni", "contribuire", "tags", "00-lista-artisti", "index", "mostre"}
RIGHE_TAG = [("tecnica", "**Tag tecnica/formato:**"), ("tema", "**Tag tema:**")]
IMG = re.compile(r"!\[[^\]]*\]\((?!https?:)([^)\s]+)")
LARGHEZZA_ANTEPRIMA = 480


def slug_tag(tag):
    return re.sub(r"[^a-z0-9-]+", "-", tag.lower()).strip("-")


def sezione(righe, titolo):
    """Righe di una sezione '## titolo' (fino alla prossima '## ')."""
    for i, riga in enumerate(righe):
        if riga.strip().lower() == f"## {titolo}".lower():
            fine = next((j for j in range(i + 1, len(righe)) if righe[j].startswith("## ")), len(righe))
            return i, fine
    return None


def crea_anteprima(slug, percorso):
    origine = ROOT / percorso
    if not origine.exists():
        return None
    (ROOT / "anteprime").mkdir(exist_ok=True)
    destinazione = ROOT / "anteprime" / f"{slug}.jpg"
    try:
        with Image.open(origine) as im:
            im.seek(0)
            im = im.convert("RGBA")
            sfondo = Image.new("RGB", im.size, "white")
            sfondo.paste(im, mask=im.split()[3])
            sfondo.thumbnail((LARGHEZZA_ANTEPRIMA, LARGHEZZA_ANTEPRIMA * 3))
            sfondo.save(destinazione, "JPEG", quality=80)
    except Exception as errore:  # immagine illeggibile: la scheda resta senza anteprima
        print(f"anteprima non creata per {slug}: {errore}")
        return None
    return f"anteprime/{slug}.jpg"


# README.md resta la pagina del repo su GitHub; sul sito diventa "informazioni"
readme = ROOT / "README.md"
if readme.exists():
    (ROOT / "informazioni.md").write_text(
        "---\ntitle: Informazioni\n---\n\n" + readme.read_text(encoding="utf-8"), encoding="utf-8"
    )
contribuire = ROOT / "contribuire.md"
if contribuire.exists():
    contribuire.write_text(
        contribuire.read_text(encoding="utf-8").replace("README.html", "informazioni.html"), encoding="utf-8"
    )

schede = []
mostre = defaultdict(lambda: {"artisti": [], "visto_da": set()})
for f in sorted(ROOT.glob("*.md")):
    if f.stem in ESCLUSE:
        continue
    righe = f.read_text(encoding="utf-8").split("\n")
    titolo = re.match(r"# (.+)", righe[0]) if righe else None
    nome = titolo.group(1).strip() if titolo else f.stem
    tag = {"tecnica": [], "tema": []}
    anteprima = None
    for i, riga in enumerate(righe[:15]):
        for chiave, prefisso in RIGHE_TAG:
            if riga.startswith(prefisso):
                trovati = re.findall(r"`([^`]+)`", riga)
                tag[chiave] = trovati
                righe[i] = prefisso + " " + " ".join(
                    f"[`{t}`](tag/{slug_tag(t)}.html)" for t in trovati
                )
        scelta = re.match(r"\*\*Immagine anteprima:\*\*\s*(\S+)", riga)
        if scelta:
            anteprima = scelta.group(1).strip("`")
    if not anteprima:
        opere = sezione(righe, "Opere principali")
        zone = ["\n".join(righe[opere[0]:opere[1]])] if opere else []
        for zona in zone + ["\n".join(righe)]:
            trovata = IMG.search(zona)
            if trovata:
                anteprima = trovata.group(1)
                break
    miniatura = crea_anteprima(f.stem, anteprima) if anteprima else None

    viste = sezione(righe, "Mostre viste")
    if viste:
        for j in range(viste[0] + 1, viste[1]):
            voce = re.match(r"\s*[-*]\s+(.*)", righe[j])
            if not voce:
                continue
            testo = voce.group(1).strip()
            chi = re.search(r"\s[—–-]\s*visto da\s+(.+)$", testo, re.I)
            nome_mostra = testo[: chi.start()].strip() if chi else testo
            chiave = re.sub(r"\s+", " ", re.sub(r"[*_]", "", nome_mostra)).strip().lower()
            m = mostre[chiave]
            m.setdefault("titolo", re.sub(r"[*_]", "", nome_mostra).strip())
            m["artisti"].append((nome, f.stem))
            if chi:
                m["visto_da"].update(re.findall(r"@([A-Za-z0-9-]+)", chi.group(1)))
            righe[j] = re.sub(
                r"(?<![\w/])@([A-Za-z0-9-]+)", r"[@\1](https://github.com/\1)", righe[j]
            )
    f.write_text("\n".join(righe), encoding="utf-8")
    schede.append({"slug": f.stem, "nome": nome, "tag": tag, "miniatura": miniatura})

per_tag = {"tecnica": {}, "tema": {}}
for s in schede:
    for chiave in per_tag:
        for t in s["tag"][chiave]:
            per_tag[chiave].setdefault(t, []).append(s)


def scheda_card(s, prefisso=""):
    tutti = s["tag"]["tecnica"] + s["tag"]["tema"]
    ricerca = html.escape((s["nome"] + " " + " ".join(tutti)).lower(), quote=True)
    if s["miniatura"]:
        thumb = f'<img loading="lazy" src="{prefisso}{s["miniatura"]}" alt="">'
    else:
        thumb = f'<span class="iniziali">{html.escape("".join(p[0] for p in s["nome"].split()[:2]).upper())}</span>'
    tags = html.escape(" · ".join(tutti))
    return (
        f'<a class="card" data-s="{ricerca}" href="{prefisso}{s["slug"]}.html">'
        f'<div class="thumb">{thumb}</div>'
        f'<div class="info"><strong>{html.escape(s["nome"])}</strong>'
        f'<span class="tags">{tags}</span></div></a>'
    )


cartella = ROOT / "tag"
cartella.mkdir(exist_ok=True)
for chiave, mappa in per_tag.items():
    for t, elenco in mappa.items():
        card = "\n".join(
            scheda_card(s, "../") for s in sorted(elenco, key=lambda x: x["nome"].lower())
        )
        pagina = f"""---
title: {t}
---

# Tag: {t}

[Tutti i tag](index.html) · [Elenco degli artisti](../index.html)

{len(elenco)} schede ({'tecnica/formato' if chiave == 'tecnica' else 'tema'}):

<div class="grid">
{card}
</div>
"""
        (cartella / f"{slug_tag(t)}.md").write_text(pagina, encoding="utf-8")

indice_tag = ["---", "title: Tag", "---", "", "# Tag", "",
              "[Elenco degli artisti](../index.html) · [Vocabolario dei tag](../tags.html)", ""]
for chiave, titolo in (("tecnica", "Tecnica e formato"), ("tema", "Tema")):
    indice_tag += [f"## {titolo}", ""]
    for t, elenco in sorted(per_tag[chiave].items()):
        indice_tag.append(f"- [{t}]({slug_tag(t)}.html) ({len(elenco)})")
    indice_tag.append("")
(cartella / "index.md").write_text("\n".join(indice_tag), encoding="utf-8")

righe_mostre = ["---", "title: Mostre viste", "---", "", "# Mostre viste", "",
                "Mostre in cui gli artisti sono stati visti di persona o incontrati per la prima volta, "
                "con il nome di chi le ha segnalate. Si aggiunge scrivendo una voce nella sezione "
                "«Mostre viste» della scheda dell'artista ([come contribuire](contribuire.html)).", "",
                "[Elenco degli artisti](index.html)", ""]
if mostre:
    for chiave in sorted(mostre):
        m = mostre[chiave]
        artisti = ", ".join(f"[{n}]({s}.html)" for n, s in sorted(set(m["artisti"])))
        visto = ", ".join(f"[@{u}](https://github.com/{u})" for u in sorted(m["visto_da"]))
        righe_mostre += [f"## {m['titolo']}", "", f"Artisti: {artisti}", ""]
        if visto:
            righe_mostre += [f"Visto da: {visto}", ""]
else:
    righe_mostre.append("Nessuna mostra segnalata per ora.")
(ROOT / "mostre.md").write_text("\n".join(righe_mostre) + "\n", encoding="utf-8")

card = "\n".join(scheda_card(s) for s in sorted(schede, key=lambda x: x["nome"].lower()))
index = f"""---
title: Artist Database
---

# Artist Database

{len(schede)} schede di artisti e riferimenti critici su new media, modellazione 3D, mondi virtuali e IA applicata all'arte. Materiale didattico dell'Accademia di Belle Arti G. Carrara di Bergamo.

> **Lavoro in corso.** Le schede sono in parte compilate con l'aiuto dell'intelligenza artificiale e vanno ancora riviste: possono contenere errori, date o titoli da verificare, schede parziali. Controlla sempre le fonti linkate e segnala o correggi ciò che non torna ([come contribuire](contribuire.html)).

[Informazioni sul progetto](informazioni.html) · [Tutti i tag](tag/index.html) · [Mostre viste](mostre.html) · [Vocabolario dei tag](tags.html) · [Come contribuire](contribuire.html)

<input id="cerca" type="search" placeholder="Cerca un artista o un tag" class="cerca">

<div class="grid" id="elenco">
{card}
</div>

<script>
document.getElementById('cerca').addEventListener('input', function (e) {{
  var q = e.target.value.toLowerCase().trim();
  document.querySelectorAll('#elenco .card').forEach(function (c) {{
    c.style.display = c.dataset.s.indexOf(q) === -1 ? 'none' : '';
  }});
}});
</script>
"""
(ROOT / "index.md").write_text(index, encoding="utf-8")
senza = sum(1 for s in schede if not s["miniatura"])
print(f"{len(schede)} schede ({senza} senza anteprima), {sum(len(m) for m in per_tag.values())} tag, {len(mostre)} mostre")
