from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

def preprocess_data(df):
    df = df.drop('id', axis=1)
    X = df.drop('kredit', axis=1)
    y = df['kredit']
    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train, y_train, n_neighbors=5):
    print("Treinando o modelo k-Nearest Neighbors...")
    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    print("\nAvaliando o modelo...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['ruim', 'bom'])
    print(f"Acurácia do modelo: {accuracy:.2f}")
    print("Relatório de Classificação:")
    print(report)
