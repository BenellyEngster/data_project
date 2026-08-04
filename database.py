import sqlite3

def create_tables():
    print("Verificando/criando banco de dados...")
    connection = sqlite3.connect("tjpr_data.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_lawsuits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_text TEXT
        )
    """)
    
    connection.commit()
    connection.close()
    print("Tabelas prontas para uso!")