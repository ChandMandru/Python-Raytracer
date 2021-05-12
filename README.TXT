Benutzungsanleitung zum Raytracer von Chand Mandru Matrikelnummer 1006182

Zeile 247 / 248

Zeile 247 ohne kommentar Rendert das Squirrel 
Zeile 248 ohne kommentar Rendert die Szene mit den 3 Spheren dem Dreieick und der Plane

Zeile 270 - 273

270 - Processing für die Standart Szene 3 Spheren dem Dreieick und der Plane
271 - Processing für das Squirrel 

272 - Threading für die Standart Szene 3 Spheren dem Dreieick und der Plane
273 - Threading für das Squirrel

Der Ordner Results enhält eine beispielmenge an gerenderten Bildern die von diesem Raytracer Produziert wurden

Zeile 14 - 32 Sind User Settings für das Programm
Der Reihe nach von oben nach unten : 

Bild Breite und Höhe Hintergrundfarbe
FOV
Shiny jedoch funktionsunfähig da es bei Dreiecken zu bugs führt
ein allgemeiner Reflektionswert (je höher desto stärker die Reflektionen)
Maxlevel für die Rekursionstiefe also die angabe an Ray Bounces

Ein Licht Objekt mit Position und Farbe

3 Material Objekte die zum Erstellen der WorldObjects benötigt werden so
aufgebaut nach (shadowAmbient noShadowAmbient diffuse specular)
aufteilung in 2 Ambient varianten für 1 mal im Schatten 1 Mal ausserhalb des Schattens

Kamera einstellungen für (e, c , up , FOV)
und Kamera Initialisierung


Threading und Processing funktioneren nicht wie erwartet : 
Laut Theorie und Testing anhand anderer beispiele stellt sich raus das Threading hier keinen Performance Boost bietet da die Arbeitslast nicht wirklich auf mehrere Kerne Parrallel aufgeteilt wird.
sondern nur abwechselnd die Arbeitsschritte ausgeführt werden jedoch auf dem Selben Kern.

Processing wiederrum führt zu einem Performance Boost da die Arbeitslast Parrallel auf mehrere Kerne aufgeteilt wird und gleichzeitig ausgeführt wird.

Fazit : Threading scheint für I/O prozesse besser gedacht zu sein als für Parrallelisierung von Arbeitslast dahingegen tut Processing genau dies wie oben bereits beschrieben.