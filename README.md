<p align="center">
  <img src="readme_files/TodaSP_Logo.png" />
</p>

# 🗺 TodaSP

## 💡 Descrição do Projeto

O **TodaSP** é uma plataforma que fornece informações estratégicas sobre transporte, saúde e segurança urbana de toda a cidade de São Paulo, garantindo maior assertividade e segurança para os cidadãos na escolha de moradias ou hospedagens na grande capital. Reunimos todas as informações essenciais da vizinhança em um só lugar, tornando a decisão de onde se hospedar ou morar simples, rápida e transparente.

A solução possui funcionalidades como a utilização de APIs e Web Crawlers para coletar dados das linhas e estações de metrô, pontos de ônibus, estabelecimentos de saúde, delegacias de polícia e seus casos reportados e dados populacionais e de risco hidrológico (inundações e alagamentos) de subprefeituras e distritos de São Paulo.

---

## 📈 Justificativa e Objetivo da Solução

A escolha de um local para morar ou se hospedar em grandes cidades é marcada pela falta de transparência sobre fatores cruciais, como segurança, acessibilidade a transportes e ruído urbano. O projeto **TodaSP** justifica-se ao centralizar esses indicadores essenciais em uma única plataforma, eliminando surpresas desagradáveis e permitindo que o usuário tome decisões mais seguras, assertivas e conscientes antes de assinar qualquer contrato ou reserva.

---

## ⚙ Tecnologias, Fontes de Dados e Bibliotecas Utilizadas

### Linguagem

* Python

### IDE

* PyCharm

### Banco de Dados

* MongoDB

### APIs

