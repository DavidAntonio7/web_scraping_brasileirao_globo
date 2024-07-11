def abrir_brave(site):
    import pyautogui as pag
    import time
    pag.hotkey('win','r') 
    time.sleep(0.5)   
    pag.write('brave')
    pag.keyDown('enter')
    time.sleep(2)
    pag.keyDown('F5')
    time.sleep(2) 
    pag.write(site)
    time.sleep(0.5) 
    pag.keyDown('enter')
    time.sleep(2)

def abrir_pagina(site):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    import pyautogui as pag
    
    ################################Entrar na pagina
    driver = webdriver.Chrome()
    driver.get(site)
    time.sleep(5)
    
    ############################### deixar a tabela visivel na pagina inteira
    pag.hotkey('F11')
    for i in range(6):
        pag.hotkey('ctrl','-')
        time.sleep(0.5)
        
    return driver


def contar_linhas_entre_rodadas(arquivo):
    with open(arquivo,'r') as arquivo:
        texto = arquivo.readlines()
        arquivo.close
        
    texto_sem_linhas_em_branco = [palavras.replace('\n','') for palavras in texto if palavras not in '\n']
    contador_linhas = 0
    contador_rodadas = 0
    index = []
    
    for i in range(0,len(texto_sem_linhas_em_branco)-1):
        if 'RODADA'  in texto_sem_linhas_em_branco[i]:
            contador_rodadas +=1
            index.append(i)
        if contador_rodadas == 2:
            break
        else:
            contador_linhas +=1
    return contador_linhas
  

def limpeza_rodadas(nome_arquivo,ano,numero_rodadas, numero_jogos,nome_arquivo_gerado):
    import pandas            as pd
    import numpy             as np
    
    todos_jogos = []

    
    ##Abre os arquivos
    with open(nome_arquivo,'r',encoding='utf-8') as arquivo:
        texto = arquivo.readlines()
        arquivo.close()
        
    ##apaga os /n
    texto_sem_linhas_em_branco = [palavras.replace('\n','') for palavras in texto if palavras not in '\n']
    
    numero_linhas_entre_rodadas = contar_linhas_entre_rodadas(nome_arquivo)
    ##monta a lista apenas com os dados importantes e ja em formato de dataFrame
    for rodada in range(numero_rodadas-1,-1, -1):
        for jogo in range(0,numero_jogos):
            mandante = (texto_sem_linhas_em_branco[numero_linhas_entre_rodadas*rodada+3+jogo*8])
            mandante_placar = (texto_sem_linhas_em_branco[numero_linhas_entre_rodadas*rodada+4+jogo*8])
            visitante_placar = (texto_sem_linhas_em_branco[numero_linhas_entre_rodadas*rodada+5+jogo*8])
            visitante = (texto_sem_linhas_em_branco[numero_linhas_entre_rodadas*rodada+6+jogo*8])
            todos_jogos.append([ano,numero_rodadas-rodada,mandante,visitante,mandante_placar,visitante_placar])

    df_rodadas = pd.DataFrame(todos_jogos,columns=['Temporada','Rodada','Mandante','Visitante','Mandante Placar','Visitante Placar'])
    df_rodadas[['Mandante Placar','Visitante Placar']] = df_rodadas[['Mandante Placar','Visitante Placar']].astype(int)
    df_rodadas.sort_values(['Temporada','Rodada'],inplace=True)
    df_rodadas.to_csv(nome_arquivo_gerado,index=False,encoding='utf-8')

def limpeza_rodadas_nao_realizadas_globo(nome_arquivo,ano,ultima_rodada_realizada,total_rodadas,numero_jogos_rodada,nome_arquivo_gerado):
    import pandas as pd
    with open(nome_arquivo,'r',encoding='utf-8') as arquivo:
      texto = arquivo.readlines()
      arquivo.close()
    texto_sem_linhas_em_branco = [palavras.replace('\n','') for palavras in texto if palavras not in '\n']
    texto_limpo = [texto for texto in texto_sem_linhas_em_branco if texto not in 'FIQUE POR DENTRO']

    todos_jogos = []
    ultima_rodada_realizada +=1
    numero_linhas_entre_rodadas = contar_linhas_entre_rodadas(nome_arquivo)
    for rodada in range(ultima_rodada_realizada,total_rodadas+1):
      for jogo in range(0,numero_jogos_rodada):
        mandante = (texto_limpo[numero_linhas_entre_rodadas*(rodada-ultima_rodada_realizada)+3+jogo*5])
        visitante = (texto_limpo[numero_linhas_entre_rodadas*(rodada-ultima_rodada_realizada)+4+jogo*5])
        todos_jogos.append([ano,rodada,mandante,visitante])

    texto_sem_linhas_em_branco = [palavras.replace('\n','') for palavras in texto if palavras not in '\n']
    texto_limpo = [texto for texto in texto_sem_linhas_em_branco if texto not in 'FIQUE POR DENTRO']

    df_rodadas_faltantes = pd.DataFrame(todos_jogos,columns=['Temporada','Rodada','Mandante','Visitante'])
    df_rodadas_faltantes.sort_values(['Temporada','Rodada'],inplace=True)
    df_rodadas_faltantes.to_csv(nome_arquivo_gerado,index=False,encoding='utf-8')

