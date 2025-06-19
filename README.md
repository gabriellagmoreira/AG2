# Projeto: Análise de Risco de Crédito com MySQL e Python

Este projeto classifica candidatos a crédito como **"bom" ou "ruim"**, usando o modelo de **k-Nearest Neighbors (KNN)** da biblioteca `Scikit-learn`. Os dados vêm do conjunto **South German Credit**, armazenados em um banco **MySQL** e processados com **Python**.

## 🧩 Requisitos

- MySQL instalado ([link](https://dev.mysql.com/downloads/))
- Python 3.8+ ([link](https://www.python.org/downloads/))
- Arquivo `SouthGermanCredit.asc` ([UCI Repository](https://archive.ics.uci.edu/ml/datasets/South+German+Credit))

## 📁 Estrutura do Projeto

```
south_german_credit/
├── config/
│   └── config.json
├── data/
│   └── SouthGermanCredit.asc
├── src/
│   ├── database.py
│   ├── model.py
│   ├── prediction.py
│   └── utils.py
├── germancredit_schema.sql
├── main.py
└── requirements.txt
```

## ⚙️ Configuração

1. **Crie o banco de dados:**

```bash
mysql -u root -p < germancredit_schema.sql
```

2. **Configure `config.json`:**

```json
{
  "mysql": {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA",
    "database": "statlog"
  }
}
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

## 🚀 Execução

```bash
cd south_german_credit
python main.py
```

A aplicação:
- Importa os dados para o MySQL (se necessário)
- Treina o modelo KNN
- Solicita dados do usuário
- Informa o risco de crédito previsto

## 📊 Exemplo

```
Insira o valor para laufkont: 2
...
Risco de crédito previsto: ruim
```
