import funções_de_transformações as fu
import listas as ls
import reps
import logo as lg
import re
import string
import os
import pyperclip
import subprocess
import importlib
import tkinter as tk
from tkinter import filedialog

# Definir o caminho até a pasta do script para leitura de arquivos.
pasta_funções = os.path.dirname(os.path.abspath(__file__))
pasta_do_script = os.path.dirname(pasta_funções)


print(lg.logo)

texto_apresentação = (
    '\n  Preparar legenda em idioma estrangeiro e traduzir no Chat GPT\n\n\n\n'
    '  Vamos preparar a legenda em idioma estrangeiro para tradução no ChatGPT.\n\n'
    '  A versão gratuita do ChatGPT não permite que a tradução de uma legenda seja feita '
    'diretamente por este programa,\n  portanto vamos seguir alguns passos '
    'para solicitar a tradução.\n\n'
    '  Para mais instruções, veja o arquivo LEIAME.txt\n\n'
    '  Você pode selecionar opções de ajustes no arquivo configurar.txt.\n'
)

# Exibir texto de apresentação e menu inicial.
print(texto_apresentação)

# Abrir configurar.txt.
input_1 = input("    Digite:\n    >> A + Enter --> abrir configurar.txt\n    "
                ">> Enter --> continuar\n\n")
if input_1.lower() == 'a':
    caminho_configurar_txt = os.path.join(pasta_do_script, 'configurar.txt')
    subprocess.Popen(["notepad.exe", caminho_configurar_txt])
    print('  Depois de ativar ou desativar opções em configurar.txt, '
          'salve o arquivo e digite Enter para continuar.\n')
    input()

# Recarregar as variáveis de configurar.txt, que está no módulo reps.

importlib.reload(reps)

print('  Vamos selecionar o arquivo da legenda a ser traduzida no ChatGPT.\n')
input('  Digite Enter para continuar.\n')


# Abrir janela para selecionar o arquivo da legenda.
def abrir_legenda_estrangeira():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    arquivo_selecionado = filedialog.askopenfilename(
        title="Abrir arquivo da legenda em idioma estrangeiro",
        filetypes=[("SubRip Files", "*.srt"), ("All Files", "*.*")]
    )

    if arquivo_selecionado:
        print("  Legenda selecionada para preparação e tradução:")
        print('  ' + arquivo_selecionado)
        print('\n')
        try:
            # Carregar legenda estrangeira e designar variável linhas.
            with open(arquivo_selecionado, 'r', encoding='utf-8') as arquivo_estr:
                legenda_estr = arquivo_estr.readlines()

        except Exception:
            print('  Não foi possível carregar o arquivo. '
                  'Certifique-se de que o nome do arquivo que consta em configurar.txt '
                  'está correto e é um arquivo .srt válido.\n')
            print('  Digite Enter para sair.\n')

    else:
        print('\n  Nenhum arquivo foi selecionado.\n')
        input('  Digite Enter para abrir de novo.\n')
        abrir_legenda_estrangeira()
    return legenda_estr


legenda_estr = abrir_legenda_estrangeira()

# Adicionar linhas vazias ao final para evitar erros de índice.
legenda_estr.append('\n')
legenda_estr.append('\n')
legenda_estr.append('\n')


# ------- começo de funções que vão nos decorators --------- #

# Remover '/' dos blocos de diálogo se uma das linhas do diálogo deixar de existir
def remover_linha_vazia_de_diálogo(linhas_estr):
    for i, linha in enumerate(linhas_estr):
        # tomar linha do timestamp como referência
        if '-->' in linhas_estr[i]:
            texto_bloco = linhas_estr[i + 1]
            texto_bloco_é_diálogo = '/' in texto_bloco

            if texto_bloco_é_diálogo:
                linha_1_é_vazia = texto_bloco.split('/')[0].strip() == ''
                linha_2_é_vazia = texto_bloco.split('/')[1].strip() == ''
                if linha_1_é_vazia or linha_2_é_vazia:
                    texto_bloco = texto_bloco.replace('/', '')
                    texto_bloco = f'{texto_bloco.strip()}\n'
            linhas_estr[i + 1] = texto_bloco

    return linhas_estr