def extrair_rodadas_nao_realizadas(site,ano, ultima_rodada,numero_de_rodadas, posicao_seta_rodada_anterior, posicao_seta_rodada_posterior, posicao_fim_tabela, nome_arquivo_gerado):
    import time
    import pyautogui as pag
    import pyperclip 
    driver = abrir_pagina(site)
       
    conteudo_clipboard = ''
    for i in range(ultima_rodada,numero_de_rodadas+1):
        
        if i == ultima_rodada:
            time.sleep(2)
            pag.click(posicao_seta_rodada_posterior[0],posicao_seta_rodada_posterior[1])
        else:
            pag.moveTo(posicao_seta_rodada_anterior[0],posicao_seta_rodada_anterior[1],1)
            pag.dragTo(posicao_fim_tabela[0],posicao_fim_tabela[1],1)
            time.sleep(1)
            pag.hotkey('ctrl','c')
            conteudo_clipboard = conteudo_clipboard + '\n' + pyperclip.paste() 
            
            pag.click(posicao_seta_rodada_posterior[0],posicao_seta_rodada_posterior[1])
            time.sleep(4.5)
    

    with open(nome_arquivo_gerado,'w',encoding='utf-8') as arquivo:
        arquivo.write(conteudo_clipboard + '\n')
        arquivo.close()
    driver.quit()


def extrair_rodadas_globo(site,ano, numero_rodadas, posicao_seta_rodada_anterior, posicao_fim_tabela, nome_arquivo_gerado):
    import time
    import pyautogui as pag
    import pyperclip 
    #driver = abrir_pagina(site)
    abrir_brave(site)  
    conteudo_clipboard = ''
    for i in range(numero_rodadas):
        
        pag.moveTo(posicao_seta_rodada_anterior[0],posicao_seta_rodada_anterior[1],1)
        pag.dragTo(posicao_fim_tabela[0],posicao_fim_tabela[1],1)
        time.sleep(1)
        pag.hotkey('ctrl','c')
        
        conteudo_clipboard = conteudo_clipboard + '\n' + pyperclip.paste() 
        
        pag.click(posicao_seta_rodada_anterior[0],posicao_seta_rodada_anterior[1])
        time.sleep(4.5)
    

    with open(nome_arquivo_gerado,'w',encoding='utf-8') as arquivo:
        arquivo.write(conteudo_clipboard + '\n')
        arquivo.close()
    pag.hotkey('ctrl','w')
    #driver.quit()

