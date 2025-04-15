from src.utils import load_config
from src.database import load_data_from_mysql, import_asc_to_mysql
from src.model import preprocess_data, split_data, train_model, evaluate_model
from src.prediction import predict_user_input

def main():
    # Carregar configurações
    config = load_config()
    if config is None:
        print("Falha ao carregar configurações. Encerrando o programa.")
        return

    mysql_config = config.get('mysql')
    if not mysql_config:
        print("Erro: Configurações do MySQL não encontradas no config.json!")
        return

    # Importar SouthGermanCredit.asc (opcional, se tabela vazia)
    asc_file_path = "data/SouthGermanCredit.asc"  # Ajuste o caminho conforme necessário
    if not import_asc_to_mysql(asc_file_path, mysql_config):
        print("Falha ao importar dados. Verifique o arquivo ou a conexão com o banco.")

    # Carregar dados do MySQL
    print("Iniciando o carregamento dos dados...")
    data = load_data_from_mysql(mysql_config)

    if data is None or data.empty:
        print("Falha ao carregar os dados. Encerrando o programa.")
        return

    # Pré-processar e dividir dados
    print("\nPré-processando os dados...")
    X, y = preprocess_data(data)
    print(f"Forma das características (X): {X.shape}")
    print(f"Forma do alvo (y): {y.shape}")

    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"Treinamento: {X_train.shape[0]} amostras, Teste: {X_test.shape[0]} amostras")

    # Treinar e avaliar o modelo
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)

    # Loop de predição
    while True:
        predict_user_input(model)
        again = input("\nDeseja fazer outra previsão? (sim/não): ").lower()
        if again != 'sim':
            break

if __name__ == "__main__":
    main()