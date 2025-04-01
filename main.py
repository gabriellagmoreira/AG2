import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Step 1: Connect to MySQL and Load Data with Verification
def load_data_from_mysql():
    try:
        # Tentativa de conexão com o banco
        print("Tentando conectar ao banco de dados MySQL...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Seu usuário MySQL
            password="#Euteamo123",  # Sua senha MySQL
            database="statlog"
        )
        print("Conexão bem-sucedida ao banco de dados 'statlog'!")

        # Executar a query
        query = "SELECT * FROM germancredit"
        print("Executando a query:", query)
        data = pd.read_sql(query, conn)

        # Verificar se os dados foram carregados
        if data.empty:
            print("Erro: Nenhum dado foi retornado da tabela 'germancredit'!")
        else:
            print(f"Dados carregados com sucesso! Número de linhas: {data.shape[0]}, Colunas: {data.shape[1]}")
            print("Primeiras 5 linhas dos dados:")
            print(data.head())  # Mostra as primeiras 5 linhas

        # Fechar conexão
        conn.close()
        print("Conexão com o banco fechada.")
        
        return data

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

# Step 2: Preprocess Data
def preprocess_data(df):
    # Drop 'id' column as it’s not a feature
    df = df.drop('id', axis=1)
    
    # Features (X) and target (y)
    X = df.drop('kredit', axis=1)  # All columns except 'kredit'
    y = df['kredit']  # Target column (0 = bad, 1 = good)
    
    return X, y

# Step 3: Split Data into Training and Testing Sets
def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Step 4: Treinar o Modelo Usando 80% dos Dados (Decision Tree)
def train_model(X_train, y_train):
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

# Step 5: Avaliar o Modelo com 20% Restantes
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['bad', 'good'])
    
    print(f"Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(report)

# Step 6: User Input for Prediction
def predict_user_input(model):
    print("\nEnter the following details for credit risk prediction:")
    user_data = []
    feature_names = [
        'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit', 
        'rate', 'famges', 'buerge', 'wohnzeit', 'verm', 'alter', 'weitkred', 
        'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb'
    ]
    
    for feature in feature_names:
        # Provide a brief description of the feature based on the code table
        if feature == 'laufkont':
            print("Status of checking account (1: no account, 2: < 0 DM, 3: 0-200 DM, 4: >= 200 DM)")
        elif feature == 'laufzeit':
            print("Duration in months (numeric)")
        elif feature == 'moral':
            print("Credit history (0: delay, 1: critical, 2: no credits, 3: paid duly, 4: all paid)")
        # Add similar descriptions for other features as needed (refer to the code table)
        
        value = int(input(f"Enter value for {feature}: "))
        user_data.append(value)
    
    # Convert to numpy array and reshape for prediction
    user_data = np.array(user_data).reshape(1, -1)
    
    # Predict
    prediction = model.predict(user_data)[0]
    result = "good" if prediction == 1 else "bad"
    print(f"\nPredicted credit risk: {result}")

# Main Execution
def main():
    # Load data
    print("Iniciando o carregamento dos dados...")
    data = load_data_from_mysql()

    # Verificar se os dados foram carregados corretamente
    if data is None or data.empty:
        print("Falha ao carregar os dados. Encerrando o programa.")
        return

    # Preprocess
    print("\nPré-processando os dados...")
    X, y = preprocess_data(data)
    print(f"Features (X) shape: {X.shape}")
    print(f"Target (y) shape: {y.shape}")

    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"Treino: {X_train.shape[0]} amostras, Teste: {X_test.shape[0]} amostras")
    
    # Train model
    print("\nTraining the Decision Tree model...")
    model = train_model(X_train, y_train)
    
    # Evaluate model
    print("\nEvaluating the model...")
    evaluate_model(model, X_test, y_test)
    
    # User prediction
    while True:
        predict_user_input(model)
        again = input("\nWould you like to predict another? (yes/no): ").lower()
        if again != 'yes':
            break

if __name__ == "__main__":
    main()