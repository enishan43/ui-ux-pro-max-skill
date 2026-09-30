/* ==========================================================================
   VIDEOS VON ELEKTRO HASANI
   --------------------------------------------------------------------------
   Hier tragen Sie Ihre eigenen Videos ein. Sie erscheinen automatisch im
   Bereich „Einblicke“ auf der Startseite. Solange die Liste leer ist, zeigt
   die Seite stattdessen einen Hinweis mit Link zu Instagram.

   MÖGLICHKEIT 1 – Video selbst hochladen (empfohlen, datenschutzfreundlich)
     1. Video als MP4 speichern (z. B. aus dem Handy), ideal 30–90 Sekunden.
     2. Datei in den Ordner  videos/  legen, z. B.  videos/zaehlerschrank.mp4
     3. Optional ein Vorschaubild (JPG) daneben legen: videos/zaehlerschrank.jpg
     4. Unten einen Eintrag hinzufügen:
          { titel: "Neuer Verteilerkasten in Heessen",
            datei: "videos/zaehlerschrank.mp4",
            vorschaubild: "videos/zaehlerschrank.jpg" },

   MÖGLICHKEIT 2 – YouTube-Video
     Aus dem Link https://www.youtube.com/watch?v=AbCdEf12345 ist die ID
     der Teil nach „v=“ – hier: AbCdEf12345
          { titel: "Wallbox-Installation", youtube: "AbCdEf12345" },
     Das Video wird erst nach einem Klick des Besuchers geladen
     (Zwei-Klick-Lösung). Bitte dann den YouTube-Abschnitt in der
     Datenschutzerklärung aktiv lassen.

   Hochkant gefilmt (Handy/Reel)? Zusätzlich  hochformat: true  angeben.
   Wichtig: Jeder Eintrag endet mit einem Komma, Texte stehen in "…".
   ========================================================================== */

window.HASANI_VIDEOS = [
  // { titel: "Neuer Verteilerkasten in Heessen", datei: "videos/verteiler.mp4", vorschaubild: "videos/verteiler.jpg" },
  // { titel: "Wallbox-Installation", youtube: "AbCdEf12345" },
  // { titel: "Einblick von der Baustelle", datei: "videos/baustelle.mp4", hochformat: true },
];
