# Projeto de Análise de Risco de Crédito com MySQL e Python
 
 Este projeto utiliza um conjunto de dados de crédito do sul da Alemanha para classificar candidatos a empréstimos como "bom" ou "ruim" usando modelos de machine learning. O banco de dados é configurado no MySQL, e o processamento é feito em Python.
 Este projeto utiliza o conjunto de dados *South German Credit* para classificar candidatos a empréstimos como "bom" ou "ruim" usando um modelo de Árvore de Decisão. Os dados são armazenados em um banco MySQL, importados do arquivo `SouthGermanCredit.asc`, e processados em Python com bibliotecas como Pandas e Scikit-learn. A aplicação solicita entradas do usuário para prever o risco de crédito, com validação baseada na tabela de códigos (`codetable.txt`).
 
 Este documento explica como configurar o ambiente MySQL e executar o script `germancredit.sql` para criar e popular o banco de dados.
 
## Modelo de Classificação

O projeto utiliza o modelo **Árvore de Decisão** (*Decision Tree Classifier*) da biblioteca Scikit-learn, configurado com o parâmetro `random_state=42` para garantir reproducibilidade. Ele é implementado em `src/model.py` e treinado para classificar o risco de crédito com base nas variáveis do conjunto de dados.

---

## Estrutura do Projeto

```
south_german_credit/
├── config/
│   └── config.json          # Credenciais do MySQL
├── data/
│   └── SouthGermanCredit.asc  # Dados brutos (opcional)
├── src/
│   ├── __init__.py         # Torna src um pacote Python
│   ├── database.py         # Conexão e importação de dados
│   ├── model.py            # Treino e avaliação do modelo
│   ├── prediction.py       # Entrada do usuário e previsão
│   └── utils.py            # Funções utilitárias
├── main.py                 # Script principal
├── requirements.txt        # Dependências Python
└── .gitignore              # Ignora arquivos sensíveis
```

---

## Pré-requisitos

Certifique-se de ter instalado:

