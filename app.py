import streamlit as st
from dataclasses import dataclass
from itertools import product

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="LoL Team Balance",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 League of Legends Team Balancer")
st.caption("Monte dois times equilibrados considerando Elo e Função.")

# =====================================================
# CONSTANTES
# =====================================================

ELOS = {
    "Ferro IV":100,
    "Ferro III":200,
    "Ferro II":300,
    "Ferro I":400,

    "Bronze IV":500,
    "Bronze III":600,
    "Bronze II":700,
    "Bronze I":800,

    "Prata IV":900,
    "Prata III":1000,
    "Prata II":1100,
    "Prata I":1200,

    "Ouro IV":1350,
    "Ouro III":1500,
    "Ouro II":1650,
    "Ouro I":1800,

    "Platina IV":2000,
    "Platina III":2200,
    "Platina II":2400,
    "Platina I":2600,

    "Esmeralda IV":2900,
    "Esmeralda III":3200,
    "Esmeralda II":3500,
    "Esmeralda I":3800,

    "Diamante IV":4200,
    "Diamante III":4600,
    "Diamante II":5000,
    "Diamante I":5400,

    "Mestre":6100,
    "Grão-Mestre":7000,
    "Desafiante":8000
}

ROTAS = [
    "Top",
    "Jungle",
    "Mid",
    "ADC",
    "Suporte"
]

PESO_ROTAS = {
    "Top":1.00,
    "Jungle":1.20,
    "Mid":1.15,
    "ADC":1.10,
    "Suporte":1.00
}

ICONE_ROTAS = {
    "Top": "⚔️",
    "Jungle": "🌳",
    "Mid": "🔮",
    "ADC": "🏹",
    "Suporte": "🛡️"
}

# =====================================================
# CLASSE DO JOGADOR
# =====================================================

@dataclass
class Jogador:
    nome: str
    rota: str
    elo: str

    @property
    def pontos(self):
        return ELOS[self.elo] * PESO_ROTAS[self.rota]

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def contar_rotas(jogadores):

    contagem = {}

    for rota in ROTAS:
        contagem[rota] = 0

    for jogador in jogadores:
        contagem[jogador.rota] += 1

    return contagem


def validar_times(jogadores):

    if len(jogadores) != 10:
        return False, "É necessário cadastrar exatamente 10 jogadores."

    contagem = contar_rotas(jogadores)

    for rota in ROTAS:

        if contagem[rota] != 2:
            return False, f"A rota {rota} deve possuir exatamente 2 jogadores."

    return True, ""


def gerar_texto_composicao(time_azul, time_vermelho, pontos_azul, pontos_vermelho):

    linhas = []

    linhas.append("=" * 40)
    linhas.append("🎮 LOL TEAM BALANCER — COMPOSIÇÃO DOS TIMES")
    linhas.append("=" * 40)
    linhas.append("")
    linhas.append(f"🟦 TIME AZUL — {int(pontos_azul)} pts")

    for jogador in time_azul:
        linhas.append(
            f"  {ICONE_ROTAS[jogador.rota]} {jogador.rota:<8} | {jogador.nome:<15} | {jogador.elo} ({int(jogador.pontos)} pts)"
        )

    linhas.append("")
    linhas.append(f"🟥 TIME VERMELHO — {int(pontos_vermelho)} pts")

    for jogador in time_vermelho:
        linhas.append(
            f"  {ICONE_ROTAS[jogador.rota]} {jogador.rota:<8} | {jogador.nome:<15} | {jogador.elo} ({int(jogador.pontos)} pts)"
        )

    linhas.append("")
    linhas.append(f"⚖️ Diferença total: {int(abs(pontos_azul - pontos_vermelho))} pts")
    linhas.append("=" * 40)

    return "\n".join(linhas)


# =====================================================
# ESTILO (CSS)
# =====================================================

