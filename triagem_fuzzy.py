import streamlit as st
import time
import pandas as pd
import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Triagem Fuzzy | Monitor Hospitalar",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS — TEMA ESCURO HOSPITALAR
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;700;800&display=swap');

/* BASE */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}
.stApp { background-color: #0d1117; }
.block-container { padding-top: 1rem !important; }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }
[data-testid="stSidebar"] hr { border-color: #30363d !important; }
[data-testid="stSidebar"] .stSlider > div > div > div { background: #1f6feb; }

/* ABAS */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #30363d;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8b949e;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: #1f6feb !important;
    color: white !important;
}

/* BOTOES */
.stButton > button {
    background: #1f6feb;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 10px 0;
    width: 100%;
    transition: background 0.2s;
}
.stButton > button:hover { background: #388bfd; }

/* HEADER */
.hdr {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1c2128 100%);
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 20px 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 20px;
}
.hdr-title { font-size: 1.5rem; font-weight: 800; color: #e6edf3; margin: 0; }
.hdr-sub   { font-size: 0.82rem; color: #8b949e; margin: 3px 0 0 0; }
.hdr-badge {
    margin-left: auto;
    background: #1f6feb22;
    border: 1px solid #1f6feb55;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.75rem;
    color: #79c0ff;
    white-space: nowrap;
    font-weight: 600;
}
.hdr-icon { font-size: 2.6rem; }

/* STATUS BAR */
.status-bar {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    gap: 24px;
    margin-bottom: 18px;
    font-size: 0.82rem;
}
.status-dot-on  { width:10px;height:10px;border-radius:50%;background:#3fb950;display:inline-block;box-shadow:0 0 8px #3fb950;margin-right:6px; }
.status-dot-off { width:10px;height:10px;border-radius:50%;background:#6e7681;display:inline-block;margin-right:6px; }
.status-label   { color: #8b949e; }
.status-value   { color: #e6edf3; font-weight: 700; margin-left: 4px; }

/* CARDS DE SINAIS VITAIS */
.vital-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 4px;
}
.vital-card.danger { border-color: #f85149; background: #1a0f0f; }
.vital-card.warn   { border-color: #d29922; background: #1a1600; }
.vital-label { font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #8b949e; margin-bottom: 4px; }
.vital-value { font-size: 1.9rem; font-weight: 800; color: #e6edf3; line-height: 1; font-family: 'JetBrains Mono', monospace; }
.vital-unit  { font-size: 0.85rem; color: #8b949e; font-weight: 400; }
.vital-sub   { font-size: 0.7rem; color: #6e7681; margin-top: 4px; }

/* BADGE MANCHESTER */
.badge {
    display: inline-block;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 800;
    font-size: 1rem;
    letter-spacing: 0.02em;
}
.b-azul     { background:#0d3b6e; color:#79c0ff; border:1px solid #1f6feb; }
.b-verde    { background:#0d2818; color:#3fb950; border:1px solid #238636; }
.b-amarelo  { background:#271d00; color:#e3b341; border:1px solid #9e6a03; }
.b-laranja  { background:#2d1200; color:#f0883e; border:1px solid #bd561d; }
.b-vermelho { background:#2d0f0f; color:#f85149; border:1px solid #b62324; }

/* ALERTA EMERGÊNCIA */
@keyframes pulse-border {
    0%,100% { border-color: #f85149; box-shadow: 0 0 0 0 #f8514955; }
    50%      { border-color: #ff7b72; box-shadow: 0 0 16px 4px #f8514933; }
}
.alerta-emerg {
    background: #1a0d0d;
    border: 2px solid #f85149;
    border-radius: 10px;
    padding: 12px 22px;
    color: #f85149;
    font-weight: 800;
    font-size: 1rem;
    text-align: center;
    animation: pulse-border 1.2s infinite;
    margin-bottom: 12px;
}

/* SECTION TITLE */
.stitle {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8b949e;
    border-bottom: 1px solid #30363d;
    padding-bottom: 6px;
    margin: 18px 0 12px 0;
}

/* TABELA */
.stDataFrame { border-radius: 10px !important; overflow: hidden; }
[data-testid="stDataFrameResizable"] { background: #161b22; }

/* WATERMARK */
.watermark {
    position: fixed;
    bottom: 50px; right: 28px;
    font-size: 4rem; font-weight: 900;
    color: rgba(31,111,235,0.07);
    pointer-events: none; user-select: none;
    letter-spacing: 0.05em;
    transform: rotate(-18deg);
    z-index: 0; line-height: 1;
}
.watermark-sub {
    position: fixed;
    bottom: 34px; right: 28px;
    font-size: 0.65rem; color: rgba(31,111,235,0.10);
    pointer-events: none; user-select: none;
    font-weight: 700; letter-spacing: 0.18em;
    transform: rotate(-18deg); z-index: 0;
}

/* INFO BOX */
.info-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 22px 28px;
    margin-bottom: 18px;
}
.info-box h3 { color: #e6edf3; margin-top: 0; font-size: 1.1rem; }
.info-box p  { color: #8b949e; margin-bottom: 0; font-size: 0.88rem; line-height: 1.6; }

/* TABELA INTERNA HTML */
.tbl { width:100%; border-collapse:collapse; font-size:0.84rem; }
.tbl th { padding:10px 12px; text-align:left; background:#1c2128; color:#8b949e; font-weight:600; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; }
.tbl td { padding:10px 12px; border-bottom:1px solid #21262d; color:#e6edf3; }
.tbl tr:last-child td { border-bottom: none; }
.tbl tr:hover td { background: #1c2128; }

/* MATPLOTLIB escuro via CSS não é possível — feito via código */

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Watermark
st.markdown("""
<div class="watermark">Pedrin</div>
<div class="watermark-sub">TRIAGEM · FUZZY · MANCHESTER</div>
""", unsafe_allow_html=True)


# ============================================================
# MOTOR FUZZY
# ============================================================

@st.cache_resource
def construir_sistema_fuzzy():
    fc   = ctrl.Antecedent(np.arange(20,  220, 1),   'freq_cardiaca')
    spo2 = ctrl.Antecedent(np.arange(60,  101, 1),   'saturacao')
    temp = ctrl.Antecedent(np.arange(34,  43,  0.1), 'temperatura')
    pas  = ctrl.Antecedent(np.arange(50,  200, 1),   'pressao_sistolica')
    dor  = ctrl.Antecedent(np.arange(0,   11,  1),   'escala_dor')
    prio = ctrl.Consequent(np.arange(0,   101, 1),   'prioridade')

    spo2['critica'] = fuzz.trapmf(spo2.universe, [60, 60, 82, 86])
    spo2['baixa']   = fuzz.trimf (spo2.universe, [83, 89, 93])
    spo2['normal']  = fuzz.trapmf(spo2.universe, [91, 95, 100, 100])

    fc['grave']       = fuzz.trapmf(fc.universe, [20,  20,  40,  50])
    fc['bradicardia'] = fuzz.trimf (fc.universe, [45,  58,  68])
    fc['normal']      = fuzz.trimf (fc.universe, [62,  80,  100])
    fc['taquicardia'] = fuzz.trimf (fc.universe, [95,  115, 140])
    fc['grave_taqui'] = fuzz.trapmf(fc.universe, [130, 150, 220, 220])

    temp['hipotermia_grave'] = fuzz.trapmf(temp.universe, [34.0,34.0,34.5,35.0])
    temp['hipotermia']       = fuzz.trimf (temp.universe, [34.5,35.2,36.0])
    temp['normal']           = fuzz.trimf (temp.universe, [35.8,36.6,37.4])
    temp['febril']           = fuzz.trimf (temp.universe, [37.2,37.9,38.5])
    temp['febre_alta']       = fuzz.trimf (temp.universe, [38.2,39.0,40.0])
    temp['hipertermia']      = fuzz.trapmf(temp.universe, [39.5,40.5,43.0,43.0])

    pas['hipotensao_grave']  = fuzz.trapmf(pas.universe, [50,  50,  70,  80])
    pas['hipotensao']        = fuzz.trimf (pas.universe, [75,  90,  100])
    pas['normal']            = fuzz.trimf (pas.universe, [95,  120, 135])
    pas['hipertensao']       = fuzz.trimf (pas.universe, [130, 150, 165])
    pas['hipertensao_crise'] = fuzz.trapmf(pas.universe, [160, 175, 200, 200])

    dor['ausente']  = fuzz.trapmf(dor.universe, [0,0,1,2])
    dor['leve']     = fuzz.trimf (dor.universe, [1,3,5])
    dor['moderada'] = fuzz.trimf (dor.universe, [4,6,8])
    dor['intensa']  = fuzz.trapmf(dor.universe, [7,9,10,10])

    prio['azul']     = fuzz.trapmf(prio.universe, [0,  0,  12, 22])
    prio['verde']    = fuzz.trimf (prio.universe, [15, 30, 45])
    prio['amarelo']  = fuzz.trimf (prio.universe, [38, 52, 65])
    prio['laranja']  = fuzz.trimf (prio.universe, [58, 72, 84])
    prio['vermelho'] = fuzz.trapmf(prio.universe, [78, 90, 100, 100])

    regras = [
        ctrl.Rule(spo2['critica'],                                        prio['vermelho']),
        ctrl.Rule(fc['grave'],                                            prio['vermelho']),
        ctrl.Rule(fc['grave_taqui'],                                      prio['vermelho']),
        ctrl.Rule(pas['hipotensao_grave'],                                prio['vermelho']),
        ctrl.Rule(temp['hipertermia'],                                    prio['vermelho']),
        ctrl.Rule(temp['hipotermia_grave'],                               prio['vermelho']),
        ctrl.Rule(pas['hipertensao_crise'] & dor['intensa'],              prio['vermelho']),
        ctrl.Rule(spo2['baixa'] & fc['grave_taqui'],                      prio['vermelho']),
        ctrl.Rule(spo2['baixa'] & fc['taquicardia'],                      prio['laranja']),
        ctrl.Rule(temp['febre_alta'] & fc['taquicardia'],                 prio['laranja']),
        ctrl.Rule(pas['hipotensao'] & fc['taquicardia'],                  prio['laranja']),
        ctrl.Rule(dor['intensa'] & fc['taquicardia'],                     prio['laranja']),
        ctrl.Rule(temp['febre_alta'] & spo2['baixa'],                     prio['laranja']),
        ctrl.Rule(pas['hipertensao_crise'],                               prio['laranja']),
        ctrl.Rule(fc['bradicardia'] & pas['hipotensao'],                  prio['laranja']),
        ctrl.Rule(temp['febre_alta'] & spo2['normal'],                    prio['amarelo']),
        ctrl.Rule(spo2['baixa'] & fc['normal'],                           prio['amarelo']),
        ctrl.Rule(fc['taquicardia'] & spo2['normal'],                     prio['amarelo']),
        ctrl.Rule(dor['intensa'] & spo2['normal'],                        prio['amarelo']),
        ctrl.Rule(pas['hipertensao'] & dor['moderada'],                   prio['amarelo']),
        ctrl.Rule(temp['hipotermia'] & fc['bradicardia'],                 prio['amarelo']),
        ctrl.Rule(dor['moderada'] & fc['taquicardia'],                    prio['amarelo']),
        ctrl.Rule(temp['febril'] & spo2['normal'] & fc['normal'],         prio['verde']),
        ctrl.Rule(dor['moderada'] & spo2['normal'] & fc['normal'],        prio['verde']),
        ctrl.Rule(pas['hipertensao'] & spo2['normal'] & fc['normal'],     prio['verde']),
        ctrl.Rule(temp['hipotermia'] & spo2['normal'] & fc['normal'],     prio['verde']),
        ctrl.Rule(dor['leve'] & temp['febril'],                           prio['verde']),
        ctrl.Rule(spo2['normal'] & fc['normal'] & temp['normal'] & pas['normal'] & dor['ausente'], prio['azul']),
        ctrl.Rule(spo2['normal'] & fc['normal'] & temp['normal'] & dor['leve'],                    prio['azul']),
        ctrl.Rule(spo2['normal'] & fc['normal'] & temp['normal'] & pas['normal'] & dor['leve'],    prio['azul']),
    ]

    sistema   = ctrl.ControlSystem(regras)
    simulador = ctrl.ControlSystemSimulation(sistema)
    return simulador, fc, spo2, temp, pas, dor, prio


simulador, _fc, _spo2, _temp, _pas, _dor, _prio = construir_sistema_fuzzy()


# ============================================================
# CONSTANTES E HELPERS
# ============================================================

MANCHESTER = {
    'azul':     {'label':'🔵 Azul',     'full':'Não Urgente',     'css':'b-azul',     'tempo':'>4 horas',  'hex':'#1f6feb'},
    'verde':    {'label':'🟢 Verde',    'full':'Pouco Urgente',   'css':'b-verde',    'tempo':'≤2 horas',  'hex':'#238636'},
    'amarelo':  {'label':'🟡 Amarelo',  'full':'Urgente',         'css':'b-amarelo',  'tempo':'≤60 min',   'hex':'#9e6a03'},
    'laranja':  {'label':'🟠 Laranja',  'full':'Muito Urgente',   'css':'b-laranja',  'tempo':'≤10 min',   'hex':'#bd561d'},
    'vermelho': {'label':'🔴 Vermelho', 'full':'Emergência',      'css':'b-vermelho', 'tempo':'Imediato',  'hex':'#b62324'},
}

COR_NIVEL = {
    'azul':    '#1f6feb', 'verde':   '#238636',
    'amarelo': '#9e6a03', 'laranja': '#bd561d', 'vermelho': '#b62324',
}

COLUNAS = ['Timestamp','ID','FC','SpO2','Temp','PAS','Dor','Score','Nivel','Espera']

plt.rcParams.update({
    'figure.facecolor': '#161b22', 'axes.facecolor': '#161b22',
    'axes.edgecolor': '#30363d',   'axes.labelcolor': '#8b949e',
    'xtick.color': '#8b949e',      'ytick.color': '#8b949e',
    'text.color': '#e6edf3',       'grid.color': '#21262d',
    'legend.facecolor': '#1c2128', 'legend.edgecolor': '#30363d',
    'legend.labelcolor': '#e6edf3',
})

def classificar(score):
    if   score < 18: return 'azul'
    elif score < 40: return 'verde'
    elif score < 60: return 'amarelo'
    elif score < 78: return 'laranja'
    else:            return 'vermelho'

def gerar_dados():
    """
    Gera sinais vitais com distribuição realista baseada em frequência clínica:
      Azul     ~20% — paciente estável, queixa leve
      Verde    ~35% — alteração leve, sem urgência imediata
      Amarelo  ~25% — urgência moderada
      Laranja  ~12% — muito urgente
      Vermelho  ~8% — emergência real
    """
    nivel_sorteado = random.choices(
        ['azul', 'verde', 'amarelo', 'laranja', 'vermelho'],
        weights=[20, 35, 25, 12, 8]
    )[0]

    perfis = {
        'azul': {
            'FC':   (62,  85),
            'SpO2': (96, 100),
            'Temp': (36.0, 37.2),
            'PAS':  (100, 125),
            'Dor':  (0,   2),
        },
        'verde': {
            'FC':   (55,  100),
            'SpO2': (93,  97),
            'Temp': (37.2, 38.4),
            'PAS':  (90,  140),
            'Dor':  (2,   5),
        },
        'amarelo': {
            'FC':   (50,  115),
            'SpO2': (90,  94),
            'Temp': (38.2, 39.5),
            'PAS':  (80,  155),
            'Dor':  (5,   7),
        },
        'laranja': {
            'FC':   (40,  135),
            'SpO2': (85,  92),
            'Temp': (34.8, 35.5),
            'PAS':  (70,  170),
            'Dor':  (7,   9),
        },
        'vermelho': {
            'FC':   (28,  45),
            'SpO2': (72,  86),
            'Temp': (34.2, 34.8),
            'PAS':  (55,  75),
            'Dor':  (8,  10),
        },
    }

    p = perfis[nivel_sorteado]
    return {
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "FC":   random.randint(*p['FC']),
        "SpO2": random.randint(*p['SpO2']),
        "Temp": round(random.uniform(*p['Temp']), 1),
        "PAS":  random.randint(*p['PAS']),
        "Dor":  random.randint(*p['Dor']),
        "ID":   f"PAC-{random.randint(1000,9999)}",
    }

def calcular_score(d):
    simulador.input['freq_cardiaca']     = float(np.clip(d["FC"],   20, 219))
    simulador.input['saturacao']         = float(np.clip(d["SpO2"], 60, 100))
    simulador.input['temperatura']       = float(np.clip(d["Temp"], 34.0, 42.9))
    simulador.input['pressao_sistolica'] = float(np.clip(d["PAS"],  50, 199))
    simulador.input['escala_dor']        = float(np.clip(d["Dor"],  0, 10))
    try:
        simulador.compute()
        return simulador.output['prioridade']
    except Exception:
        return 30.0

def plot_dark(fig):
    fig.patch.set_facecolor('#161b22')
    for ax in fig.axes:
        ax.set_facecolor('#161b22')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#30363d')
        ax.spines['bottom'].set_color('#30363d')
        ax.grid(True, alpha=0.3, linestyle='--', color='#30363d')
    return fig


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    'historico':   pd.DataFrame(columns=COLUNAS),
    'total':       0,
    'emergencias': 0,
    'rodando':     False,
    'ultimo_dado': None,
    'ultimo_score':30.0,
    'ultimo_nivel':'azul',
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## ⚙️ Controles")
    st.markdown("---")

    intervalo    = st.slider("⏱ Intervalo (segundos)", 1.0, 8.0, 2.5, 0.5)
    max_pacientes = st.slider("📋 Histórico (pacientes)", 10, 50, 20)

    st.markdown("---")
    col_ini, col_stop = st.columns(2)
    with col_ini:
        if st.button("▶ Iniciar", use_container_width=True):
            st.session_state.rodando = True
    with col_stop:
        if st.button("⏸ Pausar", use_container_width=True):
            st.session_state.rodando = False

    if st.button("🗑 Limpar painel", use_container_width=True):
        st.session_state.historico    = pd.DataFrame(columns=COLUNAS)
        st.session_state.total        = 0
        st.session_state.emergencias  = 0
        st.session_state.ultimo_dado  = None
        st.session_state.rodando      = False

    st.markdown("---")
    st.markdown("### 📌 Legenda Manchester")
    for k, v in MANCHESTER.items():
        cor = COR_NIVEL[k]
        st.markdown(
            "<div style='background:" + cor + "22;border:1px solid " + cor + "55;"
            "border-radius:8px;padding:7px 12px;margin-bottom:6px'>"
            "<span style='color:" + cor + ";font-weight:700;font-size:0.82rem'>" + v['label'] + " — " + v['full'] + "</span>"
            "<br><span style='color:#8b949e;font-size:0.72rem'>⏱ " + v['tempo'] + "</span>"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    rodando_status = "🟢 ATIVO" if st.session_state.rodando else "🔴 PARADO"
    st.markdown(
        "<div style='text-align:center;padding:8px;background:#1c2128;border-radius:8px;"
        "border:1px solid #30363d;font-weight:700;font-size:0.85rem;color:#e6edf3'>"
        "STATUS: " + rodando_status + "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<div class='hdr'>"
    "<div class='hdr-icon'>🏥</div>"
    "<div>"
    "<p class='hdr-title'>Monitor de Triagem Inteligente</p>"
    "<p class='hdr-sub'>Protocolo de Manchester &nbsp;·&nbsp; Lógica Fuzzy Mamdani &nbsp;·&nbsp; Tempo Real</p>"
    "</div>"
    "<div class='hdr-badge'>⚕️ Versão Clínica 2.0</div>"
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# ABAS
# ============================================================

aba1, aba2, aba3 = st.tabs(["📊 Painel Operacional", "🧠 Lógica Fuzzy", "ℹ️ Sobre"])


# ============================================================
# ABA 1 — PAINEL
# ============================================================

with aba1:

    # ── Processar um novo paciente se estiver rodando ──────────────
    if st.session_state.rodando:
        dados = gerar_dados()
        score = calcular_score(dados)
        nivel = classificar(score)

        st.session_state.ultimo_dado  = dados
        st.session_state.ultimo_score = score
        st.session_state.ultimo_nivel = nivel
        st.session_state.total       += 1
        if nivel == 'vermelho':
            st.session_state.emergencias += 1

        novo = pd.DataFrame([{
            'Timestamp': dados["Timestamp"],
            'ID':        dados["ID"],
            'FC':        dados["FC"],
            'SpO2':      dados["SpO2"],
            'Temp':      dados["Temp"],
            'PAS':       dados["PAS"],
            'Dor':       dados["Dor"],
            'Score':     round(score, 1),
            'Nivel':     nivel,
            'Espera':    MANCHESTER[nivel]['tempo'],
        }])
        st.session_state.historico = pd.concat(
            [novo, st.session_state.historico], ignore_index=True
        ).head(max_pacientes)

    d     = st.session_state.ultimo_dado
    score = st.session_state.ultimo_score
    nivel = st.session_state.ultimo_nivel
    info  = MANCHESTER[nivel]
    hist  = st.session_state.historico

    # ── Status bar ─────────────────────────────────────────────────
    status_dot = "<span class='status-dot-on'></span>" if st.session_state.rodando else "<span class='status-dot-off'></span>"
    st.markdown(
        "<div class='status-bar'>"
        + status_dot +
        "<span style='color:#e6edf3;font-weight:700'>"
        + ("MONITORANDO" if st.session_state.rodando else "PAUSADO") + "</span>"
        "<span style='color:#30363d'>|</span>"
        "<span class='status-label'>Pacientes triados:</span>"
        "<span class='status-value'>" + str(st.session_state.total) + "</span>"
        "<span style='color:#30363d'>|</span>"
        "<span class='status-label'>Emergências:</span>"
        "<span class='status-value' style='color:#f85149'>" + str(st.session_state.emergencias) + "</span>"
        "<span style='color:#30363d'>|</span>"
        "<span class='status-label'>Última atualização:</span>"
        "<span class='status-value'>" + (d["Timestamp"] if d else "--:--:--") + "</span>"
        "</div>",
        unsafe_allow_html=True
    )

    # ── Alerta emergência ──────────────────────────────────────────
    alerta_ph = st.empty()
    if d and nivel == 'vermelho':
        alerta_ph.markdown(
            "<div class='alerta-emerg'>🚨 EMERGÊNCIA — " + d["ID"]
            + " — Score: " + str(round(score,1))
            + " — ATENDIMENTO IMEDIATO</div>",
            unsafe_allow_html=True
        )

    # ── Sinais vitais ──────────────────────────────────────────────
    st.markdown("<div class='stitle'>Sinais Vitais — Último Paciente</div>", unsafe_allow_html=True)

    if d:
        danger = nivel == 'vermelho'
        warn   = nivel == 'laranja'
        cls    = 'danger' if danger else ('warn' if warn else '')

        def vcard(col, label, value, unit, sub=""):
            col.markdown(
                "<div class='vital-card " + cls + "'>"
                "<div class='vital-label'>" + label + "</div>"
                "<div class='vital-value'>" + str(value)
                + "<span class='vital-unit'> " + unit + "</span></div>"
                "<div class='vital-sub'>" + sub + "</div>"
                "</div>",
                unsafe_allow_html=True
            )

        c1,c2,c3,c4,c5,c6 = st.columns(6)
        vcard(c1, "Freq. Cardíaca", d["FC"],   "bpm",  "FC normal: 60–100")
        vcard(c2, "Saturação O₂",   d["SpO2"], "%",    "SpO₂ normal: ≥95%")
        vcard(c3, "Temperatura",    d["Temp"], "°C",   "Normal: 36–37,4°C")
        vcard(c4, "Pressão Sist.",  d["PAS"],  "mmHg", "Normal: 90–130")
        vcard(c5, "Dor (EVA)",      d["Dor"],  "/10",  "0=sem dor 10=máx")
        c6.markdown(
            "<div class='vital-card " + cls + "'>"
            "<div class='vital-label'>Classificação</div>"
            "<div style='margin-top:10px'><span class='badge " + info['css'] + "'>"
            + info['label'] + " — " + info['full'] + "</span></div>"
            "<div class='vital-sub' style='margin-top:8px'>⏱ Espera: " + info['tempo'] + "</div>"
            "<div class='vital-sub'>Score fuzzy: " + str(round(score,1)) + "/100</div>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div style='background:#161b22;border:1px solid #30363d;border-radius:12px;"
            "padding:30px;text-align:center;color:#8b949e;font-size:0.9rem'>"
            "▶ Clique em <b>Iniciar</b> na barra lateral para começar o monitoramento."
            "</div>",
            unsafe_allow_html=True
        )

    # ── Gráficos ───────────────────────────────────────────────────
    if len(hist) > 1:
        col_g, col_p = st.columns([3, 1])

        with col_g:
            st.markdown("<div class='stitle'>📈 Tendência de Score de Prioridade</div>", unsafe_allow_html=True)
            df_plot = hist.set_index('Timestamp')['Score'].astype(float)
            fig, ax = plt.subplots(figsize=(8, 3))
            # Zonas
            ax.axhspan(0,  18, alpha=0.15, color='#1f6feb')
            ax.axhspan(18, 40, alpha=0.15, color='#238636')
            ax.axhspan(40, 60, alpha=0.15, color='#9e6a03')
            ax.axhspan(60, 78, alpha=0.15, color='#bd561d')
            ax.axhspan(78, 100,alpha=0.15, color='#b62324')
            xs = range(len(df_plot))
            ax.plot(xs, df_plot.values, color='#79c0ff', linewidth=2, marker='o',
                    markersize=4, zorder=5)
            ax.fill_between(xs, df_plot.values, alpha=0.12, color='#79c0ff')
            ax.set_xticks(xs)
            ax.set_xticklabels(df_plot.index, rotation=45, fontsize=6)
            ax.set_ylim(0, 100)
            ax.set_ylabel('Score', fontsize=8)
            patches = [
                mpatches.Patch(color='#1f6feb', label='Azul',     alpha=0.7),
                mpatches.Patch(color='#238636', label='Verde',    alpha=0.7),
                mpatches.Patch(color='#9e6a03', label='Amarelo',  alpha=0.7),
                mpatches.Patch(color='#bd561d', label='Laranja',  alpha=0.7),
                mpatches.Patch(color='#b62324', label='Vermelho', alpha=0.7),
            ]
            ax.legend(handles=patches, fontsize=6, loc='upper left', ncol=5,
                      facecolor='#1c2128', edgecolor='#30363d')
            plot_dark(fig)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        with col_p:
            st.markdown("<div class='stitle'>🥧 Por Nível</div>", unsafe_allow_html=True)
            contagem = hist['Nivel'].value_counts()
            ordem    = ['vermelho','laranja','amarelo','verde','azul']
            cores_p  = {'vermelho':'#b62324','laranja':'#bd561d','amarelo':'#9e6a03',
                        'verde':'#238636','azul':'#1f6feb'}
            vals, lbls, clrs = [], [], []
            for n in ordem:
                if n in contagem.index:
                    vals.append(contagem[n])
                    lbls.append(n.capitalize())
                    clrs.append(cores_p[n])
            if vals:
                fig2, ax2 = plt.subplots(figsize=(3.2, 3.2))
                wedges, texts, autos = ax2.pie(
                    vals, labels=lbls, colors=clrs,
                    autopct='%1.0f%%', startangle=90,
                    textprops={'fontsize':7, 'color':'#e6edf3'},
                    wedgeprops={'linewidth':1.5, 'edgecolor':'#161b22'}
                )
                for at in autos:
                    at.set_fontsize(7)
                    at.set_color('#e6edf3')
                plot_dark(fig2)
                plt.tight_layout()
                st.pyplot(fig2, use_container_width=True)
                plt.close(fig2)

    # ── Tabela de histórico ────────────────────────────────────────
    if len(hist) > 0:
        st.markdown(
            "<div class='stitle'>🗂 Painel de Espera — "
            + str(st.session_state.total) + " triados | "
            + str(st.session_state.emergencias) + " emergências</div>",
            unsafe_allow_html=True
        )

        def estilo_nivel(val):
            estilos = {
                'vermelho': 'background-color:#2d0f0f;color:#f85149;font-weight:700',
                'laranja':  'background-color:#2d1200;color:#f0883e;font-weight:700',
                'amarelo':  'background-color:#271d00;color:#e3b341;font-weight:700',
                'verde':    'background-color:#0d2818;color:#3fb950;font-weight:700',
                'azul':     'background-color:#0d1f3c;color:#79c0ff;font-weight:700',
            }
            return estilos.get(val, '')

        styled = hist.style.map(estilo_nivel, subset=['Nivel'])
        st.dataframe(styled, use_container_width=True, height=360)

    # ── Auto-refresh ───────────────────────────────────────────────
    if st.session_state.rodando:
        time.sleep(intervalo)
        st.rerun()


# ============================================================
# ABA 2 — LÓGICA FUZZY
# ============================================================

with aba2:
    st.markdown(
        "<div class='info-box'>"
        "<h3>🧠 Funções de Pertinência — Visualização Completa</h3>"
        "<p>O sistema utiliza <b>Lógica Fuzzy Mamdani</b> com 5 variáveis de entrada e 1 de saída. "
        "Funções trapezoidais e triangulares modelam a incerteza clínica dos sinais vitais. "
        "A defuzzificação é feita pelo método do <b>centroide</b>, resultando em um score contínuo de 0 a 100.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    def plot_mf(variavel, titulo, unidade, cores):
        fig, ax = plt.subplots(figsize=(5.5, 2.6))
        for nome, cor in cores.items():
            if nome in variavel.terms:
                mf = variavel[nome].mf
                ax.plot(variavel.universe, mf, color=cor, linewidth=2, label=nome.replace('_',' ').title())
                ax.fill_between(variavel.universe, mf, alpha=0.15, color=cor)
        ax.set_title(titulo, fontsize=9, fontweight='bold', pad=8)
        ax.set_xlabel(unidade, fontsize=7)
        ax.set_ylabel('μ', fontsize=8)
        ax.set_ylim(-0.05, 1.15)
        ax.legend(fontsize=6, loc='upper right', framealpha=0.8)
        plot_dark(fig)
        plt.tight_layout()
        return fig

    c_fc   = {'grave':'#f85149','bradicardia':'#f0883e','normal':'#3fb950','taquicardia':'#e3b341','grave_taqui':'#bc8cff'}
    c_spo2 = {'critica':'#f85149','baixa':'#f0883e','normal':'#3fb950'}
    c_temp = {'hipotermia_grave':'#79c0ff','hipotermia':'#58a6ff','normal':'#3fb950','febril':'#e3b341','febre_alta':'#f0883e','hipertermia':'#f85149'}
    c_pas  = {'hipotensao_grave':'#f85149','hipotensao':'#f0883e','normal':'#3fb950','hipertensao':'#e3b341','hipertensao_crise':'#bc8cff'}
    c_dor  = {'ausente':'#3fb950','leve':'#e3b341','moderada':'#f0883e','intensa':'#f85149'}
    c_prio = {'azul':'#1f6feb','verde':'#238636','amarelo':'#9e6a03','laranja':'#bd561d','vermelho':'#b62324'}

    ca, cb = st.columns(2)
    cc, cd = st.columns(2)
    ce, cf = st.columns(2)

    with ca: st.pyplot(plot_mf(_fc,   "Frequência Cardíaca",        "bpm",   c_fc),   use_container_width=True)
    with cb: st.pyplot(plot_mf(_spo2, "Saturação O₂ (SpO₂)",       "%",     c_spo2), use_container_width=True)
    with cc: st.pyplot(plot_mf(_temp, "Temperatura Corporal",       "°C",    c_temp), use_container_width=True)
    with cd: st.pyplot(plot_mf(_pas,  "Pressão Arterial Sistólica", "mmHg",  c_pas),  use_container_width=True)
    with ce: st.pyplot(plot_mf(_dor,  "Escala de Dor (EVA)",        "0–10",  c_dor),  use_container_width=True)
    with cf: st.pyplot(plot_mf(_prio, "Saída: Score de Prioridade", "0–100", c_prio), use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<div class='info-box'>"
        "<h3>📐 Arquitetura do Sistema</h3>"
        "<table class='tbl'>"
        "<tr><th>Componente</th><th>Descrição</th></tr>"
        "<tr><td><b>Método de Inferência</b></td><td>Mamdani (max-min)</td></tr>"
        "<tr><td><b>Defuzzificação</b></td><td>Centroide (Centro de Gravidade)</td></tr>"
        "<tr><td><b>Entradas (5)</b></td><td>FC · SpO₂ · Temperatura · PAS · Escala de Dor</td></tr>"
        "<tr><td><b>Saída</b></td><td>Score de Prioridade (0–100 contínuo)</td></tr>"
        "<tr><td><b>Conjuntos Fuzzy</b></td><td>20 conjuntos de entrada + 5 de saída</td></tr>"
        "<tr><td><b>Base de Regras</b></td><td>30 regras cobrindo os 5 níveis do Manchester</td></tr>"
        "</table>"
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# ABA 3 — SOBRE
# ============================================================

with aba3:
    st.markdown(
        "<div class='info-box'>"
        "<h3>🏥 Sobre o Sistema de Triagem Inteligente</h3>"
        "<p>Este sistema implementa um <b>motor de triagem clínica baseado em Lógica Fuzzy</b> "
        "integrado ao <b>Protocolo de Manchester</b>, padrão internacional de classificação de risco. "
        "A lógica fuzzy lida com a imprecisão dos sinais vitais de forma que regras booleanas rígidas não conseguem.</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='info-box'>"
        "<h3>⚕️ Protocolo de Manchester — 5 Níveis</h3>"
        "<table class='tbl'>"
        "<tr><th>Classificação</th><th>Nível</th><th>Score</th><th>Tempo Máx.</th><th>Exemplo Clínico</th></tr>"
        "<tr><td><span style='background:#b62324;color:white;padding:2px 10px;border-radius:4px;font-weight:700;font-size:0.8rem'>Vermelho</span></td>"
        "<td>Emergência</td><td>78–100</td><td>Imediato</td><td>PCR, apneia, SpO₂ &lt; 82%</td></tr>"
        "<tr><td><span style='background:#bd561d;color:white;padding:2px 10px;border-radius:4px;font-weight:700;font-size:0.8rem'>Laranja</span></td>"
        "<td>Muito Urgente</td><td>60–77</td><td>≤ 10 min</td><td>Dor torácica, taqui + hipóxia</td></tr>"
        "<tr><td><span style='background:#9e6a03;color:white;padding:2px 10px;border-radius:4px;font-weight:700;font-size:0.8rem'>Amarelo</span></td>"
        "<td>Urgente</td><td>40–59</td><td>≤ 60 min</td><td>Febre alta, dor intensa isolada</td></tr>"
        "<tr><td><span style='background:#238636;color:white;padding:2px 10px;border-radius:4px;font-weight:700;font-size:0.8rem'>Verde</span></td>"
        "<td>Pouco Urgente</td><td>18–39</td><td>≤ 2 horas</td><td>Febre leve, dor moderada</td></tr>"
        "<tr><td><span style='background:#1f6feb;color:white;padding:2px 10px;border-radius:4px;font-weight:700;font-size:0.8rem'>Azul</span></td>"
        "<td>Não Urgente</td><td>0–17</td><td>&gt; 4 horas</td><td>Sinais normais, queixa minor</td></tr>"
        "</table>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='info-box'>"
        "<h3>🔧 Stack Tecnológico</h3>"
        "<table class='tbl'>"
        "<tr><th>Tecnologia</th><th>Uso</th></tr>"
        "<tr><td><b>Python 3.x</b></td><td>Linguagem principal</td></tr>"
        "<tr><td><b>scikit-fuzzy</b></td><td>Motor de inferência fuzzy Mamdani</td></tr>"
        "<tr><td><b>Streamlit</b></td><td>Interface web interativa em tempo real</td></tr>"
        "<tr><td><b>Matplotlib</b></td><td>Visualização das funções de pertinência</td></tr>"
        "<tr><td><b>Pandas / NumPy</b></td><td>Manipulação de dados e universos de discurso</td></tr>"
        "</table>"
        "<br>"
        "<p><b>Desenvolvido por:</b> Pedro Augusto &amp; Maria Julia</p>"
        "<p style='color:#6e7681;font-size:0.78rem;margin-bottom:0'>"
        "⚠️ Protótipo acadêmico. Não utilizar para decisão clínica real sem validação médica certificada.</p>"
        "</div>",
        unsafe_allow_html=True
    )

# FOOTER
st.markdown(
    "<div style='background:#161b22;border:1px solid #30363d;border-radius:10px;"
    "padding:12px 24px;text-align:center;font-size:0.75rem;color:#8b949e;margin-top:20px'>"
    "🏥 Monitor de Triagem Inteligente &nbsp;·&nbsp; Protocolo de Manchester &nbsp;·&nbsp;"
    " Python · scikit-fuzzy · Streamlit &nbsp;·&nbsp;"
    " <b style='color:#e6edf3'>Pedro Augusto &amp; Maria Julia</b>"
    "</div>",
    unsafe_allow_html=True
)