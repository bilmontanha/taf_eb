import streamlit as st
import pandas as pd
from pathlib import Path
from tabela_indice import *
import funcoes as f



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
    tabela_tafs.reset_index(inplace=True, drop=True)



try:
    tabela_tafs.drop(columns=['OBS','BI Publicado'], inplace=True) #limpando a tabela das colunas rolhas
    options = tabela_tafs['TAF'].value_counts().index.sort_values()
    selection = st.pills("Selecione o TAF", options, selection_mode="multi", default=None)
    nova_tabela = tabela_tafs[tabela_tafs['TAF'].isin(selection)]
    nova_tabela.reset_index(inplace=True, drop=True)
    
    #st.dataframe(nova_tabela)
    mencao_lancada = f.mencao_lancada(nova_tabela)
    lista_de_mencoes = f.lista_mencoes_pandas(nova_tabela)
    mencao_final = f.mencao_final(lista_de_mencoes)
    erros_lancamento = f.erros_lancamento(mencao_lancada=mencao_lancada, mencao_final_limpa=mencao_final)
    erros_lancamentos = pd.DataFrame(erros_lancamento.items(), columns=['Militar', 'Situação'])

    col1, col2 = st.columns([0.3,0.7], vertical_alignment='top', border=True)
    with col1:
        opcoes_selectbox = ["Verificar erros de lançamento", "Baixar nova planilha com a correção da menção final"]
        escolha = st.selectbox("Escolha uma opção abaixo",opcoes_selectbox, index=None)

    

    with col2:
        if escolha == 'Verificar erros de lançamento':
            st.dataframe(erros_lancamentos)

            
            
        if escolha == "Baixar nova planilha com a correção da menção final":
            pass
     





except Exception as e:
    st.warning(f"Erro ao executar: '{e}'")




        
        



# #para teste
# diretorio_atual = Path.cwd()
# arquivo = diretorio_atual/'PLANILHA TAF(modelo).xlsx'
# uploaded_file = arquivo
# nova_tabela = tabela_tafs[tabela_tafs['TAF'].isin(['1º TAF'])]


