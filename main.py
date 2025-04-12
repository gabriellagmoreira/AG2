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
    
    # codetable.txt
    feature_info = {
        'laufkont': {
            'description': "Status da conta corrente (1: sem conta, 2: < 0 DM, 3: 0 <= ... < 200 DM, 4: >= 200 DM ou salário por pelo menos 1 ano)",
            'valid_range': range(1, 5)
        },
        'laufzeit': {
            'description': "Duração em meses (numérico, entre 6 e 72)",
            'valid_range': range(6, 73)
        },
        'moral': {
            'description': "Histórico de crédito (0: atraso no pagamento, 1: conta crítica/outros créditos em outro lugar, 2: sem créditos tomados/todos pagos, 3: créditos existentes pagos regularmente até agora, 4: todos os créditos neste banco pagos regularmente)",
            'valid_range': range(0, 5)
        },
        'verw': {
            'description': "Finalidade (0: outros, 1: carro novo, 2: carro usado, 3: móveis/equipamentos, 4: rádio/televisão, 5: eletrodomésticos, 6: reparos, 7: educação, 8: férias, 9: reciclagem, 10: negócios)",
            'valid_range': range(0, 11)
        },
        'hoehe': {
            'description': "Valor do crédito (numérico, entre 250 e 18420)",
            'valid_range': range(250, 18421)
        },
        'sparkont': {
            'description': "Conta poupança (1: desconhecido/sem poupança, 2: < 100 DM, 3: 100 <= ... < 500 DM, 4: 500 <= ... < 1000 DM, 5: >= 1000 DM)",
            'valid_range': range(1, 6)
        },
        'beszeit': {
            'description': "Duração do emprego (1: desempregado, 2: < 1 ano, 3: 1 <= ... < 4 anos, 4: 4 <= ... < 7 anos, 5: >= 7 anos)",
            'valid_range': range(1, 6)
        },
        'rate': {
            'description': "Taxa de parcelamento (1: >= 35%, 2: 25 <= ... < 35%, 3: 20 <= ... < 25%, 4: < 20%)",
            'valid_range': range(1, 5)
        },
        'famges': {
            'description': "Estado civil/sexo (1: homem divorciado/separado, 2: mulher não solteira ou homem solteiro, 3: homem casado/viúvo, 4: mulher solteira)",
            'valid_range': range(1, 5)
        },
        'buerge': {
            'description': "Outros devedores (1: nenhum, 2: co-solicitante, 3: garantidor)",
            'valid_range': range(1, 4)
        },
        'wohnzeit': {
            'description': "Tempo de residência atual (1: < 1 ano, 2: 1 <= ... < 4 anos, 3: 4 <= ... < 7 anos, 4: >= 7 anos)",
            'valid_range': range(1, 5)
        },
        'verm': {
            'description': "Propriedade (1: desconhecido/sem propriedade, 2: carro ou outro, 3: poupança/sociedade de construção/seguro de vida, 4: imóvel)",
            'valid_range': range(1, 5)
        },
        'alter': {
            'description': "Idade em anos (numérico, entre 19 e 75)",
            'valid_range': range(19, 76)
        },
        'weitkred': {
            'description': "Outros planos de parcelamento (1: banco, 2: lojas, 3: nenhum)",
            'valid_range': range(1, 4)
        },
        'wohn': {
            'description': "Moradia (1: gratuita, 2: alugada, 3: própria)",
            'valid_range': range(1, 4)
        },
        'bishkred': {
            'description': "Número de créditos neste banco (1: 1, 2: 2-3, 3: 4-5, 4: >= 6)",
            'valid_range': range(1, 5)
        },
        'beruf': {
            'description': "Emprego (1: desempregado/não qualificado não residente, 2: não qualificado residente, 3: empregado qualificado/oficial, 4: gerente/autônomo/altamente qualificado)",
            'valid_range': range(1, 5)
        },
        'pers': {
            'description': "Pessoas dependentes (1: 3 ou mais, 2: 0 a 2)",
            'valid_range': range(1, 3)
        },
        'telef': {
            'description': "Telefone (1: não, 2: sim, registrado em nome do cliente)",
            'valid_range': range(1, 3)
        },
        'gastarb': {
            'description': "Trabalhador estrangeiro (1: sim, 2: não)",
            'valid_range': range(1, 3)
        }
    }
    
    for feature in feature_names:
        print(feature_info[feature]['description'])
        while True:
            try:
                value = int(input(f"Insira o valor para {feature}: "))
                if value not in feature_info[feature]['valid_range']:
                    print(f"Valor inválido! Deve estar entre {min(feature_info[feature]['valid_range'])} e {max(feature_info[feature]['valid_range'])}.")
                    continue
                user_data.append(value)
                break
            except ValueError:
                print("Por favor, insira um número inteiro válido.")
    
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