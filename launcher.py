"""
launcher.py — Triagem Fuzzy | by Pedrin
Execute este arquivo para iniciar o sistema com animação no terminal.
Uso: python launcher.py
"""

import sys
import time
import os
import subprocess
import threading

# ── Compatibilidade de cores no Windows ──────────────────────────────────────
try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except Exception:
    pass

# ── Códigos ANSI ─────────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
BLINK   = "\033[5m"

# Cores
AZUL    = "\033[38;5;39m"
AZUL_E  = "\033[38;5;27m"
CIANO   = "\033[38;5;51m"
VERDE   = "\033[38;5;46m"
BRANCO  = "\033[97m"
CINZA   = "\033[38;5;245m"
ROXO    = "\033[38;5;135m"
VERMELHO= "\033[38;5;196m"
AMARELO = "\033[38;5;226m"

# ── ASCII art "PEDRIN" ────────────────────────────────────────────────────────
PEDRIN_ART = r"""
██████╗ ███████╗██████╗ ██████╗ ██╗███╗   ██╗
██╔══██╗██╔════╝██╔══██╗██╔══██╗██║████╗  ██║
██████╔╝█████╗  ██║  ██║██████╔╝██║██╔██╗ ██║
██╔═══╝ ██╔══╝  ██║  ██║██╔══██╗██║██║╚██╗██║
██║     ███████╗██████╔╝██║  ██║██║██║ ╚████║
╚═╝     ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
"""

SUBTITULO = "  [ SISTEMA DE TRIAGEM INTELIGENTE · PROTOCOLO DE MANCHESTER · FUZZY v2.0 ]"

# ── Símbolos de loading ───────────────────────────────────────────────────────
SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

# ── Mensagens temáticas ───────────────────────────────────────────────────────
MENSAGENS_LOADING = [
    "Inicializando motor de inferência fuzzy...",
    "Carregando funções de pertinência...",
    "Compilando base de regras Manchester (28 regras)...",
    "Calibrando universos de discurso...",
    "Conectando ao sistema de totens virtuais...",
    "Configurando defuzzificação por centroide...",
    "Validando variáveis linguísticas...",
    "Montando painel hospitalar Streamlit...",
    "Verificando integridade do sistema...",
    "Sistema pronto. Abrindo interface...",
]

MENSAGEM_FINAL = [
    "",
    VERDE + BOLD + "  ╔══════════════════════════════════════════════════════╗" + RESET,
    VERDE + BOLD + "  ║                                                      ║" + RESET,
    VERDE + BOLD + "  ║   ✅  SISTEMA INICIALIZADO COM SUCESSO               ║" + RESET,
    VERDE + BOLD + "  ║   🏥  Abrindo painel hospitalar no navegador...      ║" + RESET,
    VERDE + BOLD + "  ║   🔗  http://localhost:8501                          ║" + RESET,
    VERDE + BOLD + "  ║                                                      ║" + RESET,
    VERDE + BOLD + "  ║   Desenvolvido por: Pedro Augusto & Maria Julia      ║" + RESET,
    VERDE + BOLD + "  ╚══════════════════════════════════════════════════════╝" + RESET,
    "",
]

# ── Funções utilitárias ───────────────────────────────────────────────────────

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def beep(n=1, intervalo=0.12):
    """Emite beep(s) pelo alto-falante do sistema (Windows)."""
    try:
        import winsound
        for _ in range(n):
            winsound.Beep(880, 120)
            time.sleep(intervalo)
    except Exception:
        # fallback: caractere BEL
        for _ in range(n):
            sys.stdout.write("\a")
            sys.stdout.flush()
            time.sleep(intervalo)

def digitar(texto, cor=BRANCO, delay=0.03):
    """Efeito de digitação letra por letra."""
    sys.stdout.write(cor)
    for ch in texto:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET + "\n")

def imprimir_header():
    limpar()
    # Borda superior
    print(AZUL_E + BOLD + "  " + "═" * 62 + RESET)
    # ASCII art colorida (letra por letra em azul → ciano)
    linhas = PEDRIN_ART.strip("\n").split("\n")
    gradiente = [AZUL_E, AZUL, AZUL, CIANO, CIANO, ROXO]
    for i, linha in enumerate(linhas):
        cor = gradiente[i % len(gradiente)]
        print(BOLD + cor + "  " + linha + RESET)
    # Subtítulo
    print(CINZA + SUBTITULO + RESET)
    print(AZUL_E + BOLD + "  " + "═" * 62 + RESET)
    print()