# -------- começo dos decorators da legenda estrangeira --------------- #


def loop_linhas_estr(função_principal):
    def wrapper(linhas_estr):

        for i, linha_estr in enumerate(linhas_estr):
            if '-->' in linhas_estr[i]:

                número_legenda_estr = linhas_estr[i - 1].strip().strip('\ufeff')
                texto_bloco_estr = linhas_estr[i + 1].strip()

                # Processar linha 1, retornando 'linhas'.
                linhas_estr = função_principal(
                    i, linhas_estr, texto_bloco_estr, número_legenda_estr,
                    )
                # Argumentos da função principal:
                # (i, linhas_estr, texto_bloco_estr, número_legenda_estr)

        # Corrige espaço antes de pontuação: Qué ? --> Qué?
        linhas_estr = fu.corrigir_espaço_pontuação_legenda_estrangeira(linhas_estr)
        linhas_estr = fu.remover_linha_vazia_de_diálogo(linhas_estr)
        linhas_estr = fu.corrigir_espaços_duplos(linhas_estr)
        return linhas_estr
    return wrapper


# --------- começo das funções exclusivas da legenda estrangeira ------------ #
@loop_linhas_estr
def remover_ah_ei_ai_estr(i, linhas_estr, texto_bloco_estr, número_legenda):

    for interjeição in reps.set_ah_ai_ei_estr:
        if re.search(rf'\b{interjeição}', texto_bloco_estr, re.IGNORECASE):
            palavras = texto_bloco_estr.split()

            for j, plv in enumerate(palavras):     # dividir linha atual em palavras

                palavra_atual = palavras[j]
                palavra_atual_é_interjeição = (
                    palavra_atual.lower().strip(string.punctuation) in reps.set_ah_ai_ei_estr
                )

                if palavra_atual_é_interjeição:
                    # remover as interjeições com pontos, exceto vírgula
                    for ponto in {'.', '!', '?', ':', '...'}:
                        if palavra_atual.lower() == f'{interjeição}{ponto}':
                            # remover palavra atual
                            palavra_atual = ''
                            # atualizar palavra em 'palavras'
                            palavras[j] = palavra_atual
                            # atualizar texto_bloco
                            texto_bloco_estr = ' '.join(palavras)
                            # atualizar texto_bloco em 'linhas_pt'
                            linhas_estr[i + 1] = texto_bloco_estr

                    existe_próxima_palavra = j + 1 < len(palavras)

                    # Remover interjeição com vírgula ou sozinha e ajustar o casing
                    # da próxima palavra, se necessário.
                    if existe_próxima_palavra:
                        próxima_palavra = palavras[j + 1]

                        # remover interjeições com vírgula ou sem ponto
                        # e manter case da interjeição na próxima palavra
                        # essa parte da função já vai remover também interjeições
                        # com vírgula na última palavra

                        # maiúscula
                        texto_bloco_estr = (
                            texto_bloco_estr.replace(
                                f'{palavra_atual.capitalize()} {próxima_palavra}',
                                próxima_palavra.capitalize())
                        )
                        # minúscula
                        texto_bloco_estr = (
                            texto_bloco_estr.replace(f'{palavra_atual} {próxima_palavra}',
                                                     próxima_palavra)
                        )

                        # variações com vírgula
                        # maiúscula
                        texto_bloco_estr = (
                            texto_bloco_estr.replace(
                                f'{palavra_atual.capitalize()}, {próxima_palavra}',
                                próxima_palavra.capitalize())
                        )
                        # minúscula
                        texto_bloco_estr = (
                            texto_bloco_estr.replace(f'{palavra_atual}, {próxima_palavra}',
                                                     próxima_palavra)
                        )

                        # atualizar linha em 'linhas'
                        linhas_estr[i + 1] = texto_bloco_estr

    return linhas_estr


