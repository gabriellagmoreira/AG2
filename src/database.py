import mysql.connector
import pandas as pd

def load_data_from_mysql(mysql_config):
    """Conecta ao MySQL e carrega dados da tabela germancredit."""
    try:
        print("Tentando conectar ao banco de dados MySQL...")
        conn = mysql.connector.connect(
            host=mysql_config["host"],
            user=mysql_config["user"],
            password=mysql_config["password"],
            database=mysql_config["database"]
        )
        print("Conexão bem-sucedida ao banco de dados 'statlog'!")

        query = "SELECT * FROM germancredit"
        print("Executando a consulta:", query)
        data = pd.read_sql(query, conn)

        if data.empty:
            print("Erro: Nenhum dado foi retornado da tabela 'germancredit'!")
        else:
            print(f"Dados carregados com sucesso! Número de linhas: {data.shape[0]}, Colunas: {data.shape[1]}")
            print("Primeiras 5 linhas dos dados:")
            print(data.head())

        conn.close()
        print("Conexão com o banco fechada.")
        
        return data

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

def import_asc_to_mysql(asc_file_path, mysql_config):
    """Importa dados de SouthGermanCredit.asc para a tabela germancredit."""
    try:
        print("Importando dados de SouthGermanCredit.asc para MySQL...")
        # Ler o arquivo .asc
        data = pd.read_csv(asc_file_path, sep='\s+', header=None)
        data.columns = [
            'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit',
            'rate', 'famges', 'buerge', 'wohnzeit', 'verm', 'alter', 'weitkred',
            'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb', 'kredit'
        ]

        # Conectar ao MySQL
        conn = mysql.connector.connect(
            host=mysql_config["host"],
            user=mysql_config["user"],
            password=mysql_config["password"],
            database=mysql_config["database"]
        )
        cursor = conn.cursor()

        # Verificar se a tabela está vazia
        cursor.execute("SELECT COUNT(*) FROM germancredit")
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            print("Tabela germancredit vazia. Inserindo dados...")
            insert_query = """
            INSERT INTO germancredit (
                laufkont, laufzeit, moral, verw, hoehe, sparkont, beszeit, rate,
                famges, buerge, wohnzeit, verm, alter, weitkred, wohn, bishkred,
                beruf, pers, telef, gastarb, kredit
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for _, row in data.iterrows():
                cursor.execute(insert_query, tuple(row))
            conn.commit()
            print(f"Dados importados com sucesso! {data.shape[0]} linhas inseridas.")
        else:
            print("Tabela germancredit já contém dados. Importação ignorada.")

        cursor.close()
        conn.close()
        print("Conexão com o banco fechada após importação.")
        return True
    except Exception as e:
        print(f"Erro ao importar SouthGermanCredit.asc: {e}")
        return False