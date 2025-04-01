## Projeto de Análise de Crédito com MySQL e Python

Este projeto utiliza um conjunto de dados de crédito do sul da Alemanha para classificar candidatos a empréstimos como "bom" ou "ruim" usando modelos de machine learning. O banco de dados é configurado no MySQL, e o processamento é feito em Python.

Este documento explica como configurar o ambiente MySQL e executar o script `germancredit.sql` para criar e popular o banco de dados.

---

## Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado:

1. **MySQL**: Baixe e instale o MySQL em [mysql.com](https://dev.mysql.com/downloads/). Siga as instruções para o seu sistema operacional.
2. **Arquivo SQL**: Tenha o arquivo `germancredit.sql` pronto com os comandos SQL para criar o banco de dados e a tabela.
3. **Acesso ao Terminal**:
   - **Windows**: Prompt de Comando (cmd).
   - **Linux/Mac**: Terminal.

---

## Configuração do MySQL

### 1. Salve o Arquivo `germancredit.sql`
Crie um arquivo chamado `germancredit.sql` com os comandos SQL necessários. Exemplo básico:

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
) ENGINE=InnoDB AUTO_INCREMENT=1001 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO germancredit VALUES
(1, 1, 18, 4, 2, 1049, 1, 2, 4, 2, 1, 4, 2, 21, 3, 1, 1, 3, 2, 1, 2, 1),
(2, 1, 9, 4, 0, 2799, 1, 3, 2, 3, 1, 2, 1, 36, 3, 1, 2, 3, 1, 1, 2, 1),
(3, 1, 12, 2, 9, 841, 2, 4, 2, 2, 1, 4, 1, 23, 3, 1, 1, 2, 2, 1, 2, 1);
```

Salve o arquivo em um local acessível, como:
- Windows: `C:\Users\SeuUsuario\germancredit.sql`
- Linux/Mac: `/home/seu_usuario/germancredit.sql`

### 2. Abra o Terminal
- **Windows**: Pressione `Win + R`, digite `cmd` e pressione Enter.
- **Linux/Mac**: Abra o aplicativo "Terminal".

### 3. Navegue até o Diretório do Arquivo (Opcional)
Use o comando `cd` para ir até o diretório onde o arquivo `germancredit.sql` está salvo:
- **Windows**: `cd C:\Users\SeuUsuario`
- **Linux/Mac**: `cd /home/seu_usuario`

Se o MySQL estiver no PATH (veja o próximo passo), você pode executar o comando de qualquer diretório, especificando o caminho completo do arquivo.

### 4. Verifique se o MySQL Está no PATH
O comando `mysql` deve estar acessível no terminal:
- Digite `mysql --version` no terminal.
- Se aparecer algo como `mysql Ver 8.0.23...`, está configurado corretamente.
- Se der erro ("comando não reconhecido"):
  - **Windows**: Adicione o caminho do MySQL ao PATH (ex.: `C:\Program Files\MySQL\MySQL Server 8.0\bin`). Veja como fazer isso em "Editar variáveis de ambiente".
  - **Linux/Mac**: Instale o MySQL se necessário (ex.: `sudo apt install mysql-server` no Ubuntu) e verifique novamente.

### 5. Execute o Script no MySQL
No terminal, digite:

```bash
mysql -u root -p < germancredit.sql
```

- **Explicação**:
  - `mysql`: Inicia o cliente MySQL.
  - `-u root`: Usa o usuário "root".
  - `-p`: Solicita a senha do usuário root.
  - `< germancredit.sql`: Redireciona o conteúdo do arquivo para o MySQL.
- Após pressionar Enter, digite a senha do usuário `root` quando solicitado.

### 6. Verifique o Resultado
Se o comando executar sem erros, o banco de dados `statlog` e a tabela `germancredit` serão criados e populados. Para confirmar:
1. Entre no MySQL:
   ```bash
   mysql -u root -p
   ```
2. Digite a senha.
3. No prompt do MySQL (`mysql>`), execute:
   ```sql
   USE statlog;
   SHOW TABLES;
   SELECT * FROM germancredit LIMIT 5;
   ```
   Você verá a tabela `germancredit` e os primeiros registros.

---

## Solução de Problemas

1. **Erro: "mysql: command not found"**
   - O MySQL não está no PATH. Adicione o caminho do binário do MySQL ao PATH (veja o passo 4).

2. **Erro: "Access denied for user 'root'@'localhost'"**
   - A senha está incorreta ou o usuário `root` não está configurado. Redefina a senha:
     ```bash
     mysql -u root
     ALTER USER 'root'@'localhost' IDENTIFIED BY 'nova_senha';
     ```
     Tente novamente.

3. **Erro: "Can't connect to MySQL server"**
   - O serviço MySQL não está rodando. Inicie-o:
     - **Windows**: `net start mysql`
     - **Linux**: `sudo service mysql start`
     - **Mac**: `mysql.server start`

4. **Arquivo Não Encontrado**
   - Verifique o caminho do arquivo. Use o caminho completo se necessário:
     ```bash
     mysql -u root -p < "C:\Users\SeuUsuario\germancredit.sql"
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

---
![CMD](https://github.com/GustavoRT-debug/AG2/blob/main/Captura%20de%20tela%202025-04-01%20154011.png)