1. **MySQL**:
   - Baixe em [mysql.com](https://dev.mysql.com/downloads/).
   - Configure o usuário `root` com senha.
2. **Python 3.8+**:
   - Baixe em [python.org](https://www.python.org/downloads/).
   - Verifique com `python --version`.
3. **SouthGermanCredit.asc**:
   - Obtenha em [UCI Repository](https://archive.ics.uci.edu/ml/datasets/South+German+Credit) ou [GitHub](https://github.com/marcelovca90-inatel/AG2).
4. **Terminal**:
   - **Windows**: Prompt de Comando (cmd).
   - **Linux/Mac**: Terminal padrão.
5. **Editor de Texto**:
   - Ex.: VS Code, para editar `config.json`.

---

## Configuração do Ambiente

### 1. Crie o Diretório do Projeto

```bash
mkdir -p south_german_credit/{config,data,src}
cd south_german_credit
```

### 2. Configure o MySQL

1. **Crie o arquivo `germancredit_schema.sql`**:

   ```sql
   CREATE DATABASE IF NOT EXISTS statlog;
   USE statlog;

   DROP TABLE IF EXISTS germancredit;
   CREATE TABLE germancredit (
       id INT NOT NULL AUTO_INCREMENT,
       laufkont INT DEFAULT NULL,
       laufzeit INT DEFAULT NULL,
       moral INT DEFAULT NULL,
       verw INT DEFAULT NULL,
       hoehe INT DEFAULT NULL,
       sparkont INT DEFAULT NULL,
       beszeit INT DEFAULT NULL,
       rate INT DEFAULT NULL,
       famges INT DEFAULT NULL,
       buerge INT DEFAULT NULL,
       wohnzeit INT DEFAULT NULL,
       verm INT DEFAULT NULL,
       alter INT DEFAULT NULL,
       weitkred INT DEFAULT NULL,
       wohn INT DEFAULT NULL,
       bishkred INT DEFAULT NULL,
       beruf INT DEFAULT NULL,
       pers INT DEFAULT NULL,
       telef INT DEFAULT NULL,
       gastarb INT DEFAULT NULL,
       kredit INT DEFAULT NULL,
       PRIMARY KEY (id)
   ) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8mb4;
   ```

   Salve em `south_german_credit/germancredit_schema.sql`.

2. **Execute o script**:

   ```bash
   mysql -u root -p < germancredit_schema.sql
   ```

   Digite a senha do `root`.

3. **Verifique**:

   ```bash
   mysql -u root -p
   ```

   No MySQL:

   ```sql
   USE statlog;
   SHOW TABLES;
   ```

   Confirme que `germancredit` está listada.

### 3. Configure o Arquivo de Configuração

Crie `config/config.json`:

```json
{
    "mysql": {
        "host": "localhost",
        "user": "root",
        "password": "#Euteamo123",
        "database": "statlog"
    }
}
```

Atualize `"password"` com a senha do seu MySQL.

### 4. Instale Dependências Python

```bash
pip install -r requirements.txt
```

Opcional: use um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 5. Configure `SouthGermanCredit.asc`

- Coloque o arquivo em `data/SouthGermanCredit.asc`.
- Ou ajuste o caminho em `main.py`:

  ```python
  asc_file_path = "/seu/caminho/SouthGermanCredit.asc"
  ```

### 6. Adicione os Arquivos do Projeto

Crie os arquivos com o código fornecido:

- `src/utils.py`
- `src/database.py`
- `src/model.py`
- `src/prediction.py`
- `src/__init__.py` (vazio)
- `main.py`
- `requirements.txt`
- `.gitignore`

---

## Definição de Descrições e Intervalos Válidos (codetable.txt)

As entradas do usuário são validadas com base na tabela de códigos (`codetable.txt`). Abaixo estão as descrições e intervalos válidos para cada variável, conforme implementado em `src/prediction.py`:

| Variável       | Descrição                                                                 | Intervalo Válido       |
|----------------|---------------------------------------------------------------------------|------------------------|
| `laufkont`     | Status da conta corrente (1: sem conta, 2: < 0 DM, 3: 0 <= ... < 200 DM, 4: >= 200 DM ou salário por pelo menos 1 ano) | 1 a 4                  |
| `laufzeit`     | Duração em meses (numérico, entre 6 e 72)                                 | 6 a 72                 |
| `moral`        | Histórico de crédito (0: atraso no pagamento, 1: conta crítica/outros créditos em outro lugar, 2: sem créditos tomados/todos pagos, 3: créditos existentes pagos regularmente até agora, 4: todos os créditos neste banco pagos regularmente) | 0 a 4                  |
| `verw`         | Finalidade (0: outros, 1: carro novo, 2: carro usado, 3: móveis/equipamentos, 4: rádio/televisão, 5: eletrodomésticos, 6: reparos, 7: educação, 8: férias, 9: reciclagem, 10: negócios) | 0 a 10                 |
| `hoehe`        | Valor do crédito (numérico, entre 250 e 18420)                            | 250 a 18420            |
| `sparkont`     | Conta poupança (1: desconhecido/sem poupança, 2: < 100 DM, 3: 100 <= ... < 500 DM, 4: 500 <= ... < 1000 DM, 5: >= 1000 DM) | 1 a 5                  |
| `beszeit`      | Duração do emprego (1: desempregado, 2: < 1 ano, 3: 1 <= ... < 4 anos, 4: 4 <= ... < 7 anos, 5: >= 7 anos) | 1 a 5                  |
| `rate`         | Taxa de parcelamento (1: >= 35%, 2: 25 <= ... < 35%, 3: 20 <= ... < 25%, 4: < 20%) | 1 a 4                  |
| `famges`       | Estado civil/sexo (1: homem divorciado/separado, 2: mulher não solteira ou homem solteiro, 3: homem casado/viúvo, 4: mulher solteira) | 1 a 4                  |
| `buerge`       | Outros devedores (1: nenhum, 2: co-solicitante, 3: garantidor)            | 1 a 3                  |
| `wohnzeit`     | Tempo de residência atual (1: < 1 ano, 2: 1 <= ... < 4 anos, 3: 4 <= ... < 7 anos, 4: >= 7 anos) | 1 a 4                  |
| `verm`         | Propriedade (1: desconhecido/sem propriedade, 2: carro ou outro, 3: poupança/sociedade de construção/seguro de vida, 4: imóvel) | 1 a 4                  |
| `alter`        | Idade em anos (numérico, entre 19 e 75)                                   | 19 a 75                |
| `weitkred`     | Outros planos de parcelamento (1: banco, 2: lojas, 3: nenhum)             | 1 a 3                  |
| `wohn`         | Moradia (1: gratuita, 2: alugada, 3: própria)                             | 1 a 3                  |
| `bishkred`     | Número de créditos neste banco (1: 1, 2: 2-3, 3: 4-5, 4: >= 6)           | 1 a 4                  |
| `beruf`        | Emprego (1: desempregado/não qualificado não residente, 2: não qualificado residente, 3: empregado qualificado/oficial, 4: gerente/autônomo/altamente qualificado) | 1 a 4                  |
| `pers`         | Pessoas dependentes (1: 3 ou mais, 2: 0 a 2)                              | 1 a 2                  |
| `telef`        | Telefone (1: não, 2: sim, registrado em nome do cliente)                  | 1 a 2                  |
| `gastarb`      | Trabalhador estrangeiro (1: sim, 2: não)                                  | 1 a 2                  |

---

## Executando o Projeto

1. **Navegue até o diretório**:

   ```bash
   cd south_german_credit
   ```

2. **Execute**:

   ```bash
   python main.py
   ```

3. **Funcionamento**:
   - Importa `SouthGermanCredit.asc` para o MySQL (se a tabela estiver vazia).
   - Carrega os dados.
   - Treina e avalia o modelo (acurácia ~0.71).
   - Solicita entradas para previsão.

4. **Exemplo de interação**:

   ```
   Insira os seguintes detalhes para previsão de risco de crédito:
   Status da conta corrente (1: sem conta, 2: < 0 DM, 3: 0 <= ... < 200 DM, 4: >= 200 DM ou salário por pelo menos 1 ano)
   Insira o valor para laufkont: 1
   ...
   Risco de crédito previsto: ruim
   Deseja fazer outra previsão? (sim/não): não
   ```

---

## Solução de Problemas

1. **Erro: "mysql: command not found"**
   - Adicione o MySQL ao PATH:
     - **Windows**: `C:\Program Files\MySQL\MySQL Server 8.0\bin`
     - **Linux**: `export PATH=$PATH:/usr/local/mysql/bin`
   - Ou reinstale o MySQL.

2. **Erro: "Access denied for user 'root'@'localhost'"**
   - Verifique a senha em `config.json`.
   - Redefina:

     ```sql
     ALTER USER 'root'@'localhost' IDENTIFIED BY 'nova_senha';
     ```

3. **Erro: "SouthGermanCredit.asc não encontrado"**
   - Confirme o caminho em `main.py`.
   - Baixe novamente o arquivo.

4. **Erro: "Nenhum dado retornado da tabela 'germancredit'"**
   - Verifique se `SouthGermanCredit.asc` foi importado:
     ```sql
     SELECT COUNT(*) FROM germancredit;
     ```
   - Reexecute a importação limpando a tabela:

     ```sql
     TRUNCATE TABLE germancredit;
     ```

5. **Erro: MySQL não está rodando**
   - Inicie o serviço:
     - **Windows**: `net start mysql`
     - **Linux**: `sudo service mysql start`
     - **Mac**: `mysql.server start`

---

## Exemplo no Terminal

**Windows (CMD)**:

```cmd
cd south_german_credit
python main.py
```

**Linux/Mac**:

```bash
cd south_german_credit
python main.py
```

**Saída esperada**:

```
Importando dados de SouthGermanCredit.asc para MySQL...
Dados importados com sucesso! 1000 linhas inseridas.
Iniciando o carregamento dos dados...
Dados carregados com sucesso! Número de linhas: 1000, Colunas: 22
...
Acurácia do modelo: 0.71
...
Risco de crédito previsto: bom
```

---
## Exemplo no Terminal (Windows)
 Supondo que o arquivo está em `C:\Users\SeuUsuario\germancredit.sql`:
 1. Abra o CMD.
 2. Digite:
    ```cmd
    cd C:\Users\SeuUsuario
    mysql -u root -p < germancredit.sql
    ```
 3. Digite a senha quando solicitado.

 ![CMD](https://github.com/GustavoRT-debug/AG2/blob/main/Captura%20de%20tela%202025-04-01%20154011.png)

## Notas

- **Importação**: `SouthGermanCredit.asc` é importado automaticamente na primeira execução, se a tabela estiver vazia.
- **Validação**: Entradas do usuário seguem a tabela acima, garantindo valores corretos.
- **Extensões**: Adicione novos modelos em `src/model.py` ou altere prompts em `src/prediction.py`.

---

*Última atualização: 14 de abril de 2025*


---

### Changes Made

1. **Added Model Information**:
   - Inserted a new subsection, “Modelo de Classificação”, under the project overview.
   - Stated that the project uses a **Decision Tree Classifier** from Scikit-learn with `random_state=42`, implemented in `src/model.py`.
   - Kept it concise and in Portuguese (e.g., “Árvore de Decisão” instead of “Decision Tree”).

2. **Preserved Existing Content**:
   - Retained all sections from the previous `README.md`, including the `codetable.txt` table, project structure, setup instructions, and troubleshooting.
   - Ensured no changes to unrelated parts, maintaining `SouthGermanCredit.asc` integration and MySQL focus.

3. **Portuguese Consistency**:
   - Used natural Portuguese phrasing (e.g., “configurado com o parâmetro `random_state=42`”).
   - Aligned with the code’s output (e.g., “bom”/“ruim” terminology).

4. **Example Alignment**:
   - Kept the clear, step-by-step style of the example `README.md`.
   - Ensured terminal commands and troubleshooting remain prominent.

5. **Artifact Tag**:
   - Wrapped the updated `README.md` in the required `<xaiArtifact>` tag with a new UUID, as this is a distinct update from previous artifacts.

---

### Setup Instructions

1. **Create Directory**:
   ```bash
   mkdir -p south_german_credit/{config,data,src}
   cd south_german_credit
   ```

2. **Save `README.md`**:
   - Copy the content from the artifact into `south_german_credit/README.md`.

3. **Add Project Files**:
   - Use files from earlier responses:
     - `config/config.json`
     - `.gitignore`
     - `requirements.txt`
     - `src/utils.py`, `src/database.py`, `src/model.py`, `src/prediction.py`, `src/__init__.py`
     - `main.py`
   - Update `main.py`’s `asc_file_path` if needed:
     ```python
     asc_file_path = "data/SouthGermanCredit.asc"
     ```

4. **Get `SouthGermanCredit.asc`**:
   - Download from [UCI](https://archive.ics.uci.edu/ml/datasets/South+German+Credit) or [GitHub](https://github.com/marcelovca90-inatel/AG2).
   - Place in `data/` or adjust the path.

5. **Set Up MySQL**:
   - Save `germancredit_schema.sql` as shown in the `README.md`.
   - Run:
     ```bash
     mysql -u root -p < germancredit_schema.sql
     ```

6. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

7. **Run**:
   ```bash
   python main.py
   ```

---

### Testing Instructions

To verify the updated `README.md` integrates with the project:

1. **Check `README.md` Content**:
   - Open `README.md` in a Markdown viewer (e.g., VS Code, GitHub).
   - Confirm the new “Modelo de Classificação” section states:
     - Uses “Árvore de Decisão” from Scikit-learn.
     - Configured with `random_state=42`.
     - Implemented in `src/model.py`.
   - Verify the `codetable.txt` table and other sections remain unchanged.

2. **Test Setup**:
   - Follow “Configuração do Ambiente” steps.
   - Check MySQL:
     ```sql
     USE statlog;
     SHOW TABLES;  -- Shows 'germancredit'
     ```

3. **Test Import**:
   - Run `main.py` with an empty table:
     ```
     Importando dados de SouthGermanCredit.asc para MySQL...
     Dados importados com sucesso! 1000 linhas inseridas.
     ```
   - Verify:
     ```sql
     SELECT COUNT(*) FROM germancredit;  -- Returns 1000
     ```

4. **Test Execution**:
   - Confirm training uses the Decision Tree model:
     ```
     Treinamento: 800 amostras, Teste: 200 amostras
     Treinando o modelo de Árvore de Decisão...
     Acurácia do modelo: 0.71
     ```
   - Test prediction with a valid input (e.g., `laufkont=1, laufzeit=18, moral=4, ...`):
     ```
     Risco de crédito previsto: bom
     ```

5. **Test Model Reference**:
   - Check `src/model.py` to confirm:
     ```python
     model = DecisionTreeClassifier(random_state=42)
     ```
   - Ensure the `README.md`’s description matches this implementation.

6. **Test Troubleshooting**:
   - Try wrong `asc_file_path`:
     ```
     Erro ao importar SouthGermanCredit.asc: [Errno 2] No such file or directory: ...
     ```
   - Test incorrect MySQL password:
     ```
     Erro ao conectar ao MySQL: Access denied for user 'root'@'localhost'
     ```

7. **Test Previous Input**:
   - Use corrected input:
     - `laufkont=1, laufzeit=6, moral=0, verw=1, hoehe=1000, sparkont=3, beszeit=4, rate=4, famges=2, buerge=1, wohnzeit=4, verm=1, alter=30, weitkred=3, wohn=2, bishkred=1, beruf=3, pers=2, telef=1, gastarb=1`
     - Confirm validation aligns with the `codetable.txt` table (e.g., `rate=5` is invalid).
