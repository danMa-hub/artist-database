# Contenuti

Qui raccogliamo, in Markdown, le informazioni sugli artisti man mano che le troviamo.

## Ambito del progetto

Il database copre **artisti visivi di arte contemporanea** che lavorano con:

- new media
- modellazione ed esecuzione 3D
- mondi virtuali
- intelligenza artificiale applicata all'arte

Non è un database di design, CG "tecnica" o tutorial: gli artisti trattati lavorano anche a un livello **concettuale e critico** (es. Ian Cheng, Lawrence Lek, Jon Rafman, Forensic Architecture, Hito Steyerl...).

Il riferimento per il linguaggio e il taglio critico da usare nelle schede sono i [programmi dei corsi](../programmi/): le schede non sono biografie neutre, ma vanno scritte nello stesso registro (storia della computer grafica, sorveglianza, economia dell'attenzione, posizionamento critico rispetto all'AI, ecc.).

## Indice

L'elenco completo di tutti gli artisti, con lo stato di avanzamento di ciascuna scheda, è in [`00-lista-artisti.md`](00-lista-artisti.md).

## Tag

Ogni scheda va taggata per permettere una navigazione per aree di interesse (utile in vista della pubblicazione online per gli studenti). Vocabolario e regole d'uso in [`tags.md`](tags.md) — lista viva, si possono proporre nuovi tag quando emergono nuclei tematici o tipologie di opere non ancora coperte.

## Struttura

- Un file `.md` per artista (es. `contenuti/nome-artista.md`)
- Le immagini vanno in `contenuti/immagini/`, richiamate nei file `.md` con link relativi:
  ```md
  ![Descrizione](immagini/nome-file.jpg)
  ```

## Template scheda artista

Ogni scheda ha due parti:

1. **Intestazione**: materiale organizzato, curato, pronto per essere mostrato agli studenti.
2. **Appunti**: materiale grezzo/non ancora organizzato, raccolto man mano (link, frammenti, cose da verificare). Si sposta nell'intestazione quando viene rifinito.

```md
# Nome Artista

**Tag tecnica/formato:** `tag1` `tag2`
**Tag tema:** `tag3` `tag4`

## Biografia
Anno di nascita, paese/città di provenienza (e dove opera, se diverso) — le informazioni di base per contestualizzare il lavoro. Può restare breve o approfondirsi quando la biografia è centrale per la poetica dell'artista. Se rilevanti e reperibili, menzionare le mostre/istituzioni più importanti della carriera (non un CV completo: solo ciò che aiuta a capire la rilevanza dell'artista).

## Poetica e ricerca
Descrizione — breve o approfondita a seconda dei casi — della ricerca dell'artista: in cosa consiste, quali sono i temi centrali, quali medium usa. Va scritta con linguaggio critico-teorico, agganciato alla storia dell'arte e alla fenomenologia delle arti contemporanee (lo stesso registro dei [programmi dei corsi](../programmi/)) — non una biografia neutra. Il testo può essere teorico, ma deve sempre fare riferimento a opere concrete: mostrare come i concetti si sono effettivamente declinati nella pratica.

## Opere principali

### Titolo opera (anno)
**Descrizione:** cosa si vede concretamente — tecnica, media, eventualmente il processo/approccio di lavoro.
**Lettura critica:** come l'opera si collega ai temi della poetica dell'artista.

(ripetere per ogni opera rilevante)

## Immagini
![Descrizione](immagini/nome-file.jpg)

## Fonti
- [Sito ufficiale dell'artista](https://...) — sempre la prima fonte, quando esiste
- [Portfolio](portfolio/nome-artista-portfolio.pdf) — se esiste un PDF, va scaricato e archiviato nel repo (vedi sotto), non solo linkato
- [Titolo fonte](https://...)

---

## Appunti da organizzare
(materiale grezzo raccolto ma non ancora sistemato sopra)
- ...
```

Nessuna regola rigida oltre a questa: l'importante è iniziare a raccogliere il materiale in modo ordinato, distinguendo sempre ciò che è rifinito da ciò che è ancora grezzo.

## Regola fondamentale: niente contenuto senza fonte

Ogni scheda deve poter essere ricondotta a qualcosa di verificabile — mai inventare o "arrotondare" informazioni. In pratica:

- **Sito ufficiale dell'artista**: prima fonte da cercare e linkare, quando esiste.
- **Portfolio PDF**: se l'artista ha un portfolio scaricabile (es. trovato su Drive o online), va **scaricato e archiviato in `contenuti/portfolio/`** — non solo linkato — perché i link esterni possono sparire nel tempo. File nominato `nome-artista-portfolio.pdf`.
- **Articoli, interviste, testi critici**: linkare sempre la fonte specifica usata, non un generico "si dice che...".
- **Materiale da mostre** (foto di pannelli/etichette): la fonte è la foto stessa — indicare da quale mostra/data proviene.
- Se un testo pre-esistente (es. da Drive) ha un'origine incerta o sembra generato da un'AI precedente senza controllo su fonti primarie, va segnalato esplicitamente come non verificato (vedi schede già migrate per un esempio), non ripulito silenziosamente.
