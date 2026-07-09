# 🎮 League of Legends Team Balancer

Aplicação em Python para balanceamento automático de equipes de League of Legends (Custom Game), utilizando análise combinatória para encontrar a distribuição mais equilibrada possível entre dois times.

Interface construída com Streamlit para facilitar o cadastro dos jogadores e a geração instantânea das equipes.

---

## 💡 Contexto Real

Em partidas personalizadas entre amigos é comum que a formação dos times seja feita manualmente, o que frequentemente gera desequilíbrios de habilidade e discussões sobre a divisão das equipes.

Este projeto surgiu com o objetivo de automatizar esse processo utilizando um algoritmo que avalia todas as combinações possíveis e seleciona aquela que apresenta o melhor equilíbrio.

---

## 🎯 Objetivo

Gerar automaticamente dois times contendo:

- 5 jogadores por equipe
- 1 jogador para cada função (Top, Jungle, Mid, ADC e Suporte)
- Menor diferença possível de pontuação entre os times
- Distribuição equilibrada considerando o Elo dos jogadores

---

## ⚙️ Lógica do Sistema

Cada jogador recebe uma pontuação baseada em:

- Elo
- Peso da função exercida

Como existem exatamente dois jogadores para cada função, o algoritmo gera todas as combinações possíveis.

```
2 × 2 × 2 × 2 × 2 = 32 combinações
```

Cada combinação é analisada considerando:

- Soma total dos pontos
- Diferença entre os times
- Diferença entre confrontos da mesma rota
- Diferença entre os maiores elos
- Diferença entre os menores elos

Ao final é selecionada automaticamente a combinação com o melhor índice de equilíbrio.

---

## 🛠️ Tecnologias

- Python
- Streamlit
- Dataclasses
- Itertools

---

## 📚 Funcionalidades

- Cadastro de até 10 jogadores
- Validação automática das funções
- Balanceamento em tempo real
- Avaliação das 32 combinações possíveis
- Índice de equilíbrio da partida
- Comparação de pontuação entre equipes
- Exportação da composição dos times em arquivo `.txt`
- Interface responsiva construída em Streamlit

---

## 📂 Estrutura do Projeto

```bash
/lol-team-balancer
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🧮 Critérios de Balanceamento

O algoritmo utiliza uma função de custo composta por múltiplos critérios.

Ordem de prioridade:

1. Menor diferença total de pontuação
2. Menor diferença entre confrontos da mesma rota
3. Menor diferença entre os maiores elos
4. Menor diferença entre os menores elos

Como apenas 32 combinações são possíveis, todas são avaliadas, garantindo que a solução encontrada seja ótima.

---

## ▶️ Como executar

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/lol-team-balancer.git
cd lol-team-balancer
```

Crie um ambiente virtual (opcional):

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

---

## 🧠 Problema Resolvido

A divisão manual de equipes normalmente resulta em:

- Times desequilibrados
- Discussões entre jogadores
- Diferenças excessivas de habilidade
- Tempo gasto montando as equipes

O sistema automatiza esse processo, encontrando a melhor distribuição possível em poucos milissegundos.

---

## 🚀 Possíveis Melhorias

- Utilização de MMR personalizado em vez do Elo oficial
- Histórico de partidas e taxa de vitória dos jogadores
- Integração com a API da Riot Games
- Ajuste automático de pesos por função
- Cadastro permanente de jogadores
- Estatísticas de partidas realizadas
- Geração de histórico das equipes
- Exportação em PDF
- Modo campeonato (várias rodadas)
- Suporte a diferentes formatos de partida

---

## 📸 Interface

A aplicação oferece uma interface intuitiva para:

- Cadastro dos jogadores
- Seleção da função e Elo
- Balanceamento automático
- Comparação visual entre as equipes
- Exportação da composição dos times

---

## 📄 Licença

Projeto desenvolvido para fins de estudo e demonstração de algoritmos de otimização combinatória utilizando Python e Streamlit.
