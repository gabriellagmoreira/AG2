import numpy as np

# Constantes para nomes de colunas
FEATURE_NAMES = [
    'laufkont', 'laufzeit', 'moral', 'verw', 'hoehe', 'sparkont', 'beszeit', 
    'rate', 'famges', 'buerge', 'wohnzeit', 'verm', 'alter', 'weitkred', 
    'wohn', 'bishkred', 'beruf', 'pers', 'telef', 'gastarb'
]

FEATURE_INFO = {
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

def get_user_input(feature, description, valid_range):
    """Obtém e valida a entrada do usuário para uma característica específica."""
    print(description)
    while True:
        try:
            value = int(input(f"Insira o valor para {feature}: "))
            if value not in valid_range:
                print(f"Valor inválido! Deve estar entre {min(valid_range)} e {max(valid_range)}.")
                continue
            return value
        except ValueError:
            print("Por favor, insira um número inteiro válido.")

def predict_user_input(model):
    """Obtém entrada do usuário e faz previsão do risco de crédito."""
    print("\nInsira os seguintes detalhes para previsão de risco de crédito:")
    user_data = [get_user_input(feature, FEATURE_INFO[feature]['description'], FEATURE_INFO[feature]['valid_range']) for feature in FEATURE_NAMES]
    
    user_data = np.array(user_data).reshape(1, -1)
    prediction = model.predict(user_data)[0]
    result = "bom" if prediction == 1 else "ruim"
    print(f"\nRisco de crédito previsto: {result}")
    return result
