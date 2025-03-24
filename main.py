import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Conexão com o banco
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sua_senha",
    database="credit_db"
)

# Leitura dos dados
query = "SELECT * FROM credit_data"
df = pd.read_sql(query, conn)
conn.close()

# Separar features e target
X = df.drop(columns=['id', 'credit_risk'])
y = df['credit_risk']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar o modelo
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Avaliar o modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy:.2f}")
print("Relatório de classificação:")
print(classification_report(y_test, y_pred))

# Função para prever dados arbitrários
def predict_credit_risk(model):
    print("Insira os dados do cliente (separados por vírgula, na ordem dos atributos):")
    print("status, duration, credit_history, purpose, amount, savings, employment_duration, installment_rate, personal_status_sex, other_debtors, present_residence, property, age, other_installment_plans, housing, number_credits, job, people_liable, telephone, foreign_worker")
    user_input = input("Digite os valores: ")
    data = [int(x) for x in user_input.split(",")]
    
    if len(data) != 20:
        print("Erro: Insira exatamente 20 valores.")
        return
    
    prediction = model.predict([data])[0]
    result = "bom" if prediction == 1 else "ruim"
    print(f"Risco de crédito previsto: {result}")

# Testar a função
predict_credit_risk(model)