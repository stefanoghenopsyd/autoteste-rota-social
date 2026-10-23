import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# -------------------------------------------------------------
# Configuração da Página
# -------------------------------------------------------------
st.set_page_config(
    page_title="A Rota da Obra | Autoavaliação Estratégica",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Estilização CSS personalizada para leitura confortável
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.3rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
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
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# Base de Dados: Etapas, Dilemas e Opções
# -------------------------------------------------------------
ETAPAS = [
    {
        "numero": 1,
        "titulo": "Etapa 1: Identidade e Direção (Missão, Visão, Valores)",
        "dilema": (
            "Uma importante fundação empresarial oferece um financiamento relevante voltado para a comunidade "
            "local em que atuamos. No entanto, impõe exigências muito rígidas e setoriais quanto ao tema das "
            "intervenções a serem apoiadas. Os temas propostos não coincidem com a tradição socioeducativa da nossa obra. "
            "Como vocês entendem que devem orientar a sua escolha?"
        ),
        "opcoes": {
            "A": (
                "Acolhemos as prioridades e a linguagem do financiador: para garantir a continuidade "
                "material do serviço e não deixar faltar o sustento à comunidade, a prioridade é captar "
                "os recursos disponíveis, adaptando inclusive as nossas atividades às demandas externas."
            ),
            "B": (
                "Recusamos a proposta: a fidelidade à vocação original da obra não admite concessões diante de "
                "prioridades definidas externamente; preferimos enfrentar sacrifícios econômicos e reduções de equipe "
                "a correr o risco de perder a nossa identidade histórica."
            ),
            "C": (
                "Verificamos a conformidade administrativa, contratual e estatutária do edital: se os requisitos formatais "
                "forem sustentáveis, participamos nos limitando a executar as entregas exigidas com precisão e respeitando as normas."
            ),
            "D": (
                "Abrimos um diálogo com o doador e tentamos negociar, buscando demonstrar como a nossa identidade e o nosso "
                "conhecimento do território podem enriquecer a proposta, traduzindo o edital em respostas reais para a comunidade "
                "sem trair a nossa missão original."
            ),
        },
    },
    {
        "numero": 2,
        "titulo": "Etapa 2: Análise do Contexto (Diagnóstico Interno e Externo)",
        "dilema": (
            "As transformações sociais e demográficas do bairro tornam evidente que alguns serviços históricos "
            "oferecidos pelo nosso centro social são cada vez menos frequentados, ao mesmo tempo em que surgem novas formas "
            "de vulnerabilidade e fragilidade às quais a obra ainda não está respondendo. Como vocês pensam em conduzir esta fase de diagnóstico?"
        ),
        "opcoes": {
            "A": (
                "Direcionamos a análise principalmente para as linhas de financiamento indicadas pelas políticas públicas "
                "ou pelos planos de assistência social do território, alinhando rapidamente a nossa atuação àquilo que será financiado nos próximos ciclos."
            ),
            "B": (
                "Mantemos inalterados os serviços históricos: a queda no número de participantes é, sem dúvida, uma crise passageira "
                "do território ou, infelizmente, uma falta de interesse em propostas de valor que nós, de qualquer forma, queremos continuar sustentando com fidelidade."
            ),
            "C": (
                "Atualizamos o diagnóstico por meio da coleta periódica de dados estatísticos, censos e formulários padronizados, "
                "elaborando um mapeamento formal útil para relatórios de prestação de contas, balanços sociais e auditorias de qualidade."
            ),
            "D": (
                "Promovemos um processo de escuta ativa no território (famílias, escolas, comerciantes e lideranças locais, serviços públicos) "
                "e o cruzamos com as competências e limites reais da equipe, para compreender com clareza o que é preciso preservar, o que transformar e o que encerrar."
            ),
        },
    },
    {
        "numero": 3,
        "titulo": "Etapa 3: Formulação dos Objetivos Estratégicos (Escolha das Prioridades)",
        "dilema": (
            "No momento do planejamento, a nossa obra se depara com múltiplos apelos da comunidade e com demandas urgentes, "
            "contando, porém, com recursos humanos e econômicos limitados. Com qual critério vocês procuram definir as metas futuras?"
        ),
        "opcoes": {
            "A": (
                "Estabelecemos uma gama muito ampla e flexível de objetivos gerais, formulados de modo a viabilizar qualquer "
                "oportunidade futura de projeto ou edital, sem fechar nenhuma porta de financiamento."
            ),
            "B": (
                "Rejeitamos a lógica de metas formais ou quantitativas: para nós, o único objetivo autêntico é a disponibilidade "
                "diária para acolher quem bate à nossa porta, sem nos deixar engessar por parâmetros pré-estabelecidos ou cálculos de gestão."
            ),
            "C": (
                "Traduzimos as diretrizes em uma lista detalhada de atribuições, volumes de atendimento e prazos alinhados aos "
                "padrões de certificação, convênios e termos de parceria com os órgãos públicos ou financiadores."
            ),
            "D": (
                "Selecionamos um conjunto restrito de prioridades estratégicas claras e compartilhadas com a equipe, definindo "
                "para cada uma a mudança esperada na vida das pessoas, os indicadores de acompanhamento e as responsabilidades operacionais."
            ),
        },
    },
    {
        "numero": 4,
        "titulo": "Etapa 4: Planejamento Operacional e Alocação de Recursos (Pessoas e Meios)",
        "dilema": (
            "Para iniciar uma nova iniciativa socioassistencial ou educativa complexa, é necessário distribuir cargas de trabalho, "
            "responsabilidades, orçamento e prazos de execução entre os educadores e colaboradores. Como se deve proceder nessa atribuição?"
        ),
        "opcoes": {
            "A": (
                "Concentramos os recursos nas atividades de maior visibilidade para os apoiadores externos, exigindo dos colaboradores "
                "flexibilidade e espírito de sacrifício constante para suprir as lacunas operacionais à medida que surgirem."
            ),
            "B": (
                "Confiamos na dedicação e no engajamento espontâneo dos colaboradores históricos, acreditando que a motivação pela causa "
                "deva compensar a escassez de recursos e a ausência de planos operacionais formais."
            ),
            "C": (
                "Estabelecemos descrições de função rígidas, horários fixos e um cronograma minucioso, exigindo o cumprimento estrito "
                "das escalas e tarefas designadas para evitar falhas organizacionais."
            ),
            "D": (
                "Construímos o plano de trabalho de forma participativa com as coordenações e com as equipes: definimos cargas sustentáveis "
                "de trabalho, asseguramos momentos dedicados de supervisão e alinhamento, e reservamos recursos específicos para a segurança e o cuidado com a equipe."
            ),
        },
    },
    {
        "numero": 5,
        "titulo": "Etapa 5: Execução e Alinhamento Organizacional (Implementação)",
        "dilema": (
            "Durante a fase de execução, ocorrem tensões imprevistas — conflitos entre colaboradores, dificuldades inesperadas no relacionamento "
            "com os atendidos ou com a administração pública, episódios de violência ou instabilidade no território — que colocam à prova a sustentação do serviço. "
            "Como a rotina de trabalho deve ser conduzida?"
        ),
        "opcoes": {
            "A": (
                "Reorientamos rapidamente as atividades do dia a dia, priorizando soluções que evitem atritos com agentes externos ou "
                "que garantam a continuidade das prestações de contas, mesmo que isso custe a profundidade do processo pedagógico e social iniciado."
            ),
            "B": (
                "Pedimos à equipe que resista e siga em frente sem alterar a condução inicial, compreendendo o desgaste e as dificuldades "
                "como parte inevitável do testemunho e da doação exigidos pela causa."
            ),
            "C": (
                "Exigimos de todos o cumprimento estrito dos regulamentos e protocolos operacionais em vigor, delegando a resolução de casos "
                "excepcionais à publicação de novas orientações internas ou ordens de serviço."
            ),
            "D": (
                "A liderança assegura proximidade e presença direta no território: criam-se momentos de escuta e suporte para acolher as dificuldades, "
                "reajustando as práticas de forma flexível, mas coerente com os propósitos originais."
            ),
        },
    },
    {
        "numero": 6,
        "titulo": "Etapa 6: Monitoramento, Avaliação de Impacto e Aprendizado",
        "dilema": (
            "Ao término do ciclo anual anterior ou do projeto executado, precisamos fazer um balanço do trabalho realizado para prestar "
            "contas da intervenção e definir os rumos do próximo ciclo. Em que vocês vão focar principalmente?"
        ),
        "opcoes": {
            "A": (
                "A prioridade é cuidar da comunicação externa e da relação com os financiadores, destacando os pontos fortes e os indicadores "
                "que favoreçam a renovação das parcerias e a continuidade dos repasses."
            ),
            "B": (
                "Não realizamos avaliações estruturadas porque temos a convicção de que o verdadeiro valor da ação socioeducativa não se mede em números. "
                "Confiamos na certeza interna de ter feito tudo o que era possível com espírito de gratuidade."
            ),
            "C": (
                "Mensuramos rigorosamente as metas quantitativas de entrega (atendimentos realizados, frequências registradas, refeições servidas, "
                "comprovantes de despesa) para assegurar a total conformidade administrativa e fiscal."
            ),
            "D": (
                "Avaliamos o impacto real envolvendo educadores, famílias atendidas e parceiros locais: analisamos tanto os avanços quanto os insucessos, "
                "convertendo a experiência concreta em aprendizado institucional para aprimorar o futuro."
            ),
        },
    },
]

PERFIS = {
    "A": {
        "nome": "O Buscador de Água",
        "subtitulo": "A urgência da fonte, o risco da deriva",
        "cor": "#0284C7",
        "virtude": (
            "Você é movido pela responsabilidade vital de assegurar a subsistência da obra. "
            "Tem sensibilidade para captar oportunidades, senso prático, facilidade para dialogar com diferentes atores "
            "e rapidez de resposta. Sem a sua atuação, muitas vezes a instituição não teria os meios concretos para abrir as portas a cada dia."
        ),
        "fragilidade": (
            "De tanto ir atrás dos cursos d'água apontados por terceiros (editais de momento, exigências de fundações ou tendências passageiras), "
            "você corre o risco de desviar a caravana do seu destino original (mission drift). Os educadores na ponta podem se sentir desorientados, "
            "com dificuldade de enxergar o sentido comum que conecta as inúmeras ações iniciadas."
        ),
        "pergunta": "«Se tivéssemos toda a água garantida para os próximos três anos, saberíamos dizer com clareza em direção a qual terra prometida estamos caminhando?»",
    },
    "B": {
        "nome": "O Carvalho de Pedra",
        "subtitulo": "As raízes firmes, a sombra que não se move",
        "cor": "#15803D",
        "virtude": (
            "Você guarda com firmeza e dedicação a memória, os princípios fundadores e o propósito da obra. "
            "Não cede diante de caminhos fáceis nem se deixa levar por modismos de gestão. É uma referência ética e afetiva "
            "que transmite acolhimento, gratuidade e forte sentimento de pertença a toda a comunidade."
        ),
        "fragilidade": (
            "Confunde a fidelidade à origem com o apego imutável às práticas do passado. Ao recusar uma leitura realista das mudanças "
            "do entorno ou ao rejeitar ferramentas organizacionais atuais, arrisca levar a obra ao isolamento e ao esgotamento financeiro, "
            "tornando-a aos poucos incapaz de atender aos reais desafios das novas gerações."
        ),
        "pergunta": "«Cuidar do fogo dos fundadores significa guardar as cinzas do passado ou acender novas chamas capazes de iluminar a realidade de hoje?»",
    },
    "C": {
        "nome": "O Relógio de Precisão",
        "subtitulo": "O ritmo compassado, o abrigo das regras",
        "cor": "#B45309",
        "virtude": (
            "Você zela pela ordem, pela prestação de contas transparente, pela equidade nas relações de trabalho e pelo rigor administrativo. "
            "Em cenários marcados por instabilidade, vulnerabilidade e improviso, traz a solidez de processos bem delineados, "
            "resguardando a instituição de riscos jurídicos, glosas financeiras e desgastes na rotina."
        ),
        "fragilidade": (
            "Confunde o cumprimento burocrático de regras com a eficácia do trabalho socioeducativo. O apego excessivo a normas, formulários "
            "e procedimentos padronizados pode sufocar o acolhimento sensível às pessoas, transformando o cuidado relacional em uma entrega fria e puramente contratual."
        ),
        "pergunta": "«Os nossos procedimentos funcionam como trilhos que ajudam as pessoas a avançar com segurança rumo ao seu desenvolvimento, ou como barreiras que distanciam o encontro humano com quem precisa?»",
    },
    "D": {
        "nome": "O Jardineiro",
        "subtitulo": "O cuidado com a vida, o discernimento das estações",
        "cor": "#4338CA",
        "virtude": (
            "Você integra a fidelidade à causa com a consistência de método. Conhece a natureza da semente (a vocação da obra) "
            "e analisa com lucidez as condições do solo e do clima (a realidade do território). Emprega as ferramentas de planejamento "
            "não como um fim em si mesmas, mas como podas necessárias e canais de irrigação para fazer desabrochar a dignidade das pessoas e da comunidade."
        ),
        "fragilidade": (
            "A sua postura exige uma capacidade constante de síntese e discernimento: sustentar a gratuidade do encontro junto à viabilidade financeira; "
            "ter a coragem de dizer 'não' a projetos desalinhados sem perder a sensibilidade social; e zelar sem trégua pela saúde física e emocional da sua equipe."
        ),
        "pergunta": "«O que precisamos ter a coragem de podar hoje para que a nossa obra continue dando frutos verdadeiros amanhã?»",
    },
}

# -------------------------------------------------------------
# Inicialização do Estado (Session State)
# -------------------------------------------------------------
if "etapa_atual" not in st.session_state:
    st.session_state.etapa_atual = 1
if "respostas" not in st.session_state:
    st.session_state.respostas = {}  # {1: 'A', 2: 'D', ...}
if "teste_concluido" not in st.session_state:
    st.session_state.teste_concluido = False


def reiniciar_teste():
    st.session_state.etapa_atual = 1
    st.session_state.respostas = {}
    st.session_state.teste_concluido = False


# -------------------------------------------------------------
# Cabeçalho da Aplicação
# -------------------------------------------------------------
st.markdown(
    '<div class="main-title">🧭 A Rota da Obra</div>', unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Percurso de reflexão e maturidade estratégica nas obras sociais e socioeducativas</div>',
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# Tela de Resultados (quando o teste é concluído)
# -------------------------------------------------------------
if st.session_state.teste_concluido:
    st.success("🎉 Você concluiu as 6 etapas do percurso estratégico!")

    # Contagem de respostas por perfil
    contagem = {"A": 0, "B": 0, "C": 0, "D": 0}
    for resp in st.session_state.respostas.values():
        if resp in contagem:
            contagem[resp] += 1

    # Identificar o perfil ou perfis predominantes
    max_respostas = max(contagem.values())
    predominantes = [
        letra for letra, qtd in contagem.items() if qtd == max_respostas
    ]

    st.subheader("📊 Distribuição dos Arquétipos na sua Liderança")

    # Gráfico Radar / Barras usando Plotly
    categorias = [PERFIS[k]["nome"] for k in ["A", "B", "C", "D"]]
    valores = [contagem[k] for k in ["A", "B", "C", "D"]]
    cores = [PERFIS[k]["cor"] for k in ["A", "B", "C", "D"]]

    fig = go.Figure(
        data=[
            go.Bar(
                x=categorias,
                y=valores,
                text=[f"{v} escolhas" for v in valores],
                textposition="auto",
                marker_color=cores,
            )
        ]
    )
    fig.update_layout(
        yaxis=dict(range=[0, 6], dtick=1, title="Número de escolhas"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Destaque do Perfil Predominante
    if len(predominantes) == 1:
        letra_p = predominantes[0]
        perfil_p = PERFIS[letra_p]
        st.markdown(
            f"""
            <div style="background-color: #EFF6FF; border: 2px solid {perfil_p['cor']}; padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <h3 style="color: {perfil_p['cor']}; margin-top: 0;">Seu Perfil Predominante: {perfil_p['nome']}</h3>
                <p><em>«{perfil_p['subtitulo']}»</em></p>
                <p><strong>A virtude do arquétipo:</strong> {perfil_p['virtude']}</p>
                <p><strong>A fragilidade institucional:</strong> {perfil_p['fragilidade']}</p>
                <hr style="border-top: 1px solid #BFDBFE;">
                <p style="font-weight: 600; font-size: 1.05rem; color: #1E3A8A;">💬 Pergunta para desenvolvimento pessoal e comunitário:<br>{perfil_p['pergunta']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info(
            f"**Perfil Híbrido Equilibrado:** Você apresentou a mesma pontuação máxima entre os perfis: "
            f"{', '.join([PERFIS[l]['nome'] for l in predominantes])}. "
            "Isso reflete uma liderança que transita entre diferentes posturas conforme a pressão do momento."
        )

    # Detalhamento de todos os arquétipos em abas
    st.markdown("### 🔍 Compreensão Detalhada dos 4 Arquétipos")
    tabs = st.tabs([PERFIS[k]["nome"] for k in ["A", "B", "C", "D"]])
    for i, k in enumerate(["A", "B", "C", "D"]):
        p = PERFIS[k]
        with tabs[i]:
            st.markdown(f"**Lema:** *«{p['subtitulo']}»*")
            st.markdown(f"**Pontuação neste teste:** {contagem[k]} de 6 etapas")
            st.write(f"**O Dom e a Virtude:** {p['virtude']}")
            st.write(f"**Atenção ao Risco / Sombra:** {p['fragilidade']}")
            st.info(f"**Questão de Reflexão:** {p['pergunta']}")

    # Resumo das escolhas etapa por etapa
    with st.expander("📝 Rever o seu histórico de escolhas"):
        for num, etapa in enumerate(ETAPAS, start=1):
            escolha = st.session_state.respostas.get(num, "-")
            p_nome = PERFIS.get(escolha, {}).get("nome", "-")
            st.markdown(
                f"**Etapa {num}:** Escolha **[{escolha}]** ({p_nome})"
            )
            st.caption(f"_{etapa['opcoes'].get(escolha, '')}_")

    st.button("🔄 Reiniciar o Teste", on_click=reiniciar_teste, type="primary")

# -------------------------------------------------------------
# Tela do Questionário Guiado (Etapas 1 a 6)
# -------------------------------------------------------------
else:
    etapa_idx = st.session_state.etapa_atual - 1
    etapa_dado = ETAPAS[etapa_idx]

    # Barra de Progresso
    progresso = (st.session_state.etapa_atual - 1) / 6.0
    st.progress(progresso)
    st.caption(
        f"Etapa {st.session_state.etapa_atual} de 6 no ciclo de planejamento estratégico"
    )

    # Apresentação do Dilema
    st.markdown(
        f"""
        <div class="step-card">
            <div class="dilemma-title">{etapa_dado['titulo']}</div>
            <div class="dilemma-text"><strong>O dilema decisório:</strong><br>{etapa_dado['dilema']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "**Como vocês orientariam a decisão real da sua organização?**"
    )

    # Opções do Radio
    opcoes_keys = ["A", "B", "C", "D"]
    opcoes_formatadas = [
        f"[{k}] {etapa_dado['opcoes'][k]}" for k in opcoes_keys
    ]

    # Recupera resposta anterior se houver
    resposta_previa = st.session_state.respostas.get(
        st.session_state.etapa_atual, None
    )
    indice_default = (
        opcoes_keys.index(resposta_previa) if resposta_previa else 0
    )

    escolha_selecionada = st.radio(
        label="Selecione a opção que melhor reflete a postura predominante:",
        options=opcoes_keys,
        index=indice_default,
        format_func=lambda k: f"[{k}] {etapa_dado['opcoes'][k]}",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.session_state.etapa_atual > 1:
            if st.button("⬅ Voltar"):
                st.session_state.etapa_atual -= 1
                st.rerun()

    with col3:
        if st.session_state.etapa_atual < 6:
            if st.button("Avançar ➡", type="primary"):
                st.session_state.respostas[st.session_state.etapa_atual] = (
                    escolha_selecionada
                )
                st.session_state.etapa_atual += 1
                st.rerun()
        else:
            if st.button("Finalizar Teste ✅", type="primary"):
                st.session_state.respostas[st.session_state.etapa_atual] = (
                    escolha_selecionada
                )
                st.session_state.teste_concluido = True
                st.rerun()