* [DEMAS - Dados Abertos](https://apidadosabertos.saude.gov.br/v1/)

    `Fonte da API: CNES (Cadastro Nacional de Estabelecimentos de Saúde)`
* [GeoSampa Metadados - Polícia Civil](https://metadados.geosampa.prefeitura.sp.gov.br/geonetwork/srv/eng/catalog.search;jsessionid=D2585C191F9FD4E123A9482ADDDCF420#/metadata/3879e65a-e9cc-4ea2-8619-2073395980cc)

    `Fonte da API: SSP-SP (Secretaria da Segurança Pública do Estado de São Paulo)`
* [Piranot - Segurança pública em SP: ocorrências por município.](https://www.piranot.com.br/datax/docs/dataset-seguranca-ssp-sp)

    `Fonte da API: SSP-SP (Secretaria da Segurança Pública do Estado de São Paulo)`
* [Transitland - São Paulo Transporte](https://www.transit.land/data/feeds/f-6gy-sptrans)

    `Fonte da API: GTFS (General Transit Feed Specification) da SPTrans`
* [Trilhos Agora - API do metrô e trens de São Paulo](https://trilhosagora.com.br/desenvolvedores)

    `Fontes da API: Metrô de São Paulo, CPTM, Trivia Trens, Motiva Trilhos, TIC Trens e LinhaUni.`

### Demais Fontes de Dados

* [ObservaSampa](https://observasampa.prefeitura.sp.gov.br/index.php?page=dadosabertos)

### Bibliotecas Externas (requirements.txt)

* `scrapy`
* `pymongo`
* `twisted`
* `pydantic`
* `requests`
* `tabulate`
* `curl_cffi`
* `itemadapter`
* `python-dotenv`

---
## ✅ Funcionamento da Solução

O sistema se baseia em um menu com 6 funcionalidades e uma opção de saída, com o qual o usuário pode interagir e escolher qual funcionalidade irá utilizar.

O sistema utiliza duas threads com responsabilidades distintas:

* `Main Thread (thread principal)`: responsável pela interação com o usuário, gerenciamento do menu e execução das funcionalidades, incluindo as consultas às APIs e o processamento dos dados.
* `TwistedReactor (thread secundária)`: responsável pela execução contínua do Reactor do Twisted, que coordena as operações assíncronas do Scrapy e a execução dos Web Crawlers.

Essa arquitetura mantém o Reactor ativo durante toda a execução do programa, permitindo iniciar o Web Crawler mais de uma vez sem precisar reinicializar o mecanismo de execução assíncrona.

A comunicação entre as threads é realizada por mecanismos de sincronização e agendamento de tarefas, como threading.Event e reactor.callFromThread(). Dessa forma, a thread principal pode aguardar a conclusão de uma coleta sem bloquear o funcionamento interno do Reactor.

### [1] Verificar Linhas de Metrô

Coleta dados de todas as linhas de metrô de São Paulo, através da API Trilhos Agora, e os armazena no banco de dados seguindo a seguinte estrutura em JSON:

```
{
  "_id": {}, - ID ÚNICO DO MONGODB
  "numero_linha": 1, - NÚMERO DA LINHA DE METRÔ
  "cor": "#005ba8", - CÓDIGO HEXADECIMAL QUE REPRESENTA A COR DA LINHA
  "data_atualizacao": "2026-11-16T20:59:03-03:00", - DATA DA ATUALIZAÇÃO DOS DADOS
  "nome": "Azul", - NOME CURTO DA LINHA
  "operadora": "Metrô de São Paulo", - OPERADORA RESPONSÁVEL PELA LINHA
  "rotulo": "Linha 1-Azul", - NOME COMPLETO DA LINHA (número + cor)
  "status": "Operação Normal", - ESTADO DA OPERAÇÃO DA LINHA
  "rota": [ - LISTA DAS ESTAÇÕES QUE A LINHA PASSA
      {
        "posicao": 1, - QUAL A POSIÇÃO DA ESTAÇÃO NO TRAJETO DA LINHA
        "nome": "Jabaquara-Comitê Paralímpico Brasileiro" - NOME DA ESTAÇÃO
      },
      {...}
  ]
}
```

### [2] Coletar Estações de Metrô

Coleta dados de todas as estações de metrô de São Paulo, através de um Web Crawler que percorre o site da Trilhos Agora buscando informações, e os armazena no banco de dados e no arquivo `data/subway_stations.json` seguindo a seguinte estrutura em JSON:

```
{
  "_id": {}, - ID ÚNICO DO MONGODB
  "nome": "Estação Palmeiras-Barra Funda", - NOME DA ESTAÇÃO
  "data_informacoes": "2026-11-16 21:32:56", - DATA DA COLETA DOS DADOS
  "endereco": "Av. Auro Soares de Moura Andrade, 664 - Barra Funda, São Paulo - SP", - ENDEREÇO DA ESTAÇÃO
  "horario_funcionamento": "Das 04:40 às 00:00", - HORÁRIO DE FUNCIONAMENTO DA ESTAÇÃO
  "integracoes": "Metrô (L3), CPTM/ViaMobilidade (L7, L8, L10), Terminal Rodoviário, Ônibus", - POSSÍVEIS INTEGRAÇÕES E BALDEAÇÕES A SEREM FEITAS DA ESTAÇÃO
  "linhas": [ - LISTA DAS LINHAS PRESENTES NA ESTAÇÃO
    "Linha 3-Vermelha", - NOMES DAS LINHAS
    "Linha 7-Rubi",
    "Linha 8-Diamante",
    "Linha 10-Turquesa",
    "Expresso Aeroporto"
  ]
}
```

### [3] Coletar Pontos de Ônibus

Coleta dados de todos os pontos de ônibus de São Paulo, através da API Transitland, e os armazena no banco de dados e no arquivo `data/bus_stops.json` seguindo a seguinte estrutura em JSON:

```
{
  "_id": {}, - ID ÚNICO DO MONGODB
  "id_ponto": "18848", - NÚMERO DE IDENTIFICAÇÃO DO PONTO DE ÔNIBUS
  "latitude": -23.554007, - LATITUDE DA LOCALIZAÇÃO DO PONTO DE ÔNIBUS
  "linhas": [ - LISTA CONTENDO AS LINHAS QUE PASSAM NO PONTO DE ÔNIBUS
    {
      "id_linha": "METRÔ L2", - IDENTIFICAÇÃO DA LINHA DE ÔNIBUS
      "nome_completo": "VILA MADALENA - VILA PRUDENTE", - NOME COMPLETO DA LINHA DO ÔNIBUS
      "nome_curto": "METRÔ L2" - NOME CURTO DA LINHA DO ÔNIBUS
    }
  ],
  "longitude": -46.671097, - LONGITUDE DA LOCALIZAÇÃO DO PONTO DE ÔNIBUS
  "nome": "Clínicas" - NOME DO PONTO DE ÔNIBUS
}
```

### [4] Verificar Delegacias de polícia

Coleta dados de todas as delegacias de polícia de São Paulo, através da API WFS GeoSampa e da API Piranot, e os armazena no banco de dados seguindo a seguinte estrutura em JSON:

```
{
  "_id": {}, - ID ÚNICO DO MONGODB
  "numero_dp": 1, - NÚMERO DE IDENTIFICAÇÃO DA DELEGACIA
  "classe": "POLICIA CIVIL", - TIPO DE POLÍCIA QUE ATENDE À DELEGACIA
  "endereco": "RUA DA GLÓRIA, 410", - ENDEREÇO DA DELEGACIA
  "nome": "1° DP - Liberdade", - NOME COMPLETO DA DELEGACIA
  "casos": [ - LISTA DE CASOS REGISTRADOS DE CADA DELEGACIA, SEPARADA POR NATUREZA DO CRIME
    {
      "id_natureza": 21, - NÚMERO DE IDENTIFICAÇÃO DA NATUREZA DO CRIME
      "natureza": "FURTO - OUTROS", - NATUREZA DO CRIME
      "quantidade_ultimo_mes": 679, - QUANTIDADE REGISTRADA NO ÚLTIMO MÊS
      "quantidade_ultimo_ano": 5960, - QUANTIDADE REGISTRADA NO ANO
      "ano": 2026 - ANO REFERENTE AOS DADOS
    },
    {}
  ]
}
```

### [5] Coletar Estabelecimentos de Saúde

Coleta dados de todos os estabelecimentos de saúde de São Paulo, através da API Dados Abertos, e os armazena no banco de dados e no arquivo `data/health_facilities.json` seguindo a seguinte estrutura em JSON:

```
{
  "_id": {} - ID ÚNICO DO MONGODB
  "cnes_id": 34673, - NÚMERO DE IDENTIFICAÇÃO DO ESTABELECIMENTO
  "bairro": "PLANALTO PAULISTA", - BAIRRO DO ESTABELECIMENTO
  "cep": "04058000", - CEP DO ESTABELECIMENTO
  "codigo_natureza_juridica": "2062", - CÓDIGO DE IDENTIFICAÇÃO DA NATUREZA JURÍDICA DO ESTABELECIMENTO
  "codigo_tipo": 7, - CÓDIGO DE IDENTIFICAÇÃO DO TIPO DO ESTABELECIMENTO
  "data_informacoes": "2026-02-27", - DATA DA ATUALIZAÇÃO DOS DADOS
  "endereco": "ALAMEDA DOS APETUPAS", - RUA/AVENIDA DO ESTABELECIMENTO
  "esfera_administrativa": "MUNICIPAL", - ESFERA ADMINISTRATIVA DO ESTABELECIMENTO
  "latitude": -23.61444663731964, - LATITUDE DA LOCALIZAÇÃO DO ESTABELECIMENTO
  "longitude": -46.64930028465461, - LONGITUDE DA LOCALIZAÇÃO DO ESTABELECIMENTO
  "natureza_juridica": "PRIVATE", - NATUREZA JURÍDICA DO ESTABELECIMENTO
  "nome_fantasia": "API ASSISTENCIA PSIQUIATRICA INTEGRADA", - NOME FANTASIA DO ESTABELECIMENTO
  "numero": "297", - NÚMERO DO ESTABELECIMENTO
  "razao_social": "CLH ASSISTENCIA PSIQUIATRICA LTDA EM RECUPERACAO JUDICIAL", - RAZÃO SOCIAL DO ESTABELECIMENTO
  "tipo": "Hospital" - TIPO DO ESTABELECIMENTO
}
```

Todos os estabelecimentos coletados estão em um destes tipos:

* `Centro de Parto Normal`
* `Clínica/Diagnóstico`
* `Farmácia`
* `Hospital`
* `Posto de Saúde`
* `Pronto Atendimento`
* `Pronto Socorro`
* `Unidade Básica de Saúde`

A api recomenda a coleta de apenas 20 estabelecimentos por requisição, portanto, esta coleta costuma demorar mais do que as outras, principalmente pela quantidade elevada de estabelecimentos.
Ao final da coleta, são registrados 28.926 estabelecimentos, de acordo com as últimas execuções.

### [6] Coletar dados de população e alagamentos de distritos e subprefeituras de São Paulo

Coleta dados populacionais e de risco hidrológico (inundações e alagamentos) de todos os distritos e subprefeituras de São Paulo, através dos indicadores disponíveis no arquivo "ObservaSampaDadosAbertosIndicadores.json", fornecido pelo [Observatório de Indicadores da Cidade de São Paulo (ObservaSampa)](https://observasampa.prefeitura.sp.gov.br/index.php), e os armazena no banco de dados seguindo as seguintes estruturas em JSON:

#### SUBPREFEITURAS

```
{
  "_id": {} - ID ÚNICO DO MONGODB
  "nome": "BUTANTÃ", - NOME DA SUBPREFEITURA
  "anos_informacoes": [ - LISTA QUE GUARDA OS ANOS DAS INFORMAÇÕES
    2025
  ],
  "area_risco_hidrologico": 66481.57 - ÁREA DE RISCO HIDROLÓGICO DE CADA SUBPREFEITURA EM m²
}
```

#### DISTRITOS

```
{
  "_id": {} - ID ÚNICO DO MONGODB
  "nome": "Campo Grande", - NOME DO DISTRITO
  "anos_informacoes": [ - LISTA QUE GUARDA OS ANOS DAS INFORMAÇÕES
    2023,
    2024
  ],
  "casos_alagamentos": 13, - NÚMERO DE OCORRÊNCIAS DE ALAGAMENTOS E INUNDAÇÕES ATENDIDAS
  "nivel_risco_hidrologico": "Alto", - NÍVEL DE RISCO HIDROLÓGICO NO DISTRITO
  "populacao": 118297, - POPULAÇÃO TOTAL DO DISTRITO
  "populacao_criancas": 16128, - POPULAÇÃO DE CRIANÇAS DO DISTRITO
  "populacao_idosa": 27275, - POPULAÇÃO DE IDOSOS DO DISTRITO
  "risco_hidrologico": 1.1 - RISCO HIDROLÓGICO NO DISTRITO
}
```

#### Cálculo do Risco Hidrológico por Distrito

O Risco Hidrológico por distrito é calculado através da seguinte fórmula:

`R = (A + I)/P * 10000`

Onde:
* R é o Risco Hidrológico
* A são as ocorrências de alagamentos atendidas
* I são as ocorrências de inundações atendidas
* P é a população total do distrito

Portanto, o resultado representa a quantidade de ocorrências a cada 10.000 habitantes do distrito e é separado entre os seguintes níveis:

* `Muito Baixo`
* `Baixo`
* `Moderado`
* `Alto`

Os limites dos níveis são definidos estatisticamente, através de quartis, que dividem a distribuição dos valores de risco em quatro intervalos. Para isso, é utilizada a função quantiles(), disponível na biblioteca nativa statistics do Python, com o método inclusive.

### [0] Sair

Encerra o sistema.

## 🏗 Estrutura do Projeto

```
TodaSP/
│
├── API/
│   ├── DadosAbertosAPI.py
│   ├── GeoSampaWFS.py
│   ├── PiranotAPI.py
│   ├── TransitlandAPI.py
│   └── TrilhosAgoraAPI.py
│
├── Database/
│   └── MongoDB.py
│
├── Model/
│   ├── GeographicalData/
│   │   ├── District.py
│   │   └── Subprefecture.py
│   │
│   ├── HealthData/
│   │   └── HealthFacility.py
│   │
│   ├── PoliceData/
│   │   ├── PoliceReport.py
│   │   └── PoliceStation.py
│   │
│   ├── PublicTransportData/
│   │   ├── BusStation.py
│   │   ├── SubwayLine.py
│   │   └── SubwayStation.py
│   │
│   └── MenuManager.py
│
├── Reader/
│   └── ObservaSampaReader.py
│
├── Scrapy/
│   ├── Scrapy/
│   │   ├── spiders/
│   │   │   ├── SubwayStationsSpider.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   └── settings.py
│   │
│   └── scrapy.cfg
│
├── Utils/
│   └── Utils.py
│
├── data/
│   └── ObservaSampaDadosAbertosIndicadoresJSON.json
│
├── readme_files/
│   └── TodaSP_Logo.png
│
├── .gitignore
├── README.md
├── main.py
└── requirements.txt
```

A pasta "readme_files" possui apenas conteúdos para o README.md.

---

## 💾 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/DAC-Developers-And-Coders/TodaSP
```

### 2. Acesse a pasta do projeto

```bash
cd TodaSP
```

### 3. Crie e ative um ambiente virtual

#### Windows

```bash
python -m venv .venv
```

ou

```bash
py -m venv .venv
```

Ative o ambiente virtual:

```bash
.\.venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv .venv
```

Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

### 4. Instale as dependências do projeto

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
TRILHOS_AGORA_KEY=insira_sua_chave_aqui
PIRANOT_KEY=insira_sua_chave_aqui
TRANSITLAND_KEY=insira_sua_chave_aqui
```

### 6. Instale o MongoDB

O TodaSP utiliza o MongoDB como banco de dados. Para instalá-lo, acesse a documentação oficial correspondente ao seu sistema operacional:

* [Windows](https://www.mongodb.com/docs/manual/administration/install-community-windows/?win-method=wizard)
* [Linux](https://www.mongodb.com/docs/manual/administration/install-community-linux/?linux-method=pkg&linux-distro=rhel)
* [macOS](https://www.mongodb.com/docs/manual/administration/install-community-macos/?macos-method=brew)

Crie um arquivo `.env` na raiz do projeto:

```
TRILHOS_AGORA_KEY=insira_sua_chave_aqui
PIRANOT_KEY=insira_sua_chave_aqui
TRANSITLAND_KEY=insira_sua_chave_aqui
```

### 7. Inicie o MongoDB

#### Windows

```bash
net start MongoDB
```

#### Linux

```bash
sudo systemctl start mongod
```

#### macOS

```bash
brew services start mongodb-community
```

### 8. Execute o programa

#### Windows

```bash
python main.py
```

ou

```bash
py main.py
```

#### Linux/macOS

```bash
python3 main.py
```

---

## ⚠ Observações e Limitações

* O sistema permite a interrupção manual através do comando `CTRL+C`, inclusive durante a interação com o menu.
* Caso a interrupção ocorra durante uma operação de Web Crawling, a coleta será encerrada abruptamente, pois o crawler ainda não possui um cancelamento controlado.
* O funcionamento do Web Crawler depende do Reactor do Twisted, mantido ativo em uma thread dedicada durante a execução do programa.

---

## 🙋‍♂️ Integrantes do Grupo

* ANDRÉ VICTOR GONÇALVES NASCIMENTO - RM 570567
* DAVI DIAS DE SOUZA FREITAS - RM 574089
* DAVID MIKAEL DIAS DA SILVA - RM 571637
* GABRIEL NOVAGA PEREIRA - RM 573196
* MATHEUS MONTEIRO DA SILVA - RM 573842