def montar_classificacao(arquivo_rodadas,numero_rodadas,numero_times,arquivo_gerado):
    import numpy as np
    import pandas as pd
    
    rodadas = pd.read_csv(arquivo_rodadas)
    
    times_mandante = rodadas.copy()
    times_mandante['Time'] = times_mandante.Mandante
    times_mandante['Mando_de_campo'] = 1

    times_visitante = rodadas.copy()
    times_visitante['Time'] = times_visitante.Visitante
    times_visitante['Mando_de_campo'] = -1
    
    df_times = pd.concat([times_mandante,times_visitante]).sort_values('Rodada')
    
    condicao = [df_times['Mandante Placar'] == df_times['Visitante Placar'],df_times['Mandante Placar'] 
                >= df_times['Visitante Placar'],df_times['Mandante Placar'] <= df_times['Visitante Placar']]
    escolhas = ['-',df_times['Mandante'],df_times['Visitante']]
    df_times['Vencedor'] = np.select(condicao, escolhas)

    #organizando
    df_times = df_times[['Time','Temporada','Rodada', 'Mandante', 'Visitante', 'Vencedor',
       'Mandante Placar', 'Visitante Placar','Mando_de_campo']]

    #novas colunas
    df_times[['Pontos','Vitoria','Derrota','Empate','Gols_pro','Gols_contra','Saldo_de_gols',
    'Vitorias_consecutivas','Derrotas_consecutivas','Jogos_marcando','Jogos_sem_sofrer_gols']] = 0
    
    def calculaTabela(x):
        pontos = 0;vitorias = 0;derrotas = 0;empates = 0;gols_pro = 0;gols_contra = 0;vitorias_consecutivas = 0;
        derrotas_consecutivas = 0;jogos_marcando = 0;jogos_sem_sofrer_gols = 0;vencedor = 0
        for i in range(0,x.shape[0]):
            ##se o time for visitante
            if x.iloc[i].Time == x.iloc[i].Visitante:
                ##pontos - vitorias - derrotas - empates - vitorias concecutivas - derrotas concecutivas
                if x.iloc[i].Visitante == x.iloc[i].Vencedor: #vencedor
                    vitorias += 1;vitorias_consecutivas += 1; derrotas_consecutivas = 0; pontos+=3
                elif x.iloc[i].Mandante == x.iloc[i].Vencedor:
                    derrotas+= 1;vitorias_consecutivas = 0; derrotas_consecutivas +=1; pontos+=0
                else:
                    empates+= 1;vitorias_consecutivas = 0; derrotas_consecutivas = 0; pontos+=1
                ##metricas de gols
                gols_pro += x.iloc[i]['Visitante Placar']; gols_contra += x.iloc[i]['Mandante Placar'];
                if x.iloc[i]['Visitante Placar'] > 0:
                    if jogos_marcando >= 0:
                        jogos_marcando+=1
                    else:
                        jogos_marcando = 1
                elif x.iloc[i]['Visitante Placar'] <= 0:
                    if jogos_marcando >= 0:
                        jogos_marcando = -1
                    else:
                        jogos_marcando += -1
                if x.iloc[i]['Mandante Placar'] > 0:
                    if jogos_sem_sofrer_gols >= 0:
                        jogos_sem_sofrer_gols = -1
                    else:
                        jogos_sem_sofrer_gols -= 1
                elif x.iloc[i]['Mandante Placar'] == 0:
                    if jogos_sem_sofrer_gols >= 0:
                        jogos_sem_sofrer_gols = +1
                    else:
                        jogos_sem_sofrer_gols += 1
            ##se o time for mandante
            if x.iloc[i].Time == x.iloc[i].Mandante:
                ##pontos - vitorias - derrotas - empates - vitorias concecutivas - derrotas concecutivas
                if x.iloc[i].Mandante == x.iloc[i].Vencedor: #vencedor
                    vitorias += 1;vitorias_consecutivas += 1; derrotas_consecutivas = 0; pontos+=3
                elif x.iloc[i].Visitante == x.iloc[i].Vencedor:
                    derrotas+= 1;vitorias_consecutivas = 0; derrotas_consecutivas +=1; pontos+=0
                else:
                    empates+= 1;vitorias_consecutivas = 0; derrotas_consecutivas = 0; pontos+=1
                ##metricas de gols
                gols_pro += x.iloc[i]['Mandante Placar']; gols_contra += x.iloc[i]['Visitante Placar'];
                if x.iloc[i]['Mandante Placar'] > 0:
                    if jogos_marcando >= 0:
                        jogos_marcando+=1
                    else:
                        jogos_marcando = 1
                elif x.iloc[i]['Mandante Placar'] <= 0:
                    if jogos_marcando >= 0:
                        jogos_marcando = -1
                    else:
                        jogos_marcando += -1
                if x.iloc[i]['Visitante Placar'] > 0:
                    if jogos_sem_sofrer_gols >= 0:
                        jogos_sem_sofrer_gols = -1
                    else:
                        jogos_sem_sofrer_gols -= 1
                elif x.iloc[i]['Visitante Placar'] == 0:
                    if jogos_sem_sofrer_gols >= 0:
                        jogos_sem_sofrer_gols = +1
                    else:
                        jogos_sem_sofrer_gols = 1
            x.iloc[i,9:] = [pontos,vitorias,derrotas,empates,gols_pro,gols_contra,(gols_pro-gols_contra),vitorias_consecutivas,derrotas_consecutivas,
        jogos_marcando,jogos_sem_sofrer_gols]
        return x
    
    df_tabela = df_times.copy()
    
    for temporada in range(df_tabela.Temporada.min(), df_tabela.Temporada.max()+1):
        for time in df_tabela[df_tabela['Temporada'] == temporada]['Time'].unique():
            selecao = df_tabela[(df_tabela['Temporada'] == temporada) & (df_tabela['Time'] == time)].copy()
            resultado = calculaTabela(selecao)
            df_tabela.loc[(df_tabela['Temporada'] == temporada) & (df_tabela['Time'] == time)] = resultado

    df_tabela.sort_values(['Temporada','Rodada','Pontos','Vitoria','Saldo_de_gols'],ascending=[True,True,False,False,False],inplace=True)
    
    for temporada in range(df_tabela.Temporada.min(),df_tabela.Temporada.max()+1):
        for rodada in range(1,numero_rodadas+1):
            df_tabela.loc[(df_tabela.Rodada == rodada) & (df_tabela.Temporada == temporada), 'Posicao'] = range(1, numero_times+1)
        
    df_tabela =  df_tabela[[
                        'Time', 'Temporada', 'Rodada', 'Posicao', 'Pontos', 'Vitoria',
                       'Derrota', 'Empate', 'Gols_pro', 'Gols_contra', 'Saldo_de_gols',
                       'Vitorias_consecutivas', 'Derrotas_consecutivas', 'Jogos_marcando',
                       'Jogos_sem_sofrer_gols'
                      ]].copy()
    
    df_tabela['Posicao'] = df_tabela['Posicao'].astype(int)
    
    df_tabela.to_csv(arquivo_gerado,index=None)