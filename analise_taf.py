import streamlit as st
import pandas as pd
from pathlib import Path
from tabela_indice import *

# diretorio_atual = Path.cwd()
# arquivo = diretorio_atual/'PLANILHA TAF.xlsx'

def pega_excel(arquivo):
    arquivo_excel = pd.ExcelFile(arquivo)#variável recebe todo o arquivo exel com suas abas
    dfs = [pd.read_excel(arquivo_excel,sheet_name=sheet).assign(TAF=sheet) for sheet in arquivo_excel.sheet_names] #cria uma lista com as abas da planilha
    tabela_tafs = pd.concat(dfs,ignore_index=True)#concatena as abas da planilha em uma só
    return tabela_tafs
    

######### INICIANDO A CRIAÇÃO DA PÁGINA
# CONFIGURANDO A PÁGINA
st.set_page_config(
     layout='wide',
     page_title='Dash TAF - 10º BIL Mth',
 )
#oferecer o arquivo de modelo
with open('PLANILHA TAF(modelo).xlsx', 'rb') as file:
    arquivo_excel = file.read()

st.download_button(
    label="# Baixar a planilha modelo",
    data=arquivo_excel,
    file_name='PLANILHA TAF.xlsx',
    mime = 	'application/vnd.ms-excel',
    icon= ':material/download:',
    type= 'primary'
     )

#solicitando o upload do arquivo
uploaded_file = st.file_uploader("Faça o upload do arquivo do TAF")
if uploaded_file is not None:
    tabela_tafs = pega_excel(uploaded_file)#carrega a tabela para um dataframe


try:
    tabela_tafs.drop(columns=['OBS','BI Publicado'], inplace=True) #limpando a tabela das colunas rolhas
    options = tabela_tafs['TAF'].value_counts().index.sort_values()
    selection = st.pills("Selecione o TAF", options, selection_mode="multi")
    st.markdown(f"Você selecionou o {selection}.")
    nova_tabela = tabela_tafs[tabela_tafs['TAF'].isin(selection)]
    st.dataframe(nova_tabela)


        
        






except Exception as e:
    st.warning(f"Erro ao executar: '{e}'")