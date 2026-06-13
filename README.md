# Case Prático - Dados Analytics

Projeto desenvolvido para tratamento, padronização e análise de uma base de dados contendo inconsistências comuns em ambientes corporativos.

## Objetivo

Realizar a limpeza e padronização dos dados, garantindo maior qualidade e confiabilidade das informações para análises futuras.

## Etapas Desenvolvidas

- Padronização de datas
- Padronização de CPFs
- Consolidação dos motivos de contato
- Tratamento de valores nulos
- Análise de duplicidades
- Exportação da base tratada
- Geração de gráficos
- Dashboard interativo com Streamlit

## Tecnologias Utilizadas

- Python
- Pandas
- NumPy
- Matplotlib
- OpenPyXL
- Streamlit

## Estrutura do Projeto

- `limpeza_dados.py` → tratamento da base
- `gerar_graficos.py` → geração das análises visuais
- `app.py` → dashboard Streamlit
- `base_tratada.xlsx` → base final tratada

## Como Executar

```bash
pip install pandas numpy matplotlib openpyxl streamlit
