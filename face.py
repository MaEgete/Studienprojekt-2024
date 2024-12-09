import cv2  # OpenCV für Video- und Bildverarbeitung
import face_recognition  # Gesichtserkennung und -kodierung
import sqlite3  # SQLite für die lokale Datenbank
import numpy as np  # Verarbeitung numerischer Daten, wie Gesichtsfingerprints
from datetime import datetime  # Zeitstempel für Datenbankeinträge


# Initialisiert die SQLite-Datenbank, falls sie noch nicht existiert
def init_database():
    # Verbindung zur SQLite-Datenbank herstellen (oder erstellen, falls nicht vorhanden)
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()

    # SQL-Befehl, um die Tabelle 'faces' zu erstellen, falls sie nicht existiert
    c.execute('''CREATE TABLE IF NOT EXISTS faces (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Automatisch inkrementierende ID
                     timestamp TEXT,  -- Zeitstempel für die Speicherung
                     name TEXT,  -- Name der Person
                     fingerprint BLOB,  -- Gesichtsfingerprint (numerische Merkmale)
                     image BLOB  -- Gesichtsausschnitt als Bild (JPEG)
                 )''')
    conn.commit()  # Änderungen speichern
    conn.close()  # Verbindung zur Datenbank schließen


# Speichert Gesichtsdaten (Name, Fingerprint, Bild) in der Datenbank
def save_data_to_database(name, fingerprint, image):
    conn = sqlite3.connect('faces.db')  # Verbindung zur Datenbank herstellen
    c = conn.cursor()

    # Bild in das JPEG-Format kodieren, um es als Blob zu speichern
    _, encoded_image = cv2.imencode('.jpg', image)

    # Fingerprint in ein BLOB-Format konvertieren
    fingerprint_blob = sqlite3.Binary(fingerprint.tobytes())

    # SQL-Befehl, um die Gesichtsdaten in die Tabelle einzufügen
    c.execute('INSERT INTO faces (timestamp, name, fingerprint, image) VALUES (?, ?, ?, ?)',
              (datetime.now().isoformat(), name, fingerprint_blob, sqlite3.Binary(encoded_image.tobytes())))
    conn.commit()  # Änderungen speichern
    conn.close()  # Verbindung zur Datenbank schließen

    # Rückmeldung im Terminal
    print(f"Bild, Name und Fingerprint erfolgreich gespeichert: {name}")


# Lädt alle gespeicherten Fingerprints und Namen aus der Datenbank
def load_fingerprints_from_database():
    conn = sqlite3.connect("faces.db")  # Verbindung zur Datenbank herstellen
    c = conn.cursor()

    # SQL-Abfrage, um alle Namen und Fingerprints aus der Tabelle zu laden
    c.execute('SELECT name, fingerprint FROM faces')
    rows = c.fetchall()  # Alle Zeilen abrufen
    conn.close()  # Verbindung schließen

    # Namen und Fingerprints getrennt extrahieren
    known_names = [row[0] for row in rows]  # Namen
    known_fingerprints = [np.frombuffer(row[1], dtype=np.float64) for row in rows]  # Fingerprints
    return known_names, known_fingerprints


# Schneidet ein Gesicht aus einem Frame basierend auf den übergebenen Koordinaten
def crop_face(frame, location):
    top, right, bottom, left = location  # Gesichtslage: oben, rechts, unten, links
    return frame[top:bottom, left:right]  # Ausschnitt aus dem Bild zurückgeben


# Hauptfunktion des Programms
def main():
    # Datenbank initialisieren
    init_database()

    # Zugriff auf die Webcam starten
    video_capture = cv2.VideoCapture(0)

    # Bereits gespeicherte Namen und Fingerprints aus der Datenbank laden
    known_names, known_fingerprints = load_fingerprints_from_database()

    # Zähler für neue Personen (basierend auf der aktuellen Anzahl von Namen)
    next_local_id = len(known_names) + 1

    # Konfiguration: Nur alle 5 Frames speichern (Optimierung)
    frame_skip = 5
    frame_count = 0

    while True:
        # Ein Frame von der Webcam lesen
        ret, frame = video_capture.read()
        if not ret:
            print("Kein Frame empfangen. Beende Aufnahme.")
            break  # Wenn kein Frame gelesen wird, Aufnahme beenden

        # Konvertiere den Frame in das RGB-Format (für face_recognition erforderlich)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Erkennung von Gesichtern und deren Positionen im Frame
        face_locations = face_recognition.face_locations(rgb_frame)

        # Kodierung der Gesichter (Fingerprints) basierend auf den erkannten Positionen
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # **Nur alle 5 Frames speichern (Frame-Skip-Logik)**
        if frame_count % frame_skip == 0:
            print(f"Speichere Gesichter aus Frame {frame_count}")
            if len(face_locations) > 0:  # Nur speichern, wenn Gesichter erkannt wurden
                for location, encoding in zip(face_locations, face_encodings):
                    # Vergleiche den Fingerprint mit gespeicherten Fingerprints
                    matches = face_recognition.compare_faces(known_fingerprints, encoding, tolerance=0.6)
                    name = "Unbekannt"  # Standard: Unbekannt

                    if True in matches:
                        # Match gefunden: Hole den entsprechenden Namen
                        match_index = matches.index(True)
                        name = known_names[match_index]
                        print(f"Bekannte Person erkannt: {name}")
                    else:
                        # Neue Person erkannt: Weisen Sie eine neue ID zu
                        name = f"PersonId{next_local_id}"
                        next_local_id += 1  # Zähler erhöhen
                        known_names.append(name)  # Namen hinzufügen
                        known_fingerprints.append(encoding)  # Fingerprint hinzufügen
                        print(f"Neue Person erkannt: {name}")

                    # Schneide das Gesicht aus dem Frame aus und speichere es in der Datenbank
                    face_image = crop_face(frame, location)
                    save_data_to_database(name, encoding, face_image)

        # **Anzeige der Erkennung in jedem Frame**
        for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
            # Vergleiche Fingerprint mit bekannten Fingerprints
            matches = face_recognition.compare_faces(known_fingerprints, encoding, tolerance=0.6)
            name = "Unbekannt"  # Standard: Unbekannt

            if True in matches:
                # Match gefunden: Bestimme den Namen
                match_index = matches.index(True)
                name = known_names[match_index]
            else:
                # Keine Übereinstimmung: Weisen Sie eine temporäre ID zu
                name = f"PersonId{next_local_id}"

                # Zeichne ein Rechteck und den Namen um das erkannte Gesicht
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        # Zeige das Video im Fenster an
        cv2.imshow('Video', frame)
        frame_count += 1  # Frame-Zähler erhöhen

        # Brich die Schleife ab, wenn die Taste 'q' gedrückt wird
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break

    # Webcam und Fenster freigeben und schließen
    video_capture.release()
    cv2.destroyAllWindows()


# Startpunkt des Programms
if __name__ == "__main__":
    main()
