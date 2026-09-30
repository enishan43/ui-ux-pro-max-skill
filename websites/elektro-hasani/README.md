# Website Elektro Hasani (Hamm-Heessen)

One-Pager für den Elektrobetrieb Elektro Hasani, Münsterstraße 41, 59065 Hamm.
Reines HTML/CSS/JS. Kein Framework, keine Cookies, kein Tracking, keine externen
Schriften oder Karten. Die Seite lädt schnell und kommt ohne Cookie-Banner aus.

**Slogan:** *Leben braucht Leitung.*
Das Wortspiel meint zweierlei: die Stromleitung in der Wand und die Führung durch
einen Fachbetrieb. Die Hero-Grafik zeigt Häuser aus der Vogelperspektive bei Nacht.
Strom fließt durch die Straßen, dann gehen nacheinander die Lichter an. Die Botschaft:
Ohne den Elektriker fehlt der Grundstein unseres Alltags.

## Öffnen

`index.html` im Browser öffnen, oder den ganzen Ordner auf einen Webspace hochladen.

Zum schnellen Ansehen gibt es außerdem **`elektro-hasani-komplett.html`**: eine einzige
Datei mit allem drin (CSS, JavaScript; Impressum und Datenschutz öffnen sich als Pop-up
über die Links im Footer). Per Doppelklick öffnen,
keine weiteren Dateien nötig. Neu erzeugen mit `python3 src/build_preview.py`.

## Aufbau (orientiert an erfolgreichen Elektriker-Websites)

1. Topbar mit Öffnungszeiten, Adresse und Notfallnummer
2. Header mit festem Telefon-Button
3. Hero: Slogan, Nutzenversprechen, zwei Buttons (Anruf / Anfrage), Google-Bewertung
4. Vertrauensleiste (Fachkräfte, transparente Preise, Pünktlichkeit, Sauberkeit)
5. „Stellen Sie sich einen Tag ohne Strom vor“ (Grundstein-Botschaft)
6. Leistungen (11 Leistungen, jede mit Anfrage-Link, der das Formular vorbelegt)
7. Warum wir, dann der Ablauf in 4 Schritten
8. Kundenstimmen (5,0 bei Google, 31 Bewertungen)
9. Einblicke / Videos (vom Betrieb selbst befüllbar, siehe unten)
10. Einsatzgebiet (Hammer Stadtbezirke), dann FAQ
11. Kontakt mit Live-Status „geöffnet/geschlossen“ und Anfrageformular
12. Auf dem Handy: feste Leiste unten mit „Anrufen“ und „Anfrage“

## Eigene Videos einfügen

Anleitung steht direkt in `videos.js`. Kurzfassung:

1. MP4-Datei in den Ordner `videos/` legen (optional mit JPG-Vorschaubild).
2. In `videos.js` eine Zeile ergänzen:
   `{ titel: "Neuer Verteilerkasten", datei: "videos/verteiler.mp4", vorschaubild: "videos/verteiler.jpg" },`
3. YouTube geht auch: `{ titel: "Wallbox", youtube: "VIDEO-ID" },`. Das Video lädt
   erst nach einem Klick des Besuchers (Zwei-Klick-Lösung, DSGVO).

Solange keine Videos eingetragen sind, zeigt die Seite einen Hinweis mit Link zu
Instagram (@elektrohasani).

## Vor dem Veröffentlichen prüfen

Die Inhalte stammen aus öffentlichen Einträgen (ElektrikerPortal, Google,
Branchenverzeichnisse, Instagram). Der Betrieb hat sie nicht bestätigt. Vor dem
Livegang bitte klären:

- [ ] **Impressum** (`impressum.html`): vertretungsberechtigte Gesellschafter,
      USt-ID, Berufsbezeichnung, Handwerkskammer, Handwerksrolle und
      Berufshaftpflicht ergänzen. Alle Stellen in `[ … ]` ersetzen.
- [ ] **Datenschutz** (`datenschutz.html`): Hosting-Anbieter und Stand eintragen,
      am besten rechtlich prüfen lassen.
- [ ] **Notdienst:** Die Seite nennt die Mobilnummer 0172 5432820 für Störungen und
      Notfälle, verspricht aber bewusst **keinen 24-h-Notdienst**. Nur ergänzen,
      wenn der Betrieb das sicher anbietet.
- [ ] **Meisterbetrieb / Netzbetreiber-Eintrag:** Laut Instagram ist es ein
      Meisterbetrieb, laut Recherche ist der Betrieb im Installateurverzeichnis der
      EWV Hamm Netz eingetragen. Beides ist ein starkes Verkaufsargument. Es steht
      noch nicht auf der Seite, weil es nicht bestätigt ist. Nach Bestätigung in die
      Vertrauensleiste aufnehmen.
- [ ] **Photovoltaik:** Nur Beratung oder auch Installation? Der Text sagt derzeit
      „Beratung und Installation“.
- [ ] **Bewertungen:** Die Zahl (31 bei Google) regelmäßig aktualisieren.
- [ ] **Echte Fotos:** Team- und Baustellenfotos erhöhen das Vertrauen deutlich.
- [ ] **Domain:** gleiche Firmendaten (Name, Adresse, Telefon) überall verwenden,
      also Website, Google-Unternehmensprofil und Verzeichnisse. Das hilft bei Google.

## Grafik und Seite neu bauen

Den Inhalt nicht direkt in `index.html` bearbeiten, sondern in `src/index.template.html`.
Danach:

```bash
python3 src/build.py           # erzeugt Hero-Grafik + index.html
python3 src/build_preview.py   # erzeugt die Einzeldatei elektro-hasani-komplett.html
```

Hintergrund-Recherche: [`docs/recherche.md`](docs/recherche.md)
