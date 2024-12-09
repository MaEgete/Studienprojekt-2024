import sqlite3  # Für die Verbindung mit SQLite-Datenbanken
import cv2  # OpenCV für Bildverarbeitung
import numpy as np  # Verarbeitung numerischer Daten, wie Bilder in Arrays

def load_images_from_database(database_path, table_name="faces"):
    """
    Lädt alle Bilder aus einer SQLite-Datenbank und zeigt sie an.

    :param database_path: Der Pfad zur SQLite-Datenbankdatei.
    :param table_name: Der Name der Tabelle, aus der die Bilder geladen werden.
    """
    try:
        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # SQL-Abfrage, um ID, Name und Bilddaten (BLOB) aus der Tabelle zu laden
        query = f"SELECT id, name, image FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()  # Alle Ergebnisse der Abfrage abrufen

        # Überprüfen, ob überhaupt Bilder in der Tabelle vorhanden sind
        if not rows:
            print("Keine Bilder in der Datenbank gefunden.")
            return

        # Verarbeitung der abgerufenen Bilder
        for row in rows:
            image_id, name, image_blob = row  # Jede Zeile enthält ID, Name und Bild-BLOB

            # Konvertiert das Bild-BLOB in ein NumPy-Array
            image_array = np.frombuffer(image_blob, dtype=np.uint8)

            # Dekodiert das NumPy-Array in ein Bild (OpenCV-Format)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Zeigt das Bild in einem Fenster an
            cv2.imshow(f"ID: {image_id} / {len(rows)}, Name: {name}", image)

            # Wartet auf Benutzereingabe (Taste drücken, um zum nächsten Bild zu gehen)
            key = cv2.waitKey(0)

            # Wenn die Taste 's' gedrückt wird, speichert das Programm das Bild als Datei
            if key == ord('s'):
                filename = f"{name}_ID_{image_id}.jpg"  # Dateiname basierend auf Name und ID
                cv2.imwrite(filename, image)  # Speichert das Bild im aktuellen Verzeichnis
                print(f"Bild gespeichert als: {filename}")

        # Alle Fenster schließen, wenn der Benutzer fertig ist
        cv2.destroyAllWindows()

    except sqlite3.Error as e:
        # Fehlerbehandlung bei Datenbankfehlern
        print(f"Datenbankfehler: {e}")

    finally:
        # Sicherstellen, dass die Datenbankverbindung geschlossen wird
        if conn:
            conn.close()


if __name__ == "__main__":
    # Hauptprogramm: Setzt den Pfad zur Datenbank und ruft die Funktion auf
    database_path = "faces.db"  # Pfad zur Datenbankdatei (anpassen, falls notwendig)
    load_images_from_database(database_path)  # Funktion aufrufen