@loop_linhas_estr
def substituições_case_insensitive_estr(i, linhas_estr, texto_bloco_estr, número_legenda_estr):

    for termo_para_sair, termo_para_entrar in reps.set_substituições_ci_estr:

        termo_para_sair_começa_com_ponto = (
            termo_para_sair[0] in ls.lista_pontuação_com_vírgula
        )

        termo_para_sair_termina_com_ponto = (
            termo_para_sair[-1] in ls.lista_pontuação_com_vírgula
        )

        if termo_para_sair_começa_com_ponto and termo_para_sair_termina_com_ponto:
            # procurar o termo da lista no texto_bloco
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(re.escape(termo_para_sair), texto_bloco_estr, re.IGNORECASE)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # fazer substituições pegando termo se for lower, capitalizer ou upper
                texto_bloco_estr = re.sub(re.escape(termo_para_sair),
                                          termo_para_entrar, texto_bloco_estr,
                                          count=0, flags=re.IGNORECASE)

        elif termo_para_sair_termina_com_ponto:
            # procurar o termo da lista no texto_bloco
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'\b{re.escape(termo_para_sair)}',
                          texto_bloco_estr, re.IGNORECASE)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # fazer substituições pegando termo se for lower, capitalizer ou upper
                texto_bloco_estr = re.sub(fr'\b{re.escape(termo_para_sair)}',
                                          termo_para_entrar, texto_bloco_estr,
                                          count=0, flags=re.IGNORECASE)

        elif termo_para_sair_começa_com_ponto:
            # procurar o termo da lista no texto_bloco
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr"{re.escape(termo_para_sair)}\b(?!'\w)",
                          texto_bloco_estr, re.IGNORECASE)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # fazer substituições pegando termo se for lower, capitalizer ou upper
                texto_bloco_estr = re.sub(fr'{re.escape(termo_para_sair)}\b',
                                          termo_para_entrar, texto_bloco_estr,
                                          count=0, flags=re.IGNORECASE)

        # se o item da lista não termina com pontuação
        elif not termo_para_sair_começa_com_ponto and not termo_para_sair_termina_com_ponto:
            # procurar termo da lista no texto bloco com e sem pontuação
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr"\b{re.escape(termo_para_sair)}\b(?!'\w)|"
                          fr'\b{re.escape(termo_para_sair)}[.,!?:"]',
                          texto_bloco_estr, re.IGNORECASE)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # fazer substituições pegando termo se for lower, capitalizer ou upper
                texto_bloco_estr = re.sub(fr"\b{re.escape(termo_para_sair)}\b(?!'\w)|"
                                          fr'\b{re.escape(termo_para_sair)}[.,!?:"]',
                                          termo_para_entrar, texto_bloco_estr,
                                          count=0, flags=re.IGNORECASE)

            # atualizar linha em 'linhas'
            linhas_estr[i + 1] = texto_bloco_estr
    return linhas_estr


@loop_linhas_estr
def substituições_case_sensitive_estr(i, linhas_estr, texto_bloco_estr, número_legenda_estr):

    for termo_para_sair, termo_para_entrar in reps.set_substituições_cs:

        # se item da lista termina com pontuação
        termo_para_sair_tem_ponto = termo_para_sair[-1] in ls.lista_pontuação_com_vírgula

        # se o item da lista termina com pontuação
        if termo_para_sair_tem_ponto:
            # procurar o termo da lista no texto_bloco
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'\b{re.escape(termo_para_sair)}', texto_bloco_estr)
            )

            if encontrar_termo_para_sair_em_texto_bloco:

                # fazer substituições pegando termo se for lower, capitalizer ou upper
                texto_bloco_estr = re.sub(fr'\b{re.escape(termo_para_sair)}',
                                          termo_para_entrar, texto_bloco_estr, count=0)

        # se o item da lista não termina com pontuação
        else:
            # procurar termo da lista no texto bloco com e sem pontuação
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'\b{re.escape(termo_para_sair)}\b|'
                          fr'\b{re.escape(termo_para_sair)}[.,!?:"]',
                          texto_bloco_estr)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # fazer substituições pegando termo se for lower, capitalizer ou upper
                texto_bloco_estr = re.sub(fr'\b{re.escape(termo_para_sair)}',
                                          termo_para_entrar, texto_bloco_estr, count=0)

            # atualizar linha em 'linhas'
            linhas_estr[i + 1] = texto_bloco_estr

    return linhas_estr


