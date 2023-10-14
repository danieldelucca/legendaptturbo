import re
import os
import sys
import listas_nomes as ln

if getattr(sys, 'frozen', False):
    # Path para quando rodar como .exe.
    pasta_do_script = sys._MEIPASS
else:
    # Path para quando rodar como script.
    pasta_funções = os.path.dirname(os.path.abspath(__file__))
    pasta_do_script = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pegar caminho até a pasta 'configurações'
pasta_configurações = os.path.join(pasta_do_script, 'configurações')


# ------------------ CONFIGURAR.TXT ----------------- #
# Definir sets e listas a serem usadas nesta parte.
set_substituições_específicas = set()
set_nomes_femininos = set()
set_nomes_masculinos = set()
set_inseparáveis = set()
lista_remover_linhas_com = []

# Variáveis a serem usadas nesta parte.
transformar_gerúndio = ''
remover_interjeições = ''
transformar_você = ''
quebrar_antes = ''
remover_caract_música = ''
transformar_de_em_do_da = ''
transformar_a_gente_em_nos = ''
diálogos_com_espaço = ''
diálogos_sem_espaço = ''
remover_reticências_do_começo = ''
remover_reticências_do_fim = ''
remover_legenda_música = ''

# Definir caminho do arquivo configurar.txt.
caminho_configurar = os.path.join(pasta_do_script, 'configurar.txt')

# Ler linhas de configurar.txt.
with open(caminho_configurar, 'r', encoding='utf=8') as arquivo_configurar:
    linhas = arquivo_configurar.readlines()

# Captar índices das linhas com títulos de cada 'sessão' de configurar.txt
# para a leitura dos nomes de arquivos .srt, parâmetros, itens das listas, etc
for i, linha in enumerate(linhas):
    if re.search('# TAMANHO MÁXIMO DE LINHA', linhas[i]):
        tamanho_máximo_de_linha = linhas[i + 1].strip()
    if re.search('# DURAÇÃO MÍNIMA DA LEGENDA', linhas[i]):
        duração_mínima = linhas[i + 1].strip()
    if re.search('# DURAÇÃO MÁXIMA DA LEGENDA', linhas[i]):
        duração_máxima = linhas[i + 1].strip()
    if re.search('# INTERVALO ENTRE LEGENDAS', linhas[i]):
        intervalo_entre_legendas = linhas[i + 1].strip()
    if re.search('# FRAME RATE', linhas[i]):
        frame_rate = linhas[i + 1].strip()
    if re.search('# NOMES FEMININOS', linhas[i]):
        i_nomes_femininos = i
    if re.search('# NOMES MASCULINOS', linhas[i]):
        i_nomes_masculinos = i
    if re.search('# SUBSTITUIÇÕES ESPECÍFICAS', linhas[i]):
        i_substituições_específicas = i
    if re.search('# REMOVER LINHAS COM ISSO', linhas[i]):
        i_remover_linhas_com = i

    # Ativar ou desativar funções no arquivo 'configurações.txt' -
    # se a linha abaixo da descrição da funcionalidade for 'ativar > sim'
    # a variável em questão vira True (o que vai ativar a função em legenda_pt_turbo.py).
    if '- remover palavras repetidas separadas por vírgula' in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            remover_palavras_repetidas = True
        else:
            remover_palavras_repetidas = False

    if '- remover frases repetidas e deixar apenas uma' in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            remover_frase_repetida = True
        else:
            remover_frase_repetida = False

    if "- remover 'se', 'me' e 'nos' dos verbos " in linhas[i]:
        if re.search('sim', linhas[i + 2], flags=re.IGNORECASE):
            remover_reflexivo = True
        else:
            remover_reflexivo = False

    if '- remover interjeições' in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            remover_interjeições = True
        else:
            remover_interjeições = False

    if '- transformar gerúndio português' in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_gerúndio = True
        else:
            transformar_gerúndio = False

    if '- transformar ênclise' in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_ênclise = True
        else:
            transformar_ênclise = False

    if "- transformar 'você'" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_você = True
        else:
            transformar_você = False

    if "- remover o caractere ♪ e colocar" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            remover_caract_música = True
        else:
            remover_caract_música = False

    if "- remover totalmente as legendas de música" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            remover_legenda_música = True
        else:
            remover_legenda_música = False

    if "- transformar 'para você' e 'a você' em 'te' com alguns verbos" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_para_você_em_te = True
        else:
            transformar_para_você_em_te = False

    if "- transformar 'a gente'" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_a_gente_em_nos = True
        else:
            transformar_a_gente_em_nos = False

    if "- transformar 'mais... do que' em 'mais... que'" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_mais_do_que_em_mais_que = True
        else:
            transformar_mais_do_que_em_mais_que = False

    if "- transformar 'de' em 'do'" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_de_em_do_da = True
        else:
            transformar_de_em_do_da = False

    if "- deixar primeira letra" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            corrigir_maiúsculas_pontuação = True
        else:
            corrigir_maiúsculas_pontuação = False

    if "- diálogos com espaço" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            diálogos_com_espaço = True
        else:
            diálogos_com_espaço = False

    if "- remover reticências (...) do começo" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            remover_reticências_do_começo = True
        else:
            remover_reticências_do_começo = False

    if "# - transformar '...' em '--'" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            transformar_reticências_em_dois_hífens = True
        else:
            transformar_reticências_em_dois_hífens = False

    if "- remover reticências (...) do fim" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            remover_reticências_do_fim = True
        else:
            remover_reticências_do_fim = False

    if "- corrigir minúsculas depois de pontuação" in linhas[i]:
        if re.search('sim', linhas[i + 1], flags=re.IGNORECASE):
            corrigir_maiúsculas_pontuação = True
        else:
            corrigir_maiúsculas_pontuação = False

