import os
import json
import sqlite3

def get_db_metadata(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    db_metadata = {
        "name": os.path.basename(db_path),
        "description": "",  # Add descriptions as needed
        "level": "",  # Add levels as needed
        "tables": []
    }

    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        record_count = cursor.fetchone()[0]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        table_metadata = {
            "name": table_name,
            "record_count": record_count,
            "columns": columns
        }

        db_metadata["tables"].append(table_metadata)

    conn.close()
    return db_metadata

def generate_metadata_json(folder_path, output_file):
    metadata = {"databases": []}

    for db_file in os.listdir(folder_path):
        if db_file.endswith(".db"):
            db_path = os.path.join(folder_path, db_file)
            db_metadata = get_db_metadata(db_path)
            metadata["databases"].append(db_metadata)

    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    sample_databases_folder = "sample_databases"
    output_metadata_file = "metadata.json"
    generate_metadata_json(sample_databases_folder, output_metadata_file)
