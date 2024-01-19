


import pandas as pd
import os



class ConsolidadorDataFrame:


    
    #Função de inicialização da classe que é chamada automaticamente quando a classe é instanciada
    def __init__ (self):
        #...
        return        

    
    
    def gerar_totais (self, caminho_arquivo_csv, colunas_interesse, codificacao='iso-8859-1', separador=';'):

        display (f'Processando arquivo: {caminho_arquivo_csv}')
        
        indice_ultimo_separador = caminho_arquivo_csv.rfind("/")
        nome_arquivo = caminho_arquivo_csv [indice_ultimo_separador+1:-4] 
    
        ano = int(nome_arquivo[:4])
        mes = int(nome_arquivo[4:6])        
        
        df = pd.read_csv(caminho_arquivo_csv, encoding=codificacao, sep=separador)
    
        df_contagem_combinacoes = df.groupby(colunas_interesse).size().reset_index(name='Contagem')    
    
        df_contagem_combinacoes['ano'] = ano
        df_contagem_combinacoes['mes'] = mes
        
        return df_contagem_combinacoes


    
    def percorre_diretorio_CSV(self, diretorio, texto_filtro_arquivo, caminho_destino_csv, colunas_interesse, tamanho_bloco=12, codificacao='iso-8859-1', separador=';'):
    
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
    
            contador_arquivos_processados += 1
            
            caminho_completo = os.path.join(diretorio, subdiretorio)
            
            arquivos_subdiretorio = os.listdir(caminho_completo) 
    
            lista_arquivo = [arquivo for arquivo in arquivos_subdiretorio if arquivo.lower().find(texto_filtro_arquivo) != -1]
    
            if len(lista_arquivo) == 1:
                
                caminho_arquivo_csv = lista_arquivo[0]
    
                caminho_completo_arquivo_csv = os.path.join(caminho_completo, caminho_arquivo_csv)                        
    
                df_total = self.gerar_totais (caminho_completo_arquivo_csv, colunas_interesse, codificacao, separador)
    
                # Concatena o DataFrame atual com o DataFrame consolidado
                df_consolidado = pd.concat([df_consolidado, df_total], ignore_index=True)
            
            else:
    
                display (f'ATENÇÃO: Mais ou nenhum arquivo csv no subdiretório {caminho_completo}')
    
            
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