# Pegar NOMES FEMININOS em configurar.txt.
for i, linha in enumerate(linhas[i_nomes_femininos + 1:i_nomes_masculinos],
                          start=i_nomes_femininos + 1):
    linha = linhas[i].strip()
    if len(linhas[i]) > 2 and '#' not in linha:
        ln.set_nomes_femininos_default.add(linha)

# Pegar NOMES MASCULINOS em configurar.txt.
for i, linha in enumerate(linhas[i_nomes_masculinos + 1:i_substituições_específicas],
                          start=i_nomes_masculinos + 1):
    linha = linhas[i].strip()
    if len(linhas[i]) > 2 and '#' not in linha:
        ln.set_nomes_masculinos_default.add(linha)

# Pegar SUBSTITUIÇÕES ESPECÍFICAS em configurar.txt.
for i, linha in enumerate(linhas[i_substituições_específicas + 1:i_remover_linhas_com],
                          start=i_substituições_específicas + 1):
    linha = linhas[i].strip()
    if '=' in linhas[i]:
        partes = linhas[i].split('=')
        # Remover "" e '', que são delimitadores dos termos com espaços nas bordas.
        termo_antes = partes[0].strip().strip('\'').strip("\"")
        termo_depois = partes[1].strip().strip('\'').strip("\"")
        # adicionar tupla ao set com 'termo a sair' e 'termo a entrar'
        set_substituições_específicas.add((termo_antes, termo_depois))

# Fazer lista de REMOVER LINHAS COM...
for i, linha in enumerate(linhas[i_remover_linhas_com + 1:],
                          start=i_remover_linhas_com):
    linha = linhas[i].strip()
    if len(linhas[i]) > 2:
        lista_remover_linhas_com.append(linha)


# ----------------------- LISTAS DOS ARQUIVOS .TXT ------------------------- #

# ---- Arquivos .txt que atuarão sobre a legenda em português ---- #


# ---- Substituições Case Insensitive - Português ---- #

# Definir caminho do arquivo substituições_case_insensitive.txt.
caminho_substituições_case_insensitive = (
    os.path.join(pasta_configurações, 'substituições_case_insensitive_português.txt')
)

# Set para armazenar itens da lista.
set_substituições_ci = set()
# Pegar os termos do arquivo substituições_case_insensitive.txt.
with open(caminho_substituições_case_insensitive, 'r', encoding='utf-8') as arq_subst_ci:
    for linha in arq_subst_ci:
        # Incluir as linhas com os termos, excluindo os comentários '#'.
        if '=' in linha and not linha.startswith('#'):
            # Excluir comentários inline, à direita do item da lista.
            if '#' in linha:
                ind_coment = linha.index('#')
                linha = linha[:ind_coment].strip()
            # Dividir termo a ser encontrado e substituído e o que vai entrar.
            partes = linha.split('=')
            # Definir termo_antes e termo_depois para o que deve sair e entrar.
            # Remover "" e '', que são delimitadores dos termos quando há espaço nas bordas.
            termo_antes = partes[0].strip().strip('\'')
            termo_depois = partes[1].strip().strip('\'')
            # Adicionar tupla com os dois termos ao set.
            set_substituições_ci.add((termo_antes, termo_depois))


