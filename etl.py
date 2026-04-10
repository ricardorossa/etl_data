

import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Inicializando a biblioteca faker com padrao americano
fake = Faker('en_US')

def gerar_dados_pedidos_etl(n_registros):
    # Extraindo dados
    dados_brutos = []
    tipos_pagamento = ['Cartão de Crédito', 'Boleto', 'Pix', 'Cartão de Débito']
    produtos_exemplo = ['Mouse Gamer', 'Teclado Mecânico', 'Monitor 24"', 'Headset', 'Webcam HD', 'Pad Mouse XL']

    for i in range(1, n_registros + 1):
        # Gerar data aleatória nos últimos 30 dias
        data_aleatoria = datetime.now() - timedelta(days=random.randint(0, 30))
        
        itens_pedido = random.sample(produtos_exemplo, k=random.randint(1, 3))
        
        registro = {
            'numero_pedido': 1000 + i,
            'codigo_cliente': f'CLI-{random.randint(100, 999)}',
            'nome_cliente': fake.name(),
            'tipo_pagamento': random.choice(tipos_pagamento),
            'valor_pedido': round(random.uniform(50.0, 2000.0), 2),
            'itens': ", ".join(itens_pedido),
            'data_criacao': data_aleatoria.strftime('%Y-%m-%d %H:%M:%S')
        }
        dados_brutos.append(registro)
    
    df = pd.DataFrame(dados_brutos)

    # --- T (TRANSFORM) ---
    # Transformação 1: Normalizar nomes para maiúsculas (Padronização)
    df['nome_cliente'] = df['nome_cliente'].str.upper()

    # Transformação 2: Criar categoria de status baseada no valor (Regra de Negócio)
    # Pedidos acima de R$ 1.500,00 entram em 'Análise de Risco', outros são 'Aprovado'
    df['status_pedido'] = df['valor_pedido'].apply(lambda x: 'ANÁLISE DE RISCO' if x > 1500 else 'APROVADO')

    # Transformação 3: Converter data_criacao para o tipo datetime do Pandas (Tipagem)
    df['data_criacao'] = pd.to_datetime(df['data_criacao'])
    
    return df

# --- L (LOAD) ---
# Gerar os dados processados
df_final = gerar_dados_pedidos_etl(1000)

# --- VISUALIZAÇÃO (GRÁFICO DE PIZZA) ---
# Contar a quantidade de pedidos por tipo de pagamento
contagem_pagamentos = df_final['tipo_pagamento'].value_counts()

plt.figure(figsize=(10, 7))
contagem_pagamentos.plot(
    kind='pie', 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'],
    explode=(0.05, 0, 0, 0) # Destaca a primeira fatia
)

plt.title('Distribuição de Pedidos por Tipo de Pagamento')
plt.ylabel('') # Remove o label do eixo Y para ficar mais limpo
plt.show()

# Salvar o arquivo final
nome_arquivo = 'pedidos_processados_etl.csv'
df_final.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')

print(f"ETL Concluído! Arquivo '{nome_arquivo}' gerado.")
print("-" * 30)
print(df_final.head())