import pandas as pd
from pathlib import Path
import streamlit as st
import funcoes as f
import plotly.express as px
from tabela_indice import *

#DEFININDO CAMINHO PARA O ARQUIVO, DEVERÁ ESTÁR NO MESMO DIRETÓRIO DO SCRIPT
diretorio_atual = Path.cwd()
arquivo = diretorio_atual/'PLANILHA TAF(modelo).xlsx'

arquivo_excel = pd.ExcelFile(arquivo)#variável recebe todo o arquivo exel com suas abas
dfs = [pd.read_excel(arquivo_excel,sheet_name=sheet).assign(TAF=sheet) for sheet in arquivo_excel.sheet_names] #cria uma lista com as abas da planilha
tabela_tafs = pd.concat(dfs,ignore_index=True)#concatena as abas da planilha em uma só

options = tabela_tafs['TAF'].value_counts().index

taf_1 = tabela_tafs[tabela_tafs['TAF'].isin(['1º TAF'])]


B = str(taf_1.iloc[37]['CORRIDA'])



a = f.lista_mencoes_pandas(taf_1)
erro = f.verifica_erros_lancamento(a)
sem_erro = f.limpa_mencao(a,erro)
mencao_final = f.mencao_final(a)
mencao_final_sem_erro = f.mencao_final_limpa(a)
erros_mais_especificado = f.mencao_final_erros(a)
mencao_lancada = f.mencao_lancada(taf_1)
erros_lançamento = f.erros_lancamento(mencao_lancada, mencao_final)

a['SD EV THOMAS'][1].isnan()
mencao_lancada['SD EV THOMAS']
mencao_final['SD EV THOMAS'][0]




mencao_final_sem_erro['2º SGT ALESSANDRO']
len(a)
len(erro)
len(mencao_final)
len(mencao_final_sem_erro)
len(a)-len(erro)
