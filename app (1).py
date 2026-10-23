import os
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# -------------------------------------------------------------
# Configuracao da Pagina
# -------------------------------------------------------------
st.set_page_config(
    page_title="A Rota da Obra | Autoavaliacao Estrategica",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilizacao CSS personalizada
st.markdown("""
    <style>
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-bottom: 2rem;
    }
    .logo-img {
        width: 100%;
        max-width: 240px;
        height: auto;
        margin: 0 auto 1.2rem auto;
        display: block;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.3rem;
        text-align: center;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .step-card {
        background-color: #F8FAFC;
        border-left: 5px solid #2563EB;
        padding: 1.2rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
    }
    .dilemma-title {
        font-weight: 600;
        color: #1E293B;
        font-size: 1.15rem;
        margin-bottom: 0.5rem;
    }
    .dilemma-text {
        font-size: 1rem;
        line-height: 1.55;
        color: #334155;
    }
    .profile-card {
        padding: 1.2rem;
        border-radius: 8px;
        background-color: #FFFFFF;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-top: 4px solid #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Base de Dados: Etapas, Dilemas e Opcoes
# -------------------------------------------------------------
ETAPAS = [
    {
        "numero": 1,
        "titulo": "Etapa 1: Identidade e Direcao (Missao, Visao, Valores)",
        "dilema": (
            "Uma importante fundacao empresarial oferece um financiamento relevante voltado para a comunidade "
            "local em que atuamos. No entanto, impoe exigencias muito rigidas e setoriais quanto ao tema das "
            "intervencoes a serem apoiadas. Os temas propostos nao coincidem com a tradicao socioeducativa da nossa obra. "
            "Como voces entendem que devem orientar a sua escolha?"
        ),
        "opcoes": {
            "A": (
                "Acolhemos as prioridades e a linguagem do financiador: para garantir a continuidade "
                "material do servico e nao deixar faltar o sustento a comunidade, a prioridade e captar "
                "os recursos disponiveis, adaptando inclusive as nossas atividades as demandas externas."
            ),
            "B": (
                "Recusamos a proposta: a fidelidade a vocacao original da obra nao admite concessoes diante de "
                "prioridades definidas externamente; preferimos enfrentar sacrificios economicos e reducoes de equipe "
                "a correr o risco de perder a nossa identidade historica."
            ),
            "C": (
                "Verificamos a conformidade administrativa, contratual e estatutaria do edital: se os requisitos formais "
                "forem sustentaveis, participamos nos limitando a executar as entregas exigidas com precisao e respeitando as normas."
            ),
            "D": (
                "Abrimos um dialogo com o doador e tentamos negociar, buscando demonstrar como a nossa identidade e o nosso "
                "conhecimento do territorio podem enriquecer a proposta, traduzindo o edital em respostas reais para a comunidade "
                "sem trair a nossa missao original."
            )
        }
    },
    {
        "numero": 2,
        "titulo": "Etapa 2: Analise do Contexto (Diagnostico Interno e Externo)",
        "dilema": (
            "As transformacoes sociais e demograficas do bairro tornam evidente que alguns servicos historicos "
            "oferecidos pelo nosso centro social sao cada vez menos frequentados, ao mesmo tempo em que surgem novas formas "
            "de vulnerabilidade e fragilidade as quais a obra ainda nao esta respondendo. Como voces pensam em conduzir esta fase de diagnostico?"
        ),
        "opcoes": {
            "A": (
                "Direcionamos a analise principalmente para as linhas de financiamento indicadas pelas politicas publicas "
                "ou pelos planos de assistencia social do territorio, alinhando rapidamente a nossa atuacao aquilo que sera financiado nos proximos ciclos."
            ),
            "B": (
                "Mantemos inalterados os servicos historicos: a queda no numero de participantes e, sem duvida, uma crise passageira "
                "do territorio ou, infelizmente, uma falta de interesse em propostas de valor que nos, de qualquer forma, queremos continuar sustentando com fidelidade."
            ),
            "C": (
                "Atualizamos o diagnostico por meio da coleta periodica de dados estatisticos, censos e formularios padronizados, "
                "elaborando um mapeamento formal util para relatorios de prestacao de contas, balancos sociais e auditorias de qualidade."
            ),
            "D": (
                "Promovemos um processo de escuta ativa no territorio (familias, escolas, comerciantes e liderancas locais, servicos publicos) "
                "e o cruzamos com as competencias e limites reais da equipe, para compreender com clareza o que e preciso preservar, o que transformar e o que encerrar."
            )
        }
    },
    {
        "numero": 3,
        "titulo": "Etapa 3: Formulacao dos Objetivos Estrategicos (Escolha das Prioridades)",
        "dilema": (
            "No momento do planejamento, a nossa obra se depara com multiplos apelos da comunidade e com demandas urgentes, "
            "contando, porem, com recursos humanos e economicos limitados. Com qual criterio voces procuram definir as metas futuras?"
        ),
        "opcoes": {
            "A": (
                "Estabelecemos uma gama muito ampla e flexivel de objetivos gerais, formulados de modo a viabilizar qualquer "
                "oportunidade futura de projeto ou edital, sem fechar nenhuma porta de financiamento."
            ),
            "B": (
                "Rejeitamos a logica de metas formais ou quantitativas: para nos, o unico objetivo autentico e a disponibilidade "
                "diaria para acolher quem bate a nossa porta, sem nos deixar engessar por parametros pre-estabelecidos ou calculos de gestao."
            ),
            "C": (
                "Traduzimos as diretrizes em uma lista detalhada de atribuicoes, volumes de atendimento e prazos alinhados aos "
                "padroes de certificacao, convenios e termos de parceria com os orgaos publicos ou financiadores."
            ),
            "D": (
                "Selecionamos um conjunto restrito de prioridades estrategicas claras e compartilhadas com a equipe, definindo "
                "para cada uma a mudanca esperada na vida das pessoas, os indicadores de acompanhamento e as responsabilidades operacionais."
            )
        }
    },
    {
        "numero": 4,
        "titulo": "Etapa 4: Planejamento Operacional e Alocacao de Recursos (Pessoas e Meios)",
        "dilema": (
            "Para iniciar uma nova iniciativa socioassistencial ou educativa complexa, e necessario distribuir cargas de trabalho, "
            "responsabilidades, orcamento e prazos de execucao entre os educadores e colaboradores. Como se deve proceder nessa atribuicao?"
        ),
        "opcoes": {
            "A": (
                "Concentramos os recursos nas atividades de maior visibilidade para os apoiadores externos, exigindo dos colaboradores "
                "flexibilidade e espirito de sacrificio constante para suprir as lacunas operacionais a medida que surgirem."
            ),
            "B": (
                "Confiamos na dedicacao e no engajamento espontaneo dos colaboradores historicos, acreditando que a motivacao pela causa "
                "deva compensar a escassez de recursos e a ausencia de planos operacionais formais."
            ),
            "C": (
                "Estabelecemos descricoes de funcao rigidas, horarios fixos e um cronograma minucioso, exigindo o cumprimento estrito "
                "das escalas e tarefas designadas para evitar falhas organizacionais."
            ),
            "D": (
                "Construimos o plano de trabalho de forma participativa com as coordenacoes e com as equipes: definimos cargas sustentaveis "
                "de trabalho, asseguramos momentos dedicados de supervisao e alinhamento, e reservamos recursos especificos para a seguranca e o cuidado com a equipe."
            )
        }
    },
    {
        "numero": 5,
        "titulo": "Etapa 5: Execucao e Alinhamento Organizacional (Implementacao)",
        "dilema": (
            "Durante a fase de execucao, ocorrem tensoes imprevistas - conflitos entre colaboradores, dificuldades inesperadas no relacionamento "
            "com os atendidos ou com a administracao publica, episodios de violencia ou instabilidade no territorio - que colocam a prova a sustentacao do servico. "
            "Como a rotina de trabalho deve ser conduzida?"
        ),
        "opcoes": {
            "A": (
                "Reorientamos rapidamente as atividades do dia a dia, priorizando solucoes que evitem atritos com agentes externos ou "
                "que garantam a continuidade das prestacoes de contas, mesmo que isso custe a profundidade do processo pedagogico e social iniciado."
            ),
            "B": (
                "Pedimos a equipe que resista e siga em frente sem alterar a conducao inicial, compreendendo o desgaste e as dificuldades "
                "como parte inevitavel do testemunho e da doacao exigidos pela causa."
            ),
            "C": (
                "Exigimos de todos o cumprimento estrito dos regulamentos e protocolos operacionais em vigor, delegando a resolucao de casos "
                "excepcionais a publicacao de novas orientacoes internas ou ordens de servico."
            ),
            "D": (
                "A lideranca assegura proximidade e presenca direta no territorio: criam-se momentos de escuta e suporte para acolher as dificuldades, "
                "reajustando as praticas de forma flexivel, mas coerente com os propositos originais."
            )
        }
    },
    {
        "numero": 6,
        "titulo": "Etapa 6: Monitoramento, Avaliacao de Impacto e Aprendizado",
        "dilema": (
            "Ao termino do ciclo anual anterior ou do projeto executado, precisamos fazer um balanco do trabalho realizado para prestar "
            "contas da intervencao e definir os rumos do proximo ciclo. Em que voces vao focar principalmente?"
        ),
        "opcoes": {
            "A": (
                "A prioridade e cuidar da comunicacao externa e da relacao com os financiadores, destacando os pontos fortes e os indicadores "
                "que favorecam a renovacao das parcerias e a continuidade dos repasses."
            ),
            "B": (
                "Nao realizamos avaliacoes estruturadas porque temos a conviccao de que o verdadeiro valor da acao socioeducativa nao se mede em numeros. "
                "Confiamos na certeza interna de ter feito tudo o que era possivel com espirito de gratuidade."
            ),
            "C": (
                "Mensuramos rigorosamente as metas quantitativas de entrega (atendimentos realizados, frequencias registradas, refeicoes servidas, "
                "comprovantes de despesa) para assegurar a total conformidade administrativa e fiscal."
            ),
            "D": (
                "Avaliamos o impacto real envolvendo educadores, familias atendidas e parceiros locais: analisamos tanto os avancos quanto os insucessos, "
                "convertendo a experiencia concreta em aprendizado institucional para aprimorar o futuro."
            )
        }
    }
]

PERFIS = {
    "A": {
        "nome": "O Buscador de Agua",
        "subtitulo": "A urgencia da fonte, o risco da deriva",
        "cor": "#0284C7",
        "imagem": "logo_buscador_de_agua.png",
        "virtude": (
            "Voce e movido pela responsabilidade vital de assegurar a subsistencia da obra. "
            "Tem sensibilidade para captar oportunidades, senso pratico, facilidade para dialogar com diferentes atores "
            "e rapidez de resposta. Sem a sua atuacao, muitas vezes a instituicao nao teria os meios concretos para abrir as portas a cada dia."
        ),
        "fragilidade": (
            "De tanto ir atras dos cursos d agua apontados por terceiros (editais de momento, exigencias de fundacoes ou tendencias passageiras), "
            "voce corre o risco de desviar a caravana do seu destino original (mission drift). Os educadores na ponta podem se sentir desorientados, "
            "com dificuldade de enxergar o sentido comum que conecta as inumeras acoes iniciadas."
        ),
        "pergunta": "«Se tivessemos toda a agua garantida para os proximos tres anos, saberiamos dizer com clareza em direcao a qual terra prometida estamos caminhando?»"
    },
    "B": {
        "nome": "O Carvalho de Pedra",
        "subtitulo": "As raizes firmes, a sombra que nao se move",
        "cor": "#15803D",
        "imagem": "logo_carvalho_de_pedra.png",
        "virtude": (
            "Voce guarda com firmeza e dedicacao a memoria, os principios fundadores e o proposito da obra. "
            "Nao cede diante de caminhos faceis nem se deixa levar por modismos de gestao. E uma referencia etica e afetiva "
            "que transmite acolhimento, gratuidade e forte sentimento de pertenca a toda a comunidade."
        ),
        "fragilidade": (
            "Confunde a fidelidade a origem com o apego imutavel as praticas do passado. Ao recusar uma leitura realista das mudancas "
            "do entorno ou ao rejeitar ferramentas organizacionais atuais, arrisca levar a obra ao isolamento e ao esgotamento financeiro, "
            "tornando-a aos poucos incapaz de atender aos reais desafios das novas geracoes."
        ),
        "pergunta": "«Cuidar do fogo dos fundadores significa guardar as cinzas do passado ou acender novas chamas capazes de iluminar a realidade de hoje?»"
    },
    "C": {
        "nome": "O Relogio de Precisao",
        "subtitulo": "O ritmo compassado, o abrigo das regras",
        "cor": "#B45309",
        "imagem": "logo_relogio_de_precisao.png",
        "virtude": (
            "Voce zela pela ordem, pela prestacao de contas transparente, pela equidade nas relacoes de trabalho e pelo rigor administrativo. "
            "Em cenarios marcados por instabilidade, vulnerabilidade e improviso, traz a solidez de processos bem delineados, "
            "resguardando a instituicao de riscos juridicos, glosas financeiras e desgastes na rotina."
        ),
        "fragilidade": (
            "Confunde o cumprimento burocratico de regras com a eficacia do trabalho socioeducativo. O apego excessivo a normas, formularios "
            "e procedimentos padronizados pode sufocar o acolhimento sensivel as pessoas, transformando o cuidado relacional em uma entrega fria e puramente contratual."
        ),
        "pergunta": "«Os nossos procedimentos funcionam como trilhos que ajudam as pessoas a avancar com seguranca rumo ao seu desenvolvimento, ou como barreiras que distanciam o encontro humano com quem precisa?»"
    },
    "D": {
        "nome": "O Jardineiro",
        "subtitulo": "O cuidado com a vida, o discernimento das estacoes",
        "cor": "#4338CA",
        "imagem": "logo_jardineiro.png",
        "virtude": (
            "Voce integra a fidelidade a causa com a consistencia de metodo. Conhece a natureza da semente (a vocacao da obra) "
            "e analisa com lucidez as condicoes do solo e do clima (a realidade do territorio). Emprega as ferramentas de planejamento "
            "nao como um fim em si mesmas, mas como podas necessarias e canais de irrigacao para fazer desabrochar a dignidade das pessoas e da comunidade."
        ),
        "fragilidade": (
            "A sua postura exige uma capacidade constante de sintese e discernimento: sustentar a gratuidade do encontro junto a viabilidade financeira; "
            "ter a coragem de dizer nao a projetos desalinhados sem perder a sensibilidade social; e zelar sem tregua pela saude fisica e emocional da sua equipe."
        ),
        "pergunta": "«O que precisamos ter a coragem de podar hoje para que a nossa obra continue dando frutos verdadeiros amanha?»"
    }
}

# -------------------------------------------------------------
# Inicializacao do Estado (Session State)
# -------------------------------------------------------------
if "etapa_atual" not in st.session_state:
    st.session_state.etapa_atual = 1
if "respostas" not in st.session_state:
    st.session_state.respostas = {}
if "teste_concluido" not in st.session_state:
    st.session_state.teste_concluido = False

def reiniciar_teste():
    st.session_state.etapa_atual = 1
    st.session_state.respostas = {}
    st.session_state.teste_concluido = False

# -------------------------------------------------------------
# Cabecalho da Aplicacao com Logo Responsivo
# -------------------------------------------------------------
logo_path = "logo_autoteste_rota.png"

col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)

st.markdown('<div class="main-title">A Rota da Obra</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Percurso de reflexao e maturidade estrategica nas obras sociais e socioeducativas</div>', unsafe_allow_html=True)

# -------------------------------------------------------------
# Tela de Resultados
# -------------------------------------------------------------
if st.session_state.teste_concluido:
    st.success("Voce concluiu as 6 etapas do percurso estrategico.")

    contagem = {"A": 0, "B": 0, "C": 0, "D": 0}
    for resp in st.session_state.respostas.values():
        if resp in contagem:
            contagem[resp] += 1

    max_respostas = max(contagem.values())
    predominantes = [letra for letra, qtd in contagem.items() if qtd == max_respostas]

    st.subheader("Distribuicao dos Arquetipos na sua Lideranca")

    categorias = [PERFIS[k]["nome"] for k in ["A", "B", "C", "D"]]
    valores = [contagem[k] for k in ["A", "B", "C", "D"]]
    cores = [PERFIS[k]["cor"] for k in ["A", "B", "C", "D"]]

    fig = go.Figure(data=[
        go.Bar(
            x=categorias,
            y=valores,
            text=[f"{v} escolhas" for v in valores],
            textposition="auto",
            marker_color=cores
        )
    ])
    fig.update_layout(
        yaxis=dict(range=[0, 6], dtick=1, title="Numero de escolhas"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=320
    )
    st.plotly_chart(fig, use_container_width=True)

    # Destaque do Perfil Predominante com Imagem
    if len(predominantes) == 1:
        letra_p = predominantes[0]
        perfil_p = PERFIS[letra_p]
        
        st.markdown(f"### Perfil Predominante: {perfil_p['nome']}")
        
        # Exibicao da imagem correspondente em destaque centralizado
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            if os.path.exists(perfil_p["imagem"]):
                st.image(perfil_p["imagem"], use_container_width=True)

        st.markdown(f"""
            <div style="background-color: #EFF6FF; border: 2px solid {perfil_p['cor']}; padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <p><em>«{perfil_p['subtitulo']}»</em></p>
                <p><strong>A virtude do arquetipo:</strong> {perfil_p['virtude']}</p>
                <p><strong>A fragilidade institucional:</strong> {perfil_p['fragilidade']}</p>
                <hr style="border-top: 1px solid #BFDBFE;">
                <p style="font-weight: 600; font-size: 1.05rem; color: #1E3A8A;">Pergunta para desenvolvimento pessoal e comunitario:<br>{perfil_p['pergunta']}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        nomes_predominantes = [PERFIS[l]['nome'] for l in predominantes]
        st.info(
            f"Perfil Hibrido Equilibrado: Voce apresentou a mesma pontuacao maxima entre os perfis: "
            f"{', '.join(nomes_predominantes)}. "
            "Isso reflete uma lideranca que transita entre diferentes posturas conforme o contexto."
        )

    # Detalhamento de todos os arquetipos em abas
    st.markdown("### Compreensao Detalhada dos 4 Arquetipos")
    tabs = st.tabs([PERFIS[k]["nome"] for k in ["A", "B", "C", "D"]])
    for i, k in enumerate(["A", "B", "C", "D"]):
        p = PERFIS[k]
        with tabs[i]:
            # Imagem do perfil na aba
            col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
            with col_t2:
                if os.path.exists(p["imagem"]):
                    st.image(p["imagem"], use_container_width=True)

            st.markdown(f"**Lema:** *«{p['subtitulo']}»*")
            st.markdown(f"**Pontuacao neste teste:** {contagem[k]} de 6 etapas")
            st.write(f"**O Dom e a Virtude:** {p['virtude']}")
            st.write(f"**Atencao ao Risco / Sombra:** {p['fragilidade']}")
            st.info(f"Questao de Reflexao: {p['pergunta']}")

    # Resumo das escolhas
    with st.expander("Rever o seu historico de escolhas"):
        for num, etapa in enumerate(ETAPAS, start=1):
            escolha = st.session_state.respostas.get(num, "-")
            p_nome = PERFIS.get(escolha, {}).get("nome", "-")
            st.markdown(f"**Etapa {num}:** Escolha **[{escolha}]** ({p_nome})")
            st.caption(f"_{etapa['opcoes'].get(escolha, '')}_")

    st.button("Reiniciar o Teste", on_click=reiniciar_teste, type="primary")

# -------------------------------------------------------------
# Tela do Questionario Guiado (Etapas 1 a 6)
# -------------------------------------------------------------
else:
    etapa_idx = st.session_state.etapa_atual - 1
    etapa_dado = ETAPAS[etapa_idx]

    progresso = (st.session_state.etapa_atual - 1) / 6.0
    st.progress(progresso)
    st.caption(f"Etapa {st.session_state.etapa_atual} de 6 no ciclo de planejamento estrategico")

    st.markdown(f"""
        <div class="step-card">
            <div class="dilemma-title">{etapa_dado['titulo']}</div>
            <div class="dilemma-text"><strong>O dilema decisorio:</strong><br>{etapa_dado['dilema']}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**Como voces orientariam a decisao real da sua organizacao?**")

    opcoes_keys = ["A", "B", "C", "D"]
    resposta_previa = st.session_state.respostas.get(st.session_state.etapa_atual, None)
    indice_default = opcoes_keys.index(resposta_previa) if resposta_previa else 0

    escolha_selecionada = st.radio(
        label="Selecione a opcao que melhor reflete a postura predominante:",
        options=opcoes_keys,
        index=indice_default,
        format_func=lambda k: f"[{k}] {etapa_dado['opcoes'][k]}",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.session_state.etapa_atual > 1:
            if st.button("Voltar"):
                st.session_state.etapa_atual -= 1
                st.rerun()

    with col3:
        if st.session_state.etapa_atual < 6:
            if st.button("Avancar", type="primary"):
                st.session_state.respostas[st.session_state.etapa_atual] = escolha_selecionada
                st.session_state.etapa_atual += 1
                st.rerun()
        else:
            if st.button("Finalizar Teste", type="primary"):
                st.session_state.respostas[st.session_state.etapa_atual] = escolha_selecionada
                st.session_state.teste_concluido = True
                st.rerun()
