import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import json

# Carregar credenciais do arquivo config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    mysql_config = config['mysql']

# Step 1: Connect to MySQL and Load Data with Verification
def load_data_from_mysql():
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
        print("Executando a query:", query)
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

# (O resto do código permanece igual ao da Opção 1)
def preprocess_data(df):
    df = df.drop('id', axis=1)
    X = df.drop('kredit', axis=1)
    y = df['kredit']
    return X, y

def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['bad', 'good'])
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)

def predict_user_input(model):
    print("\nEnter the following details for credit risk prediction:")
    user_data = []
    feature_names = [
        'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit', 
        'rate', 'famges', 'buerge', 'wohnzeit', 'verm', 'alter', 'weitkred', 
        'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb'
    ]
    
    for feature in feature_names:
        if feature == 'laufkont':
            print("Status of checking account (1: no account, 2: < 0 DM, 3: 0-200 DM, 4: >= 200 DM)")
        elif feature == 'laufzeit':
            print("Duration in months (numeric)")
        elif feature == 'moral':
            print("Credit history (0: delay, 1: critical, 2: no credits, 3: paid duly, 4: all paid)")
        
        value = int(input(f"Enter value for {feature}: "))
        user_data.append(value)
    
    user_data = np.array(user_data).reshape(1, -1)
    prediction = model.predict(user_data)[0]
    result = "good" if prediction == 1 else "bad"
    print(f"\nPredicted credit risk: {result}")

def main():
    print("Iniciando o carregamento dos dados...")
    data = load_data_from_mysql()

    if data is None or data.empty:
        print("Falha ao carregar os dados. Encerrando o programa.")
        return

    print("\nPré-processando os dados...")
    X, y = preprocess_data(data)
    print(f"Features (X) shape: {X.shape}")
    print(f"Target (y) shape: {y.shape}")

    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"Treino: {X_train.shape[0]} amostras, Teste: {X_test.shape[0]} amostras")
    
    print("\nTraining the Decision Tree model...")
    model = train_model(X_train, y_train)
    
    print("\nEvaluating the model...")
    evaluate_model(model, X_test, y_test)
    
    while True:
        predict_user_input(model)
        again = input("\nWould you like to predict another? (yes/no): ").lower()
        if again != 'yes':
            break

if __name__ == "__main__":
    main()