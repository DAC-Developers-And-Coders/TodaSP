# 🤖 Uso de IA no TodaSP

Este arquivo contém as principais formas que utilizamos IA durante o desenvolvimento do projeto, seguindo os seguintes requisitos:

* Nome das ferramentas de IA utilizadas e suas finalidades.
* Prompts utilizados nas ferramentas.
* Descrição das funcionalidades desenvolvidas, sugeridas ou modificadas com auxílio da IA.
* Explicação de como o grupo verificou, testou e ajustou os resultados gerados.
* Análise crítica com breve reflexão sobre os benefícios, limitações e as dificuldades encontradas durante o uso da IA.

## ⚙ Ferramentas

### ChatGPT

Utilizado para auxiliar na busca por fonte de dados, na conversão dos dados recebidos para dados válidos no banco e na elaboração do sistema de threads para permitir múltiplas execuções do Web Crawler em Scrapy.

## ℹ Prompts e análises

### Pesquisa de APIs e Fontes de Dados

#### Prompts

```
Estou desenvolvendo uma plataforma que possui informações sobre toda a cidade de São Paulo (capital), incluindo
transporte público (como estações e linhas de metrô e ônibus), estabelecimentos de saúde, segurança,
demografia e riscos de alagamento.

Você consegue pesquisar fontes de dados abertas que forneçam esses dados?
```

```
Existe alguma API que consigo usar pra coletar dados de todas as estações de metrô de São Paulo capital, e suas
respectivas linhas?
```

```
Existe alguma alternativa à API Olho Vivo, onde posso coletar dados de todos os pontos de ônibus da cidade de
São Paulo?
```

```
Preciso coletar informações sobre todas as delegacias de polícia da cidade de São Paulo para o projeto TodaSP, existe
alguma API que me permita fazer esta coleta de forma inteligente?
```

```
Como posso coletar dados de estabelecimentos de saúde em São Paulo capital? Como hospitais e postos de saúde
```

#### Fontes retornadas que foram utilizadas no projeto:

