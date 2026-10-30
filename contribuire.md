# Come contribuire

Qui raccogliamo, in Markdown, le informazioni sugli artisti man mano che le troviamo. Chiunque può proporre correzioni o nuove schede con una *pull request* (vedi [Informazioni](README.html)).

## Ambito del progetto

Il database copre **artisti visivi di arte contemporanea** che lavorano con:

- new media
- modellazione ed esecuzione 3D
- mondi virtuali
- intelligenza artificiale applicata all'arte

Non è un database di design, CG "tecnica" o tutorial: gli artisti trattati lavorano anche a un livello **concettuale e critico** (es. Ian Cheng, Lawrence Lek, Jon Rafman, Forensic Architecture, Hito Steyerl...).

Il riferimento per il linguaggio e il taglio critico da usare nelle schede sono i programmi dei corsi di Daniele Maffeis: le schede non sono biografie neutre, ma vanno scritte nello stesso registro (storia della computer grafica, sorveglianza, economia dell'attenzione, posizionamento critico rispetto all'AI, ecc.).

## Indice

L'elenco completo di tutti gli artisti, con lo stato di avanzamento di ciascuna scheda, è in [`00-lista-artisti.md`](00-lista-artisti.md).

## Tag

Ogni scheda va taggata per permettere una navigazione per aree di interesse (utile in vista della pubblicazione online per gli studenti). Vocabolario e regole d'uso in [`tags.md`](tags.md) — lista viva, si possono proporre nuovi tag quando emergono nuclei tematici o tipologie di opere non ancora coperte.

## Struttura

- Un file `.md` per artista (es. `nome-artista.md`)
- Le immagini vanno in `immagini/`, richiamate nei file `.md` con link relativi:
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
Descrizione — breve o approfondita a seconda dei casi — della ricerca dell'artista: in cosa consiste, quali sono i temi centrali, quali medium usa. Va scritta con linguaggio critico-teorico, agganciato alla storia dell'arte e alla fenomenologia delle arti contemporanee (lo stesso registro dei programmi dei corsi) — non una biografia neutra. Il testo può essere teorico, ma deve sempre fare riferimento a opere concrete: mostrare come i concetti si sono effettivamente declinati nella pratica.

## Opere principali

### Titolo opera (anno)
**Descrizione:** cosa si vede concretamente — tecnica, media, eventualmente il processo/approccio di lavoro.
**Lettura critica:** come l'opera si collega ai temi della poetica dell'artista.

(ripetere per ogni opera rilevante)

## Immagini
![Descrizione](immagini/nome-file.jpg)

