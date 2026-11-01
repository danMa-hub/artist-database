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
RIGHE_TAG = [("tecnica", "**Tag tecnica/formato:**"), ("tema", "**Tag tema:**"), ("corso", "**Tag corso:**")]
TAG_CORSO = ["TAD-DCV", "TAD-AVM", "AW", "M3D"]
PADRE = {  # sotto-tag -> categoria ampia: chi usa il sotto-tag compare anche nella categoria
    "visual-live-e-vjing": "performance-audiovisiva",
    "video-mapping-e-proiezione": "performance-audiovisiva",
    "lecture-performance": "performance-audiovisiva",
    "animazione-dal-vivo": "performance-audiovisiva",
    "performance-con-corpo-e-motion-capture": "performance-audiovisiva",
    "performance-nei-mondi-virtuali": "performance-audiovisiva",
}


def espandi(lista):
    out = list(lista)
    for x in lista:
        padre = PADRE.get(x)
        if padre and padre not in out:
            out.append(padre)
    return out
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

RIGA_IMMAGINE = re.compile(r'^\s*!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)\s*$')
RIGA_VIDEO = re.compile(r"^\s*(?:[-*]\s+)?\*\*Video[^*]*:\*\*")
LINK = re.compile(r"https?://[^\s)>\]]+")
APERTE = {"poetica e ricerca", "opere principali", "interviste e talk", "fonti"}


def incorpora(url):
    """Indirizzo di incorporamento per YouTube e Vimeo, altrimenti None."""
    y = re.search(r"(?:youtube\.com/(?:watch\?(?:[^\s]*&)?v=|embed/|shorts/)|youtu\.be/)([\w-]{11})", url)
    if y:
        return f"https://www.youtube-nocookie.com/embed/{y.group(1)}"
    v = re.search(r"vimeo\.com/(?:video/)?(\d+)(?:/(\w+))?", url)
    if v:
        extra = f"?h={v.group(2)}" if v.group(2) else ""
        return f"https://player.vimeo.com/video/{v.group(1)}{extra}"
    return None


def carosello(righe):
    """Raggruppa in un carosello orizzontale le immagini consecutive (2 o più)."""
    uscita, i = [], 0
    while i < len(righe):
        if not RIGA_IMMAGINE.match(righe[i]):
            uscita.append(righe[i])
            i += 1
            continue
        gruppo, j = [i], i + 1
        while j < len(righe):
            if righe[j].strip() == "":
                j += 1
            elif RIGA_IMMAGINE.match(righe[j]):
                gruppo.append(j)
                j += 1
            else:
                break
        if len(gruppo) < 2:
            uscita.append(righe[i])
            i += 1
            continue
        figure = []
        for k in gruppo:
            alt, src = RIGA_IMMAGINE.match(righe[k]).groups()
            figure.append(
                f'<figure><img loading="lazy" src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}">'
                f"<figcaption>{html.escape(alt)}</figcaption></figure>"
            )
        uscita += ["", '<div class="carosello">'] + figure + ["</div>", ""]
        i = gruppo[-1] + 1
    return uscita


def video(righe):
    """Sotto ogni riga '**Video:**' incorpora i link YouTube e Vimeo."""
    uscita = []
    for riga in righe:
        uscita.append(riga)
        if RIGA_VIDEO.match(riga):
            frame = []
            for url in LINK.findall(riga):
                src = incorpora(url)
                if src:
                    frame.append(
                        f'<iframe loading="lazy" src="{src}" title="Video" allowfullscreen '
                        'referrerpolicy="strict-origin-when-cross-origin"></iframe>'
                    )
            if frame:
                uscita += ["", '<div class="video">'] + frame + ["</div>", ""]
    return uscita


def sotto_opere(righe):
    """Ogni '#### Titolo' diventa un sotto-capitolo chiuso, con miniatura e titolo nel sommario."""
    uscita, i = [], 0
    while i < len(righe):
        if not righe[i].startswith("#### "):
            uscita.append(righe[i])
            i += 1
            continue
        titolo = righe[i][5:].strip()
        j = i + 1
        while j < len(righe) and not righe[j].startswith(("#", "<details")):
            j += 1
        corpo = righe[i + 1:j]
        mini = ""
        for k, r in enumerate(corpo):
            m = RIGA_IMMAGINE.match(r)
            if m:
                mini = f'<img class="mini" loading="lazy" src="{html.escape(m.group(2), quote=True)}" alt=""> '
                corpo = corpo[:k] + corpo[k + 1:]
                break
        uscita += ["", '<details markdown="1" class="sotto-opera">', f"<summary>{mini}{html.escape(titolo)}</summary>", ""]
        uscita += corpo
        uscita += ["", "</details>", ""]
        i = j
    return uscita