@loop_linhas_estr
def substituições_sem_limite_palavra_estr(i, linhas_estr, texto_bloco_estr, número_legenda_estr):

    # loopar lista do arquivo txt
    for termo_para_sair, termo_para_entrar in reps.set_substituições_sem_limite_de_palavra_estr:
        if re.search(rf'{re.escape(termo_para_sair)}', texto_bloco_estr):
            texto_bloco_estr = (
                re.sub(rf'{re.escape(termo_para_sair)}', termo_para_entrar, texto_bloco_estr)
            )

            # atualizar linha em 'linhas'
            linhas_estr[i + 1] = texto_bloco_estr

    return linhas_estr


def remover_linhas_vazias_estr(linhas_estr):
    set_remover_linhas = set()      # Set para armazenar linhas a serem removidas.

    # Remover blocos de legenda cujo texto foi excluído por alguma das funções.
    for i, linha in enumerate(linhas_estr):

        if i + 3 < len(linhas_estr):
            # Tomar como referência o índice da linha de temporização.
            if '-->' in linhas_estr[i]:
                texto_bloco = linhas_estr[i + 1].strip()
                texto_bloco_está_vazio = texto_bloco == ''

                # Se linhas 1/2, 2/2 e 3/2 estiverem vazias, remover todo o bloco.
                if texto_bloco_está_vazio:
                    for i in range(i - 1, i + 1):
                        set_remover_linhas.add(i)

    # Redefinir linhas, excluindo as linhas que constam em 'set_remover_linhas'.
    linhas_estr = [linha for i, linha in enumerate(linhas_estr)
                   if i not in set_remover_linhas]

    return linhas_estr


lista_remover_linhas_só_tags = [r'^{\\an8}$', r'^<i>$', r'^<\/i>$', r'^<i></i>$']


@loop_linhas_estr
def remover_linhas_apenas_com_tags(i, linhas_estr, texto_bloco_estr, número_legenda_estr):
    for tag in lista_remover_linhas_só_tags:
        if re.search(tag, texto_bloco_estr.strip()):
            texto_bloco_estr = ''
            # Atualizar texto_bloco_estr em linhas_estr.
            linhas_estr[i + 1] = texto_bloco_estr
    return linhas_estr


# --------- fim das funções exclusivas da legenda estrangeira ------------ #

print('  Realizando transformações na legenda em idioma estrangeiro.')

# lista para armazenar as linhas da legenda estrangeira
linhas_estr = []

# recolher '-' dos diálogos
linhas_estr = fu.juntar_linhas_de_texto(legenda_estr, linhas_estr)

linhas_estr = fu.recolher_top_center(linhas_estr)

linhas_estr = fu.recolher_diálogos(linhas_estr)

linhas_estr = fu.remover_pontos_invertidos_espanhol(linhas_estr)

# remover closed captions
linhas_estr = fu.remover_closed_captions(linhas_estr)
linhas_estr = fu.remover_nomes_closed_captions(linhas_estr)

linhas_estr = fu.corrigir_l_I(linhas_estr)

linhas_estr = fu.corrigir_espaço_pontuação_legenda_estrangeira(linhas_estr)

if reps.remover_interjeições is True:
    # remover ah, ey, ay, etc
    linhas_estr = remover_ah_ei_ai_estr(linhas_estr)