## Mostre viste
(opzionale: mostre in cui l'artista è stato visto di persona o incontrato per la prima volta)
- *Titolo della mostra*, luogo (anno) — visto da @tuo-utente-github

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
- **Portfolio PDF**: se l'artista ha un portfolio scaricabile (es. trovato su Drive o online), va **scaricato e archiviato in `portfolio/`** — non solo linkato — perché i link esterni possono sparire nel tempo. File nominato `nome-artista-portfolio.pdf`.
- **Articoli, interviste, testi critici**: linkare sempre la fonte specifica usata, non un generico "si dice che...".
- **Materiale da mostre** (foto di pannelli/etichette): la fonte è la foto stessa — indicare da quale mostra/data proviene, e aggiungere la mostra a «Mostre viste» (vedi sotto).
- Se un testo pre-esistente (es. da Drive) ha un'origine incerta o sembra generato da un'AI precedente senza controllo su fonti primarie, va segnalato esplicitamente come non verificato (vedi schede già migrate per un esempio), non ripulito silenziosamente.
- **Collegamenti teorici/filosofici** (es. "l'opera di X richiama Heidegger/Foucault/Kant..."): va sempre citata la fonte che ha fatto quel collegamento — un'intervista, un saggio critico, una dichiarazione dell'artista. Il linguaggio tecnico/filosofico va benissimo nella parte "Poetica e ricerca" (è il registro dei programmi dei corsi), ma **non deve essere un'elaborazione teorica generata dall'AI senza aggancio a una fonte reale**: il rischio è che la connessione risulti suggestiva ma infondata. Se non si trova la fonte del collegamento, va tolto o segnalato esplicitamente come non verificato — mai lasciato come se fosse un fatto critico consolidato.

## Regola fondamentale: verifica sostanziale, non opportunistica

Ogni scheda va sottoposta a un controllo puntuale di **tutte** le affermazioni fattuali (titoli, anni, medium, dove/come un'opera è stata esposta, cosa mostra concretamente) tramite ricerca diretta — non solo quando capita di trovare un'immagine o un dettaglio che insospettisce. Il caso di Meriem Bennani (*Windy* descritta come "un video con un personaggio animato", quando è in realtà una scultura cinetica sulla High Line) è l'esempio di un errore che sarebbe potuto restare invisibile per sempre senza un controllo esplicito. Quindi:

- Ogni opera elencata in una scheda va verificata con almeno una ricerca dedicata, non solo trascritta dalla fonte Drive originale.
- Le schede migrate più rapidamente (primi batch, senza verifica approfondita) vanno riprese e sottoposte allo stesso controllo, non solo le nuove.
- Non aspettare un'occasione (un'immagine, un dubbio) per verificare: la verifica è il passo di default, non l'eccezione.

## Regola: referenze video e interviste per ogni scheda

Oltre alle immagini, ogni scheda dovrebbe raccogliere link a **video delle opere** (idealmente opere complete, in alternativa ampi estratti) e a **interviste/contenuti con informazioni significative sull'artista** — materiale pensato per essere mostrato direttamente in classe agli studenti, non solo letto. In pratica:

- Cercare per ogni opera principale il video integrale (canale ufficiale dell'artista, Vimeo, museo, galleria) prima di accontentarsi di un trailer o di un estratto breve.
- I link vanno verificati (aprire/controllare che siano quelli giusti, non indovinati) e da fonti affidabili — stessa regola del sourcing generale.
- Le interviste vanno preferite quando aggiungono informazioni sostanziali sulla poetica dell'artista (non semplici promo).
- Se non si trova un video completo affidabile, va bene un estratto ampio, segnalato come tale — meglio di niente ma da migliorare quando possibile.

## Mostre viste

Ogni scheda può avere una sezione `## Mostre viste`, con una voce per mostra nel formato:

```md
- *Titolo della mostra*, luogo (anno) — visto da @nome-utente-github
```

Il «visto da» è facoltativo; se manca, la mostra compare comunque. Tutte le mostre di tutte le schede sono raccolte nella pagina [Mostre viste](mostre.html).

## Immagine di anteprima

Nell'elenco degli artisti ogni scheda è mostrata con un'immagine. Per impostazione predefinita è la prima immagine della sezione «Opere principali». Per sceglierne un'altra, aggiungere sotto i tag una riga:

```md
**Immagine anteprima:** immagini/nome-file.jpg
```

## Immagini, carosello e video

- **Da 3 a 4 immagini per ogni opera**, quando si trovano. Si mettono una dopo l'altra sotto l'opera, ognuna con la sua didascalia nel testo alternativo: `![didascalia](immagini/nome-file.jpg)`. Da due immagini consecutive in su il sito le mostra in un **carosello a scorrimento orizzontale**; una sola immagine resta fissa.
- **Video**: una riga `**Video:** [titolo](https://www.youtube.com/watch?v=...)` sotto l'opera. Se il link è di YouTube o di Vimeo il sito incorpora il video direttamente nella pagina, sotto la riga.
- Nelle schede ogni sezione si apre e si chiude: sono aperte per impostazione predefinita *Poetica e ricerca* e *Opere principali*, le altre (Biografia, Immagini, Mostre viste, Fonti, Appunti da organizzare) sono chiuse. Nella biografia vanno solo i dati biografici; la poetica e lo statement vanno in *Poetica e ricerca*.

## Tag

Per ora i tag sono solo sugli artisti. In futuro potranno essere aggiunti anche alle singole opere, per collegare opere che parlano degli stessi temi.
