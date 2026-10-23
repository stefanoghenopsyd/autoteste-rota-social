# A Rota da Obra: Autoavaliacao Estrategica

## 1. Apresentacao / Presentazione

### Versao em Portugues

A Rota da Obra e uma ferramenta didatica interativa de autorreflexao e diagnostico desenvolvida para liderancas, conselheiros e educadores de obras sociais, centros comunitarios e organizacoes do Terceiro Setor (especialmente em contextos de vulnerabilidade e periferia urbana).

O percurso e estruturado em 6 etapas sequenciais, correspondentes as fases classicas do planejamento estrategico, apresentadas sob a forma de dilemas decisorios concretos:

1. Identidade e Direcao (Missao, Visao e Valores)
2. Analise do Contexto (Diagnostico Interno e Externo)
3. Formulacao dos Objetivos Estrategicos (Escolha das Prioridades)
4. Planejamento Operacional e Alocacao de Recursos (Pessoas e Meios)
5. Execucao e Alinhamento Organizacional (Implementacao)
6. Monitoramento, Avaliacao de Impacto e Aprendizado Continuo

Ao final do questionario, o participante recebe uma devolutiva grafica detalhada com a distribuicao dos 4 Arquetipos Estrategicos:

- O Buscador de Agua ("A urgencia da fonte, o risco da deriva")
- O Carvalho de Pedra ("As raizes firmes, a sombra que nao se move")
- O Relogio de Precisao ("O ritmo compassado, o abrigo das regras")
- O Jardineiro ("O cuidado com a vida, o discernimento das estacoes")

### Versione in Italiano

A Rota da Obra e uno strumento didattico interattivo di autoriflessione e diagnosi organizzativa, progettato per coordinatori, dirigenti ed educatori di enti del Terzo Settore, centri educativi e opere sociali attive in contesti di periferia e vulnerabilita.

Il percorso guida l'utente attraverso i 6 snodi del ciclo di pianificazione strategica, decodificando la postura prevalente attraverso 4 archetipi organizzativi (Il Cercatore d'Acqua, La Quercia di Pietra, L'Orologio di Precisione e Il Giardiniere), offrendo spunti di maturazione e domande di discernimento comunitario.

---

## 2. Como Executar Localmente / Come eseguire in locale

### Prerequisiti / Pre-requisitos

- Python 3.9 o superiore installato.
- Gestore pacchetti pip.

### Passo 1: Clonare il repository

```bash
git clone https://github.com/SEU-USUARIO/autoteste-rota-social.git
cd autoteste-rota-social
```

### Passo 2: Creare e attivare l'ambiente virtuale

Linux e macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Installare le dipendenze

```bash
pip install -r requirements.txt
```

### Passo 4: Avviare l'applicazione

```bash
streamlit run app.py
```

L'applicazione sara accessibile nel browser all'indirizzo: http://localhost:8501

---

## 3. Pubblicazione su Streamlit Community Cloud

Per distribuire online l'applicazione gratuitamente:

1. Caricare questo progetto in un repository pubblico su GitHub contenente i file app.py, requirements.txt e README.md.
2. Accedere a share.streamlit.io con il proprio account GitHub.
3. Selezionare "New app" (oppure "Create app").
4. Indicare il repository, il branch (es. main) e confermare che Main file path sia impostato su app.py.
5. Cliccare su "Deploy".
6. Il link pubblico sara disponibile per la compilazione via web o smartphone.

---

## 4. Struttura dei File

- app.py: Codice sorgente dell'applicazione Streamlit.
- requirements.txt: Elenco delle librerie necessarie (streamlit, plotly, pandas).
- README.md: Documentazione del progetto.

---

## 5. Licenza

Distribuito sotto licenza MIT.