# fazer substituições sem_limite_de_palavra
# do arquivo substituições_sem_limite_de_palavra_estrangeiro.txt
linhas_estr = substituições_sem_limite_palavra_estr(linhas_estr)

# fazer substituições case insensitive do arquivo substituições_case_insenstivie_estrangeiro.txt
linhas_estr = substituições_case_insensitive_estr(linhas_estr)

# fazer substituições case insensitive do arquivo substituições_case_senstivie_estrangeiro.txt
linhas_estr = substituições_case_sensitive_estr(linhas_estr)

if reps.remover_palavras_repetidas is True:
    linhas_estr = fu.remover_palavras_repetidas_separadas_vírgula(linhas_estr)

# remover linhas em que sobrarem apenas tags como '{\an8}' e '<i></i>'.
linhas_estr = remover_linhas_apenas_com_tags(linhas_estr)

# remover linhas que ficaram vazias depois das substituições
linhas_estr = fu.remover_linhas_vazias(linhas_estr)

linhas_estr = fu.corrigir_maiúsculas_depois_de_pontuação(linhas_estr)

linhas_estr = fu.devolver_top_center(linhas_estr)

# recontar números da legenda estrangeira
linhas_estr = fu.recontar_números(linhas_estr)

print('\n  Transformações concluídas.\n')

# Lista para pôr apenas as linhas de texto das legendas.
linhas_de_texto = []

# remover linhas com número e timestamp
for i, linha in enumerate(linhas_estr):
    if '-->' in linhas_estr[i]:

        número_legenda = linhas_estr[i - 1].strip()
        linha_de_texto = linhas_estr[i + 1].strip()
        texto_bloco = f'{número_legenda}#\noriginal: {linha_de_texto}\ntradução:\n'
        linhas_de_texto.append(texto_bloco)

cole_aqui = 'Cole a tradução aqui.'

caminho_legenda_traduzida_sem_srt = (
    os.path.join(pasta_do_script, 'cole_a_tradução_aqui.txt')
)

caminho_legenda_traduzida_sem_srt = (
    os.path.join(pasta_do_script, caminho_legenda_traduzida_sem_srt)
)
with open(caminho_legenda_traduzida_sem_srt, 'w', encoding='utf-8') as file:
    file.writelines(cole_aqui)

# Agora serão preparados blocos de 100 linhas para que sejam copiados, colados no ChatGPT
# e traduzidos por ele.

número_linhas_legenda = ''
# Detectar número de linhas.
for linha in reversed(linhas_de_texto):
    if '#' in linha:
        # Pegar apenas o número.
        número_linhas_legenda = int(linha.split('#')[0])
        break

número_de_blocos_de_100 = número_linhas_legenda // 100
resto = número_linhas_legenda % 100
lista_de_blocos_de_100 = []
lista_número_blocos = []

# Criar uma lista com os números de 1 ao número total de blocos de 100 linhas de linhas_de_texto.
for i in range(0, número_de_blocos_de_100):
    # Adicionar à lista números de bloco + 1 (para não iniciar em zero)
    lista_número_blocos.append(i + 1)

# Iterar sobre a lista com o número de blocos de 100
# e adicionar as linhas à lista_de_blocos_de_100.
for número in lista_número_blocos:
    # Variável para índice inicial.
    # Se o número for > 1, o número inicial das linhas será o número total do bloco anterior + 1.
    # Se agora é o bloco 2, a linha inicial desse bloco é a 101 e a última, 200.
    número_de_partida = número * 100 - 100
    número_máximo_do_bloco = número * 100

    bloco_atual = ''.join(linhas_de_texto[número_de_partida:número_máximo_do_bloco])
    lista_de_blocos_de_100.append(bloco_atual)

if resto > 0:
    número_de_partida = número_de_blocos_de_100 * 100
    número_máximo_do_bloco = número_de_partida + resto
    bloco_atual = '\n'.join(linhas_de_texto[número_de_partida:])
    lista_de_blocos_de_100.append(bloco_atual)

