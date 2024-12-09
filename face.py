import cv2
import face_recognition
import sqlite3
import numpy as np
from datetime import datetime

# Initialisiert die SQLite-Datenbank
def init_database():
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS faces (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     timestamp TEXT,
                     name TEXT,
                     fingerprint BLOB,
                     image BLOB
                 )''')
    conn.commit()
    conn.close()

# Speichert Gesichtsdaten in der Datenbank
def save_data_to_database(name, fingerprint, image):
    conn = sqlite3.connect('faces.db')
    c = conn.cursor()
    _, encoded_image = cv2.imencode('.jpg', image)
    fingerprint_blob = sqlite3.Binary(fingerprint.tobytes())
    c.execute('INSERT INTO faces (timestamp, name, fingerprint, image) VALUES (?, ?, ?, ?)',
              (datetime.now().isoformat(), name, fingerprint_blob, sqlite3.Binary(encoded_image.tobytes())))
    conn.commit()
    conn.close()
    print(f"Bild, Name und Fingerprint erfolgreich gespeichert: {name}")

# Lädt Fingerprints und Namen aus der Datenbank
def load_fingerprints_from_database():
    conn = sqlite3.connect("faces.db")
    c = conn.cursor()
    c.execute('SELECT name, fingerprint FROM faces')
    rows = c.fetchall()
    conn.close()
    known_names = [row[0] for row in rows]
    known_fingerprints = [np.frombuffer(row[1], dtype=np.float64) for row in rows]
    return known_names, known_fingerprints

# Schneidet Gesichter aus dem Frame aus
def crop_face(frame, location):
    top, right, bottom, left = location
    return frame[top:bottom, left:right]

# Hauptfunktion
def main():
    init_database()
    video_capture = cv2.VideoCapture(0)
    known_names, known_fingerprints = load_fingerprints_from_database()
    frame_skip = 5  # Alle 5 Frames wird gespeichert
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Kein Frame empfangen. Beende Aufnahme.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Alle 5 Frames speichern
        if frame_count % frame_skip == 0 and len(face_locations) > 0:
            for location, encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_fingerprints, encoding, tolerance=0.6)
                name = "Unbekannt"

                if True in matches:
                    match_index = matches.index(True)
                    name = known_names[match_index]
                    print(f"Bekannte Person erkannt: {name}")
                else:
                    # Neue Person
                    name = f"PersonId{len(known_names) + 1}"
                    known_names.append(name)
                    known_fingerprints.append(encoding)
                    print(f"Neue Person erkannt: {name}")

                # Gesichtsausschnitt speichern
                face_image = crop_face(frame, location)
                save_data_to_database(name, encoding, face_image)

        # Anzeigen der Erkennung
        for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_fingerprints, encoding, tolerance=0.6)
            name = "Unbekannt"
            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]
            else:
                name = f"PersonId{len(known_names) + 1}"

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow('Video', frame)
        frame_count += 1

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()