# ---- Substituições Case Sensitive - Português ---- #

# Definir caminho do arquivo substituições_case_insensitive.txt.
caminho_substituições_case_sensitive = (
    os.path.join(pasta_configurações, 'substituições_case_sensitive_português.txt')
)

# Set para armazenar itens da lista.
set_substituições_cs = set()
# Pegar os termos do arquivo substituições_case_sensitive.txt.
with open(caminho_substituições_case_sensitive, 'r', encoding='utf-8') as arq_subst_cs:
    for linha in arq_subst_cs:
        # Incluir as linhas com os termos, excluindo os comentários '#'.
        if '=' in linha and not linha.startswith('#'):
            # Excluir comentários inline, à direita do item da lista.
            if '#' in linha:
                ind_coment = linha.index('#')
                linha = linha[:ind_coment].strip()
            # Dividir termo a ser encontrado e substituído e o que vai entrar.
            partes = linha.split('=')
            # Remover "" e '', que são delimitadores dos termos quando há espaço nas bordas.
            termo_antes = partes[0].strip().strip('\'').strip("\"")
            termo_depois = partes[1].strip().strip('\'').strip("\"")
            # Adicionar tupla com os dois termos ao set.
            set_substituições_cs.add((termo_antes, termo_depois))


# ---- Substituições Sem Pontuação - Português ---- #
# São as substituições realizadas se o termo não terminar com pontuação na frase.

# Definir caminho do arquivo substituições_sem_pontuação.txt.
caminho_substituições_sem_pontuação = (
    os.path.join(pasta_configurações, 'substituições_sem_pontuação_português.txt')
)

# Set para armazenar itens da lista.
set_substituições_sem_pontuação = set()
# Pegar os termos do arquivo substituições_sem_pontuação.txt.
with open(caminho_substituições_sem_pontuação, 'r', encoding='utf-8') as arq_subst_sp:
    for linha in arq_subst_sp:
        # Incluir as linhas com os termos, excluindo os comentários '#'.
        if '=' in linha and not linha.startswith('#'):
            # Excluir comentários inline, à direita do item da lista.
            if '#' in linha:
                ind_coment = linha.index('#')
                linha = linha[:ind_coment].strip()
            # Dividir termo a ser encontrado e substituído e o que vai entrar.
            partes = linha.split('=')
            termo_antes = partes[0].strip()
            termo_depois = partes[1].strip()
            # Adicionar tupla com os dois termos ao set.
            set_substituições_sem_pontuação.add((termo_antes, termo_depois))


# ---- Substituições Sem Limite de Palavra - Português ---- #

# Definir caminho do arquivo substituições_sem_limite_de_palavra.txt.
caminho_substituições_sem_limite_de_palavra = (
    os.path.join(pasta_configurações, 'substituições_sem_limite_de_palavra_português.txt')
)

# Set para armazenar itens da lista.
set_subst_sem_limite_de_palavra = set()
# Pegar os termos do arquivo substituições_sem_limite_de_palavra.txt.
with open(caminho_substituições_sem_limite_de_palavra, 'r', encoding='utf-8') as arq_subst_slp:
    for linha in arq_subst_slp:
        linha = linha.strip()
        # Incluir as linhas com os termos, excluindo os comentários '#'.
        if '=' in linha:
            partes = linha.split('=')
            # Dividir termo a ser encontrado e substituído e o que vai entrar.
            # Remover "" e '', que são delimitadores dos termos quando há espaço nas bordas.
            termo_antes = partes[0].strip().strip('\'').strip("\"")
            termo_depois = partes[1].strip().strip('\'').strip("\"")
            # Adicionar tupla com os dois termos ao set.
            set_subst_sem_limite_de_palavra.add((termo_antes, termo_depois))


# ---- Substituições em Começo de Pergunta - Português ---- #

# Definir caminho do arquivo substituições_começo_de_pergunta.txt.
caminho_substituições_começo_de_pergunta = (
    os.path.join(pasta_configurações, 'substituições_começo_de_pergunta_português.txt')
)

