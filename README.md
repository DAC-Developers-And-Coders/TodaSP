# 🌌 NebulaNoise

## 💡 Descrição do Projeto

O **NebulaNoise** é uma plataforma de simulação e monitoramento de instabilidades em sistemas de comunicação orbital. A solução busca simular e analisar condições espaciais, identificar possíveis riscos de interferência em sinais eletromagnéticos e gerar alertas preventivos para operadores e usuários.

A solução possui funcionalidades como a simulação do cálculo da estabilidade do sinal, o nível de risco de interferência causada pelos detritos e pela atividade orbital, a emissão de relatórios e alertas para cada simulação, o histórico de relatórios e o salvamento dos relatórios em arquivos.

---

## 📈 Objetivo da Solução

O objetivo do **NebulaNoise** é simular e monitorar possíveis interferências em sinais de sistemas de comunicação via satélite. Causadas pelo aumento de objetos na órbita terrestre e pelo aumento da atividade orbital, tais interferências ocorrem devido à crescente de explorações e pesquisas espaciais.

O NebulaNoise busca:

* Simular cenários de emissão de sinais via satélite;
* Calcular a estabilidade dos sinais eletromagnéticos, considerando o nível de atividade orbital e a densidade de objetos;
* Classificar o nível de risco de interferência nos sinais;
* Gerar alertas e recomendações preventivas;
* Registrar simulações realizadas por meio de relatórios e logs.

---

## ⚙ Tecnologias e Bibliotecas Utilizadas

### Linguagem

* Python

### IDE

* PyCharm

### Bibliotecas

* `os`
* `sys`
* `time`
* `logging`
* `datetime`

Todas as bibliotecas utilizadas fazem parte da biblioteca padrão do Python.

---

## ⚒ Funcionamento da Solução

O sistema solicita ao usuário três parâmetros:

1. Intensidade do sinal (0 a 100);
2. Densidade de objetos em órbita (0 a 100);
3. Velocidade da atividade orbital (0 a 100).

Com base nesses valores, é calculada a estabilidade do sinal utilizando a fórmula:

`E = I / (1 + 0.7(D/100) + 0.4(V/100))`

Onde:

* **E** = Estabilidade do sinal;
* **I** = Intensidade do sinal;
* **D** = Densidade de objetos em órbita;
* **V** = Velocidade da atividade orbital.

Após o cálculo, o sistema:

* Classifica o risco como **Baixo**, **Moderado** ou **Alto**;
* Gera recomendações operacionais;
* Armazena a simulação no histórico;
* Permite salvar relatórios em arquivos TXT;
* Registra eventos e alertas em arquivos de log.

---

## ✅ Funcionalidades

### [1] O que é NebulaNoise?

Exibe um texto de 5 linhas informando o que é a solução.

### [2] Simular interferência orbital de sinal

Permite executar análises utilizando parâmetros definidos pelo usuário.

### [3] Histórico de Simulações

Armazena todas as simulações realizadas durante a execução do programa.

### [4] Salvar relatórios

Permite salvar:

* A última análise realizada;
* Todo o histórico de análises.

### [5] Verificar emissão de alertas por simulação

Identifica, no histórico, simulações de alto risco e informa se alertas foram emitidos.

### [6] Sair

Encerra o sistema.

### Registro de Logs

Armazena eventos importantes em:

`logs/logs.txt`

---

## 🏗 Estrutura do Projeto

```
GS_NebulaNoise/
│
├── main.py
|
├── classes/
│   └── MenuManager.py
│   └── Simulation.py
│   └── Log.py
│
├── logs/ (gerada automaticamente)
│   └── logs.txt
│
├── relatorios/ (gerada automaticamente)
│   └── relatorio_*.txt
│
└── README.md
```

A pasta "assets" possui apenas conteúdos para o README.md.

---

## 💾 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/DAC-Developers-And-Coders/GS_NebulaNoise
```

### 2. Acesse a pasta do projeto

```bash
cd GS_NebulaNoise
```

### 3. Execute o programa

#### Windows

```bash
python main.py
```

ou

```bash
py main.py
```

#### Linux

```bash
python3 main.py
```

---

## 💿 Exemplo de Uso

### Menu

```
======NebulaNoise Menu======
| [1] O que é NebulaNoise?
| [2] Simular interferência orbital de sinal
| [3] Histórico de simulações
| [4] Salvar relatórios
| [5] Verificar emissão de alertas por simulação
| [6] Sair
```

#### [1] O que é NebulaNoise?

![1](assets/1.gif)

#### [2] Simular interferência orbital de sinal

![2](assets/2.gif)

#### [3] Histórico de simulações

![3](assets/3.gif)


#### [4] Salvar relatórios

![4](assets/4.gif)

#### [5] Verificar emissão de alertas por simulação

![5](assets/5.gif)

#### [6] Sair

![6](assets/6.gif)

---

## 🙋‍♂️ Integrantes do Grupo

* ANDRÉ VICTOR GONÇALVES NASCIMENTO - RM 570567
* DAVI DIAS DE SOUZA FREITAS - RM 574089
* DAVID MIKAEL DIAS DA SILVA - RM 571637
* GABRIEL NOVAGA PEREIRA - RM 573196
* MATHEUS MONTEIRO DA SILVA - RM 573842
