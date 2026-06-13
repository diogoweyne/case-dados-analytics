import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('base_tratada.xlsx')
df['data'] = pd.to_datetime(df['data'])

# Gráfico 1 — quantidade por motivo
plt.figure(figsize=(6,4))
df['motivo_contato'].value_counts().plot(kind='bar', color='#4C72B0')
plt.title('Atendimentos por Motivo de Contato')
plt.ylabel('Quantidade')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('grafico_motivo_contato.png', dpi=120)
plt.close()

# Gráfico 2 — tempo médio por motivo
plt.figure(figsize=(6,4))
df.groupby('motivo_contato')['tempo_espera_seg'].mean().plot(kind='bar', color='#DD8452')
plt.title('Tempo Médio de Espera por Motivo (seg)')
plt.ylabel('Segundos')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('grafico_tempo_medio.png', dpi=120)
plt.close()

# Gráfico 3 — atendimentos por data
plt.figure(figsize=(6,4))
df.groupby('data').size().plot(kind='bar', color='#55A868')
plt.title('Atendimentos por Data')
plt.ylabel('Quantidade')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('grafico_por_data.png', dpi=120)
plt.close()

print("Gráficos salvos!")