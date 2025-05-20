# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path
import streamlit as st
import funcoes as f
import plotly.express as px
from tabela_indice import *


######### INICIANDO A CRIAÇÃO DA PÁGINA
# CONFIGURANDO A PÁGINA
st.set_page_config(
     layout='wide',
     page_title='Dash TAF - 10º BIL Mth',
 )

# CSS personalizado para remover espaçamento e definir cor de fundo
st.markdown(f.config_pagina, unsafe_allow_html=True)

@st.cache_data #Jogando a tabela para a memória, não precisa carregar toda vez
def pega_excel(arquivo):
    arquivo_excel = pd.ExcelFile(arquivo)#variável recebe todo o arquivo exel com suas abas
    dfs = [pd.read_excel(arquivo_excel,sheet_name=sheet).assign(TAF=sheet) for sheet in arquivo_excel.sheet_names] #cria uma lista com as abas da planilha
    tabela_tafs = pd.concat(dfs,ignore_index=True)#concatena as abas da planilha em uma só
    return tabela_tafs

uploaded_file = st.file_uploader("CAREEGUE A PLANILHA DO TAF NO BOTÃO ABAIXO")
if uploaded_file is not None:
    tabela_tafs = pega_excel(uploaded_file)#carrega a tabela para um dataframe
    tabela_tafs.reset_index(inplace=True, drop=True)
    #limpando as colunas 'rolhas'
    tabela_tafs.drop(columns=['OBS','BI Publicado'], inplace=True)

    #TÍTULO
    st.markdown("<h2 style='text-align: center;'>TAF - 10º BIL Mth</h2>", unsafe_allow_html=True)

    
   

    col1, col2 = st.columns([0.3,0.7], vertical_alignment='top', border=True)
    #Montando o menu da esqueda
    with col1:
        #Coletando as opções na coluna do TAF
        op_taf = tabela_tafs["TAF"].unique()
        #Botões e filtros para o TAF
        with st.container(border=True):
            taf_selecionados = st.pills("# Selecione o TAF", op_taf, selection_mode="multi")
            if taf_selecionados:
                tabela_final = tabela_tafs[tabela_tafs['TAF'].isin(taf_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
            else:
                tabela_final = tabela_tafs.copy()
        
        #coletando as opções de segmento
        op_seg = tabela_final["SEGMENTO"].unique()
        #Filtro para segmento
        with st.container(border=True):
            seg_selecionados = st.pills("Selecione o Segmento", op_seg, selection_mode="multi")
            if seg_selecionados:
                tabela_final = tabela_final[tabela_final['SEGMENTO'].isin(seg_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
        
        #coletando as opções de posto e graduação
        op_pg = tabela_final["P/G"].unique()
        #Filtro Posto e Graduação
        with st.container(border=True):
            pg_selecionados = st.pills("Selecione o Posto/Graduação", op_pg, selection_mode="multi")
            if pg_selecionados:
                tabela_final = tabela_final[tabela_final['P/G'].isin(pg_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
        
        #Coletando as opções de subunidade
        op_su = tabela_final["COMPANHIA"].unique()
        #Filtro Posto e Graduação
        with st.container(border=True):
            su_selecionados = st.pills("Selecione a Companhia/Fração", op_su, selection_mode="multi")
            if su_selecionados:
                tabela_final = tabela_final[tabela_final['COMPANHIA'].isin(su_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)
        
        #coletando as opções de chamada
        op_ch = tabela_final["CHAMADA"].unique()
        #Filtro Chamadas
        with st.container(border=True):
            ch_selecionados = st.pills("Selecione a Chamada", op_ch, selection_mode="multi")
            if ch_selecionados:
                tabela_final = tabela_final[tabela_final['CHAMADA'].isin(ch_selecionados)]
                tabela_final.reset_index(inplace=True, drop=True)


    #CRIA UMA TABELA COM AS MENÇÕES POR ATIVIDADE
    tabela_mencao_atividades = f.criar_coluna_mencao_atividade(tabela_final)



    #Montando a coluna dos gráficos
    with col2:
        #coletando as opções de atividade e menção
        op_atv = tabela_tafs.columns[5:10]
        atv_selecionados = st.pills("Selecione a opção para combinação dos gráficos", op_atv, selection_mode="multi")
        #devolvendo boleanos para as variaveis corrida, flexão, abdominal, barra e mencao para poder utilizar nas funções de gráficos
        corrida, flexao, abdominal, barra, mencao = f.devolve_boleanos(atv_selecionados)
        atividades = (corrida, flexao, abdominal, barra, mencao)
        #CORRIDA
        if (False, False, False, False, True) == atividades:
            st.pyplot(f.grafico_pizza(tabela_final, 'MENÇÃO'))
        elif (False, False, False, False, False) == atividades:
            st.write("Escolha uma ou mais opções.")
        else:
            st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
        
        
    #Mostrar tabela no final
    if st.button('Mostrar Tabela filtrada'): #,on_click=None):
        tabela_final
else:
    st.write("Aguardando carregamento da planilha")





# #Tabela só com os NR
# tabela_NR = tabela_filtrada_idade[((tabela_filtrada_idade['IDADE']=='NR') | (tabela_filtrada_idade['MENÇÃO']=='NR'))]



# if idade:
#     if corrida:
#         if flexao:
#             if abdominal:
#                 if barra:
#                     if mencao:#Todos os itens
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                         #with mid_col:
#                             # st.subheader(f'Para idade entre {escolha_idade}')
#                             # st.dataframe(tabela_filtrada_idade.drop(columns=['COMPANHIA', 'CHAMADA','TAF',]))
#                     else:#IDADE - CORRIDA - FLEXÃO - ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# IDADE - CORRIDA - FLEXÃO - ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - CORRIDA - FLEXÃO - ABDOMINAL
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#             else:
#                 if barra:
#                     if mencao:#IDADE - CORRIDA - FLEXÃO - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - CORRIDA - FLEXÃO - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# IDADE - CORRIDA - FLEXÃO - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - CORRIDA - FLEXÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#         else:
#             if abdominal:
#                 if barra:
#                     if mencao:# IDADE - CORRIDA - ABDOMINAL - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - CORRIDA - ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# IDADE - CORRIDA - ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - CORRIDA - ABDOMINAL
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#             else:
#                 if barra:
#                     if mencao:#IDADE - CORRIDA - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - CORRIDA - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# IDADE - CORRIDA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else: #IDADE E CORRIDA
#                         col5.write(f'Este gráfico de disperção mostra o desempenho na CORRIDA por SEGMENTO E IDADE -> {escolha_idade} anos')
#                         with col6:
#                             f.idade_seg_atv(tabela_filtrada_idade, 'CORRIDA')
#     else:# corrida não
#         if flexao:
#             if abdominal:
#                 if barra:
#                     if mencao:# IDADE - FLEXÃO - ABDOMINAL - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - FLEXÃO - ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# IDADE - FLEXÃO - ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# IDADE - FLEXÃO - ABDOMINAL
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#             else: #corrida abdominal não
#                 if barra:
#                     if mencao:# IDADE - FLEXÃO - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - FLEXÃO - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:#barra não
#                     if mencao:# IDADE - FLEXÃO - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# IDADE E FLEXÃO
#                         col5.write(f'Este gráfico de disperção mostra o desempenho na FLEXÃO DE BRAÇO por SEGMENTO E IDADE -> {escolha_idade} anos')
#                         with col6:
#                             f.idade_seg_atv(tabela_filtrada_idade, 'FLEXÃO')
#         else: #corrida - flexão - não
#             if abdominal:
#                 if barra:
#                     if mencao:# IDADE - ABDOMINAL - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#IDADE - ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# IDADE - ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# IDADE E ABDOMINAL
#                         col5.write(f'Este gráfico de disperção mostra o desempenho no ABDOMINAL por SEGMENTO E IDADE -> {escolha_idade} anos')
#                         with col6:
#                             f.idade_seg_atv(tabela_filtrada_idade, 'ABDOMINAL')
#             else: #corrida - flexão - abdominal
#                 if barra:
#                     if mencao:# IDADE - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else: #IDADE E BARRA
#                         col5.write(f'Este gráfico de disperção mostra o desempenho na BARRA por SEGMENTO E IDADE -> {escolha_idade} anos')
#                         with col6:
#                             f.idade_seg_atv(tabela_filtrada_idade, 'BARRA')
#                 else:#barra não
#                     if mencao:#MENÇÃO E IDADE
#                         with col5:
#                             st.write('O gráfico apresenta a distribuição da menção final do(s) TAF(s) selecionado(s), podendo ser alterado o SEGMENTO e a IDADE')
#                         with col6:
#                             st.pyplot(f.grafico_pizza(tabela_filtrada_idade, "MENÇÃO"))
#                         with col6:
#                             fig_mencoes = f.graf_linhas_mencoes_por_taf(tabela_filtrada_idade)
#                             st.plotly_chart(fig_mencoes, use_container_width=True)
#                     else:#SOMENTE IDADE
#                         col5.write('**SIM** - idade')
#                         col6.write('**NÃO** - corrida - flexão - abdominal - barra - menção')
# else: #idade não
#     if corrida:
#         if flexao:
#             if abdominal:
#                 if barra:
#                     if mencao:
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                     else: # CORRIDA - FLEXÃO - ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
                       
#                 else:#idade - barra -não
#                     if mencao:# CORRIDA - FLEXÃO - ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# CORRIDA - FLEXÃO - ABDOMINAL
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#             else:#idade - abdominal não
#                 if barra:
#                     if mencao:# CORRIDA - FLEXÃO - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# CORRIDA - FLEXÃO - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# CORRIDA - FLEXÃO - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#CORRIDA - FLEXÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#         else:
#             if abdominal:
#                 if barra:
#                     if mencao:# CORRIDA - ABDOMINAL - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#CORRIDA - ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# CORRIDA - ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#CORRIDA - ABDOMINAL
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#             else:
#                 if barra:
#                     if mencao:# CORRIDA - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#CORRIDA - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:#CORRIDA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#SOMENTE CORRIDA
#                         tabela_filtrada_idade = tabela_filtrada_idade[~((tabela_filtrada_idade["CORRIDA"] == 'A') | (tabela_filtrada_idade["CORRIDA"].isna()) | (tabela_filtrada_idade["CORRIDA"] == 'X'))] # trata a tabela para tirar "A", nulo e 'X'
#                         tabela_filtrada_idade["Menção na corrida"] = tabela_filtrada_idade.apply(lambda row: f.determinar_mencao(row['IDADE'],dicio_atividades,'CORRIDA', row['LEM'], row['SEGMENTO'], row['CORRIDA']), axis=1)
#                         with col5:
#                             st.dataframe(tabela_filtrada_idade["Menção na corrida"].value_counts())
#                         with col6:
#                             st.pyplot(f.grafico_pizza(tabela_filtrada_idade, "Menção na corrida"))
#     else:# corrida não
#         if flexao:
#             if abdominal:
#                 if barra:
#                     if mencao:# FLEXÃO - ABDOMINAL - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#FLEXÃO - ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# FLEXÃO - ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#FLEXÃO - ABDOMINAL
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#             else: #corrida abdominal não
#                 if barra:
#                     if mencao:# FLEXÃO - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# FLEXÃO - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:#barra não
#                     if mencao:# FLEXÃO - MENÇÃO
#                         col5.write('**SIM** - flexão - menção')
#                         col6.write('**NÃO** -idade -  corrida - abdominal - barra')
#                     else: #SOMENTE FLEXÃO
#                         tabela_filtrada_idade = tabela_filtrada_idade[~((tabela_filtrada_idade["FLEXÃO"] == 'A') | (tabela_filtrada_idade["FLEXÃO"].isna()) | (tabela_filtrada_idade["FLEXÃO"] == 'X'))] # trata a tabela para tirar "A", nulo e 'X'
#                         tabela_filtrada_idade["Menção na flexão"] = tabela_filtrada_idade.apply(lambda row: f.determinar_mencao(row['IDADE'],dicio_atividades,'FLEXAO', row['LEM'], row['SEGMENTO'], row['FLEXÃO']), axis=1)
#                         with col5:
#                             st.dataframe(tabela_filtrada_idade["Menção na flexão"].value_counts())
#                         with col6:
#                             st.pyplot(f.grafico_pizza(tabela_filtrada_idade, "Menção na flexão"))
#         else: #corrida - flexão - não
#             if abdominal:
#                 if barra:
#                     if mencao:# ABDOMINAL - BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:#ABDOMINAL - BARRA
#                         col5.write('Gráfico comparativo das menções por cada atividade')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra))
#                 else:
#                     if mencao:# ABDOMINAL - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# SOMENTE ABDOMINAL
#                         tabela_filtrada_idade = tabela_filtrada_idade[~((tabela_filtrada_idade["ABDOMINAL"] == 'A') | (tabela_filtrada_idade["ABDOMINAL"].isna()) | (tabela_filtrada_idade["ABDOMINAL"] == 'X'))] # trata a tabela para tirar "A", nulo e 'X'
#                         tabela_filtrada_idade["Menção no abdominal"] = tabela_filtrada_idade.apply(lambda row: f.determinar_mencao(row['IDADE'],dicio_atividades,'ABDOMINAL', row['LEM'], row['SEGMENTO'], row['ABDOMINAL']), axis=1)
#                         with col5:
#                             st.dataframe(tabela_filtrada_idade["Menção no abdominal"].value_counts())
#                         with col6:
#                             st.pyplot(f.grafico_pizza(tabela_filtrada_idade, "Menção no abdominal"))
#             else: #corrida - flexão - abdominal
#                 if barra:
#                     if mencao:# BARRA - MENÇÃO
#                         col5.write('Gráfico comparativo das menções por cada atividade com a menção geral')
#                         with col6:
#                             st.plotly_chart(f.grafico_linha(tabela=tabela_mencao_atividades, corrida=corrida, flexao=flexao, abdominal=abdominal, barra=barra, mencao=mencao))
#                     else:# SOMENTE BARRA
#                         tabela_filtrada_idade = tabela_filtrada_idade[~((tabela_filtrada_idade["BARRA"] == 'A') | (tabela_filtrada_idade["BARRA"].isna()) | (tabela_filtrada_idade["BARRA"] == 'X'))] # trata a tabela para tirar "A", nulo e 'X'
#                         tabela_filtrada_idade["Menção na barra"] = tabela_filtrada_idade.apply(lambda row: f.determinar_mencao(row['IDADE'],dicio_atividades,'BARRA', row['LEM'], row['SEGMENTO'], row['BARRA']), axis=1)
#                         with col5:
#                             st.dataframe(tabela_filtrada_idade["Menção na barra"].value_counts())
#                         with col6:
#                             st.pyplot(f.grafico_pizza(tabela_filtrada_idade, "Menção na barra"))
#                 else:#barra não
#                     if mencao:#SOMENTE MENÇÃO
#                         with col5:
#                             st.write('O gráfico apresenta a distribuição da menção final do(s) TAF(s) selecionado(s), podendo ser alterado o SEGMENTO e a IDADE')
#                         with col6:
#                             st.pyplot(f.grafico_pizza(tabela_filtrada_idade, "MENÇÃO"))
#                         with col6:
#                             fig_mencoes = f.graf_linhas_mencoes_por_taf(tabela_filtrada_idade)
#                             st.plotly_chart(fig_mencoes, use_container_width=True)
#                     else:#(tudo desmarcado)
#                         with mid_col:
#                             st.write('NENHUMA ATIVIDADE OU MENÇÃO SELECIONADA')