# Set para armazenar itens da lista.
set_subst_começo_pergunta = set()
# Pegar os termos do arquivo substituições_começo_de_pergunta.txt.
with open(caminho_substituições_começo_de_pergunta,
          'r', encoding='utf-8') as arq_subst_começo_pergunta:
    for linha in arq_subst_começo_pergunta:
        linha = linha.strip()
        # Incluir as linhas com os termos, excluindo os comentários '#'.
        if '=' in linha and not linha.startswith('#'):
            if '#' in linha:
                ind_coment = linha.index('#')
                linha = linha[:ind_coment].strip()
            partes = linha.split('=')
            # Remover "" e '', que são delimitadores dos termos quando há espaço nas bordas.
            termo_antes = partes[0].strip().strip('\'').strip("\"")
            termo_depois = partes[1].strip().strip('\'').strip("\"")
            # Adicionar tupla com os dois termos ao set.
            set_subst_começo_pergunta.add((termo_antes, termo_depois))


# ---- Traduções Específicas de Frases ---- #

# Definir caminho do arquivo traduções_específicas_frases.txt.
caminho_traduções_específicas_frases = (
    os.path.join(pasta_configurações, 'traduções_específicas_frases.txt')
)

# Set para armazenar itens da lista.
set_trad_esp_frases = set()
# Pegar os termos do arquivo traduções_específicas_frases.txt.
with open(caminho_traduções_específicas_frases, 'r', encoding='utf-8') as arq_trad_esp:
    linhas = arq_trad_esp.readlines()
    # Pegar índice do início da lista.
    for i, linha in enumerate(linhas):
        if re.search('# INÍCIO DA LISTA:', linhas[i]):
            te_index = i

    # Pegar lista de traduções específicas de frases - traduções_específicas_frases.txt.
    for i, linha in enumerate(linhas[te_index + 1:], start=te_index + 1):
        # Incluir as linhas com os termos, excluindo os comentários '#'.
        if '=' in linha and not linha.startswith('#'):
            if '#' in linha:
                ind_coment = linha.index('#')
                linha = linha[:ind_coment].strip()
            partes = linhas[i].split('=')
            termo_antes = partes[0].strip()
            termo_depois = partes[1].strip()
            # adicionar tupla com os dois termos ao set
            set_trad_esp_frases.add((termo_antes, termo_depois))


# ---- Remover ah, ai, ei - Português ---- #

# Definir set com interjeições de remover_ah_ai_ei_português.
set_ah_ai_ei_pt = set()
# Definir caminho até remover_ah_ai_ei_português.txt.
caminho_remover_ah_ai_ui_ei_português = (
    os.path.join(pasta_configurações, 'remover_ah_ai_ei_português.txt')
)

# Pegar interjeições em remover_ah_ai_ei_português.txt.
with open(caminho_remover_ah_ai_ui_ei_português, 'r', encoding='utf-8') \
        as arq_remover_ah_ai_ei_português:

    # Se funcionalidade estiver ativada ('ativar > sim') em configurar.txt.
    if remover_interjeições is True:
        for linha in arq_remover_ah_ai_ei_português:

            linha_vazia = linha.strip() == ''
            # Excluir comentários.
            if not linha_vazia and not linha.startswith('#'):
                # Excluir comentários inline nos itens da lista.
                if '#' in linha:
                    ind_coment = linha.index('#')
                    interjeição = linha[:ind_coment].strip()
                else:
                    interjeição = linha.strip()
                set_ah_ai_ei_pt.add(interjeição)


# ------- Arquivos .txt que atuarão sobre a legenda em idioma estrangeiro. ----- #


# ---- Remover ah, ai, ei - Idioma Estrangeiro ---- #

# Definir set com interjeições de remover_ah_ai_ei_português.
set_ah_ai_ei_estr = set()

# Definir caminho até remover_ah_ai_ei_estrangeiro.txt.
caminho_remover_ah_ai_ui_ei_estrangeiro = (
    os.path.join(pasta_configurações, 'remover_ah_ai_ei_estrangeiro.txt')
)

