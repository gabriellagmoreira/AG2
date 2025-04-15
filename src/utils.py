import json

def load_config(config_path='config/config.json'):
    """Carrega as credenciais do arquivo config.json."""
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Erro: Arquivo config.json não encontrado!")
        return None
    except json.JSONDecodeError:
        print("Erro: Formato inválido no config.json!")
        return None