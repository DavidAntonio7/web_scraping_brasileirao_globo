import head 

rodada = int(input("Digite o número de rodadas: "))

head.extrair_rodadas_globo('https://ge.globo.com/futebol/brasileirao-serie-a/',2023,rodada,(919,213),(1039,794),'txt/brasileirao2023.txt')
head.limpeza_rodadas('txt/brasileirao2023.txt',2023,rodada,10,'csv/Brasileirao_2023/Rodadas_Realizadas_2023.csv')
head.montar_classificacao('csv/Brasileirao_2023/Rodadas_Realizadas_2023.csv',rodada,20,'csv/Brasileirao_2023/Classificacao_2023.csv')


    