# Pegar lista de interjeições para remover em remover_ah_ai_ei_estrangeiro.txt.
with open(caminho_remover_ah_ai_ui_ei_estrangeiro, 'r', encoding='utf-8') \
        as arq_remover_ah_ai_ei_estrangeiro:

    # Se funcionalidade estiver ativada ('ativar > sim') em configurar.txt.
    if remover_interjeições is True:
        for linha in arq_remover_ah_ai_ei_estrangeiro:

            linha_vazia = linha.strip() == ''
            # Excluir comentários.
            if not linha_vazia and not linha.startswith('#'):
                # Excluir comentários inline nos itens da lista.
                if '#' in linha:
                    ind_coment = linha.index('#')
                    interjeição = linha[:ind_coment].strip()
                else:
                    interjeição = linha.strip()
                set_ah_ai_ei_estr.add(interjeição)


# ------ Substituições Case Insensitive - Idioma Estrangeiro ------ #

# Definir caminho até substituições_case_insensitive_estrangeiro.txt.
caminho_substituições_case_insensitive_estr = (
    os.path.join(pasta_configurações, 'substituições_case_insensitive_estrangeiro.txt')
)

# Definir set para armazenar itens da lista.
set_substituições_ci_estr = set()

# Pegar termos para substituição case insensitive em idioma estrangeiro.
with open(caminho_substituições_case_insensitive_estr, 'r', encoding='utf-8') as arq_subst_ci_estr:
    for linha in arq_subst_ci_estr:
        linha = linha.strip()
        if '=' in linha and not linha.startswith('#'):
            if '#' in linha:
                ind_coment = linha.index('#')
                linha = linha[:ind_coment].strip()
            # Dividir termo a ser encontrado e substituído e o que vai entrar.
            partes = linha.split('=')
            # Remover "" e '', que são delimitadores dos termos quando há espaço nas bordas.
            termo_antes = partes[0].strip().strip('\'').strip("\"")
            termo_depois = partes[1].strip().strip('\'').strip("\"")
            # adicionar tupla com os dois termos ao set
            set_substituições_ci_estr.add((termo_antes, termo_depois))


# ------ Substituições Case Sensitive - Idioma Estrangeiro ------ #

# Definir caminho até substituições_case_sensitive_estrangeiro.txt.
caminho_substituições_case_sensitive_estr = (
    os.path.join(pasta_configurações, 'substituições_case_sensitive_estrangeiro.txt')
)

# Definir set para armazenar itens da lista.
set_substituições_cs_estr = set()

# Pegar termos para substituição case sensitive em idioma estrangeiro.
with open(caminho_substituições_case_sensitive_estr, 'r', encoding='utf-8') as arq_subst_cs_estr:
    # Incluir as linhas com os termos.
    for linha in arq_subst_cs_estr:
        linha = linha.strip()
        # Dividr entre termo a ser substituído e termo que entrará.
        if '=' in linha:
            partes = linha.split('=')
            # Remover "" e '', que são delimitadores dos termos quando há espaço nas bordas.
            termo_antes = partes[0].strip().strip('\'').strip("\"")
            termo_depois = partes[1].strip().strip('\'').strip("\"")
            # adicionar tupla com os dois termos ao set
            set_substituições_cs_estr.add((termo_antes, termo_depois))


# ------ Substituições Sem Limite de Palavra - Idioma Estrangeiro ------ #

# Definir caminho até substituições_sem_limite_de_palavra_estrangeiro.txt.
caminho_substituições_sem_limite_de_palavra_estr = (
    os.path.join(pasta_configurações, 'substituições_sem_limite_de_palavra_estrangeiro.txt')
)

# Definir set para armazenar itens da lista.
set_substituições_sem_limite_de_palavra_estr = set()

# Pegar termos para substituição case sensitive em idioma estrangeiro.
with open(caminho_substituições_sem_limite_de_palavra_estr, 'r', encoding='utf-8') as arquivo:
    # Incluir as linhas com os termos.
    for linha in arquivo:
        linha = linha.strip()
        # Dividr entre termo a ser substituído e termo que entrará.
        if '=' in linha:
            partes = linha.split('=')
            # Remover "" e '', que são delimitadores dos termos quando há espaço nas bordas.
            palavra_antes = partes[0].strip().strip('\'').strip("\"")
            palavra_depois = partes[1].strip().strip('\'').strip("\"")
            # Adicionar tupla com os dois termos ao set.
            set_substituições_sem_limite_de_palavra_estr.add((palavra_antes, palavra_depois))
