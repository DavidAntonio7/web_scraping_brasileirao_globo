# web_scraping_brasileirao_globo
* Web scraping na tabela do brasileirao da globo.com
* Feito atraves da posição dos objetos no display (precisando da localizao da seta anterior e a posição final da tabela, que pode ser conseguida via pyautogui.displayMousePosition())
* Por ser feita atraves da posição do display ela não é tão efetiva quanto o web scraping premier league que localiza pelas tags csv. Porem nao pude fazer da mesma forma pois o html da globo se mostrou complexo para o webDriver (biblioteca que encontra as tags). Deste modo é importante tirar o zoom até que toda a tabela seja vista no display
* Com esse codigo peguei os dados de todos os brasileiroes de pontos corridos (adicionando um laço na main para todas as temporadas e os parametros corretos)
