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

# Passo 1: Conectar ao MySQL e Carregar Dados com Verificação
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

# Passo 2: Pré-processar Dados
def preprocess_data(df):
    df = df.drop('id', axis=1)
    X = df.drop('kredit', axis=1)
    y = df['kredit']
    return X, y

# Passo 3: Dividir Dados (80% Treinamento, 20% Teste)
def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Passo 4: Treinar o Modelo (Árvore de Decisão)
def train_model(X_train, y_train):
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

# Passo 5: Avaliar o Modelo
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['ruim', 'bom'])
    print(f"Acurácia do modelo: {accuracy:.2f}")
    print("Relatório de Classificação:")
    print(report)

# Passo 6: Entrada do Usuário para Predição
def predict_user_input(model):
    print("\nInsira os seguintes detalhes para previsão de risco de crédito:")
    user_data = []
    feature_names = [
        'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit', 
        'rate', 'famges', 'buerge', 'wohnzeit', 'verm', 'alter', 'weitkred', 
        'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb'
    ]
    
    for feature in feature_names:
        if feature == 'laufkont':
            print("Status da conta corrente (1: sem conta, 2: < 0 DM, 3: 0-200 DM, 4: >= 200 DM)")
        elif feature == 'laufzeit':
            print("Duração em meses (numérico)")
        elif feature == 'moral':
            print("Histórico de crédito (0: atraso, 1: crítico, 2: sem créditos, 3: pago regularmente, 4: todos pagos)")
        
        value = int(input(f"Insira o valor para {feature}: "))
        user_data.append(value)
    
    user_data = np.array(user_data).reshape(1, -1)
    prediction = model.predict(user_data)[0]
    result = "bom" if prediction == 1 else "ruim"
    print(f"\nRisco de crédito previsto: {result}")

# Execução Principal
def main():
    print("Iniciando o carregamento dos dados...")
    data = load_data_from_mysql()

    if data is None or data.empty:
        print("Falha ao carregar os dados. Encerrando o programa.")
        return

    print("\nPré-processando os dados...")
    X, y = preprocess_data(data)
    print(f"Forma das características (X): {X.shape}")
    print(f"Forma do alvo (y): {y.shape}")

    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"Treinamento: {X_train.shape[0]} amostras, Teste: {X_test.shape[0]} amostras")
    
    print("\nTreinando o modelo de Árvore de Decisão...")
    model = train_model(X_train, y_train)
    
    print("\nAvaliando o modelo...")
    evaluate_model(model, X_test, y_test)
    
    while True:
        predict_user_input(model)
        again = input("\nDeseja fazer outra previsão? (sim/não): ").lower()
        if again != 'sim':
            break

if __name__ == "__main__":
    main()