def animar_cadeado():
    """Animação rápida de 'desbloqueando sistema'."""
    frames = ["🔒", "🔓", "🔓", "✅"]
    for f in frames:
        sys.stdout.write(f"\r  {CIANO}STATUS  {RESET}{f}  Autenticando sistema...    ")
        sys.stdout.flush()
        time.sleep(0.35)
    print()

def barra_loading():
    """Barra de progresso animada com mensagens temáticas."""
    total   = 40          # largura da barra
    etapas  = len(MENSAGENS_LOADING)
    spinner_idx = 0

    for i, msg in enumerate(MENSAGENS_LOADING):
        preenchido = int((i / etapas) * total)
        vazio      = total - preenchido
        pct        = int((i / etapas) * 100)

        barra = (
            VERDE  + "█" * preenchido +
            CINZA  + "░" * vazio      +
            RESET
        )
        spin  = AMARELO + SPINNER[spinner_idx % len(SPINNER)] + RESET
        linha = (
            f"\r  {spin} {CIANO}[{barra}{CIANO}]{RESET} "
            f"{AMARELO}{pct:3d}%{RESET}  {CINZA}{msg}{RESET}"
        )
        sys.stdout.write(linha)
        sys.stdout.flush()
        spinner_idx += 1
        time.sleep(0.55)

    # Barra completa
    barra_final = VERDE + "█" * total + RESET
    sys.stdout.write(
        f"\r  {VERDE}✔{RESET} {CIANO}[{barra_final}{CIANO}]{RESET} "
        f"{VERDE}{BOLD}100%{RESET}  {VERDE}Sistema carregado.{RESET}          \n"
    )
    sys.stdout.flush()

def exibir_stats():
    """Exibe bloco de informações do sistema."""
    print()
    print(AZUL_E + "  ┌─────────────────────────────────────────────────┐" + RESET)
    infos = [
        ("ENGINE",     "scikit-fuzzy · Mamdani Inference"),
        ("PROTOCOLO",  "Manchester (5 níveis de risco)"),
        ("VARIÁVEIS",  "FC · SpO₂ · Temp · PAS · Dor (EVA)"),
        ("REGRAS",     "28 regras de inferência fuzzy"),
        ("INTERFACE",  "Streamlit · localhost:8501"),
        ("DEVS",       "Pedro Augusto  &  Maria Julia"),
    ]
    for chave, valor in infos:
        print(
            AZUL_E + "  │  " +
            CIANO  + BOLD + f"{chave:<12}" + RESET +
            CINZA  + "→  " +
            BRANCO + valor +
            RESET
        )
    print(AZUL_E + "  └─────────────────────────────────────────────────┘" + RESET)
    print()

def exibir_mensagem_final():
    for linha in MENSAGEM_FINAL:
        print(linha)
        time.sleep(0.08)

# ── Sequência principal ───────────────────────────────────────────────────────

def main():
    # 1. Header + beep de abertura
    imprimir_header()
    beep(1)
    time.sleep(0.4)

    # 2. Animação de desbloqueio
    animar_cadeado()
    time.sleep(0.3)

    # 3. Stats do sistema
    exibir_stats()
    time.sleep(0.3)

    # 4. Barra de loading com mensagens
    barra_loading()
    time.sleep(0.4)

    # 5. Beep triplo de conclusão
    beep(3, intervalo=0.08)
    time.sleep(0.3)

    # 6. Mensagem final
    exibir_mensagem_final()
    time.sleep(1.2)

    # 7. Lança o Streamlit
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "triagem_fuzzy.py")
    print(CINZA + f"  >> streamlit run {script}" + RESET)
    print()

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", script,
             "--server.headless", "false"],
            check=True
        )
    except KeyboardInterrupt:
        print()
        print(AMARELO + "  Sistema encerrado pelo usuário." + RESET)
    except FileNotFoundError:
        print(VERMELHO + "  ERRO: triagem_fuzzy.py não encontrado na mesma pasta!" + RESET)
        print(CINZA   + "  Coloque launcher.py e triagem_fuzzy.py na mesma pasta." + RESET)
    except Exception as e:
        print(VERMELHO + f"  ERRO ao iniciar Streamlit: {e}" + RESET)
        print(CINZA   + "  Tente manualmente: streamlit run triagem_fuzzy.py" + RESET)


if __name__ == "__main__":
    main()