* [Transitland API](https://www.transit.land/data/feeds/f-6gy-sptrans)
* [GeoSampa WFS](https://metadados.geosampa.prefeitura.sp.gov.br/geonetwork/srv/eng/catalog.search;jsessionid=D2585C191F9FD4E123A9482ADDDCF420#/metadata/3879e65a-e9cc-4ea2-8619-2073395980cc)
* [ObservaSampa Indicadores](https://observasampa.prefeitura.sp.gov.br/index.php?page=dadosabertos)

#### Fontes encontradas pelo grupo, que foram utilizadas no projeto:

* [TrilhosAgora API](https://trilhosagora.com.br/desenvolvedores)
* [Piranot API](https://www.piranot.com.br/datax/docs/dataset-seguranca-ssp-sp)
* [DEMAS - API Dados Abertos](https://apidadosabertos.saude.gov.br/v1/)

#### Como foram feitas as escolhas de ferramentas

O grupo verificou quais informações são fornecidas pelas APIs e a forma na qual elas são fornecidas, através da documentação de cada uma, e verificou quais seriam úteis para concluir o objetivo do projeto.
Também foram estudadas as possibilidades do cruzamento de dados entre diferentes fontes (como ocorre entre a GeoSampa WFS e a Piranot API), com a finalidade de possuir um banco de dados completo.


Para a verificação dos registros retornados, o grupo comparou as informações que estavam sendo guardadas no banco de dados com a fonte oficial das APIs, quando tais fontes eram fornecidas
(como os arquivos GTFS disponibilizados pela Transitland e SPTrans), além de terem sido feitas investigações referentes a campos que retornavam sem dados.

#### Análise crítica

O ChatGPT facilitou a descoberta de fontes de dados que poderiam ser utilizadas no projeto e ajudou a compreender as diferenças entre serviços com finalidades semelhantes.
Entretanto, as sugestões precisaram ser verificadas diretamente nas APIs. Algumas fontes apresentavam falta de informações importantes para o projeto e inconsistência de dados.

A principal dificuldade foi encontrar fontes que oferecessem dados suficientemente completos e atualizados para todas as funcionalidades planejadas.

### Auxílio na utilização do Pydantic

#### Prompts

```
Em um projeto anterior, utilizei o Pydantic para transformar dados de um banco de dados local em objetos para serem
enviados por uma API em FastAPI, gostaria de entender como posso utilizar essa ferramenta para transformar os dados
recebidos pelo TodaSP (projeto que estamos discutindo) em dados no nosso banco em MongoDB.

Quero utilizar o Pydantic para criar modelos que representem os dados coletados, permitindo validar os atributos,
definir tipos de dados e estabelecer valores padrão, caso alguma informação esteja faltando.
```

```
Da forma que estou lidando com os dados recebidos das APIs, alguns valores chegam para o BaseModel como None e percebi
que definir um valor padrão no atributo não substitui automaticamente esse None pelo valor padrão.

O que posso fazer para identificar esses casos e atribuir o valor padrão?
```

#### Principais ganhos gerados pelos prompts

* Melhor entendimento da estrutra de modelos BaseModel;
* Entendimento da diferença entre atributos ausentes e atributos com valor None;
* Utilização de aliases para adaptar os nomes dos campos e armazená-los no banco de dados;
* Utilização de `@field_validator` com `mode="before"`;
* Conversão de objetos Pydantic com `model_dump()`.

#### Validação do que foi dito e retornado pela IA

A validação foi realizada durante a implementação dos modelos, analisando exemplos de dados recebidos das APIs e os comportamentos dos modelos diante de diferentes entradas. 
Também foram comparados os resultados da utilização de valores padrão e validadores.

#### Análise crítica

O Pydantic ajudou a tornar a estrutura dos dados mais consistente, reduzindo a possibilidade de armazenar documentos com formatos inesperados e o auxílio da IA foi especialmente útil para compreender 
recursos da biblioteca e identificar problemas de tipagem e validação.

Por outro lado, foi necessário ajustar as sugestões de acordo com as particularidades de cada fonte, pois nem todos os dados retornados pelas APIs seguiam o mesmo padrão, além de  avaliar cada 
atributo individualmente, visto que aplicar valores alternativos sem nenhuma avaliação poderia gerar informações incoerentes e comprometer a confiabilidade dos dados armazenados.

### Adaptação da Pipeline do Scrapy para receber o objeto do MongoDB

#### Prompt

```
Estou integrando o Scrapy ao TodaSP, que já possui uma classe responsável por criar e gerenciar a conexão com o MongoDB.
Quero adaptar minha MongoPipeline, que tenho de um projeto anterior, para receber o objeto do banco de dados e
utilizá-lo durante o processamento dos itens coletados.

Como posso transferir esse objeto do código principal para a Pipeline do Scrapy?
```

#### Principais ganhos gerados pelo prompt

* Fazer a pipeline reutilizar a conexão MongoDB existente;
* Adaptar a inicialização das Spiders;
* Definir como a pipeline recebe o objeto;
* Manter a responsabilidade de conexão centralizada na classe MongoDB.

#### Validação do que foi dito e retornado pela IA

A primeira abordagem discutida foi criando uma variável para receber a instância, no arquivo `settings.py`, e a acessar utilizando `crawler.settings["MONGO_DB_INSTANCE"]`.

Durante os testes, foi identificado um problema envolvendo `thread.lock` ao tentar transportar o objeto MongoDB pelas configurações do Scrapy. Isso ocorreu porque determinados 
objetos internos de conexão não podem ser copiados ou serializados dessa maneira. Isso levou a uma troca de abordagem para compartilhar a instância diretamente, evitando recriar ou fechar a conexão dentro da pipeline.

A solução final discutida foi utilizar o parâmetro mongo_db na inicialização da Spider e disponibilizar o objeto para a pipeline por meio do método `open_spider()`.

Durante os testes:

* Foi investigado o erro relacionado a `thread.lock`;
* O objeto do MongoDB foi removido das configurações;
* Foram revisadas as configurações de descoberta dos módulos e Spiders;
* Foi avaliada a possibilidade de transmitir o objeto diretamente à Spider.

#### Análise crítica

A IA foi útil para compreender como integrar o objeto do MongoDB na pipeline do Scrapy, onde a principal dificuldade foi lidar com o compartilhamento do objeto entre componentes que possuem mecanismos de execução 
diferentes.

Entretanto, a primeira abordagem apresentou problemas, sendo necessário analisar os erros e ajustar a forma de transmissão do banco. Isso demonstrou a importância de testar as sugestões da IA em um ambiente real, 
em vez de simplesmente aplicar o código gerado.

### Auxílio no gerenciamento de execução do Scrapy em uma thread separada

#### Prompts

```
Como posso implementar o CrawlerRunner do Scrapy no meu projeto, para que o crawler possa ser executado mais de uma
vez, sem que o menu interfira na sua execução e vice-versa?
```

```
Estou tendo dificuldades para integrar o Reactor do Twisted com o funcionamento normal do meu programa. Como posso
organizar isso?
```

```
Como faço para que o menu espere o Crawler do TrilhosAgora terminar de executar antes de voltar a mostrar as opções
para o usuário?
```

```
Desde que implementei o sistema de threads no projeto, um erro que trava o terminal tem ocorrido quando uso o CTRL+C,
tanto durante a execução do Crawler, quanto nos inputs do menu, resultando em um erro de EOF.
Como posso solucionar isso?
```

#### Principais ganhos gerados pelos prompts

* Separação da execução do crawler e do Reactor do fluxo principal da aplicação;
* Utilização de `Deferred` e `threading.Event` para identificar o término das operações e liberar a execução principal;
* Investigação e implementação de alternativas para lidar com `CTRL+C`, `KeyboardInterrupt` e `EOFError`;
* Ajustes para evitar tentativas de inicialização ou encerramento de um Reactor em estado inadequado.

#### Validação do que foi dito e retornado pela IA

Foram estudados recursos como `threading.Thread`, `CrawlerRunner`, `Deferred`, `threading.Event` e os métodos `reactor.callFromThread()` e `reactor.callInThread()`.

A escolha dessa abordagem teve como objetivo permitir que o Scrapy executasse suas coletas sem comprometer o funcionamento do menu principal, além de possibilitar o controle da execução e do encerramento dos crawlers.

Também foram investigadas alternativas para gerenciar interrupções manuais, evitando conflitos entre a interrupção do programa com `CTRL+C` e o gerenciamento do Reactor.

O grupo realizou testes práticos executando os crawlers por meio do menu principal, observando o comportamento das threads, a finalização das coletas, o armazenamento de dados e o retorno da aplicação ao funcionamento 
normal.

Também foram analisadas as mensagens de erro apresentadas no terminal, permitindo identificar problemas como `Unhandled error in Deferred` e `EOFError`, e testes pressionando CTRL+C em diferentes momentos da execução, 
verificando se o crawler e o restante da aplicação conseguiam encerrar suas atividades corretamente.

A partir dos resultados, foram feitos ajustes na inicialização do Reactor, na comunicação entre as threads e no tratamento das exceções.

#### Análise crítica

O ChatGPT auxiliou na compreensão de conceitos relacionados à programação concorrente e assíncrona, especialmente na integração entre o Scrapy, o Twisted e o restante da aplicação.

A ferramenta facilitou a identificação de possíveis causas dos erros e apresentou diferentes alternativas para controlar a execução dos crawlers, permitindo desenvolver um fluxo melhor
entre a coleta de dados e o menu principal.

Entretanto, essa foi uma das etapas que apresentou maior dificuldade técnica, pois as soluções sugeridas inicialmente nem sempre funcionavam corretamente com a arquitetura existente. 
Problemas envolvendo o ciclo de vida do Reactor, a sincronização entre threads e o tratamento de interrupções exigiram diversas adaptações.

A principal dificuldade foi entender como diferentes mecanismos de execução poderiam funcionar em conjunto sem provocar bloqueios ou erros durante a inicialização e o encerramento do programa e buscar meios de aplicar
as soluções. Por isso, foi necessário realizar testes em diferentes situações e ajustar as implementações conforme os resultados observados.
