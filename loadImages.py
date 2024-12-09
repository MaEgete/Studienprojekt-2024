import sqlite3
import cv2
import numpy as np


def load_images_from_database(database_path, table_name="faces"):
    """
    Lädt alle Bilder aus der Datenbank und zeigt sie an.

    :param database_path: Pfad zur SQLite-Datenbank.
    :param table_name: Name der Tabelle, in der die Bilder gespeichert sind.
    """
    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Abfrage aller Daten aus der Tabelle
        query = f"SELECT id, name, image FROM {table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            print("Keine Bilder in der Datenbank gefunden.")
            return

        # Bilder anzeigen
        for row in rows:
            image_id, name, image_blob = row

            # Blob in ein Bild umwandeln
            image_array = np.frombuffer(image_blob, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Bild anzeigen mit ID und Name
            cv2.imshow(f"ID: {image_id} / {len(rows)}, Name: {name}", image)
            key = cv2.waitKey(0)

            # Optional: Bild speichern, wenn 's' gedrückt wird
            if key == ord('s'):
                filename = f"{name}_ID_{image_id}.jpg"
                cv2.imwrite(filename, image)
                print(f"Bild gespeichert als: {filename}")

        cv2.destroyAllWindows()

    except sqlite3.Error as e:
        print(f"Datenbankfehler: {e}")

    finally:
        # Verbindung zur Datenbank schließen
        if conn:
            conn.close()


if __name__ == "__main__":
    # Pfad zur Datenbank anpassen
    database_path = "faces.db"
    load_images_from_database(database_path)