
# Face Recognition and Storage System

## Projektbeschreibung

Dieses Projekt implementiert ein System zur **Echtzeit-Gesichtserkennung** und Speicherung der erkannten Gesichter in einer **SQLite-Datenbank**. Es besteht aus zwei Hauptkomponenten:

1. **Face.py**: Hauptskript zur Gesichtserkennung und Speicherung der Daten in der Datenbank.
2. **LoadImages.py**: Hilfsskript zum Abrufen und Anzeigen der gespeicherten Bilder aus der Datenbank.

## Verwendete Technologien

- **Python**: Programmiersprache
- **OpenCV**: Für Video- und Bildverarbeitung
- **Face_Recognition**: Bibliothek zur Gesichtserkennung und Fingerprint-Kodierung
- **SQLite**: Lokale Datenbank für die Speicherung von Gesichtsdaten
- **NumPy**: Verarbeitung numerischer Daten

---

## Dateien und Funktionen

### 1. **Face.py**

Das Hauptskript für die Gesichtserkennung und -speicherung.

- **Hauptfunktionen**:
  - **`init_database()`**: Erstellt die SQLite-Datenbank und die Tabelle `faces`, falls diese nicht existiert.
  - **`save_data_to_database(name, fingerprint, image)`**: Speichert den Namen, den Fingerprint und das Bild eines erkannten Gesichts in der Datenbank.
  - **`load_fingerprints_from_database()`**: Lädt Namen und Fingerprints aus der Datenbank für Vergleiche.
  - **`crop_face(frame, location)`**: Schneidet ein Gesicht basierend auf den erkannten Koordinaten aus dem Bild aus.
  - **`main()`**: Die Hauptlogik:
    - Startet die Webcam.
    - Erkennt Gesichter in Echtzeit.
    - Vergleicht neue Gesichter mit bereits gespeicherten Daten.
    - Speichert neue Gesichter in der Datenbank.

- **Ablauf von Face.py**:
  1. Die Webcam wird gestartet.
  2. Gesichter werden erkannt und deren Fingerprints berechnet.
  3. Neue Fingerprints werden mit gespeicherten Fingerprints verglichen.
  4. Bekannte Gesichter werden identifiziert; neue Gesichter erhalten eine ID und werden gespeichert.
  5. Ein Rechteck wird um erkannte Gesichter gezeichnet, und der Name wird angezeigt.

- **Verwendung**:
  ```bash
  python face.py
  ```
  - Drücke `q`, um das Programm zu beenden.

---

### 2. **LoadImages.py**

Ein Hilfsskript, um die gespeicherten Bilder aus der Datenbank anzuzeigen.

- **Hauptfunktionen**:
  - **`load_images_from_database(database_path, table_name="faces")`**:
    - Lädt alle Bilder aus der Tabelle `faces` der SQLite-Datenbank.
    - Zeigt jedes Bild mit der zugehörigen ID und dem Namen an.
    - Ermöglicht das Speichern eines Bildes als JPEG-Datei, wenn die Taste `s` gedrückt wird.

- **Ablauf von LoadImages.py**:
  1. Stellt eine Verbindung zur SQLite-Datenbank her.
  2. Ruft alle gespeicherten Bilder (BLOB-Format) ab.
  3. Wandelt die Bilder in ein OpenCV-Format um und zeigt sie an.
  4. Gibt die Möglichkeit, die Bilder lokal zu speichern.

- **Verwendung**:
  ```bash
  python loadImages.py
  ```
  - Drücke eine Taste, um zum nächsten Bild zu wechseln.
  - Drücke `s`, um das aktuelle Bild zu speichern.

---

## Datenbankstruktur

- **Datenbankname**: `faces.db`
- **Tabelle**: `faces`
- **Spalten**:
  - `id`: Automatisch inkrementierende ID
  - `timestamp`: Zeitstempel der Speicherung
  - `name`: Name der Person
  - `fingerprint`: Gesichtsfingerprint (numerische Merkmale)
  - `image`: Gesichtsausschnitt als JPEG-Bild

---

## Installation und Einrichtung

1. **Abhängigkeiten installieren**:
   - Python-Version: 3.6 oder höher
   - Installiere die erforderlichen Bibliotheken:
     ```bash
     pip install opencv-python face-recognition numpy
     ```

2. **Code ausführen**:
   - Gesichtserkennung und Speicherung:
     ```bash
     python face.py
     ```
   - Bilder aus der Datenbank laden:
     ```bash
     python loadImages.py
     ```

---

## Verwendung

### Face.py
- Startet die Webcam, erkennt Gesichter und speichert sie in der Datenbank.
- Neue Gesichter werden automatisch erkannt und gespeichert.
- Drücke `q`, um das Programm zu beenden.

### LoadImages.py
- Zeigt alle gespeicherten Gesichter aus der Datenbank.
- Drücke `s`, um ein Bild lokal zu speichern.
- Drücke eine beliebige Taste, um zum nächsten Bild zu wechseln.

---

## Projektstruktur

```
├── face.py           # Hauptskript zur Gesichtserkennung und Speicherung
├── loadImages.py     # Skript zur Anzeige und Speicherung der Bilder aus der Datenbank
├── faces.db          # SQLite-Datenbank (wird automatisch erstellt)
└── README.md         # Dokumentation
```

---

## Hinweise

- Die Gesichtserkennung basiert auf der Bibliothek `face_recognition`, die ein vortrainiertes Modell verwendet.
- **Toleranzwert**: Der Standardwert `tolerance=0.6` wird verwendet, um die Genauigkeit der Gesichtserkennung zu bestimmen.
- **Speicherung**: Nur alle 5 Frames werden verarbeitet und gespeichert, um die Leistung zu optimieren.

---

## Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**. Sie können den Code frei verwenden, ändern und verteilen.
