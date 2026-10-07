# E.C Webdesigns

## Instagram (`instagram/`)
- `EC-Webdesigns-Profilbild.png`: Profilbild (1080 × 1080, Instagram schneidet es rund zu)
- `EC-Webdesigns-1` bis `-5`: Beiträge im Hochformat 4:5 (1080 × 1350). In umgekehrter
  Reihenfolge posten (erst 5, zuletzt 1), dann steht die Vorstellung oben links im Profil.
- Neu erzeugen: Texte in `instagram/src/posts.html` ändern, dann die PNGs per Screenshot
  der einzelnen `<section>`-Elemente rendern (1080 px breit).

## Website-Vorlage (`vorlage/`)
Allgemeine Vorlage für Handwerksbetriebe, Beispiel: Tischlerei Brandt (fiktiv).
- Farben: oben im `<style>` unter `:root` (`--accent`, `--warm` …)
- Texte, Leistungen, Ablauf, Bewertungen, Kontaktdaten: im `CONFIG`-Block am Ende der Datei
- Schriften liegen lokal in `fonts/` (keine Verbindung zu Google, DSGVO-freundlich)
- Bewertungen sind als „Beispielbewertung“ markiert und werden für echte Kunden durch
  deren echte Bewertungen ersetzt. Die Hinweisleiste oben vor dem Livegang entfernen.
