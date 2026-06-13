import pandas as pd
import numpy as np
import os

print("Diretório atual:", os.getcwd())
print("Arquivos encontrados:", os.listdir())

df = pd.read_excel('base_suja_case.xlsx', header=1)

# PARTE 1 — CARREGAR OS DADOS
df = pd.read_excel('base_suja_case.xlsx', header=1)
df = df.drop(columns=[df.columns[-1]])
df.columns = ['id_atendimento', 'data', 'c_p_f', 
              'motivo_contato', 'tempo_espera_seg']

print("Shape inicial:", df.shape)
print(df.head())



# PARTE 2 — PADRONIZAR DATAS
meses_pt = {
    'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',
    'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
}
def parse_data(valor):
    s = str(valor).strip().lower()
    # formato '15-mai-26'
    if '-' in s and any(m in s for m in meses_pt):
        dia, mes, ano = s.split('-')
        mes_num = meses_pt[mes]
        ano_completo = '20' + ano if len(ano) == 2 else ano
        return pd.Timestamp(f"{ano_completo}-{mes_num}-{dia.zfill(2)}")
    # formato '2026-05-15' ou '2026-05-15 00:00:00'
    if '-' in s:
        return pd.Timestamp(s)
    # formato '2026/06/01' (ano/mes/dia)
    if '/' in s and s.split('/')[0].isdigit() and len(s.split('/')[0]) == 4:
        return pd.Timestamp(s.replace('/', '-'))
    # formato '01/06/2026' (dia/mes/ano)
    if '/' in s:
        dia, mes, ano = s.split('/')
        return pd.Timestamp(f"{ano}-{mes}-{dia}")
    return pd.NaT

df['data'] = df['data'].apply(parse_data)
print("\nDatas nulas após conversão:", df['data'].isna().sum())


 
# PARTE 3 — PADRONIZAR CPF
df['c_p_f'] = df['c_p_f'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(11)
print("\nCPFs únicos (amostra):", df['c_p_f'].unique()[:5])



# PARTE 4 — PADRONIZAR MOTIVO DE CONTATO
mapa_motivo = {
    'cartão': 'Cartão de Crédito',
    'cartao': 'Cartão de Crédito',
    'cartão de crédito': 'Cartão de Crédito',
    'senha': 'Senha',
    'senha app': 'Senha App',
    'bloqueio': 'Bloqueio de Conta',
    'bloqueio conta': 'Bloqueio de Conta',
}

df['motivo_contato'] = df['motivo_contato'].astype(str).str.strip().str.lower().map(mapa_motivo)

print("\nMotivos padronizados:")
print(df['motivo_contato'].value_counts())
print("Motivos não mapeados (NaN):", df['motivo_contato'].isna().sum())


# PARTE 5 — PADRONIZAR TEMPO DE ESPERA
df['tempo_espera_seg'] = df['tempo_espera_seg'].astype(str).str.replace('s', '', regex=False)
df['tempo_espera_seg'] = pd.to_numeric(df['tempo_espera_seg'], errors='coerce')

print("\nNulos em tempo_espera_seg:", df['tempo_espera_seg'].isna().sum())
print(df['tempo_espera_seg'].describe())


# PARTE 6 — TRATAR NULOS (IMPUTAÇÃO POR MEDIANA)
medianas = df.groupby('motivo_contato')['tempo_espera_seg'].median()
global_median = df['tempo_espera_seg'].median()

print("\nMedianas por motivo:")
print(medianas)

df['tempo_espera_seg'] = df.apply(
    lambda row: medianas.get(row['motivo_contato'], global_median)
    if pd.isna(row['tempo_espera_seg']) else row['tempo_espera_seg'],
    axis=1
)

print("\nNulos restantes:", df['tempo_espera_seg'].isna().sum())


# PARTE 7 — VERIFICAR DUPLICADOS
print("\nLinhas com id_atendimento repetido:", df['id_atendimento'].duplicated().sum())
print("Linhas 100% idênticas (todas colunas):", df.duplicated(keep=False).sum())

# Não há linhas 100% idênticas -> não são duplicatas reais,
# apenas erro de numeração na origem. Mantemos todas as linhas
# e recriamos o ID sequencial.
df_final = df.reset_index(drop=True).copy()
df_final['id_atendimento'] = range(1, len(df_final) + 1)

print("\nShape final:", df_final.shape)


# PARTE 8 — AJUSTES FINAIS DE TIPOS
df_final['id_atendimento'] = df_final['id_atendimento'].astype(int)
df_final['tempo_espera_seg'] = df_final['tempo_espera_seg'].astype(int)
df_final['data'] = pd.to_datetime(df_final['data']).dt.date

print("\n=== BASE FINAL TRATADA ===")
print(df_final.head(10))
print(df_final.info())


# PARTE 9 — EXPORTAR
df_final.to_excel('base_tratada.xlsx', index=False)
print("\nArquivo 'base_tratada.xlsx' salvo com sucesso!")