st.markdown("""
<style>
.team-card {
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}
.blue-card {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    color: white;
}
.red-card {
    background: linear-gradient(135deg, #7f1d1d, #b91c1c);
    color: white;
}
.team-card h3 {
    margin-top: 0;
    margin-bottom: 4px;
}
.team-total {
    font-size: 0.95rem;
    opacity: 0.9;
    margin-bottom: 14px;
}
.player-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.18);
    font-size: 0.95rem;
}
.player-row:last-child {
    border-bottom: none;
}
.player-role {
    opacity: 0.85;
    font-size: 0.85rem;
}
.winner-badge {
    display: inline-block;
    background: gold;
    color: #1a1a1a;
    padding: 2px 12px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.8rem;
    margin-left: 8px;
}
.rota-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
}
.rota-completa {
    background: rgba(46, 204, 113, 0.18);
    color: #2ecc71;
    border: 1px solid rgba(46, 204, 113, 0.4);
}
.rota-incompleta {
    background: rgba(241, 196, 15, 0.15);
    color: #f1c40f;
    border: 1px solid rgba(241, 196, 15, 0.35);
}
@media (max-width: 640px) {
    .team-card {
        padding: 16px;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# ESTADO DE SESSÃO
# =====================================================

if "jogadores" not in st.session_state:
    st.session_state.jogadores = []

if "resultado" not in st.session_state:
    st.session_state.resultado = None

# =====================================================
# CADASTRO DE JOGADORES (formulário único)
# =====================================================

st.header("Cadastro de Jogadores")

contagem_atual = contar_rotas(st.session_state.jogadores)
vagas_disponiveis = [
    rota for rota in ROTAS if contagem_atual[rota] < 2
]
cadastro_completo = (len(st.session_state.jogadores) >= 10)

with st.form("form_add_jogador", clear_on_submit=True):

    c1, c2, c3, c4 = st.columns([3, 2, 2, 1.4])

    with c1:
        nome_input = st.text_input("Nome", placeholder="Nome do jogador")

    with c2:
        rota_input = st.selectbox(
            "Função",
            ROTAS if not vagas_disponiveis else vagas_disponiveis,
        )

    with c3:
        elo_input = st.selectbox(
            "Elo",
            list(ELOS.keys()),
            index=12
        )

    with c4:
        st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
        confirmar = st.form_submit_button(
            "➕ Adicionar",
            type="primary",
            use_container_width=True,
            disabled=cadastro_completo
        )

if confirmar:

    if cadastro_completo:
        st.error("Já existem 10 jogadores cadastrados.")

    elif not nome_input.strip():
        st.error("Informe o nome do jogador antes de adicionar.")

    elif contagem_atual[rota_input] >= 2:
        st.error(f"A rota {rota_input} já possui 2 jogadores cadastrados.")

    else:
        st.session_state.jogadores.append(
            Jogador(
                nome=nome_input.strip(),
                rota=rota_input,
                elo=elo_input
            )
        )
        st.success(f"{nome_input.strip()} adicionado como {rota_input}.")
        st.rerun()

# --------------------------------------------
# STATUS DAS ROTAS (badges)
# --------------------------------------------

contagem_atual = contar_rotas(st.session_state.jogadores)

badges_html = ""
for rota in ROTAS:
    classe = "rota-completa" if contagem_atual[rota] == 2 else "rota-incompleta"
    badges_html += f'<span class="rota-badge {classe}">{ICONE_ROTAS[rota]} {rota}: {contagem_atual[rota]}/2</span>'

st.markdown(badges_html, unsafe_allow_html=True)

# =====================================================
# LISTA DE JOGADORES CADASTRADOS
# =====================================================

st.divider()

col_titulo, col_limpar = st.columns([4, 1])

with col_titulo:
    st.header(f"Jogadores cadastrados ({len(st.session_state.jogadores)}/10)")

with col_limpar:
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    if st.button("🧹 Limpar tudo", use_container_width=True, disabled=(len(st.session_state.jogadores) == 0)):
        st.session_state.jogadores = []
        st.session_state.resultado = None
        st.rerun()

if st.session_state.jogadores:

    for i, jogador in enumerate(st.session_state.jogadores):

        r1, r2, r3, r4, r5 = st.columns([0.6, 2.5, 1.5, 2, 0.8])

        with r1:
            st.markdown(f"**{ICONE_ROTAS[jogador.rota]}**")
        with r2:
            st.markdown(f"**{jogador.nome}**")
        with r3:
            st.markdown(jogador.rota)
        with r4:
            st.markdown(f"{jogador.elo} · {int(jogador.pontos)} pts")
        with r5:
            if st.button("🗑️", key=f"remover_{i}", use_container_width=True):
                st.session_state.jogadores.pop(i)
                st.session_state.resultado = None
                st.rerun()

else:

    st.info("Nenhum jogador cadastrado. Use o formulário acima para adicionar.")

# =====================================================
# VALIDAÇÃO
# =====================================================

valido, mensagem = validar_times(st.session_state.jogadores)

st.divider()

if valido:
    st.success("Cadastro válido — pronto para balancear.")
else:
    st.warning(mensagem)

# =====================================================
# BOTÕES
# =====================================================

col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    balancear = st.button(
        "🎮 Balancear Times",
        type="primary",
        use_container_width=True,
        disabled=not valido
    )

with col_btn2:
    recalcular = st.button(
        "🔁 Recalcular",
        use_container_width=True,
        disabled=(st.session_state.resultado is None)
    )

if recalcular:
    st.session_state.resultado = None
    st.rerun()

if balancear:

    if not valido:
        st.error(mensagem)
        st.stop()

    jogadores = st.session_state.jogadores

    # ==================================================
    # ORGANIZAÇÃO DOS JOGADORES POR ROTA
    # ==================================================

    jogadores_por_rota = {}

    for rota in ROTAS:
        jogadores_por_rota[rota] = []

    for jogador in jogadores:
        jogadores_por_rota[jogador.rota].append(jogador)

    # ==================================================
    # GERAÇÃO DAS 32 COMBINAÇÕES
    # ==================================================

    melhor_time_azul = None
    melhor_time_vermelho = None

    melhor_diferenca = float("inf")
    melhor_diferenca_rotas = float("inf")
    melhor_maior_elo = float("inf")
    melhor_menor_elo = float("inf")

    pontos_finais_azul = 0
    pontos_finais_vermelho = 0

    for escolha in product([0, 1], repeat=5):

        time_azul = []
        time_vermelho = []

        for indice, rota in enumerate(ROTAS):

            primeiro = jogadores_por_rota[rota][0]
            segundo = jogadores_por_rota[rota][1]

            if escolha[indice] == 0:
                time_azul.append(primeiro)
                time_vermelho.append(segundo)
            else:
                time_azul.append(segundo)
                time_vermelho.append(primeiro)

        # -----------------------------------------

        pontos_azul = sum(j.pontos for j in time_azul)
        pontos_vermelho = sum(j.pontos for j in time_vermelho)

        diferenca = abs(pontos_azul - pontos_vermelho)

        # -----------------------------------------
        # Critério de desempate 1
        # Diferença individual das rotas
        # -----------------------------------------

        diferenca_rotas = 0

        for a, v in zip(time_azul, time_vermelho):
            diferenca_rotas += abs(a.pontos - v.pontos)

        # -----------------------------------------
        # Critério de desempate 2
        # Diferença entre maiores elos
        # -----------------------------------------

        maior_azul = max(j.pontos for j in time_azul)
        maior_vermelho = max(j.pontos for j in time_vermelho)

        diferenca_maiores = abs(maior_azul - maior_vermelho)

        # -----------------------------------------
        # Critério de desempate 3
        # Diferença entre menores elos
        # -----------------------------------------

        menor_azul = min(j.pontos for j in time_azul)
        menor_vermelho = min(j.pontos for j in time_vermelho)

        diferenca_menores = abs(menor_azul - menor_vermelho)

        # -----------------------------------------
        # Escolha da melhor combinação
        # -----------------------------------------

        atualizar = False

        if diferenca < melhor_diferenca:
            atualizar = True

        elif diferenca == melhor_diferenca:

            if diferenca_rotas < melhor_diferenca_rotas:
                atualizar = True

            elif diferenca_rotas == melhor_diferenca_rotas:

                if diferenca_maiores < melhor_maior_elo:
                    atualizar = True

                elif diferenca_maiores == melhor_maior_elo:

                    if diferenca_menores < melhor_menor_elo:
                        atualizar = True

        if atualizar:

            melhor_diferenca = diferenca
            melhor_diferenca_rotas = diferenca_rotas
            melhor_maior_elo = diferenca_maiores
            melhor_menor_elo = diferenca_menores

            melhor_time_azul = time_azul
            melhor_time_vermelho = time_vermelho

            pontos_finais_azul = pontos_azul
            pontos_finais_vermelho = pontos_vermelho

    # ==================================================
    # ÍNDICE DE EQUILÍBRIO
    # ==================================================

    if melhor_diferenca <= 50:
        estrelas = "⭐⭐⭐⭐⭐"
        avaliacao = "Perfeito"
        equilibrio_percentual = 100

    elif melhor_diferenca <= 150:
        estrelas = "⭐⭐⭐⭐"
        avaliacao = "Muito equilibrado"
        equilibrio_percentual = 85

    elif melhor_diferenca <= 300:
        estrelas = "⭐⭐⭐"
        avaliacao = "Bom"
        equilibrio_percentual = 65

    elif melhor_diferenca <= 600:
        estrelas = "⭐⭐"
        avaliacao = "Aceitável"
        equilibrio_percentual = 40

    else:
        estrelas = "⭐"
        avaliacao = "Desequilibrado"
        equilibrio_percentual = 15

    # ==================================================
    # SALVANDO RESULTADO NA SESSÃO
    # ==================================================

    st.session_state.resultado = {
        "time_azul": melhor_time_azul,
        "time_vermelho": melhor_time_vermelho,
        "pontos_azul": pontos_finais_azul,
        "pontos_vermelho": pontos_finais_vermelho,
        "diferenca": melhor_diferenca,
        "estrelas": estrelas,
        "avaliacao": avaliacao,
        "equilibrio_percentual": equilibrio_percentual,
    }

# =====================================================
# PARTE 3 — EXIBIÇÃO DO RESULTADO
# =====================================================

resultado = st.session_state.resultado

if resultado:

    st.divider()
    st.header("🏆 Resultado do Balanceamento")

    time_azul = resultado["time_azul"]
    time_vermelho = resultado["time_vermelho"]
    pontos_azul = resultado["pontos_azul"]
    pontos_vermelho = resultado["pontos_vermelho"]
    diferenca = resultado["diferenca"]
    estrelas = resultado["estrelas"]
    avaliacao = resultado["avaliacao"]
    equilibrio_percentual = resultado["equilibrio_percentual"]

    time_vencedor = "azul" if pontos_azul >= pontos_vermelho else "vermelho"

    # --------------------------------------------
    # MÉTRICAS
    # --------------------------------------------

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "🟦 Time Azul",
            f"{int(pontos_azul)} pts",
            delta=int(pontos_azul - pontos_vermelho) if time_vencedor == "azul" else None
        )

    with m2:
        st.metric(
            "🟥 Time Vermelho",
            f"{int(pontos_vermelho)} pts",
            delta=int(pontos_vermelho - pontos_azul) if time_vencedor == "vermelho" else None
        )

    with m3:
        st.metric(
            "⚖️ Diferença",
            f"{int(diferenca)} pts"
        )

    # --------------------------------------------
    # BARRA DE EQUILÍBRIO
    # --------------------------------------------

    st.markdown(f"**Índice de equilíbrio:** {estrelas} — {avaliacao}")
    st.progress(equilibrio_percentual / 100)

    st.markdown("")

    # --------------------------------------------
    # CARDS DOS TIMES
    # --------------------------------------------

    col_azul, col_vermelho = st.columns(2)

    def montar_html_time(time, pontos, cor_classe, titulo, vencedor):

        badge = '<span class="winner-badge">🏆 Maior pontuação</span>' if vencedor else ""

        linhas_jogadores = ""

        for jogador in time:
            linhas_jogadores += (
                '<div class="player-row">'
                f'<div>{ICONE_ROTAS[jogador.rota]} <b>{jogador.nome}</b>'
                f'<div class="player-role">{jogador.rota}</div></div>'
                f'<div>{jogador.elo}<br><b>{int(jogador.pontos)} pts</b></div>'
                '</div>'
            )

        html = (
            f'<div class="team-card {cor_classe}">'
            f'<h3>{titulo}{badge}</h3>'
            f'<div class="team-total">Pontuação total: {int(pontos)} pts</div>'
            f'{linhas_jogadores}'
            '</div>'
        )

        return html

    with col_azul:
        st.markdown(
            montar_html_time(
                time_azul,
                pontos_azul,
                "blue-card",
                "🟦 Time Azul",
                vencedor=(time_vencedor == "azul")
            ),
            unsafe_allow_html=True
        )

    with col_vermelho:
        st.markdown(
            montar_html_time(
                time_vermelho,
                pontos_vermelho,
                "red-card",
                "🟥 Time Vermelho",
                vencedor=(time_vencedor == "vermelho")
            ),
            unsafe_allow_html=True
        )

    # --------------------------------------------
    # COPIAR / EXPORTAR
    # --------------------------------------------

    st.divider()
    st.subheader("📋 Copiar ou exportar composição")

    texto_composicao = gerar_texto_composicao(
        time_azul, time_vermelho, pontos_azul, pontos_vermelho
    )

    col_copiar, col_exportar = st.columns(2)

    with col_copiar:
        st.caption("Clique no ícone de cópia no canto do bloco abaixo:")
        st.code(texto_composicao, language=None)

    with col_exportar:
        st.caption("Ou baixe a composição como arquivo de texto:")
        st.download_button(
            label="💾 Exportar times (.txt)",
            data=texto_composicao,
            file_name="times_lol.txt",
            mime="text/plain",
            use_container_width=True
        )