def sezioni_comprimibili(righe):
    """Avvolge ogni sezione '## ' in <details>: aperte poetica e opere, le altre chiuse."""
    uscita, aperta = [], False
    for riga in righe:
        if riga.startswith("## "):
            if aperta:
                uscita += ["", "</details>", ""]
            titolo = riga[3:].strip()
            apri = " open" if titolo.lower() in APERTE else ""
            uscita += ["", f'<details markdown="1"{apri}>', f"<summary>{html.escape(titolo)}</summary>", ""]
            aperta = True
        elif aperta and riga.strip() == "---":
            continue
        else:
            uscita.append(riga)
    if aperta:
        uscita += ["", "</details>", ""]
    return uscita


RIGA_OPERA_TAG = re.compile(r"^\*\*(Corso|Temi):\*\*\s*(.*)$")


def tag_opere(righe, titoli_usati):
    """Legge le righe **Corso:** e **Temi:** sotto ogni opera, le rende link e dà un'ancora a ogni titolo."""
    opere, i = [], 0
    in_opere = False
    while i < len(righe):
        r = righe[i]
        if r.startswith("## "):
            in_opere = r.strip().lower() == "## opere principali"
        if in_opere and r.startswith("### "):
            titolo = re.sub(r"\s*\{#[^}]*\}\s*$", "", r[4:]).strip()
            base = "opera-" + (slug_tag(titolo)[:40] or "senza-titolo")
            ancora, n = base, 2
            while ancora in titoli_usati:
                ancora, n = f"{base}-{n}", n + 1
            titoli_usati.add(ancora)
            righe[i] = f"### {titolo} {{#{ancora}}}"
            corso, temi = [], []
            j = i + 1
            while j < len(righe) and not righe[j].startswith("## ") and not righe[j].startswith("### "):
                m = RIGA_OPERA_TAG.match(righe[j])
                if m:
                    trovati = re.findall(r"`([^`]+)`", m.group(2)) or m.group(2).split()
                    (corso if m.group(1) == "Corso" else temi).extend(trovati)
                    righe[j] = f"**{m.group(1)}:** " + " ".join(
                        f"[`{x}`](tag/{slug_tag(x)}.html)" for x in trovati
                    )
                j += 1
            opere.append({"titolo": titolo, "ancora": ancora, "corso": corso, "tema": temi})
        i += 1
    return opere


titoli_usati = set()
schede = []
mostre = defaultdict(lambda: {"artisti": [], "visto_da": set()})
for f in sorted(ROOT.glob("*.md")):
    if f.stem in ESCLUSE:
        continue
    righe = f.read_text(encoding="utf-8").split("\n")
    titolo = re.match(r"# (.+)", righe[0]) if righe else None
    nome = titolo.group(1).strip() if titolo else f.stem
    tag = {"tecnica": [], "tema": [], "corso": []}
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
    opere = tag_opere(righe, set())
    righe = sezioni_comprimibili(video(carosello(sotto_opere(righe))))
    f.write_text("\n".join(righe), encoding="utf-8")
    tag["tema"] = espandi(tag["tema"])
    for o in opere:
        o["tema"] = espandi(o["tema"])
        for chiave, lista in (("corso", o["corso"]), ("tema", o["tema"])):
            for x in lista:
                if x not in tag[chiave]:
                    tag[chiave].append(x)
    schede.append({"slug": f.stem, "nome": nome, "tag": tag, "miniatura": miniatura, "opere": opere})

per_tag = {"tecnica": {}, "tema": {}, "corso": {t: [] for t in TAG_CORSO}}
for s in schede:
    for chiave in per_tag:
        for t in s["tag"][chiave]:
            per_tag[chiave].setdefault(t, []).append(s)

lavori = defaultdict(list)  # (categoria, tag) -> [(scheda, opera)]
for s in schede:
    for o in s["opere"]:
        for chiave, lista in (("corso", o["corso"]), ("tema", o["tema"])):
            for x in lista:
                lavori[(chiave, x)].append((s, o))


def scheda_card(s, prefisso=""):
    tutti = s["tag"]["corso"] + s["tag"]["tecnica"] + s["tag"]["tema"]
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