print('\n\n  Vamos abrir um arquivo .txt onde você vai colar o texto traduzido pelo ChatGPT.\n')
input('  Digite Enter para continuar.\n')
subprocess.Popen(["notepad.exe", caminho_legenda_traduzida_sem_srt])

print('  Agora vamos copiar para o seu clipboard o texto da legenda de 100 em 100 linhas.\n  '
      'Antes de colar o prompt no ChatGPT, abra um "novo chat", no topo do menu à esquerda.\n  '
      'Certifique-se de que a resposta do ChatGPT engloba todas as linhas aqui mencionadas\n  '
      'em cada passo e não remove a indicação "tradução" das linhas traduzidas.\n  '
      'Se a resposta do ChatGPT não apresentar todas as linhas, '
      'não traduzir algumas linhas \n  ou fizer algo diferente do esperado, '
      'abra um "novo chat" e cole o prompt novamente.\n')
input('  Digite Enter para continuar.\n')

for i, bloco_de_linhas in enumerate(lista_de_blocos_de_100):
    número_de_partida = ((i + 1) * 100) - 100
    número_máximo_do_bloco = ((i + 1) * 100)
    último_número_de_blocos = len(lista_de_blocos_de_100) - 1
    número_de_partida_mensagem = número_de_partida + 1

    mensagem_copiar = (
        'Traduza a seguinte legenda para para português brasileiro natural da forma mais clara, '
        'natural e resumida possível. Evite traduzir literalmente, se possível '
        'e elimine redundâncias e vícios de linguagem sem significado. '
        'Mantenha maiúsculas e minúsculas como estão. '
        'Mantenha o formato, mantenha a linha original e preencha apenas a linha "tradução". '
        'Mantenha as tags <i>, </i> e {\an8} da mesma forma, se aparecerem. '
        f'Inclua todos os números de {número_de_partida_mensagem} a {número_máximo_do_bloco}.\n\n'
    )

    mensagem_bloco_inicial = (
        f'\n\n  >> As linhas de {número_de_partida_mensagem} a {número_máximo_do_bloco}'
        ' da legenda foram copiadas para o seu clipboard.\n  Abra um "novo chat" no ChatGPT, '
        'cole este bloco de linhas e, quando a tradução terminar, '
        'cole todo o resultado no arquivo .txt.\n'
    )

    mensagem_bloco_meio = (
        f'\n\n  >> As linhas de {número_de_partida_mensagem} a {número_máximo_do_bloco}'
        ' da legenda foram copiadas para o seu clipboard.\n  Abra um "novo chat" no ChatGPT, '
        ' e repita a operação anterior.\n'
    )

    mensagem_bloco_final = (
        '\n\n  >> Agora as linhas finais da legenda foram copiadas. '
        'Abra um "novo chat" no ChatGPT e repita a operação anterior.\n'
    )

    mensagem_próximo_passo_início = (
        '    Digite:\n    >> Enter --> ir para o próximo passo\n'
        '    >> C + Enter --> copiar este bloco de linhas novamente\n'
    )

    mensagem_próximo_passo = (
        '    Digite:\n    >> Enter --> ir para o próximo passo\n'
        '    >> C + Enter --> copiar este bloco de linhas novamente\n'
    )

    só_tem_um_bloco = último_número_de_blocos == 0
    tem_mais_de_um_bloco = último_número_de_blocos != 0

    if só_tem_um_bloco:
        def bloco_único(número_de_partida_mensagem, número_máximo_do_bloco,
                        bloco_de_linhas, mensagem_copiar):

            pyperclip.copy(mensagem_copiar + bloco_de_linhas)
            print(mensagem_bloco_inicial)

            resposta = input(mensagem_próximo_passo_início)
            if resposta.lower() == 'c':
                bloco_único(número_de_partida_mensagem, número_máximo_do_bloco,
                            bloco_de_linhas, mensagem_copiar)

        bloco_único(número_de_partida_mensagem, número_máximo_do_bloco,
                    bloco_de_linhas, mensagem_copiar)

    # Se tem mais de um bloco.
    elif tem_mais_de_um_bloco:

        if i == 0:

            def bloco_inicial(número_de_partida_mensagem, número_máximo_do_bloco,
                              bloco_de_linhas, mensagem_copiar):

                pyperclip.copy(mensagem_copiar + bloco_de_linhas)
                print(mensagem_bloco_inicial)
                resposta = input(mensagem_próximo_passo_início)
                if resposta.lower() == 'c':
                    bloco_inicial(número_de_partida_mensagem, número_máximo_do_bloco,
                                  bloco_de_linhas, mensagem_copiar)

            bloco_inicial(número_de_partida_mensagem, número_máximo_do_bloco,
                          bloco_de_linhas, mensagem_copiar)

        elif i > 0 and i < último_número_de_blocos:

            def blocos_meio(número_de_partida_mensagem, número_máximo_do_bloco,
                            bloco_de_linhas, mensagem_copiar):

                pyperclip.copy(mensagem_copiar + bloco_de_linhas)
                print(mensagem_bloco_meio)
                resposta = input(mensagem_próximo_passo)

                if resposta.lower() == 'c':
                    blocos_meio(número_de_partida_mensagem, número_máximo_do_bloco,
                                bloco_de_linhas, mensagem_copiar)
            blocos_meio(número_de_partida_mensagem, número_máximo_do_bloco,
                          bloco_de_linhas, mensagem_copiar)

        # Print comunicando a cópia para o clipboard do último bloco de linhas.
        elif i == último_número_de_blocos:
            def bloco_último(resto, bloco_de_linhas, mensagem_copiar):

                pyperclip.copy(mensagem_copiar + bloco_de_linhas)
                print(mensagem_bloco_final)
                resposta = input(mensagem_próximo_passo)

                if resposta.lower() == 'c':
                    bloco_último(resto, bloco_de_linhas, mensagem_copiar)

            bloco_último(resto, bloco_de_linhas, mensagem_copiar)

