import streamlit as st
import pandas as pd


st.set_page_config(
    layout="wide",
    page_title="Home"
    )

uploaded_file = st.file_uploader('Insira aqui o arquivo',type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    descricao = pd.DataFrame({'Descrição': df['Description'].str.replace("Run Queue - ","").str.replace("sequence", "Sequence:")})
    
    detalhes = pd.DataFrame({'Detalhes' : df['Details'].fillna(0)})
    
    date = pd.DataFrame({'Data': df['Date/Time']})
    
    filtro_df = pd.concat([date,descricao,detalhes], axis=1)
    filtro_df = filtro_df.dropna(how='any')
    print(filtro_df)
    
    #df = df.dropna(inplace=True)
    data = filtro_df["Data"].str.split(" ", n = 1, expand = True) 
    date_df = pd.DataFrame(data)
    hora = date_df[1]. str.split("-",n=1, expand=True)
    dia = date_df[0]. str.split("",n=1, expand=True)
    hora_df = pd.DataFrame({'Hora' : hora[0]}) 
    dia_df = pd.DataFrame({'Dia': dia[1]})
    
    #Filtrando detalhes de cada injeção (Matéria-prima, teste, Fornecedor e POP)
    mp = filtro_df["Detalhes"].str.split("/", expand=True)
    mp['MP'] = mp[3]
    mp[['Matéria-prima','Teste','Fornecedor','POP']] = mp['MP'].str.split("_", expand=True)
    materia_prima_df = pd.DataFrame({'Matéria-prima': mp['Matéria-prima'],'Teste':mp['Teste'],'Fornecedor':mp['Fornecedor'], 'POP':mp['POP']})
    
    #Descriçao
    descricao = filtro_df["Descrição"].str.split(":", expand=True)
    descricao1 = descricao[1].str.replace(" - COQ","COQ")  
    descricao2 = descricao1.str.rsplit("- ",n=2, expand=True)
    descricao_df = pd.DataFrame({'Ação': descricao[0].str.replace("Sequence",""),'Descrição': descricao2[0],'Injeção':descricao2[2]}) 
    
    dia_hora_df = pd.concat([dia_df,hora_df], axis=1)
    final_df = pd.concat([dia_hora_df, descricao_df, materia_prima_df], axis=1)
    #final_df = final_df.drop(columns=['Data','Detalhes'])
    final_df

    