def sezione_opere(chiave, tag):
    voci = lavori.get((chiave, tag), [])
    if not voci:
        return ""
    per_artista = defaultdict(list)
    for s, o in voci:
        per_artista[(s["nome"], s["slug"])].append(o)
    righe = ["", "## Opere", ""]
    for (nome, slug), ops in sorted(per_artista.items(), key=lambda x: x[0][0].lower()):
        righe.append(f"- [{nome}](../{slug}.html)")
        for o in ops:
            righe.append(f"  - [{o['titolo']}](../{slug}.html#{o['ancora']})")
    return "\n".join(righe) + "\n"


def sezione_figli(tag):
    figli = sorted(f for f, padre in PADRE.items() if padre == tag)
    if not figli:
        return ""
    righe = ["Sotto-tag: " + " · ".join(
        f"[{f}]({slug_tag(f)}.html) ({len(per_tag['tema'].get(f, []))})" for f in figli
    ), ""]
    return "\n".join(righe) + "\n"


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

{len(elenco)} schede ({ {'tecnica': 'tecnica/formato', 'tema': 'tema', 'corso': 'corso'}[chiave] }):

{sezione_figli(t)}<div class="grid">
{card}
</div>
{sezione_opere(chiave, t)}"""
        (cartella / f"{slug_tag(t)}.md").write_text(pagina, encoding="utf-8")

indice_tag = ["---", "title: Tag", "---", "", "# Tag", "",
              "[Elenco degli artisti](../index.html) · [Vocabolario dei tag](../tags.html)", ""]
for chiave, titolo in (("corso", "Corso"), ("tecnica", "Tecnica e formato"), ("tema", "Tema")):
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

_rilievo = Path(__file__).parent / "rilievo.txt"
SLUG_RILIEVO = [
    r.strip() for r in _rilievo.read_text(encoding="utf-8").splitlines()
    if r.strip() and not r.startswith("#")
] if _rilievo.exists() else []
in_evidenza = sorted((s for s in schede if s["slug"] in SLUG_RILIEVO), key=lambda x: x["nome"].lower())
card_evidenza = "\n".join(scheda_card(s) for s in in_evidenza)
blocco_evidenza = f"""<div id="evidenza">

## In evidenza

{len(in_evidenza)} artisti dell'archivio iniziale: sono quelli da cui il database è partito, raccolti come riferimenti per i corsi prima di tutti gli altri. Le loro schede vengono riviste per prime.

<div class="grid">
{card_evidenza}
</div>

## Tutti gli artisti

</div>
""" if in_evidenza else ""
card = "\n".join(scheda_card(s) for s in sorted(schede, key=lambda x: x["nome"].lower()))
index = f"""---
title: Artist Database
---

# Artist Database

{len(schede)} schede di artisti e riferimenti critici su new media, modellazione 3D, mondi virtuali e IA applicata all'arte. Materiale didattico a cura di **Daniele Maffeis**, docente all'Accademia di Belle Arti G. Carrara – Politecnico delle Arti di Bergamo dei corsi di *Tecniche di animazione digitale* (triennio Design della Comunicazione Visiva e biennio), *Tecniche di modellazione digitale 3D* (triennio Multimedia) e *Mondi virtuali* (Audiovisivi per il web).

> **Lavoro in corso.** Le schede sono in parte compilate con l'aiuto dell'intelligenza artificiale e vanno ancora riviste: possono contenere errori, date o titoli da verificare, schede parziali. Controlla sempre le fonti linkate e segnala o correggi ciò che non torna ([come contribuire](contribuire.html)).

[Informazioni sul progetto](informazioni.html) · Per corso: [TAD-DCV](tag/tad-dcv.html), [TAD-AVM](tag/tad-avm.html), [AW](tag/aw.html), [M3D](tag/m3d.html) · [Tutti i tag](tag/index.html) · [Mostre viste](mostre.html) · [Vocabolario dei tag](tags.html) · [Come contribuire](contribuire.html)

{blocco_evidenza}
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
  var ev = document.getElementById('evidenza');
  if (ev) ev.style.display = q ? 'none' : '';
}});
</script>
"""
(ROOT / "index.md").write_text(index, encoding="utf-8")
senza = sum(1 for s in schede if not s["miniatura"])
print(f"{len(schede)} schede ({senza} senza anteprima), {sum(len(m) for m in per_tag.values())} tag, {len(mostre)} mostre")
