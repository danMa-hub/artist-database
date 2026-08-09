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

## Bio breve
(2-4 righe: chi è, ambito, perché è rilevante)

## Ambito / media
(es. simulazione 3D, mondi virtuali, AI generativa, video...)

## Opere principali
- ...

## Immagini
![Descrizione](immagini/nome-file.jpg)

## Fonti
- [Titolo fonte](https://...)

---

## Appunti da organizzare
(materiale grezzo raccolto ma non ancora sistemato sopra)
- ...
```

Nessuna regola rigida oltre a questa: l'importante è iniziare a raccogliere il materiale in modo ordinato, distinguendo sempre ciò che è rifinito da ciò che è ancora grezzo.
