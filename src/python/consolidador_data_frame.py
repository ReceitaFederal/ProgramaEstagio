


import pandas as pd
import os



class ConsolidadorDataFrame:


    
    #Função de inicialização da classe que é chamada automaticamente quando a classe é instanciada
    def __init__ (self):
        #...
        return        

    
    def consolidar(self, diretorio_csv, funcao_filtro, dicionario_parametros_funcao_filtro, codificacao='iso-8859-1', separador=';'):
                
        indice_ultimo_separador = diretorio_csv.rfind("/")
        nome_diretorio = diretorio_csv [indice_ultimo_separador+1:] 
    
        ano = nome_diretorio[:4]
        mes = nome_diretorio[4:6]
        
        
        caminho_arquivo_cadastro = f'{diretorio_csv}/{ano}{mes}_Cadastro.csv'
        caminho_arquivo_remuneracao = f'{diretorio_csv}/{ano}{mes}_Remuneracao.csv'
        
        df_cadastro = pd.read_csv(caminho_arquivo_cadastro, encoding=codificacao, sep=separador)
        df_remuneracao = pd.read_csv(caminho_arquivo_remuneracao, encoding=codificacao, sep=separador)

        #TODO: Remover servidores duplicados
        
        
        df = pd.merge(df_cadastro, df_remuneracao, on=["Id_SERVIDOR_PORTAL"], how="left")
            
        
        df_filtrado = funcao_filtro(df, dicionario_parametros_funcao_filtro)
    
        df_filtrado['ano'] = int(ano)
        df_filtrado['mes'] = int(mes)
        df_filtrado['ano_mes'] = df_filtrado['ano'].astype(str) + '-' + df_filtrado['mes'].astype(str).str.zfill(2)
        
        return df_filtrado
    
    
    def gerar_totais_colunas_interesse (self, df, dicionario_parametros_funcao_filtro):

        display (f'{type(self)} --- {type(df)} --- {type (dicionario_parametros_funcao_filtro)}')
        
        df_contagem_combinacoes = df.groupby(dicionario_parametros_funcao_filtro['colunas_interesse']).size().reset_index(name='Contagem')    

        return df_contagem_combinacoes



    def filtrar_dataframe_cargos_analista_auditor (self, df, dicionario_parametros_funcao_filtro):
       
        linhas_uorg_lotacao_invalida = df.loc[df['UORG_LOTACAO'] == 'Inválido']

        df.loc [linhas_uorg_lotacao_invalida, 'UORG_LOTACAO'] = df.loc[linhas_uorg_lotacao_invalida, 'UORG_EXERCICIO']
        
        df.loc[df['UORG_LOTACAO'] == 'Inválido', 'UORG_LOTACAO'] = df['UORG_EXERCICIO']

        # Filtra o dataframe para pegar apenas auditores e analistas da receita federal
        filtro_analista = df['DESCRICAO_CARGO'].str.contains('ANALISTA TRIBUTARIO REC FEDERAL BRASIL', case=False, na=False)
        filtro_auditor =  df['DESCRICAO_CARGO'].str.contains('RECEITA FEDERAL BRASIL', case=False, na=False)

        df_filtrado_auditor_analista = df[filtro_analista | filtro_auditor]                    

        # Extrai uma lista com todos os UORG únicos que tem auditor ou analista trabalhando
        lista_uorg_lotacao = df_filtrado_auditor_analista.value_counts("UORG_LOTACAO").index

        # Remove do dataframe original apenas quem for dar uorg que tem auditor e analista trabalhando
        df_filtrado = df[df['UORG_LOTACAO'].isin(lista_uorg_lotacao)]
        
        return df_filtrado



    def filtrar_dataframe_valor_procurado (self, df, dicionario_parametros_funcao_filtro):

        df_filtrado = df[df[dicionario_parametros_funcao_filtro['nome_coluna'].str.contains(dicionario_parametros_funcao_filtro['valor_procurado'], case=False, na=False)]]
        
        return df_filtrado
    

    
    def percorre_diretorio_CSV(self, diretorio, texto_filtro_arquivo, caminho_destino_csv, funcao_filtro, dicionario_parametros_funcao_filtro, tamanho_bloco=12, codificacao='iso-8859-1', separador=';', ano_inicio=None):
    
        #Declarando variáveis globais para o escopo da função percorre_diretorio_CSV
        #elas serão usadas na função salvar_e_reiniciar_parte
        global numero_parte
        global contador_arquivos_processados    
        global df_consolidado
    
        
        #Variáveis para calcular tamanho da parte    
        numero_parte = 0        
        contador_arquivos_processados = 0
    
        
        #Dataframe para consolidação
        df_consolidado = pd.DataFrame()
    
        
        
        def salvar_e_reiniciar_parte():
    
            #Referenciando as variáveis globais criadas pela função pai percorre_diretorio_CSV
            global numero_parte
            global contador_arquivos_processados
            global df_consolidado        
            
            numero_parte += 1
                
            #colocar número da parte no nome do CSV consolidado       
            nome_destino_csv = f'{caminho_destino_csv[:-4]}_parte_{numero_parte}{caminho_destino_csv[-4:]}'
    
            display (f'*********************** Salvando arquivo de parte: {nome_destino_csv}')
            
            #Salva o bloco atual
            df_consolidado.to_csv(nome_destino_csv, index=False)
            
            #Reinicia o Dataframe
            df_consolidado = pd.DataFrame()
    
            contador_arquivos_processados = 0
    
        
        
        # Lista todos os arquivos no diretório
        arquivos = os.listdir(diretorio)    
        
        # Filtra apenas os subdiretorios, excluindo arquivos
        subdiretorios = [arquivo for arquivo in arquivos if os.path.isdir(os.path.join(diretorio, arquivo))]
    
        
        # Ordena os subdiretórios alfabeticamente
        subdiretorios_ordenados = sorted(subdiretorios)
        
        
        # Itera a lista de subdiretorios
        for subdiretorio in subdiretorios_ordenados:

            ano_subdiretorio = int(subdiretorio[0:4])
            
            if (ano_inicio == None) or (ano_subdiretorio >= ano_inicio):
            
                contador_arquivos_processados += 1
                
                caminho_completo = os.path.join(diretorio, subdiretorio)
                        
                df_total = self.consolidar(caminho_completo, funcao_filtro, dicionario_parametros_funcao_filtro, codificacao='iso-8859-1', separador=';')
                                                                                                                            
                # Concatena o DataFrame atual com o DataFrame consolidado
                df_consolidado = pd.concat([df_consolidado, df_total], ignore_index=True)                    
                
                #Se formou uma parte com TAMANHO_BLOCO arquivos a serem salvos
                if contador_arquivos_processados >= tamanho_bloco:
        
                    salvar_e_reiniciar_parte()
    
        
        #Se existe um resto de arquivos que ainda não foram salvos em uma parte
        if contador_arquivos_processados > 0:
    
                salvar_e_reiniciar_parte()




    def consolida_partes(self, diretorio, texto_filtro_arquivo, destino_csv):
    
        #Dataframe para consolidação
        df_consolidado_total= pd.DataFrame()
    
        # Lista todos os arquivos no diretório    
        arquivos_partes = os.listdir(diretorio) 
        arquivos_partes = [arquivo for arquivo in arquivos_partes if arquivo.lower().find(texto_filtro_arquivo) != -1]
    
        # Itera a lista de arquivos
        for arquivo_parte in arquivos_partes:
                    
            caminho_completo_arquivo_parte = os.path.join(diretorio, arquivo_parte) 
    
            display (f'Processando arquivo: {arquivo_parte}')
            
            #df_consolidado = pd.read_csv(caminho_completo_arquivo_parte, encoding='iso-8859-1', sep=';')
            df_consolidado = pd.read_csv(caminho_completo_arquivo_parte)
    
            # Concatena o DataFrame atual com o DataFrame consolidado
            df_consolidado_total = pd.concat([df_consolidado_total, df_consolidado], ignore_index=True)
                    
    
        display (f'Vai salvar....')
    
        #Salva o arquivo consolidado com todos os anos
        df_consolidado_total.to_csv(destino_csv, index=False)
    
    
        display (f'Finalizado!')