print('\n  Salve o arquivo .txt')
input('  Digite Enter para o próximo passo.')

# Carregar tradução do arquivo cole_a_tradução_aqui.txt, devolver o timestamp,
# ajustar o formato e salvar em nova_legenda_pt_raw.srt
pasta_do_script = os.path.dirname(os.path.abspath(__file__))

# Carregar legenda em PT e designar variável linhas.
with open(caminho_legenda_traduzida_sem_srt, 'r',
          encoding='utf-8') as arquivo_pt_sem_srt:
    legenda_pt_sem_srt = arquivo_pt_sem_srt.readlines()

# Adicionar linhas no final do arquivo traduzido bruto para não ter problemas de índice.
três_linhas = ['n', 'n', 'n']
legenda_pt_sem_srt.extend(três_linhas)

# Preparar arquivo apenas com números e linhas da tradução.
linhas_tradução = []

for i, linha in enumerate(legenda_pt_sem_srt):

    if '#' in legenda_pt_sem_srt[i]:
        número_linha = legenda_pt_sem_srt[i].split('#')[0]
        tradução = ''
        # Determinar a linha com a tradução
        # (às vezes o ChatGPT coloca o número da legenda na mesma linha do 'original:')
        if 'tradução:' in legenda_pt_sem_srt[i] or 'Tradução:' in legenda_pt_sem_srt[i]:
            linha_tradução = legenda_pt_sem_srt[i].split('#')[1]
            tradução = linha_tradução.replace('tradução:', '')
        elif 'tradução:' in legenda_pt_sem_srt[i + 1] or 'Tradução:' in legenda_pt_sem_srt[i + 1]:
            tradução = legenda_pt_sem_srt[i + 1].replace('tradução:', '')
            tradução = tradução.replace('Tradução:', '')
        elif 'tradução:' in legenda_pt_sem_srt[i + 2] or 'Tradução:' in legenda_pt_sem_srt[i + 2]:
            tradução = legenda_pt_sem_srt[i + 2].replace('tradução:', '')
            tradução = tradução.replace('Tradução:', '')
        elif 'tradução:' in legenda_pt_sem_srt[i + 3] or 'Tradução:' in legenda_pt_sem_srt[i + 3]:
            tradução = legenda_pt_sem_srt[i + 3].replace('tradução:', '')
            tradução = tradução.replace('Tradução:', '')
        linhas_tradução.append(f'{número_linha} # {tradução}')

novo_srt_pt = []

for i, linha_pt in enumerate(linhas_tradução):
    for j, linha_estr in enumerate(linhas_estr):
        if '-->' in linhas_estr[j]:

            número_legenda_estr = linhas_estr[j - 1].strip()
            timestamp_estr = linhas_estr[j].strip()

            if '#' in linhas_tradução[i]:

                linha_pt_partes = linha_pt.split('#')
                número_pt = linha_pt_partes[0].strip()
                texto_pt = linha_pt_partes[1].strip()

                números_da_legenda_batem = número_legenda_estr == número_pt
                if números_da_legenda_batem:
                    novo_srt_pt.append(f'{número_pt}\n')
                    novo_srt_pt.append(f'{timestamp_estr}\n')
                    novo_srt_pt.append(f'{texto_pt}\n\n')

# colocar '\n' em linhas_estr
for i, linha_estr in enumerate(linhas_estr):
    if '-->' in linhas_estr[i]:

        # adicionar \n (nova linha) em:
        # número da legenda
        linhas_estr[i - 1] = f'{linhas_estr[i - 1].strip()}\n'
        # timestamp
        linhas_estr[i] = f'{linhas_estr[i].strip()}\n'
        # linha unificada de texto
        linhas_estr[i + 1] = f'{linhas_estr[i + 1].strip()}\n\n'

# adicionar linhas vazias no fim de novo_srt_pt
novo_srt_pt.append('\n\n\n\n')

# quebrar linhas do texto_bloco da legenda estrangeira
# linhas_estr = fu.quebrar_linhas_de_diálogo(linhas_estr)
# linhas_estr = fu.quebrar_linhas(linhas_estr)

# adicionar linhas vazias no fim da legenda estrangeira
linhas_estr.append('\n\n\n\n')


def salvar_srt(srt_final, título, nome_inicial):
    novo_arquivo = (
        filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")],
                                     title= título, initialfile= nome_inicial)
    )

    if novo_arquivo:
        with open(novo_arquivo, "w", encoding='utf-8') as file:
            file.writelines(srt_final)
            print(f'  Arquivo salvo com sucesso:\n  {novo_arquivo}\n\n')

    else:
        print('  Salve o arquivo .srt na janela que vamos abrir.')
        input('  Digite Enter para continuar.\n')
        salvar_srt(srt_final, título, nome_inicial)


print('\n  Foram feitos ajustes na legenda estrangeira '
      'e sua tradução para português foi realizada pelo ChatGPT.\n')

input('  Vamos salvar a legenda prévia em português.\n  Digite Enter para continuar.\n')
salvar_srt(novo_srt_pt, 'Salvar legenda provisória em português', 'legenda_prévia_português.srt')

input('  Agora vamos salvar a legenda prévia em idioma estrangeiro.\n  Digite Enter para continuar.\n')
salvar_srt(linhas_estr, 'Salvar legenda provisória estrangeira', 'legenda_prévia_estrangeira.srt')



print('  Deseja realizar agora as transformações da legenda traduzida?\n')

print('    Digite:\n    >> Enter --> continuar\n    >> X + Enter --> sair\n')
input_4 = input()

if input_4.lower() == 'x':
    print('Obrigado por usar o LEGENDA PT TURBO.\n\n')
    exit()
else:
    caminho_legenda_pt_turbo = os.path.join(pasta_funções, 'transformações_legenda_português.py')
    subprocess.run(['python', caminho_legenda_pt_turbo])
