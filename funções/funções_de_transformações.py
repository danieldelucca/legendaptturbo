import reps, listas as ls, listas_verbos as lv, listas_nomes as ln
import re
import string
import tkinter as tk
from tkinter import filedialog

set_top_center = set()
set_abrir_itálicas = set()
set_fechar_itálicas = set()
quote_start_list = []
set_diálogos = set()
set_linhas_2_esvaziadas = set()
set_FNs = set()

# Cada unidade de legenda conta com três ou quatro linhas:
# O número da legenda, o 'timestamp' e uma ou duas linhas de texto.
# Vamos chamar 'texto_bloco' as linhas de texto de cada bloco.
# A referência no script para cada bloco de legenda será a linha do timestamp.
# Que tem o tempo de início e tempo de fim de cada bloco, separados por '-->'.
# As duas linhas de texto serão unidas em uma para facilitar o trabalho de cada função.


# --------------- menu abertura dos arquivos -------------- #

# --------- funções para abrir arquivos de legenda --------- #

# Janela para selecionar arquivos de legenda.
def selecionar_arquivo_legenda(idioma):
    arquivo_selecionado = filedialog.askopenfilename(
        title=f"Abrir arquivo da legenda em {idioma}",
        filetypes=[("SubRip Files", "*.srt"), ("All Files", "*.*")]
    )

    if arquivo_selecionado:
        if idioma == 'português':
            print("  Legenda selecionada para preparação e tradução:")
        else:
            print("  Legenda em idioma estrangeiro selecionada:")
        print('    ' + arquivo_selecionado + '\n')
        # Carregar legenda estrangeira e designar variável linhas.
        with open(arquivo_selecionado, 'r', encoding='utf-8') as arquivo:
            legenda = arquivo.readlines()
    else:
        print('\n  Nenhum arquivo foi selecionado.\n')
        input('  Digite Enter para abrir de novo.\n')
        selecionar_arquivo_legenda(idioma)
    return legenda


# ------- funções de preparação da legenda para as funções ------- #


# Identificar e listar ocorrências de <i> e </i> para serem removidas
# e devolvidas no final do script.
# Isso evitará conflitos durante as funções.
def registrar_ocorrências_de_itálicas(linhas_pt):
    for i, linha in enumerate(linhas_pt):
        # Usar linha do 'timestamp' como referência de cada bloco.
        if '-->' in linhas_pt[i]:
            número_legenda = linhas_pt[i - 1].strip()
            linha_1 = linhas_pt[i + 1].strip()
            linha_2 = linhas_pt[i + 2].strip()
            # Adicionar ao set correspondente o número da legenda e a linha.
            if '<i>' in linha_1:
                set_abrir_itálicas.add((número_legenda, 1))
            if '<i>' in linha_2:
                set_abrir_itálicas.add((número_legenda, 2))

            if '</i>' in linha_1:
                set_fechar_itálicas.add((número_legenda, 1))
            if '</i>' in linha_2:
                set_fechar_itálicas.add((número_legenda, 2))

    return linhas_pt


# Criar uma nova lista sem linhas vazias
# e com as duas linhas de texto unificadas em uma só.
def juntar_linhas_de_texto(lista_de_linhas, nova_lista):
    for i, linha in enumerate(lista_de_linhas):
        if '-->' in lista_de_linhas[i]:

            número_legenda = f'{lista_de_linhas[i - 1].strip()}\n'
            temporização = f'{lista_de_linhas[i].strip()}\n'
            linha_1 = lista_de_linhas[i + 1].strip()
            linha_2 = ''
            if i + 2 < len(lista_de_linhas):
                linha_2 = lista_de_linhas[i + 2].strip()
            # Juntar as duas linhas de texto de cada legenda.
            linha_2_é_preenchida = linha_2.strip() != ''

            # Preparar diálogos trocando a segunda '-' por '/' e tirando a primeira.
            # Depois a primeira '-' será devolvida e '/' voltará a ser '-'.
            bloco_é_diálogo = linha_1.startswith('-') or linha_2.startswith('-')
            if bloco_é_diálogo:
                linha_2 = f'/ {linha_2}'

            # Vamos chamar as duas linhas juntas de texto de cada bloco de texto_bloco.
            texto_bloco = f'{linha_1} {linha_2}\n\n' if linha_2_é_preenchida else f'{linha_1}\n\n'
            # Adicionar apenas as linhas preenchidas de cada legenda.
            nova_lista.append(número_legenda)
            nova_lista.append(temporização)
            nova_lista.append(texto_bloco)

    return nova_lista


# ------- funções de limpeza das linhas que vão nos decorators a seguir ------- #

# OK.
# Remover linhas de legendas vazias, seus números, timestamps, etc.
def remover_linhas_vazias(linhas_pt):
    set_remover_linhas = set()  # Set para armazenar linhas a serem removidas.

    # Remover blocos de legenda cujo texto foi excluído por alguma das funções.
    for i, linha in enumerate(linhas_pt):

        if i + 3 < len(linhas_pt):
            # Tomar como referência o índice da linha de temporização.
            if '-->' in linhas_pt[i]:
                texto_bloco_strip = linhas_pt[i + 1].strip()
                texto_bloco_está_vazio = texto_bloco_strip == ''

                # Se linhas 1/2, 2/2 e 3/2 estiverem vazias, remover todo o bloco.
                if texto_bloco_está_vazio:
                    for i in range(i - 1, i + 2):
                        set_remover_linhas.add(i)

    # Redefinir linhas, excluindo as linhas que constam em 'set_remover_linhas'.
    linhas_pt = [linha for i, linha in enumerate(linhas_pt)
                 if i not in set_remover_linhas]

    return linhas_pt


# OK.
# Remover linha em que sobrar apenas um ponto ou '...'.
def remover_linhas_só_com_um_ponto(linhas_pt):
    for i, linha in enumerate(linhas_pt):
        if '-->' in linhas_pt[i]:
            texto_bloco = linhas_pt[i + 1]
            texto_bloco_strip = texto_bloco.strip()
            texto_bloco_só_tem_um_ponto = texto_bloco_strip in ls.lista_pontuação_com_vírgula

            if texto_bloco_só_tem_um_ponto:
                texto_bloco = ''  # Depois outra função vai apagar todo o bloco.
            # Atualizar o texto bloco em linhas_pt.
            linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK.
# Remover espaços sobrando em começo e fim de linha.
def remover_espaço_começo_fim(linhas_pt):
    for i, linha in enumerate(linhas_pt):
        if '-->' in linhas_pt[i]:
            linhas_pt[i + 1] = f'{linhas_pt[i + 1].strip()}\n\n'
    return linhas_pt


# OK.
# Adicionar três linhas no final para evitar 'index error' em algumas funções.
def pôr_linhas_no_fim(linhas_pt):
    linhas_pt += ['\n'] * 3
    return linhas_pt


# Remover '/' dos blocos de diálogo se uma das linhas do diálogo deixar de existir.
def remover_linha_vazia_de_diálogo(linhas_pt):
    for i, linha in enumerate(linhas_pt):
        # Tomar linha do timestamp como referência.
        if '-->' in linhas_pt[i]:
            texto_bloco = linhas_pt[i + 1]
            texto_bloco_é_diálogo = '/' in texto_bloco

            if texto_bloco_é_diálogo:
                linha_1_é_vazia = texto_bloco.split('/')[0].strip() == ''
                linha_2_é_vazia = texto_bloco.split('/')[1].strip() == ''
                if linha_1_é_vazia or linha_2_é_vazia:
                    texto_bloco = texto_bloco.replace('/', '')
                    texto_bloco = f'{texto_bloco.strip()}\n'
            linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# --------- início dos decorators ---------- #

# Decorator que loopa as linhas da legenda PT com os blocos de texto unificado.
def loop_legenda_pt(função_principal):
    def wrapper(legenda_pt):

        for i, linha in enumerate(legenda_pt):
            if '-->' in legenda_pt[i]:

                número_legenda = legenda_pt[i - 1].strip().strip('\ufeff')
                linha_1 = legenda_pt[i + 1].strip()
                linha_2 = legenda_pt[i + 2].strip()
                # Processar linha 1, retornando 'linhas'.
                legenda_pt = função_principal(i, legenda_pt, linha_1, linha_2, número_legenda)
                # Argumentos da função principal:
                # (i, linhas_pt, linha_1, linha_2, número_legenda).

        return legenda_pt
    return wrapper


# Decorator que loopa as linhas da legenda PT com os blocos de texto unificado.
def loop_linhas_pt(função_principal):
    def wrapper(linhas_pt):

        for i, linha in enumerate(linhas_pt):
            if '-->' in linhas_pt[i]:

                número_legenda = linhas_pt[i - 1].strip().strip('\ufeff')
                texto_bloco = linhas_pt[i + 1]
                # Processar linha 1, retornando 'linhas'.
                linhas_pt = função_principal(i, linhas_pt, texto_bloco, número_legenda)
                # Argumentos da função principal:
                # (i, linhas_pt, texto_bloco, número_legenda).

        # Funções que serão executadas a cada uso do decorator para evitar qualquer problema.
        # De indexação e na execução das próximas funções.
        linhas_pt = corrigir_dupla_pontuação(linhas_pt)
        linhas_pt = remover_linha_vazia_de_diálogo(linhas_pt)
        linhas_pt = remover_linhas_só_com_um_ponto(linhas_pt)
        linhas_pt = remover_linhas_vazias(linhas_pt)
        linhas_pt = corrigir_espaços_duplos(linhas_pt)
        linhas_pt = remover_espaço_começo_fim(linhas_pt)
        return linhas_pt
    return wrapper


# Decorator que loopa as linhas da legenda estrangeira com bloco de texto unificado.
def loop_linhas_estr(função_principal):
    def wrapper(linhas_estr):

        for i, linha_estr in enumerate(linhas_estr):
            if '-->' in linhas_estr[i]:

                número_legenda_estr = linhas_estr[i - 1].strip().strip('\ufeff')
                texto_bloco_estr = linhas_estr[i + 1]

                # Processar linha 1, retornando 'linhas'.
                linhas_estr = função_principal(
                    i, linhas_estr, texto_bloco_estr, número_legenda_estr,
                    )
                # Argumentos da função principal:
                # (i, linhas_estr, texto_bloco_estr, número_legenda_estr).

        return linhas_estr
    return wrapper


# -------- fim dos decorators ----------- #

# -------- início das funções ----------- #


# OK.
# Remover <i> e </i> temporariamente.
@loop_linhas_pt
def recolher_itálicas(i, linhas_pt, texto_bloco, número_legenda):
    texto_bloco = texto_bloco.replace('<i>', '')
    texto_bloco = texto_bloco.replace('</i>', '')
    # Atualizar texto em linhas_pt.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK.
# Identificar e listar legendas FN (aquelas em caixa alta traduzindo textos da tela).
@loop_linhas_pt
def listar_FNs(i, linhas_pt, texto_bloco, número_legenda):

    # Achar linhas sem minúsculas na linha 1.
    if re.search(r'^[^a-záàâçéêíóú]+$', texto_bloco):
        palavras = texto_bloco.split()  # Dividir linha em palavras.
        mais_que_uma_plv = len(palavras) > 1
        só_uma_plv = len(palavras) == 1
        palavra_1_mais_que_2_caracteres = len(palavras[0]) > 2

        # Se encontrar palavras totalmente maiúsculas, adicionar número da legenda ao set.
        if mais_que_uma_plv:
            set_FNs.add(número_legenda)

        # Para evitar que pegue 'E...'.
        elif só_uma_plv and palavra_1_mais_que_2_caracteres > 2:
            set_FNs.add(número_legenda)

    return linhas_pt


# Corrige espaços antes de pontos na legenda estrangeira.
@loop_linhas_estr
def corrigir_espaço_pontuação_legenda_estrangeira(i, linhas_estr,
                                                  texto_bloco_estr, número_legenda_estr):

    for ponto in {'.', '?', '!', ':', '¨'}:
        texto_bloco_estr = texto_bloco_estr.replace(f' {ponto}', f'{ponto}')
        # Atualizar texto_bloco em 'linhas_estr'.
        linhas_estr[i + 1] = texto_bloco_estr
    return linhas_estr


# Corrige espaços antes de pontos na legenda PT.
@loop_linhas_pt
def corrigir_espaço_pontuação_legenda_pt(i, linhas_pt, texto_bloco, número_legenda):

    for ponto in {'.', '?', '!', ':', '¨'}:
        texto_bloco = texto_bloco.replace(f' {ponto}', f'{ponto}')
        linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK.
# Trocar l por I em palavras totalmente maiúsculas (legendas FN).
# RlTMO -> RITMO.
@loop_linhas_pt
def corrigir_l_I(i, linhas_pt, texto_bloco, número_legenda):

    # Definir padrões regex de palavras maiúsculas com l em vez de I.
    padrões = [r'[A-Z][l][A-Z]', r'[A-Z][l]$', r'^[l][A-Z]']

    for padrão in padrões:
        # Procurar os padrões nas linhas de texto.
        if re.search(padrão, texto_bloco):
            # Dividir linha em palavras.
            palavras = texto_bloco.split()  # Dividir linha em palavras.
            # Procurar palavra com o padrão e substituir l -> I.
            for j, palavra in enumerate(palavras):
                palavra_sem_pto = palavras[j].strip(string.punctuation)
                if re.search(padrão, palavra_sem_pto):
                    palavras[j] = re.sub('l', 'I', palavras[j])
            # Atualizar texto_bloco.
            texto_bloco = f"{' '.join(palavras).strip()}\n"
            # Atualizar linha atual em 'linhas'.
            linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# Remover closed captions: [pássaros cantando].
@loop_linhas_pt
def remover_closed_captions(i, linhas_pt, texto_bloco, número_legenda):

    # Padrões para encontrar '[...]', '[...' ou '...]'.
    tags = [r'\[(.*?)\]', r'\((.*?)\)']
    # Achar e remover tag de closed caption na linha.
    for tag in tags:
        if re.search(tag, texto_bloco):
            texto_bloco = re.sub(tag, '', texto_bloco).strip()
            # Tirar espaço de antes dos ':', se houver.
            texto_bloco = texto_bloco.replace(' :', ':')

    # Atualizar texto_bloco em linhas_pt.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# Registrar e recolher diálogos.
# Na função 'juntar_linhas_de_texto', que unifica as linhas de texto,.
# Foram identificadas as '-' e a segunda transformada em '/'.
# Esta função vai remover '-' das linhas e deixar apenas '/'.
@loop_linhas_pt
def recolher_diálogos(i, linhas_pt, texto_bloco, número_legenda):

    # Ver se há outras ocorrências de diálogos com '-' no meio da linha.
    diálogo_ainda_não_detectado = '/' not in texto_bloco

    if diálogo_ainda_não_detectado:
        # Procurar '-' sem ser no começo da linha.
        if ' -' in texto_bloco[1:]:
            texto_bloco = texto_bloco.replace(' -', ' / ')

    legenda_é_diálogo = '/' in texto_bloco

    if legenda_é_diálogo:
        texto_bloco = texto_bloco.strip()
        texto_bloco = texto_bloco.replace(' -', ' ')
        if texto_bloco.startswith('-'):
            texto_bloco = texto_bloco[1:]

        # Registrar no set o número da legenda.
        set_diálogos.add(número_legenda)

    # Devolver '-' às ênclises (-me, -lhe, -a, -o, etc) e interjeições 'mm-hum'.
    oblíquos = {
        'a', 'as', 'o', 'os', 'lhe', 'lo', 'la', 'me', 'nas', 'nos', 'se', 'uh', 'hm', 'hum'
        }

    # Substituir /me --> -me, etc.
    for oblíquo in oblíquos:
        texto_bloco = texto_bloco.replace(f'/{oblíquo}', f'-{oblíquo}')

    # Atualizar texto em linhas_pt.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK.
# Tirar nomes dos personagens de antes das falas: DAVID: Onde estou?.
@loop_linhas_pt
def remover_nomes_closed_captions(i, linhas_pt, texto_bloco, número_legenda):

    # Procurar padrão.
    # Ver quantas tags há, se houver duas, trocar por diálogo, se já não estiver.
    # Pôr na lista de diálogos, se for o caso.

    if número_legenda not in set_FNs:
        # Padrões de palavras em caixa alta seguidas de ':'.
        padrão = (r'(?:^|\b)(?:[A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ0-9]+\s)*'
                  r'[A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ0-9]+(?:\s[A-ZÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ0-9]+)*'
                  r'\b(?::(?:\s|$))')

        # Procurar ocorrências de tags cc com nomes na linha 1.
        encontrar_nomes_cc = re.findall(padrão, texto_bloco)

        if encontrar_nomes_cc:

            número_de_nomes_cc = len(encontrar_nomes_cc)

            # Se há apenas um nome CC na primeira linha.
            if número_de_nomes_cc == 1:
                texto_bloco = re.sub(padrão, '', texto_bloco)

            # Se há dois nomes CC na primeira linha, trocar por '-' para virar diálogo.
            elif número_de_nomes_cc == 2:
                # Atualizar texto_bloco.
                texto_bloco = re.sub(padrão, '-', texto_bloco)

        # Atualizar texto_bloco em linhas_pt.
        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


@loop_linhas_pt
def remover_pontos_invertidos_espanhol(i, linhas_pt, texto_bloco, número_legenda):
    # Remover caracteres de texto_bloco.
    texto_bloco = texto_bloco.replace('¡', '').replace('¿', '')
    # Atualizar texto_bloco em 'linhas'.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# Recolher {\an8} temporariamente.
@loop_linhas_pt
def recolher_top_center(i, linhas_pt, texto_bloco, número_legenda):

    # Achar {\an8} na linha 1.
    if re.search(r'\{\\an8\}', texto_bloco):
        # Adicionar número ao set_top_center.
        set_top_center.add(número_legenda)
        # Remover {\an8} da linha 1.
        linhas_pt[i + 1] = re.sub(r'\{\\an8\}', '', texto_bloco)

    return linhas_pt


set_nomes = set()
set_original_capitalizadas = set()
lista_titulos = ['Sr.', 'Sr', 'Sra.', 'Sra', 'Mr.', 'Mr',
                 'Mrs.', 'Mrs', 'Miss', 'Ms.', 'Ms', 'Dr.']


# Detectar e guardar nomes próprios, reverter traduções indevidas de nomes.
# (e adicionar artigos, numa função futura).
def nomes_próprios(linhas_pt, linhas_estr):
    # Pegar todas as palavras capitalizadas da legenda original.
    # (exceto as do set_exceções)
    # Entre elas estarão os nomes dos personagens.
    @loop_linhas_estr
    def pegar_palavras_capitalizadas_do_original(
            i, linhas_estr, texto_bloco_estr, número_legenda_estr):

        set_remover_original = {
            '{\an8}', '-', '<i>', '</i>', '"', "'m", "'s", "'re", "'ve", "'d", "'ll", "|"
            }
        set_exceções = {  # Inglês.
                        'A', 'Actually', 'All', 'Alright', 'Although', 'And',
                        'Are', "Aren't", 'As', 'At', 'But', 'Can', "Can't",
                        'Did', "Didn't", 'Do', 'Does', "Doesn't", "Don't",
                        'Excuse', 'For', 'Good', 'Great', 'He', 'Hello',
                        'Hey', 'Her', 'Here', 'Hi', 'His', 'How', 'I', 'If',
                        'In', 'Is', 'It', 'Let', 'Look', 'Must', 'My', 'No',
                        'Not', 'Of', 'Okay', 'On', 'Our', 'Right', 'She',
                        'Should', "Shouldn't", 'Since', 'So', 'Sure', 'Thank',
                        'Thanks', 'That', 'The', 'Their', 'They', 'This',
                        'To', 'We', 'Well', 'What', 'When', 'Where', 'Who',
                        'Why', 'Will', "Won't", 'Would', "Wouldn't", 'Yeah',
                        'Yes', 'You',
                        # Espanhol.
                        'Aunque', 'Como', 'Con', 'Cual', 'Cuando', 'Él',
                        'Ella', 'Ellas', 'Ellos', 'El', 'Gracias', 'La',
                        'Las', 'Los', 'Mi', 'Muchas', 'No', 'Nosotros',
                        'Para', 'Pero', 'Por', 'Quien', 'Quienes', 'Si',
                        'Su', 'Todavía', 'Un', 'Una', 'Yo'}

        # Criar cópia do texto_bloco_estr para remover as tags.
        texto_bloco_estr_cópia = texto_bloco_estr
        # Remover as tags do set_remover_original do texto_bloco_estr.
        for tag in set_remover_original:
            texto_bloco_estr_cópia = texto_bloco_estr_cópia.replace(tag, '')

        # Dividir linha atual em palavras.
        palavras = texto_bloco_estr_cópia.split()  # Dividir linha atual em palavras.
        for j, palavra in enumerate(palavras):

            palavra_sem_ponto = palavras[j].strip(string.punctuation)
            # Evitar que a palavra seja toda upper.
            palavra_tem_letras = re.search(r'^[A-ZÁÉÍÓÚÇÊÂa-záéíóúâê]+$', palavra_sem_ponto)
            índice_próxima_palavra = j + 1
            palavra_não_está_nas_exceções = palavra_sem_ponto not in set_exceções

            # Filtrar palavras com inicial maiúscula, os nomes serão separados depois.
            # Set_exceções - evita captar palavras comuns em começos de frases.
            # Apenas para diminuir um pouco a incidência de não-nomes nessa lista.
            if palavra_tem_letras:

                palavra_é_capitalized = (
                    palavra_sem_ponto[0].isupper() and palavra_sem_ponto[1:].islower()
                )

                if palavra_é_capitalized and palavra_não_está_nas_exceções:

                    # Adicionar ao set.
                    set_original_capitalizadas.add(
                        (palavra_sem_ponto, número_legenda_estr)
                        )

                    if índice_próxima_palavra < len(palavras):

                        palavra_atual_não_tem_ponto = palavras[j] == palavra_sem_ponto
                        próxima_palavra_sem_ponto = palavras[j + 1].strip(string.punctuation)
                        próxima_palavra_começa_com_maiúscula = palavras[j + 1][0].isupper()
                        duas_palavras_seguidas_são_capitalized = (
                            palavra_atual_não_tem_ponto and próxima_palavra_começa_com_maiúscula
                        )

                        if duas_palavras_seguidas_são_capitalized:
                            set_original_capitalizadas.add(
                                (f'{palavra_sem_ponto} {próxima_palavra_sem_ponto}',
                                 número_legenda_estr)
                                )
        return linhas_estr

    pegar_palavras_capitalizadas_do_original(linhas_estr)

    # Reverter tradução de nomes (Carlos -> Charles, Cíntia -> Cynthia).
    @loop_linhas_pt
    def reverter_traduções_indevidas_de_nomes(i, linhas_pt, texto_bloco, número_legenda):

        for maiúscula_original, número in set_original_capitalizadas:
            # Encontrar número da legenda e nome no PT.
            if número_legenda == número:
                # Consultar lista de nomes traduzidos.
                for nome_estrangeiro, nome_traduzido in ln.traduções_nomes:
                    # Encontrar nome traduzido na legenda PT.

                    nome_traduzido_no_texto_bloco = (
                        re.search(fr'\b{nome_traduzido}[.,?!:]|\b{nome_traduzido}\b',
                                  texto_bloco, re.IGNORECASE)
                        )

                    if nome_traduzido_no_texto_bloco:

                        # Dividir linha atual em palavras.
                        palavras = texto_bloco.split()
                        # Loopar as palavras da linha.
                        for j, plv in enumerate(palavras):
                            plv_atual = palavras[j].strip(string.punctuation)
                            nome_traduzido_minúsculo = nome_traduzido.lower()
                            # Se a palavra maiúscula da legenda original.
                            # Que está na lista estiver na lista de nomes estrangeiros.
                            if maiúscula_original == nome_estrangeiro:

                                # Se a palavra atual do loop maiúscula ou minúscula estiver.
                                # Na lista de nomes traduzidos.
                                if plv_atual == nome_traduzido \
                                        or plv_atual == nome_traduzido_minúsculo:
                                    # Mudar a palavra de nome traduzido.
                                    # Para o nome equivalente estrangeiro.
                                    # (Carlos -> Charles, Cíntia -> Cynthia).
                                    palavras[j] = palavras[j].replace(plv_atual, nome_estrangeiro)
                                    # Atualizar linha.
                                    linhas_pt[i + 1] = f"{' '.join(palavras).strip()}\n"

        return linhas_pt
    linhas_pt = reverter_traduções_indevidas_de_nomes(linhas_pt)
    return linhas_pt


@loop_linhas_pt
def corrigir_linha_apenas_com_eu(i, linhas_pt, texto_bloco, número_legenda):
    if texto_bloco.strip() == 'EU...':
        texto_bloco = texto_bloco.replace('EU...', 'Eu...')

    # Atualizar linha em 'linhas'.
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# Remover linhas com coisas como créditos ('legenda por:), etc.
# Specs.txt.
@loop_linhas_pt
def remover_linhas_com_créditos_e_outros(i, linhas_pt, texto_bloco, número_legenda):

    # Se item da lista estiver na linha.
    for item in reps.lista_remover_linhas_com:
        if item in texto_bloco:
            linhas_pt[i + 1] = '\n'  # Esvaziar a linha.
    # A função remover_linhas_vazias do decorator irá remover.
    # Possíveis linhas vazias que sobrarem.
    return linhas_pt


lista_de_traduções_específicas = []


def traduções_específicas_de_frases(linhas_pt, linhas_estr):

    @loop_linhas_estr
    def achar_frase_no_original(i, linhas_estr, texto_bloco_estr, número_legenda_estr):

        remover_original = {'{\an8}', '- ', '-', '<i>', '</i>', '\n', '"'}
        # Criar uma cópia do texto_bloco para remover as tags.
        texto_bloco_cópia = texto_bloco_estr

        # If i + 3 < len(linhas_estr):
        # Remover tags da cópia da linha do original.
        for item in remover_original:
            texto_bloco_cópia = texto_bloco_cópia.replace(item, '')

        # Procurar termos e frases da lista case sensitive de trad_especiais.txt.
        for frase_original, frase_traduzida in reps.set_trad_esp_frases:
            # Pegar número da legenda e da linha e outras informações sobre a linha original.
            if frase_original in texto_bloco_cópia:
                palavras = texto_bloco_cópia.split()  # Dividir texto_bloco em palavras.

                for j, plv in enumerate(palavras):

                    palavra_anterior = palavras[j - 1]
                    pontuação_palavra_anterior = palavra_anterior[-1]
                    pontuação_depois = frase_original[-1]
                    posição_final = ''

                    primeira_palavra_frase_original = frase_original.split()[0]
                    última_palavra_frase_original = frase_original.split()[-1]
                    última_palavra_da_linha = texto_bloco_cópia.split()[-1]

                    frase_termina_no_fim_da_linha = (
                        última_palavra_frase_original == última_palavra_da_linha
                    )

                    frase_original_split = frase_original.split()
                    número_palavras_frase_original = len(frase_original_split)

                    if número_palavras_frase_original == 1:
                        if palavras[j] == primeira_palavra_frase_original:
                            # Detectar a posição exata da frase na linha,.
                            # Caso haja incongruências na versão traduzida.
                            posição_final = 'fim' if frase_termina_no_fim_da_linha else 'meio'

                            # Se palavra atual for primeira da linha.
                            if j == 0:
                                lista_de_traduções_específicas.append(
                                    (número_legenda_estr,
                                     None,
                                     pontuação_depois,
                                     posição_final,
                                     frase_traduzida)
                                    )
                            # Se palavra atual não for primeira, detectar a pontuação anterior.
                            else:
                                lista_de_traduções_específicas.append(
                                    (número_legenda_estr,
                                     pontuação_palavra_anterior,
                                     pontuação_depois,
                                     posição_final,
                                     frase_traduzida)
                                    )

                    elif número_palavras_frase_original > 1:

                        segunda_palavra_frase_original = frase_original.split()[1]

                        if palavras[j] == primeira_palavra_frase_original \
                                and palavras[j + 1] == segunda_palavra_frase_original:

                            posição_final = 'fim' if frase_termina_no_fim_da_linha else 'meio'

                            # Se palavra atual for primeira da linha.
                            if j == 0:
                                lista_de_traduções_específicas.append(
                                    (número_legenda_estr,
                                     None,
                                     pontuação_depois,
                                     posição_final,
                                     frase_traduzida)
                                    )
                            # Se palavra atual não for primeira, detectar a pontuação anterior.
                            else:
                                lista_de_traduções_específicas.append(
                                    (número_legenda_estr,
                                     pontuação_palavra_anterior,
                                     pontuação_depois,
                                     posição_final,
                                     frase_traduzida)
                                    )
        return linhas_estr
    achar_frase_no_original(linhas_estr)

    @loop_linhas_pt
    def aplicar_traduções_específicas(i, linhas_pt, texto_bloco, número_legenda):

        # Procurar no set_traduções específicas as legendas com traduções específicas.
        for legenda_trad_específica, ponto_anterior, \
                ponto_final, posição_final, frase_traduzida \
                in lista_de_traduções_específicas:

            index_ponto_final = len(texto_bloco)

            if legenda_trad_específica == número_legenda:
                primeira_parte_linha = ''
                segunda_parte_linha = ''

                # Se a frase está no começo da linha.
                if ponto_anterior is None:
                    index_ponto_final = texto_bloco.find(ponto_final) + 1
                    segunda_parte_linha = texto_bloco[index_ponto_final:]

                    # Atualizar linha atual.
                    texto_bloco = f'{frase_traduzida} {segunda_parte_linha}'
                    # # Atualizar linha em 'linhas'.
                    linhas_pt[i + 1] = texto_bloco

                # Se a frase começar no meio da linha, depois de ponto.
                else:

                    # Detectar índice do ponto anterior.
                    # (+ 1 para excluir também o ponto ao fazer o 'slice' da linha).
                    index_ponto_anterior = texto_bloco.find(ponto_anterior)
                    primeira_parte_linha = texto_bloco[:index_ponto_anterior + 1]

                    # Descobrir o índice do ponto final contando a partir do ponto anterior.
                    index_ponto_final_menos_anterior = (
                        texto_bloco[index_ponto_anterior + 1:].find(ponto_final)
                    )

                    index_ponto_final = (
                        index_ponto_final_menos_anterior + index_ponto_anterior + 1
                    )

                    segunda_parte_linha = texto_bloco[index_ponto_final + 1:]

                    # Atualizar linha atual.
                    texto_bloco = (
                        f'{primeira_parte_linha} {frase_traduzida} {segunda_parte_linha}'
                    )
                    # Atualizar linha em 'linhas'.
                    linhas_pt[i + 1] = texto_bloco

        return linhas_pt

    linhas_pt = aplicar_traduções_específicas(linhas_pt)

    return linhas_pt


# Faz substituições específicas listadas no arquivo configurar.txt.
@loop_linhas_pt
def substituições_específicas(i, linhas_pt, texto_bloco, número_legenda):

    # Loopar lista do txt.
    for termo_para_sair, termo_para_entrar in reps.set_substituições_específicas:

        if re.search(fr'\b{re.escape(termo_para_sair)}\b', texto_bloco):
            linhas_pt[i + 1] = (
                re.sub(fr'\b{re.escape(termo_para_sair)}\b', termo_para_entrar, texto_bloco)
            )

    return linhas_pt


# OK.
# Arrumar dupla pontuação .. ?? !! ,, --.
def corrigir_dupla_pontuação(linhas_pt):
    for i, linha in enumerate(linhas_pt):
        linhas_pt[i] = re.sub(r'\b(\w+)\.\.(?!\.)', r'\1.', linhas_pt[i], count=0)  # ..
        linhas_pt[i] = re.sub(r'\?\?', '?', linhas_pt[i], count=0)  # ??
        linhas_pt[i] = re.sub(r'!!', '!', linhas_pt[i], count=0)  # !!
        linhas_pt[i] = re.sub(r',,', ',', linhas_pt[i], count=0)  # ,,
        linhas_pt[i] = re.sub(r'^--', '-', linhas_pt[i], count=0)  # -- em começo de frase
        linhas_pt[i] = linhas_pt[i].replace(' ,', ',')  # ' ,'
        linhas_pt[i] = linhas_pt[i].replace(' .', '.')  # ' .'
        linhas_pt[i] = linhas_pt[i].replace(' !', '!')  # ' !'
        linhas_pt[i] = linhas_pt[i].replace(' ?', '?')  # ' ?'
        linhas_pt[i] = linhas_pt[i].replace(',!', '!')  # ',!'
        linhas_pt[i] = linhas_pt[i].replace(',.', '.')  # ',!'
    return linhas_pt


# OK.
# Arrumar espaços duplos.
def corrigir_espaços_duplos(linhas_pt):
    for i, linha in enumerate(linhas_pt):
        linhas_pt[i] = re.sub('  ', ' ', linhas_pt[i])

    return linhas_pt


# OK.
# Ajude-me --> Me ajude.
# Pronome_depois é o que fica depois do verbo: -lhe Entreguei-lhe.
# Pronome_antes vai ficar antes do verbo: -te Te entreguei.
def pronomes_oblíquos_para_antes(linhas_pt):

    def oblíquo_para_antes(linhas_pt, pronome_depois, pronome_antes):
        for i, linha in enumerate(linhas_pt):
            if '-->' in linhas_pt[i]:

                texto_bloco = linhas_pt[i + 1]
                if '-' in texto_bloco:
                    palavras = texto_bloco.split()  # Dividir linha em palavras.
                    for j, palavra in enumerate(palavras):

                        # Procurar verbo com oblíquo (amo-te) na palavra atual do loop.
                        encontrar_verbo_com_oblíquo = re.search(fr'-{pronome_depois}\b', palavra)

                        if encontrar_verbo_com_oblíquo:

                            capitalizar = True if palavra[0].isupper() else False

                            # Remover '-' e pronome oblíquo de depois do verbo.
                            palavra = palavra.replace(f'-{pronome_depois}', '')
                            palavra = palavra.replace(f'{palavra}', f'{pronome_antes} {palavra}')
                            # Tornar pronome antes do verbo maiúsculo, se necessário.
                            palavra = palavra.capitalize() if capitalizar is True else palavra

                            # Atualizar palavra em 'palavras'.
                            palavras[j] = palavra

                    # Atualizar texto_bloco.
                    texto_bloco = f"{' '.join(palavras).strip()}\n"
                    # Atualizar linha em 'linhas'.
                    linhas_pt[i + 1] = texto_bloco

        return linhas_pt

    linhas_pt = oblíquo_para_antes(linhas_pt, 'me', 'me')
    linhas_pt = oblíquo_para_antes(linhas_pt, 'lhe', 'te')
    # Atenção! - o pronome lhe pode se referir à terceira pessoa.
    linhas_pt = oblíquo_para_antes(linhas_pt, 'te', 'te')

    # OK.
    # Torna-se --> se torna (exceto em começo de frase, por causa dos imperativos).
    def oblíquo_para_antes_sem_imperativo(linhas_pt, pronome_depois, pronome_antes):
        for i, linha in enumerate(linhas_pt):
            if '-->' in linhas_pt[i]:

                texto_bloco = linhas_pt[i + 1].strip()
                if '-' in texto_bloco:
                    palavras = texto_bloco.split()  # Dividir linha em palavras.

                    for j, palavra in enumerate(palavras):

                        encontrar_verbo_com_oblíquo = (
                            re.search(fr'-{pronome_depois}\b', palavras[j])
                        )

                        # Se a palavra for minúscula (evita começo de frases).
                        if palavras[j].islower() and encontrar_verbo_com_oblíquo:
                            existe_palavra_antes = j - 1 > -1

                            if existe_palavra_antes:

                                não_há_vírgula_antes = palavras[j - 1][-1] != ','

                                if não_há_vírgula_antes:

                                    # Substituir verbo + oblíquo por oblíquo + verbo.
                                    # Disse-lhe ---> lhe disse.
                                    palavra = palavra.replace(f'-{pronome_depois}', '')
                                    palavra = palavra.replace(
                                        f'{palavra}', f'{pronome_antes} {palavra}'
                                        )
                                    # Atualizar palavra em 'palavras'.
                                    palavras[j] = palavra
                                    # Atualizar texto_bloco.
                                    texto_bloco = f"{' '.join(palavras).strip()}\n"
                                    # Atualizar linha em 'linhas'.
                                    linhas_pt[i + 1] = texto_bloco
        return linhas_pt

    # OK.
    # 'banhou-se' --> 'se banhou'.
    # Não muda no imperativo: "Comporte-se." permanece como está.
    linhas_pt = oblíquo_para_antes_sem_imperativo(linhas_pt, 'nos', 'nos')
    linhas_pt = oblíquo_para_antes_sem_imperativo(linhas_pt, 'o', 'o')
    linhas_pt = oblíquo_para_antes_sem_imperativo(linhas_pt, 'a', 'a')
    linhas_pt = oblíquo_para_antes_sem_imperativo(linhas_pt, 'os', 'os')
    linhas_pt = oblíquo_para_antes_sem_imperativo(linhas_pt, 'as', 'as')
    linhas_pt = oblíquo_para_antes_sem_imperativo(linhas_pt, 'se', 'se')

    return linhas_pt


# OK.
# Remover interjeições como ah, ei, eh, hum, etc.
@loop_linhas_pt
def remover_ah_ei_ai(i, linhas_pt, texto_bloco, número_legenda):

    for interjeição in reps.set_ah_ai_ei_pt:
        if re.search(rf'\b{interjeição}', texto_bloco, re.IGNORECASE):
            palavras = texto_bloco.split()

            for j, plv in enumerate(palavras):  # Dividir linha atual em palavras.

                palavra_atual = palavras[j]
                palavra_atual_é_interjeição = (
                    palavra_atual.lower().strip(string.punctuation) in reps.set_ah_ai_ei_pt
                )

                if palavra_atual_é_interjeição:
                    # Remover palavra atual.
                    palavra_atual = ''
                    # Atualizar palavra em 'palavras'.
                    palavras[j] = palavra_atual
                    # Atualizar texto_bloco.
                    texto_bloco = ' '.join(palavras)
                    # Atualizar texto_bloco em 'linhas_pt'.
                    linhas_pt[i + 1] = texto_bloco
                    # Se for necessário, outra função, que está no decorator,.
                    # Vai transformar a próxima palavra em maiúscula.
    return linhas_pt


# OK.
# Adoro você ---> te adoro / amo você ---> te amo / odeio você ---> te odeio.
@loop_linhas_pt
def transformar_você_em_te(i, linhas_pt, texto_bloco, número_legenda):

    if re.search(r'(?<!^[.,!?:]) você\b|\bvocê[.,!?:]', texto_bloco):

        palavras = texto_bloco.split()  # Dividir linha em palavras.
        for j, plv in enumerate(palavras):
            if j + 1 < len(palavras):
                palavra_atual = palavras[j]
                próxima_palavra = palavras[j + 1]

                você_é_próxima_palavra = re.search(r'você[.!?:,]|você\b', próxima_palavra)

                if você_é_próxima_palavra:

                    palavra_atual_não_está_nas_exceções = (
                        not palavra_atual.lower() in ls.set_exceções_antes_você
                    )
                    palavra_atual_não_termina_com_ponto = (
                        not palavra_atual.endswith((',', '.', '?', '!', ':', '¨'))
                    )

                    if palavra_atual_não_está_nas_exceções and palavra_atual_não_termina_com_ponto:

                        palavra_atual_é_verbo_trans_direto = (
                            palavra_atual.lower()
                            in lv.set_de_verbos_transitivos_diretos_conjugados
                            )

                        if palavra_atual_é_verbo_trans_direto:

                            palavra_verbo = palavra_atual
                            palavra_você = próxima_palavra
                            ponto = (
                                palavra_você[-1]
                                if palavra_você[-1] in ls.lista_pontuação_com_vírgula
                                else ''
                            )

                            palavra_verbo = (
                                palavra_verbo.replace(palavra_verbo.capitalize(),
                                                      f'Te {palavra_verbo.lower()}{ponto}')
                            )
                            palavra_verbo = (
                                palavra_verbo.replace(palavra_verbo.lower(),
                                                      f'te {palavra_verbo.lower()}{ponto}')
                            )

                            # Atualizar palavras.
                            palavras[j] = palavra_verbo
                            # Remover.
                            palavras[j + 1] = ''
                            # Atualizar linha atual.
                            texto_bloco = f"{' '.join(palavras).strip()}\n"

    # Atualizar linha em 'linhas'.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK.
# Remover ... do começo.
@loop_linhas_pt
def remover_reticências_começo(i, linhas_pt, texto_bloco, número_legenda):
    linhas_pt[i + 1] = re.sub(r'^\¨', '', texto_bloco)
    return linhas_pt


# OK.
# Remover ... do fim.
@loop_linhas_pt
def remover_reticências_fim(i, linhas_pt, texto_bloco, número_legenda):
    # As '...' foram substituídas por '¨' (trema).
    # Ver se texto_bloco termina com '¨'.
    texto_bloco_strip = texto_bloco.strip()

    if re.search(r'\¨$', texto_bloco_strip):
        # Remover '...' do fim do texto_bloco.
        texto_bloco = re.sub(r'\¨$', '', texto_bloco_strip) + '\n'
        # Atualizar linha em linhas_pt.
        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


@loop_linhas_pt
def transformar_reticências_em_dois_hífens(i, linhas_pt, texto_bloco, número_legenda):

    texto_bloco = texto_bloco.replace('¨', '--')
    # Atualizar linha em linhas_pt.
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# Separar palavras iguais separadas por ','.
@loop_linhas_pt
def remover_palavras_repetidas_separadas_vírgula(i, linhas_pt, texto_bloco, número_legenda):

    # Padrão em regex para achar palavras iguais separadas por ','.
    padrão = r'(\b\w+\b), \1'
    encontrar_palavras_repetidas_sep_vírgula = (
        re.search(padrão, texto_bloco, re.IGNORECASE)
    )

    if encontrar_palavras_repetidas_sep_vírgula:
        deletar_índice = []
        # Dividir linha em palavras.
        palavras = texto_bloco.split()
        for j, plv in enumerate(palavras):
            # Excluir última palavra da iteração para não dar erro de índice.
            if j + 1 < len(palavras):
                palavra_atual = palavras[j].lower().strip(string.punctuation)
                próxima_palavra = palavras[j + 1].lower().strip(string.punctuation)
                if plv.endswith(',') and palavra_atual == próxima_palavra:
                    if 'não' not in plv and 'sim' not in plv:
                        # Guardar índice da palavra atual para excluir em seguida.
                        # Se for maiúscula, será corrigida por uma função futura.
                        deletar_índice.append(j)
        # Excluir palavras dos índices guardados na lista.
        for número in reversed(deletar_índice):
            del palavras[número]

        # Atualizar texto_bloco.
        texto_bloco = ' '.join(palavras)
        # Atualizar linha em linhas_pt.
        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# Se houver a mesma frase repetida, remover a primeira.
@loop_linhas_pt
def remover_frase_repetida_do_mesmo_bloco(i, linhas_pt, texto_bloco, número_legenda):
    # Procurar pontos na linha para achar pontos iguais seguidos.
    # Incluir '/' para excluir a quebra de linha.
    encontrar_pontos = re.findall(r'[.,?!/]', texto_bloco)
    # Criar lista de pontos e índices dos pontos.
    # Uma primeira tupla foi adicionada com o valor -1 no lugar do índice,.
    # Para que ocorra um slice de texto_bloco partindo do índice 0 (será somado 1), se precisar.
    pontos_e_índices = [-1]
    if encontrar_pontos:
        número_de_pontos = len(encontrar_pontos)
        linha_tem_mais_de_um_ponto = número_de_pontos > 1
        remover_índices = []
        if linha_tem_mais_de_um_ponto:
            palavras = texto_bloco.split()  # Dividir texto_bloco em palavras.

            for j, plv in enumerate(palavras):
                if plv.endswith(('.', ',', '!', '?', '¨')):
                    pontos_e_índices.append(j)

            for k, índice in enumerate(pontos_e_índices):
                # Evitar erro de índice.
                if k + 2 < len(pontos_e_índices):

                    # Determinar índices dos pontos (início e fim das frases).
                    # Somar 1 para o slice incluir palavras[0]
                    # e incluir as outras palavras iniciais.
                    # (depois de pontos) e finais (que terminam com ponto).

                    índice_inicial_1 = pontos_e_índices[k] + 1
                    índice_final_1 = pontos_e_índices[k + 1] + 1

                    índice_inicial_2 = pontos_e_índices[k + 1] + 1
                    índice_final_2 = pontos_e_índices[k + 2] + 1

                    frase_atual = list(map(str.lower, palavras[índice_inicial_1:índice_final_1]))
                    próxima_frase = list(map(str.lower, palavras[índice_inicial_2:índice_final_2]))
                    if frase_atual == próxima_frase:
                        remover_índices.append((índice_inicial_1, índice_final_1))

            for índice_inicial, índice_final in remover_índices:
                del palavras[índice_inicial + 1:índice_final + 1]
            # Atualizar texto_bloco.
            texto_bloco = ' '.join(palavras)
            # Atualizar linha em linhas_pt.
            linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK
# Estava a fazer --> estava fazendo.
@loop_linhas_pt
def transformar_gerúndio_português_em_brasileiro(i, linhas_pt, texto_bloco, número_legenda):
    palavras = texto_bloco.split()
    índice_começar_busca = ''
    índice_parar_busca = ''
    for j, plv in enumerate(palavras[:-2]):

        palavra_atual = palavras[j]
        palavra_dois = palavras[j + 1]
        palavra_três = palavras[j + 2].strip(string.punctuation)

        palavra_atual_é_verbo_estar = palavra_atual[:3].lower() == 'est'
        palavra_três_é_infinitivo = palavra_três in lv.set_verbos_no_infinitivo

        if palavra_atual_é_verbo_estar and palavra_dois == 'a' and palavra_três_é_infinitivo:
            índice_começar_busca = j
            # Procurar mais verbos.
            # Detectar ponto ou palavra na frase para parar de procurar verbos.

    if índice_começar_busca != '':
        for j, plv in enumerate(palavras[índice_começar_busca:], start=índice_começar_busca):
            if plv.endswith(('.', '!', ':', '?')):
                índice_parar_busca = j + 1
            elif plv in ['para', 'que', 'porque', 'mas']:
                índice_parar_busca = j + 1

        for j, plv in enumerate(palavras[índice_começar_busca:índice_parar_busca]):
            palavra_sem_ponto = plv.strip(string.punctuation)
            if palavra_sem_ponto in lv.set_verbos_no_infinitivo:
                infinitivo = palavra_sem_ponto
                palavras[j] = palavras[j].replace(infinitivo, f'{infinitivo[:-1]}ndo')
                palavra_anterior = palavras[j - 1]
                # Se palavra anterior for 'a', remover.
                if palavra_anterior == 'a':
                    palavras[j - 1] = ''
                # Atualizar texto_bloco.
                texto_bloco = ' '.join(palavras)
                # Atualizar linha em linhas_pt.
                linhas_pt[i + 1] = texto_bloco

    # Atualizar linha em 'linhas'.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


@loop_linhas_pt
def corrigir_tags_de_itálico_maiúsculas(i, linhas_pt, texto_bloco, número_legenda):

    linhas_pt[i + 1] = texto_bloco.replace('<I>', '<i>').replace('</I>', '</i>')
    return linhas_pt


# OK.
# Substituições sem limite de palavra (podem ocorrer dentro de uma palavra) -.
# Subst_sem_limite_de_palavra.txt.
@loop_linhas_pt
def substuições_sem_limite_de_palavra(i, linhas_pt, texto_bloco, número_legenda):
    # Loopar lista do arquivo txt.
    for termo_para_sair, termo_para_entrar in reps.set_subst_sem_limite_de_palavra:
        if re.search(re.escape(termo_para_sair), texto_bloco):

            texto_bloco = re.sub(re.escape(termo_para_sair), termo_para_entrar, texto_bloco)

    # Atualizar linha em 'linhas'.
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


set_exceções_subst_sem_pontuação = {'ou', 'e', 'porque'}


# Substituir termos da lista substituições_sem_pontuação.txt.
# Evita que substituição seja feita em final de frase.
@loop_linhas_pt
def substituições_sem_pontuação(i, linhas_pt, texto_bloco, número_legenda):

    for termo_para_sair, termo_para_entrar in reps.set_substituições_sem_pontuação:

        for item in set_exceções_subst_sem_pontuação:
            # 'o meu ou o dela?', 'o meu e o seu.', (não tira o artigo).
            evitar = f'{item} {termo_para_sair}'

            if evitar in texto_bloco:
                pass
            else:
                texto_bloco = re.sub(fr'\b{re.escape(termo_para_sair)}\b(?![:.,!?])',
                                     termo_para_entrar, texto_bloco, flags=re.IGNORECASE)
                linhas_pt[i + 1] = texto_bloco

    return linhas_pt


@loop_linhas_pt
def substituições_case_sensitive(i, linhas_pt, texto_bloco, número_legenda):

    for termo_para_sair, termo_para_entrar in reps.set_substituições_cs:

        # Se item da lista termina com pontuação.
        termo_para_sair_tem_ponto = termo_para_sair[-1] in ls.lista_pontuação_com_vírgula

        # Se o item da lista termina com pontuação.
        if termo_para_sair_tem_ponto:
            # Procurar o termo da lista no texto_bloco.
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'\b{re.escape(termo_para_sair)}', texto_bloco)
            )

            if encontrar_termo_para_sair_em_texto_bloco:

                # Fazer substituições pegando termo se for lower, capitalizer ou upper.
                texto_bloco = re.sub(fr'\b{re.escape(termo_para_sair)}',
                                     termo_para_entrar, texto_bloco, count=0)

        # Se o item da lista não termina com pontuação.
        else:
            # Procurar termo da lista no texto bloco com e sem pontuação.
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'\b{re.escape(termo_para_sair)}\b|'
                          fr'\b{re.escape(termo_para_sair)}[.,!?:"]',
                          texto_bloco)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # Fazer substituições pegando termo se for lower, capitalizer ou upper.
                texto_bloco = re.sub(fr'\b{re.escape(termo_para_sair)}',
                                     termo_para_entrar, texto_bloco, count=0)

            # Atualizar linha em 'linhas'.
            linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# Substituir termos listados em substituições_case_insensitive_txt.
@loop_linhas_pt
def substituições_case_insensitive(i, linhas_pt, texto_bloco, número_legenda):

    for termo_para_sair, termo_para_entrar in reps.set_substituições_ci:

        termo_para_sair_começa_com_ponto = (
            termo_para_sair[0] in ls.lista_pontuação_com_vírgula
        )

        termo_para_sair_termina_com_ponto = (
            termo_para_sair[-1] in ls.lista_pontuação_com_vírgula
        )
        substituição_esvaziou_linha_2 = texto_bloco.strip() == ''

        if termo_para_sair_começa_com_ponto and termo_para_sair_termina_com_ponto:
            # Procurar o termo da lista no texto_bloco.
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(re.escape(termo_para_sair), texto_bloco, re.IGNORECASE)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # Fazer substituições pegando termo se for lower, capitalizer ou upper.
                texto_bloco = re.sub(rf'{re.escape(termo_para_sair)}',
                                     termo_para_entrar, texto_bloco, count=0, flags=re.IGNORECASE)

        elif termo_para_sair_termina_com_ponto:
            # Procurar o termo da lista no texto_bloco.
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'\b{re.escape(termo_para_sair)}',
                          texto_bloco, re.IGNORECASE)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # Fazer substituições pegando termo se for lower, capitalizer ou upper.
                texto_bloco = re.sub(fr'\b{re.escape(termo_para_sair)}',
                                     termo_para_entrar, texto_bloco, count=0, flags=re.IGNORECASE)

        elif termo_para_sair_começa_com_ponto:
            # Procurar o termo da lista no texto_bloco.
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'{re.escape(termo_para_sair)}\b',
                          texto_bloco, re.IGNORECASE)
            )

            if encontrar_termo_para_sair_em_texto_bloco:
                # Fazer substituições pegando termo se for lower, capitalizer ou upper.
                texto_bloco = re.sub(fr'{re.escape(termo_para_sair)}\b',
                                     termo_para_entrar, texto_bloco, count=0, flags=re.IGNORECASE)

        # Se o item da lista não termina com pontuação.
        else:
            # Procurar termo da lista no texto bloco com e sem pontuação.
            encontrar_termo_para_sair_em_texto_bloco = (
                re.search(fr'\b{re.escape(termo_para_sair)}\b|'
                          fr'\b{re.escape(termo_para_sair)}[.,!?:"]',
                          texto_bloco, re.IGNORECASE)
            )
            if encontrar_termo_para_sair_em_texto_bloco:

                # Fazer substituições pegando termo se for lower, capitalizer ou upper.
                texto_bloco = re.sub(fr'\b{re.escape(termo_para_sair)}\b|'
                                     fr'\b{re.escape(termo_para_sair)}[.,!?:"]',
                                     termo_para_entrar, texto_bloco, count=0, flags=re.IGNORECASE)

                # Se a linha 2 ficar vazia, colocar o número da legenda nessa lista.
                # (para devolver itálicas e diálogos certos).
                if substituição_esvaziou_linha_2:
                    set_linhas_2_esvaziadas.add(número_legenda)
            # Atualizar linha em 'linhas'.
            linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK.
# Arrumar maiúsculas depois de pontuação.
@loop_linhas_pt
def corrigir_maiúsculas_depois_de_pontuação(i, linhas_pt, texto_bloco, número_legenda):

    # Se a primeira linha de texto do primeiro bloco de legenda começar com minúscula.
    # (3, 4, 5, 6 são números de linhas onde possivelmente essa primeira linha vai estar.
    # Caso haja algumas linhas em branco no início).
    if i in [3, 4, 5, 6] and re.search(r'^[a-z]', texto_bloco):
        texto_bloco = f'{texto_bloco[0].capitalize()}{texto_bloco[1:]}'
        # Atualizar linha em 'linhas'.
        linhas_pt[i + 1] = texto_bloco

    if i + 6 < len(linhas_pt):
        # De minúscula para maiúscula depois de pontuação entre linhas.
        próxima_linha = linhas_pt[i + 4]
        num_próx_linha = 4

        # Prevenir erros de índice (i + 1 é a linha do texto_bloco).
        if i + 1 + num_próx_linha < len(linhas_pt):

            legenda_atual_é_diálogo = '/' in texto_bloco
            texto_bloco_strip = texto_bloco.strip()
            texto_bloco_termina_com_pto = texto_bloco_strip.endswith(('!', '?', ':', '.'))

            legenda_atual_não_é_FN = número_legenda not in set_FNs
            próxima_linha_começa_com_minúscula = (
                re.search(r'^[a-záàêéíóôç]', próxima_linha.strip())
            )
            próxima_linha_é_diálogo = '/' in próxima_linha

            # Se legenda atual não for FN, não for diálogo.
            if legenda_atual_não_é_FN:
                if not legenda_atual_é_diálogo:
                    if texto_bloco_termina_com_pto and próxima_linha_começa_com_minúscula:
                        próxima_linha = próxima_linha[0].capitalize() + próxima_linha[1:]

                # Se próxima linha for próxima legenda.
                elif legenda_atual_é_diálogo:
                    linha_1 = texto_bloco.split('/')[0].strip()
                    linha_2 = texto_bloco.split('/')[1].strip()
                    linha_1_diálogo_termina_com_pto = linha_1.endswith(('!', '?', ':', '.'))
                    linha_2_diálogo_termina_com_pto = linha_2.endswith(('!', '?', ':', '.'))

                    if linha_1_diálogo_termina_com_pto and linha_2_diálogo_termina_com_pto:
                        if próxima_linha_começa_com_minúscula:
                            próxima_linha = próxima_linha[0].capitalize() + próxima_linha[1:]

                if próxima_linha_é_diálogo:
                    próx_linha_1 = próxima_linha.split('/')[0].strip()
                    próx_linha_2 = próxima_linha.split('/')[1].strip()
                    próx_linha_2_diálogo_começa_com_minúscula = (
                        re.search(r'^[a-záàêéíóôç]', próx_linha_2)
                    )

                    if texto_bloco_termina_com_pto:
                        # A primeira linha do diálogo já foi resolvida nos passos acima.
                        # Verificar e capitalizar a segunda.
                        if próx_linha_2_diálogo_começa_com_minúscula:
                            próx_linha_2 = f'{próx_linha_2[0].strip().upper()}{próx_linha_2[1:]}'
                        # Juntar próxima linha 1 e 2.
                        próxima_linha = f'{próx_linha_1} / {próx_linha_2}'
                        linhas_pt[i + 4] = próxima_linha

            # Atualizar próxima linha em 'linhas'.
            linhas_pt[i + 4] = próxima_linha

    # De minúscula para maiúscula depois de pontuação na mesma linha.
    palavras = texto_bloco.split()
    for j, plv in enumerate(palavras):
        for ponto in ls.set_pontuação:

            próxima_palavra_existe = j + 1 < len(palavras)

            if próxima_palavra_existe:

                palavra_atual = palavras[j]
                palavra_atual_termina_com_ponto = palavra_atual[-1] in ponto
                próxima_palavra = palavras[j + 1]
                próxima_palavra_começa_com_minúscula = próxima_palavra[0].islower()

                if palavra_atual_termina_com_ponto and próxima_palavra_começa_com_minúscula:
                    # Capitalizar próxima palavra.
                    próxima_palavra = próxima_palavra.capitalize()
                    # Atualizar próxima_palavra em 'palavras'.
                    palavras[j + 1] = próxima_palavra
                    # Atualizar linha atual.
                    texto_bloco = f"{' '.join(palavras).strip()}\n"
    # Atualizar linha atual em 'linhas'.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# Encontrar nomes de pessoas no set_original_capitalizadas e separar por gênero.
@loop_linhas_pt
def separar_nomes_por_gênero(i, linhas_pt, texto_bloco, número_legenda):

    def separar_nomes(set_gênero, lista_default, diminutivo_espanhol_ito, diminutivo_espanhol_ico):

        diminutivos_espanhol = set()
        # Loopar set com capitalizadas do original.
        for nome, legenda in set_original_capitalizadas:
            # Se item da lista for nome composto (ex: Juan Pablo ou Juan Gonzáles).
            nome_composto = len(nome.split()) > 1

            if nome_composto:
                primeiro_nome = nome.split()[0]  # Separar primeiro nome do nome composto.
                # Se primeiro nome estiver na lista default de nomes masculinos/femininos.
                if primeiro_nome in lista_default:
                    # Adicionar ao set de nomes masculinos/femininos da legenda.
                    set_gênero.add(nome)
            # Se há um único nome e ele constar na lista default de nomes masculinos/femininos.
            elif nome in lista_default:
                set_gênero.add(nome)  # Adicionar ao set de nomes.

            # Detectar nomes próprios no diminutivo do espanhol ('-ito'/'-ita', '-ico'/'-ica').
            if nome.endswith((diminutivo_espanhol_ito, diminutivo_espanhol_ico)):
                diminutivos_espanhol.add(nome)

        novos_nomes = []
        # Se encontrar diminutivos de nomes, adicionar à lista novos_nomes.
        for nome_diminutivo in diminutivos_espanhol:
            for nome in set_gênero:
                if nome_diminutivo[:-4] in nome or nome_diminutivo[:-5] in nome:
                    novos_nomes.append(nome_diminutivo)

        # Adicionar os novos nomes ao set_gênero.
        for nome in novos_nomes:
            set_gênero.add(nome)

    separar_nomes(reps.set_nomes_femininos, ln.set_nomes_femininos_default, 'ita', 'ica')
    separar_nomes(reps.set_nomes_masculinos, ln.set_nomes_masculinos_default, 'ito', 'ico')

    return linhas_pt


@loop_linhas_pt
def abreviar_títulos(i, linhas_pt, texto_bloco, número_legenda):

    for tit_extenso, tit_abrv in ls.títulos_extenso_e_abrv:
        encontrar_título = re.search(tit_extenso, texto_bloco, re.IGNORECASE)

        if encontrar_título:
            # Dividir texto_bloco em palavras.
            palavras = texto_bloco.split()
            # Procurar título por extenso na lista de palavras.
            for j, plv in enumerate(palavras[:-1]):
                if plv.lower() == tit_extenso:

                    próxima_palavra = palavras[j + 1].strip(string.punctuation)

                    # Se palavra depois do título for cargo (prefeito, etc).
                    # Ou estiver em maiúscula, abreviar o título.
                    # Outra função vai deixar palavra seguinte maiúscula (Sr. Prefeito).
                    if próxima_palavra in ls.cargos_depois_de_títulos:
                        # Abreviar título por extenso:
                        palavras[j] = tit_abrv

                    elif próxima_palavra == próxima_palavra.capitalize():
                        # Abreviar título por extenso:
                        palavras[j] = tit_abrv

                    # Atualizar texto_bloco.
                    texto_bloco = ' '.join(palavras)

    # Atualizar linha em linhas_pt.
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# !!! antes de fix casing.
# Adicionar artigo (o/a) antes de nomes próprios depois de certas palavras.
# A função primeiro separa nomes por gênero
# e depois usa uma nested function para pegar nomes e títulos
def pôr_artigos_antes_de_nomes_e_títulos(linhas_pt):

    set_títulos_masculinos = {'Sr.', 'Sr', 'Dr.', 'Dr'}
    set_títulos_femininos = {'Dona', 'Sra.', 'Sra', 'Srta.', 'Srta', 'Sra.', 'Sra', 'Dona'}
    set_exceções_artigos = {'de', 'do', 'da', 'no', 'na', 'o', 'ao', 'a', 'à', 'esse',
                            'essa', 'este', 'esta', 'aquele', 'aquela',
                            'sr.', 'sr', 'dr.', 'dr', 'sra.', 'sra', 'srta.',
                            'srta', 'dra.', 'dra', 'dona', 'mesmo', 'mesma', 'obrigado',
                            'obrigada', 'outro', 'outra', 'amigo', 'amiga', 'prefeita',
                            'prefeito', 'professor', 'professora', 'primo', 'prima',
                            'tio', 'tia', 'presidente', 'inspetor', 'coronel', 'general'}

    # Adiconar as conjugações do verbo 'chamar' ao set de exceções.
    # De palavras para adicionar artigos depois delas.
    for verbo in lv.lista_geral_de_verbos_conjugados:
        for value in verbo.values():
            if verbo['infinitivo'] == 'chamar':
                set_exceções_artigos.add(value)

    @loop_linhas_pt
    def artigos_antes_de_nomes_e_títulos(i, linhas_pt, texto_bloco, número_legenda):

        palavras = texto_bloco.split()  # Dividir linha atual em palavras.

        # NOMES.
        # Função para rodar nomes femininos e masculinos.
        def artigo_antes_de_nome(lista, artigo):

            # Juntar primeiro e segundo nomes,
            # Em caso de nome composto, em um único item em 'palavras'.
            excluir_segundo_nome_duplicado = []
            for j, plv in enumerate(palavras):

                palavra_atual = palavras[j]
                palavra_atual_é_nome = palavra_atual.strip(string.punctuation) in lista
                próxima_palavra_existe = j + 1 < len(palavras)

                # Ver se palavra atual do loop + próxima formam um nome composto da lista.
                if palavra_atual_é_nome and próxima_palavra_existe:
                    próxima_palavra = palavras[j + 1]
                    é_nome_composto = (
                        f'{palavra_atual} {próxima_palavra.strip(string.punctuation)}' in lista
                    )

                    if é_nome_composto:
                        # Juntar o segundo nome ao primeiro, formando um único item em 'palavras'.
                        palavras[j] = f'{palavra_atual} {próxima_palavra}'
                        # Guardar índice original do segundo nome.
                        excluir_segundo_nome_duplicado.append(j + 1)
                        # Agora os nomes compostos serão tratados como nomes simples.

            # Excluir índice original do segundo nome.
            for k in reversed(excluir_segundo_nome_duplicado):
                del palavras[k]

            # Adicionar artigo antes de nome.
            # Novo loop para adicionar os artigos tratando nomes compostos como simples.
            for j, plv in enumerate(palavras):

                palavra_atual = palavras[j]
                palavra_atual_é_nome = palavra_atual.strip(string.punctuation) in lista
                nome_termina_com_ponto = palavra_atual[-1] in ls.lista_pontuação_com_vírgula
                nome_é_primeira_palavra = j == 0
                próxima_palavra_existe = j + 1 < len(palavras)

                if palavra_atual_é_nome:
                    # Se for começo de linha.
                    if nome_é_primeira_palavra:
                        if not nome_termina_com_ponto:
                            palavra_atual = artigo + palavra_atual
                            palavras[j] = palavra_atual  # Atualizar 'palavras'.
                    # Sem ser começo de frase.
                    else:
                        palavra_anterior = palavras[j - 1]
                        palavra_anterior_termina_com_ponto = (
                            palavra_anterior[-1] in ls.lista_pontuação_com_vírgula
                        )
                        palavra_anterior_é_quebra_diálogo = (
                            palavra_anterior == '/'
                        )
                        palavra_anterior_não_é_exceção = (
                            palavra_anterior.lower() not in set_exceções_artigos
                        )

                        if palavra_anterior_termina_com_ponto or palavra_anterior_é_quebra_diálogo:
                            if nome_termina_com_ponto:
                                pass
                        else:
                            if palavra_anterior_não_é_exceção:
                                palavra_atual = artigo + palavra_atual
                                palavras[j] = palavra_atual  # Atualizar 'palavras'.

                # Atualizar linha em 'linhas'.
                texto_bloco = f"{' '.join(palavras).strip()}\n"
                linhas_pt[i + 1] = texto_bloco

            return linhas_pt

        # Chamar função para pôr artigo masculino ou feminino.
        linhas_pt = artigo_antes_de_nome(reps.set_nomes_femininos, 'a ')
        linhas_pt = artigo_antes_de_nome(reps.set_nomes_masculinos, 'o ')

        # TÍTULOS.
        # Função para rodar nomes femininos e masculinos.
        def artigo_antes_de_título(lista, artigo):

            # Juntar título e nome em um único item em 'palavras'.
            excluir_nome_duplicado = []
            for j, plv in enumerate(palavras):

                palavra_atual = palavras[j]
                palavra_atual_é_título = palavra_atual in lista
                próxima_palavra_existe = j + 1 < len(palavras)

                # Ver se palavra atual do loop + próxima formam um nome composto da lista.
                if palavra_atual_é_título and próxima_palavra_existe:
                    próxima_palavra = palavras[j + 1]

                    # Juntar o segundo nome ao primeiro, formando um único item em 'palavras'.
                    palavras[j] = f'{palavra_atual} {próxima_palavra}'
                    # Guardar índice original do segundo nome.
                    excluir_nome_duplicado.append(j + 1)
                    # Agora os nomes compostos serão tratados como nomes simples.

            # Excluir índice original do segundo nome.
            for k in reversed(excluir_nome_duplicado):
                del palavras[k]

            # Adicionar artigo antes de título.
            # Novo loop para adicionar os artigos tratando título
            # e nome como um item só na lista 'palavras'
            for j, plv in enumerate(palavras):

                palavra_atual = palavras[j]
                palavra_atual_é_título = palavra_atual.split()[0] in lista
                título_é_primeira_palavra = j == 0
                próxima_palavra_existe = j + 1 < len(palavras)
                nome_termina_com_ponto = palavra_atual[-1] in ls.lista_pontuação_com_vírgula

                if palavra_atual_é_título:
                    # Se for começo de linha.
                    if título_é_primeira_palavra and próxima_palavra_existe:

                        if not nome_termina_com_ponto:
                            palavra_atual = artigo + palavra_atual
                            palavras[j] = palavra_atual  # Atualizar 'palavras'.
                    # Sem ser começo de frase.
                    else:
                        palavra_anterior = palavras[j - 1]
                        palavra_anterior_termina_com_ponto = (
                            palavra_anterior[-1] in ls.lista_pontuação_com_vírgula
                        )
                        palavra_anterior_não_é_exceção = (
                            palavra_anterior.lower() not in set_exceções_artigos
                        )

                        if palavra_anterior_termina_com_ponto and nome_termina_com_ponto:
                            pass
                        else:
                            if palavra_anterior_não_é_exceção:
                                palavra_atual = artigo + palavra_atual
                                palavras[j] = palavra_atual  # Atualizar 'palavras'.

                # Atualizar linha em 'linhas'.
                texto_bloco = f"{' '.join(palavras).strip()}\n"
                linhas_pt[i + 1] = texto_bloco

            return linhas_pt

        linhas_pt = artigo_antes_de_título(set_títulos_femininos, 'a ')
        linhas_pt = artigo_antes_de_título(set_títulos_masculinos, 'o ')

        return linhas_pt

    linhas_pt = artigos_antes_de_nomes_e_títulos(linhas_pt)

    # Corrigir 'por o João' --> 'pelo João'
    set_corrigir_por_mais_artigo = {
        (r'\bpor o\b', 'pelo'),
        (r'\bpor a\b', 'pela'),
        (r'\bpor os\b', 'pelos'),
        (r'\bpor as\b', 'pelas')
    }

    for i, linha in enumerate(linhas_pt):
        for termo_errado, termo_certo in set_corrigir_por_mais_artigo:
            linhas_pt[i] = re.sub(termo_errado, termo_certo, linhas_pt[i])

    return linhas_pt


@loop_linhas_pt
def subsitutir_reticências_por_trema(i, linhas_pt, texto_bloco, número_legenda):

    texto_bloco = texto_bloco.replace('...', '¨')
    # Atualizar linha em linhas_pt
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


@loop_linhas_pt
def devolver_reticências(i, linhas_pt, texto_bloco, número_legenda):

    texto_bloco = texto_bloco.replace('¨', '...')
    # Atualizar linha em linhas_pt
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# De João --> do João.
def transformar_de_em_da_ou_do(linhas_pt):

    def do_da_nomes(lista, do_da):

        palavra_atual = palavras[j]
        palavra_atual_está_na_lista = palavra_atual.strip(string.punctuation) in lista
        palavra_anterior = palavras[j - 1]

        if palavra_atual_está_na_lista and palavra_anterior:

            if palavra_anterior in ['de', 'De']:
                # Juntar primeira letra de 'de' ou 'De'.
                # + segunda letra em diante de 'do', 'da', etc.
                palavra_anterior = palavra_anterior[0] + do_da[1:]

                # Atualizar 'palavras' e 'linhas'.
                palavras[j - 1] = palavra_anterior
                linhas_pt[i] = f"{' '.join(palavras).strip()}\n"
        return linhas_pt

    for i, linha in enumerate(linhas_pt):
        palavras = linhas_pt[i].split()  # Dividir linha em palavras.
        for j, plv in enumerate(palavras):

            do_da_nomes(reps.set_nomes_femininos, 'da')
            do_da_nomes(reps.set_nomes_masculinos, 'do')
            do_da_nomes(ls.possessivos_sing_m, 'do')
            do_da_nomes(ls.possessivos_pl_m, 'dos')
            do_da_nomes(ls.possessivos_sing_f, 'da')
            do_da_nomes(ls.possessivos_pl_f, 'das')
            do_da_nomes(ls.títulos_masculinos, 'do')
            do_da_nomes(ls.títulos_femininos, 'da')
    return linhas_pt


# A gente vai --> vamos.
# A gente foi --> fomos.
# A gente saiu e passeou --> saímos e passeamos.
# A gente pensou, refletiu e decidiu --> nós pensamos, refletimos e decidimos.
@loop_linhas_pt
def transformar_a_gente_em_nós(i, linhas_pt, texto_bloco, número_legenda):

    # Procurar 'a gente' or 'A gente' nas linhas, exceto em final de frase.
    if re.search(r'\ba gente\b(?![.!?":])', texto_bloco, re.IGNORECASE):

        número_de_verbos = []
        próxima_linha = 4
        índice_gente = -1

        # Essa função encontra a altura da frase para parar de detectar e transformar os verbos.
        def detectar_índice_para_parar(palavras, índice_gente):
            # Começar a iterar depois de "a gente".
            for j, plv in enumerate(palavras[índice_gente:], start=índice_gente):
                palavra_atual = palavras[j].strip()
                palavra_atual_termina_com_ponto = palavra_atual[-1] in ls.set_pontuação
                palavra_atual_termina_com_vírgula = palavra_atual[-1] == ','

                # Se achar 'que' ou 'porque' ou pontuação (menos vírgula),.
                # Definir índice para parar a busca por verbos.
                # 'Decidimos ir ao parque QUE ela recomendou'.
                # 'Pensamos em viajar PORQUE ele estava de férias'.
                if palavra_atual in ['que', 'porque'] or palavra_atual_termina_com_ponto:
                    índice_parar = j

                # Se houver ',' ou 'e' e a próxima palavra estiver na lista abaixo, definir índice.
                # 'Pensamos, refletimos E ELE me ajudou...'.
                # 'Pesquisamos, investigamos E UNS dias depois...'.
                # 'Depois que cozinhamos e comemos, ELA disse...'.
                # Ver se existe próxima palavra - j + 1 < len(palavras).
                elif palavra_atual_termina_com_vírgula or palavra_atual == 'e':
                    if j + 1 < len(palavras):
                        if próxima_palavra in [
                                'ele', 'ela', 'eles', 'elas', 'eu', 'o', 'a', 'os',
                                'as', 'um', 'uns', 'uma', 'umas', 'aquele', 'aquela',
                                'aqueles', 'aquelas', 'esse', 'essa', 'esses', 'essas'
                                ]:
                            índice_parar = j + 1
                # Se a frase não tiver os itens acima,.
                # Procurar verbos na próxima linha nos passos abaixo.
                else:
                    índice_parar = -1  # Iterar até o fim da linha atual.
            return índice_parar

        palavras = texto_bloco.split()  # Dividir linha em palavras.
        # Detectar as palavras "a gente" da linha e índice do primeiro verbo.
        for j, plv in enumerate(palavras[:-1]):

            palavra_atual = palavras[j]
            existe_terceira_palavra = j + 2 < len(palavras)
            próxima_palavra = palavras[j + 1]

            if palavra_atual.lower() == 'a' \
                    and próxima_palavra == 'gente' and existe_terceira_palavra:
                índice_gente = j + 1

        # Detectar index para parar a iteração da linha com "a gente".
        índice_parar = detectar_índice_para_parar(palavras, índice_gente)
        # Somar um número ao índice, pois iterar até :índice_parar exclui "índice_parar".
        índice_parar = índice_parar + 1

        # Detectar a próxima linha, se busca por verbos não parou na linha atual.
        próxima_linha = linhas_pt[i + 4]
        num_próx_linha = 4

        # Se a palavra estiver na lista da 3a pessoa
        # e não estiver nas exceções
        # e a palavra anterior não estiver nas exceções e não terminar com vírgula

        for j, plv in enumerate(palavras[índice_gente:índice_parar], start=índice_gente):
            palavra_atual = palavras[j]
            palavra_anterior = palavras[j - 1]
            palavra_anterior_termina_com_vírgula = palavras[j - 1][-1] == ','
            palavra_atual_strip = palavra_atual.strip(string.punctuation)

            palavra_atual_é_verbo_3a_sing = (
                palavra_atual_strip in lv.set_3a_pess_sing
            )

            if palavra_atual_é_verbo_3a_sing and palavra_atual.islower() \
                    and palavra_atual not in ls.a_gente_nós_exceções \
                    and palavra_anterior not in ls.a_gente_nós_exceções:

                # 'A gente CHEGOU e O avisou que...' - depois de 'a gente', depois de 'o'.
                # 'A gente chegou, pediu para...' - depois de ','.
                if palavra_anterior in ['gente', 'o', 'a', 'os', 'as', 'e', 'depois'] \
                                    or palavra_anterior_termina_com_vírgula:
                    # Colocar verbo numa lista para medir a quantidade.
                    número_de_verbos.append(palavras[j])

                    # Trocar verbo na terceira do singular (faz, trabalha, etc ).
                    # Por primeira do plural (fazemos, trabalhamos, etc).

                    for terceira_p_sing, primeira_p_pl in lv.set_a_gente_nós:

                        if palavra_atual_strip == terceira_p_sing:

                            palavra_atual = (
                                palavra_atual.replace(palavra_atual_strip,
                                                      primeira_p_pl)
                            )

                            # Atualizar 'palavras'.
                            palavras[j] = palavra_atual
                            # Atualizar texto_bloco.
                            texto_bloco = f"{' '.join(palavras).strip()}\n"
                            # Atualizar linha em 'linhas'.
                            linhas_pt[i + 1] = texto_bloco
                            break

        # Se houver pronome objeto depois de 'a gente', deixar 'nós'.
        entre_a_gte_e_verbo = ['a', 'o', 'as', 'os', 'te', 'lhe']
        for item in entre_a_gte_e_verbo:
            texto_bloco = texto_bloco.replace(f'a gente {item}', f'nós {item}') \
                 .replace(f'A gente {item}', f'nós {item}')
            # O case do verbo vai ser consertado depois.
            linhas_pt[i + 1] = texto_bloco

        # Se houver dois ou menos verbos, simplesmente eliminar 'a gente', sem adicionar 'nós'.
        if len(número_de_verbos) <= 2:
            texto_bloco = texto_bloco.replace('a gente ', '').replace('A gente ', '')
            linhas_pt[i + 1] = texto_bloco

        # Se houver mais de dois verbos, a gente --> nós.
        else:
            texto_bloco = texto_bloco.replace('a gente ', 'nós ').replace('A gente ', 'Nós ')
            linhas_pt[i + 1] = texto_bloco

        texto_bloco_strip = texto_bloco.strip()
        texto_bloco_não_termina_com_ponto = (
            texto_bloco_strip[-1] not in ['.', '?', '"', '!', ':', '¨']
        )

        # Se não houver ponto ou index parar na primeira linha, verificar segunda.
        if índice_parar == len(palavras) and texto_bloco_não_termina_com_ponto:
            palavras2 = próxima_linha.split()
            index_parar2 = detectar_índice_para_parar(palavras2, 0)
            # Inserir temporariamente a última palavra da primeira linha na segunda.
            # (evitar problemas de índice).
            palavras2.insert(0, palavras[-1])

            # Somar mais um número ao índice para parar a busca por verbos,.
            # Pois foi acrescentada uma palavra no começo.
            index_parar2 = index_parar2 + 2
            # Procurar verbos ligados a 'a gente' na segunda linha.
            for k, plv2 in enumerate(palavras2[0:index_parar2], start=0):
                for terceira_p_sing, primeira_p_pl in lv.set_a_gente_nós:
                    palavra_atual2 = palavras2[k]
                    palavra_atual2_sem_ponto = palavras2[k].strip(string.punctuation)
                    palavra_atual2_é_verbo_3a_sing = (
                        palavra_atual2_sem_ponto == terceira_p_sing
                    )
                    palavra_anterior2 = palavras2[k - 1]

                    if palavra_atual2_é_verbo_3a_sing and palavra_atual2.islower() \
                            and palavra_atual not in ls.a_gente_nós_exceções \
                            and palavra_anterior not in ls.a_gente_nós_exceções:

                        palavra_anterior2_termina_com_vírgula = palavra_anterior2[-1] == ','

                        if palavra_anterior2 in ['gente', 'o', 'a', 'os', 'as', 'e', 'depois'] \
                                or palavra_anterior2_termina_com_vírgula:
                            # Substituir: coloca --> colocamos.
                            palavra_atual2_strip = palavra_atual2.strip(string.punctuation)
                            palavra_atual2 = (
                                palavra_atual2.replace(palavra_atual2_strip,
                                                       primeira_p_pl)
                            )
                            # Atualizar 'palavras'.
                            palavras2[k] = palavra_atual2
                            # Remover primeira palavra de palavra2 (posta temporariamente).
                            palavras2[0] = ''
                            # Atualizar linha em 'linhas'.
                            próxima_linha = f"{' '.join(palavras2).strip()}\n"
                            linhas_pt[i + 1 + num_próx_linha] = próxima_linha
                            break
    return linhas_pt


@loop_linhas_pt
def transformar_para_que_faça_em_para_fazer(i, linhas_pt, texto_bloco, número_legenda):
    índice_que = ''
    encontrar_para_que = re.search(r'\bpara que\b', texto_bloco, re.IGNORECASE)

    if encontrar_para_que:
        palavras = texto_bloco.split()  # Dividir texto_bloco em palavras.

        # Procurar 'para que' nas palavras.
        for j, plv in enumerate(palavras[:-1]):
            palavra_atual = palavras[j]
            próxima_palavra = palavras[j + 1]
            if palavra_atual.lower() == 'para' and próxima_palavra == 'que':
                # Pegar índice de 'que'.
                índice_que = j + 1

        # Procurar verbo no subjuntivo a partir de 'que'.
        for j, plv in enumerate(palavras):
            palavra_atual = palavras[j]
            palavra_atual_sem_pto = palavra_atual.strip(string.punctuation)

            if palavra_atual_sem_pto in lv.set_pres_pret_subjuntivo:
                # Remover 'que' da frase.
                palavras[índice_que] = ''
                # Encontrar no set a palavra atual (subjuntivo) e o imperativo correspondente.
                for imperativo, subjuntivo in lv.set_sub_pres_fut:
                    if palavra_atual_sem_pto == subjuntivo:

                        # Transformar palavra atual no imperativo.
                        palavra_atual = palavra_atual.replace(subjuntivo, imperativo)
                        # Atualizar palavra atual.
                        palavras[j] = palavra_atual
                        # Atualizar texto_bloco.
                        texto_bloco = f'{" ".join(palavras)}\n'
                        # Atualizar linha em linhas_pt.
                        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


@loop_linhas_pt
def transformar_sem_que_faça_em_sem_fazer(i, linhas_pt, texto_bloco, número_legenda):
    índice_que = ''
    encontrar_sem_que = re.search(r'\bsem que\b', texto_bloco, re.IGNORECASE)

    if encontrar_sem_que:
        palavras = texto_bloco.split()  # Dividir texto_bloco em palavras.

        # Procurar 'para que' nas palavras.
        for j, plv in enumerate(palavras[:-1]):
            palavra_atual = palavras[j]
            próxima_palavra = palavras[j + 1]
            if palavra_atual.lower() == 'sem' and próxima_palavra == 'que':
                # Pegar índice de 'que'.
                índice_que = j + 1

        # Procurar verbo no subjuntivo a partir de 'que'.
        for j, plv in enumerate(palavras):
            palavra_atual = palavras[j]
            palavra_atual_sem_pto = palavra_atual.strip(string.punctuation)

            if palavra_atual_sem_pto in lv.set_pres_pret_subjuntivo:
                # Remover 'que' da frase.
                palavras[índice_que] = ''
                # Encontrar no set a palavra atual (subjuntivo) e o imperativo correspondente.
                for imperativo, subjuntivo in lv.set_sub_pres_fut:
                    if palavra_atual_sem_pto == subjuntivo:
                        # Transformar palavra atual no imperativo.
                        palavra_atual = palavra_atual.replace(subjuntivo, imperativo)
                        # Atualizar palavra atual.
                        palavras[j] = palavra_atual
                        # Atualizar texto_bloco.
                        texto_bloco = f'{" ".join(palavras)}\n'
                        # Atualizar linha em linhas_pt.
                        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


def remover_reflexivo_opcional(linhas_pt):

    def remover_reflexivo_op(linhas_pt, pronome, lista):

        for i, linha in enumerate(linhas_pt):
            if '-->' in linhas_pt[i]:
                texto_bloco = linhas_pt[i + 1]
                # Encontrar 'se' ou '-se' em texto_bloco.
                encontrar_reflexivo_em_texto_bloco = (
                    re.search(rf'\b{pronome}\b', texto_bloco, re.IGNORECASE) or
                    re.search(rf'-{pronome}\b|-{pronome}[.,!?:]', texto_bloco)
                )

                if encontrar_reflexivo_em_texto_bloco:

                    remover_reflexivo = []
                    palavras = texto_bloco.split()  # Dividir texto_bloco em palavras.

                    for j, plv in enumerate(palavras[:-1]):

                        palavra_sem_ponto = plv.strip(string.punctuation)
                        próxima_palavra_sem_ponto = palavras[j + 1].strip(string.punctuation)
                        palavra_atual_é_pronome_reflexivo = plv.lower() == pronome

                        if palavra_atual_é_pronome_reflexivo:
                            é_infinitivo = (
                                próxima_palavra_sem_ponto.lower() in lv.set_reflexivos_opcionais
                            )
                            é_gerúndio = (
                                próxima_palavra_sem_ponto in lv.set_reflexivos_opcionais_gerúndio
                            )
                            if é_infinitivo or é_gerúndio:

                                if pronome == 'se':
                                    remover_reflexivo.append(j)

                                else:
                                    # No caso de 'me' e 'nos', se não tiver verbo
                                    # na pessoa correspondente, tirar o pronome.
                                    for k, plv_k in reversed(list(enumerate(palavras[:j]))):
                                        if plv_k.lower() in ['vou', 'vamos', 'eu', 'nós']:
                                            remover_reflexivo.append(j)

                            # Se não for infinitivo.
                            else:
                                if próxima_palavra_sem_ponto.lower() in lista:
                                    remover_reflexivo.append(j)

                        # Reflexivo é ênclise.
                        elif palavra_sem_ponto.lower().endswith(f'-{pronome}'):
                            # Remover '-se' do verbo.
                            if palavra_sem_ponto.lower().replace(f'-{pronome}', '') in lista:
                                palavras[j] = palavras[j].replace(f'-{pronome}', '')

                    # Remover 'se' de palavras.
                    if len(remover_reflexivo) > 0:
                        for índice in reversed(sorted(remover_reflexivo)):
                            del palavras[índice]

                    # Atualizar texto_bloco.
                    texto_bloco = ' '.join(palavras)
                    # Atualizar linha em linhas_pt.
                    linhas_pt[i + 1] = texto_bloco

        return linhas_pt

    linhas_pt = remover_reflexivo_op(linhas_pt, 'se', lv.set_reflexivo_3a_pessoa)
    linhas_pt = remover_reflexivo_op(linhas_pt, 'me', lv.set_reflexivo_1a_pess_sing)
    linhas_pt = remover_reflexivo_op(linhas_pt, 'nos', lv.set_reflexivo_1a_pess_pl)

    return linhas_pt


# OK.
# Põe vírgula antes da última palavra da linha.
@loop_linhas_pt
def vírgula_antes_de_sim_não_em_fim_de_frase(i, linhas_pt, texto_bloco, número_legenda):

    não_pôr_vírgula_depois = [
        'ainda', 'digo', 'diria', 'diríamos', 'diriam', 'disse', 'disseram', 'dizemos',
        'dissemos', 'diz', 'dizem', 'dirá', 'dizer', 'diremos', 'dirão', 'ou', 'porque', 'que',
        'talvez', 'também'
        ]

    palavras = texto_bloco.split()
    for j, palavra in enumerate(palavras):

        palavra_atual = palavras[j]
        palavra_atual_sem_ponto = palavra_atual.strip(string.punctuation)
        palavra_atual_termina_com_ponto = palavra_atual[-1] in {'.', '?', '!', ':', '¨'}
        palavra_anterior_não_tem_ponto = palavras[j - 1][-1] not in {'.', '?', '!', ':', '¨'}

        if palavra_atual_sem_ponto in ['sim', 'não'] and palavra_atual_termina_com_ponto \
                and palavra_anterior_não_tem_ponto:

            palavra_anterior_não_é_exceção = palavras[j - 1].lower() not in não_pôr_vírgula_depois

            if palavra_anterior_não_é_exceção:
                # Pôr vírgula antes de 'sim' ou 'não' e atualizar a linha atual em 'linhas'.
                palavras[j - 1] = f'{palavras[j - 1]},'
                linhas_pt[i + 1] = f"{' '.join(palavras).strip()}\n"
    return linhas_pt


@loop_linhas_pt
def transformar_mais_do_que_em_mais_que(i, linhas_pt, texto_bloco, número_legenda):

    encontrar_mais_do_que = (
        re.search(r'\bmais [^.,!?:"]* do que\b', texto_bloco)
    )
    encontrar_menos_do_que = (
        re.search(r'\bmenos [^.,!?:"]* do que\b', texto_bloco)
    )
    if encontrar_mais_do_que or encontrar_menos_do_que:
        texto_bloco = texto_bloco.replace('do que', 'que')

    # Atualizar linha em linhas_pt.
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


@loop_linhas_pt
def transformar_para_você_em_te(i, linhas_pt, texto_bloco, número_legenda):

    encontrar_para_você_ou_a_você = (
        re.search(r'\bpara você\b|\ba você\b', texto_bloco, re.IGNORECASE)
    )

    não_transformar = False
    índice_a_ou_para = ''
    índice_você = ''
    índice_verbo = ''

    if encontrar_para_você_ou_a_você:
        palavras = texto_bloco.split()  # Dividir texto_bloco em palavras.

        # Encontrar 'para'/'a' + 'você' em 'palavras'.

        for j, plv in enumerate(palavras):
            # Para evitar erros de índice.
            if j + 1 < len(palavras):
                encontrar_para_você_em_palavras = (
                    palavras[j] == 'para' and palavras[j + 1].strip(string.punctuation) == 'você'
                    )
                encontrar_a_você_em_palavras = (
                    palavras[j] == 'a' and palavras[j + 1].strip(string.punctuation) == 'você'
                    )

            if encontrar_para_você_em_palavras or encontrar_a_você_em_palavras:
                # Evitar frases como 'trouxe isso para você beber',
                # (com um infinitivo depois de 'para você').
                if j + 2 < len(palavras):
                    if palavras[j + 2] in lv.set_verbos_no_infinitivo:
                        não_transformar = True

                índice_a_ou_para = j
                índice_você = j + 1

                # Encontrar verbo antes de 'para você' / 'a você'.
                if não_transformar is False:
                    for j, plv in reversed(list(enumerate(palavras[:índice_a_ou_para]))):
                        if plv.lower() in lv.set_verbos_conjugados_transformar_para_você_em_te:
                            índice_verbo = j

                            # Adicionar 'te' antes do verbo.
                            palavras[índice_verbo] = f'te {plv.lower()}'
                            palavras[índice_a_ou_para] = ''
                            palavras[índice_você] = palavras[índice_você].replace('você', '')
                            # Atualizar texto_bloco.
                            texto_bloco = ' '.join(palavras)
                            # Remover 'o te entregou', 'a te entregou', etc,
                            # caso a frase anterior seja 'a entregou a você'?
                            texto_bloco = texto_bloco.replace(' o te ', ' te ')\
                                .replace(' a te ', ' te ')\
                                .replace(' os te ', ' te ').replace(' as te ', ' te ')

    # Atualizar linha em linhas_pt.
    linhas_pt[i + 1] = texto_bloco
    # Eliminar a te entregou, o te entregou, etc

    return linhas_pt


# OK.
# Substituições a serem feitas em perguntas.
# Você quer...? --> Quer...?.
@loop_linhas_pt
def substituições_começo_de_pergunta(i, linhas_pt, texto_bloco, número_legenda):

    # Consultar lista de substituir_começo_de_pergunta.txt.
    for termo_antes, termo_depois in reps.set_subst_começo_pergunta:
        # Procurar termo da lista na linha atual.
        if re.search(rf'\b{termo_antes}\b.*?\?|{termo_antes}\?', texto_bloco):

            # Substituir (se tiver ? logo em seguida ao termo).
            texto_bloco = re.sub(rf'{termo_antes}', rf'{termo_depois}', texto_bloco)
            # Substituir (se tiver ? logo em seguida ao termo).
            texto_bloco = re.sub(rf'{termo_antes}\?', rf'{termo_depois}\?', texto_bloco)
            # Atualizar linha atual em 'linhas'.
            linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK
# Escreve números por extenso de 11 a 100 em começos de frase.
@loop_linhas_pt
def número_começo_por_extenso(i, linhas_pt, texto_bloco, número_legenda):

    # Encontrar números de dois dígitos ou 100.
    if re.search(r'(?:\d{2}|100)\b', texto_bloco):

        # Definir linha anterior: se for a primeira linha de um bloco, são 4 linhas cima;.
        # Se for a segunda linha de um bloco, é uma linha acima.
        linha_anterior = linhas_pt[i - 2].strip()
        palavras = texto_bloco.split()  # Dividir linha atual em palavras.
        linha_anterior_termina_com_ponto = linha_anterior[-1] in ls.set_pontuação
        primeira_palavra_sem_ponto = palavras[0].strip(string.punctuation)
        primeira_palavra = palavras[0]

        # Ver se o número está no começo da linha e se a linha anterior termina com pontuação.
        if re.search(r'^(?:\d{2}|100)\b', texto_bloco) and linha_anterior_termina_com_ponto:

            # Consultar lista de algarismos e números por extenso de 0 a 100.
            for algarismo, número_por_extenso in ls.set_0_a_100_algarismo_e_por_extenso:

                if algarismo == primeira_palavra_sem_ponto:  # Se primeira palavra for algarismo.

                    # Subsituir algarismo por número por extenso.
                    primeira_palavra = (
                        primeira_palavra.replace(algarismo, número_por_extenso.capitalize())
                    )
                    # Atualizar primeira palavra em 'palavras'.
                    palavras[0] = primeira_palavra
                    # Atualizar linha atual em 'linhas'.
                    texto_bloco = f"{' '.join(palavras).strip()}\n"

        # Ver se o número está no meio da linha, depois de pontuação.
        for j, plv in enumerate(palavras[1:], start=1):  # Loopar as palavras da linha atual.

            palavra_atual = palavras[j].strip(string.punctuation)
            palavra_anterior_tem_pontuação = palavras[j - 1][-1] in ls.set_pontuação

            if re.search(r'(?:\d{2}|100)\b', palavra_atual) and palavra_anterior_tem_pontuação:

                for algarismo, número_por_extenso in ls.set_0_a_100_algarismo_e_por_extenso:
                    # Se palavra atual for algarismo de 0 a 100.
                    if algarismo == palavra_atual:
                        palavra_atual = (
                            palavra_atual.replace(algarismo, número_por_extenso.capitalize())
                        )

                        # Atualizar palavra atual:
                        palavras[j] = palavra_atual

                        texto_bloco = ' '.join(palavras) + '\n'
        # Atualizar linha atual em 'linhas'.
        linhas_pt[i + 1] = texto_bloco

        # Se for FN, deixar tudo em maiúsculas.
        if número_legenda in set_FNs:
            texto_bloco = texto_bloco.upper()
            # Atualizar linha atual em 'linhas'.
            linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# Conserta imperativos traduzidos do inglês como infinitivos -> Come. --> Vir. --> Venha.
@loop_linhas_pt
def corrigir_imperativos_traduzidos_como_infinitivos(i, linhas_pt, texto_bloco, número_legenda):

    for sufixo in ['ar', 'er', 'ir', 'or']:
        if re.search(rf'{sufixo}[.,!]|Ir[.,!?]', texto_bloco):
            palavras = texto_bloco.split()  # Dividir linha em palavras.
            for j, plv in enumerate(palavras):
                palavra_atual = palavras[j]

                palavra_atual_é_maiúscula = palavra_atual.capitalize() == palavra_atual
                palavra_atual_é_infinitivo = (
                    palavra_atual.lower().strip(string.punctuation) in lv.set_verbos_no_infinitivo
                )
                if palavra_atual_é_maiúscula and palavra_atual_é_infinitivo:

                    for infinitivo, imperativo in lv.set_imperativos_infinitivos:
                        if re.search(rf'\b{infinitivo}[.,!]', texto_bloco):

                            palavra_atual_termina_com_ponto = palavra_atual[-1] \
                                in ['.', ',', '!', '¨']
                            palavra_atual_é_infinitivo = palavra_atual[:-1] == infinitivo

                            if palavra_atual_é_infinitivo and palavra_atual_termina_com_ponto:
                                palavra_atual = palavra_atual.replace(infinitivo, imperativo)
                                # Atualizar palavra atual em 'palavras'.
                                palavras[j] = palavra_atual
                                # Atualizar linha atual.
                                texto_bloco = f"{' '.join(palavras).strip()}\n"
                                # Atualizar linha em 'linhas'.
                                linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK
# Escreve por extenso números de zero a dez.
@loop_linhas_pt
def número_zero_dez_por_extenso(i, linhas_pt, texto_bloco, número_legenda):

    # Encontrar números 0-10.
    encontrar_número_0_10 = re.search(r'\b(?:[0-9](?:\.\d+)?|10)\b(?!\:)(?!\,)', texto_bloco)

    if encontrar_número_0_10:

        palavras = texto_bloco.split()  # Dividir linha em palavras.
        for j, plv in enumerate(palavras):

            for algarismo, número_por_extenso in ls.num_zero_dez:

                palavra_atual = palavras[j]
                palavra_atual_é_algarismo = (
                    str(algarismo) == palavra_atual.strip(string.punctuation)
                )
                palavra_atual_não_é_milhar_nem_float = (
                    ',' not in palavra_atual[:-1] and '.' not in palavra_atual[:-1]
                )
                palavra_atual_termina_com_pontuação = (
                    palavra_atual[-1] in ls.lista_pontuação_com_vírgula
                )

                if palavra_atual_é_algarismo and palavra_atual_não_é_milhar_nem_float:
                    if palavra_atual_termina_com_pontuação:
                        palavra_atual = número_por_extenso + palavra_atual[-1]
                    else:
                        # Consertar gênero de 1 ou 2 (um/uma, dois/duas).
                        if len(palavras) > 1:
                            if palavra_atual in ['1', '2']:
                                próxima_palavra_existe = j + 1 < len(palavras)

                                if próxima_palavra_existe:
                                    próxima_palavra = palavras[j + 1]
                                    próxima_palavra_não_tem_só_um_caractere = (
                                        len(próxima_palavra) > 1
                                    )

                                    if próxima_palavra_não_tem_só_um_caractere:
                                        próxima_palavra_termina_com_a = (
                                            próxima_palavra.strip(string.punctuation)[-1] == 'a'
                                        )

                                        if palavra_atual == '1':
                                            if próxima_palavra_termina_com_a:
                                                palavra_atual = 'uma'
                                            else:
                                                palavra_atual = 'um'

                                        próxima_palavra_termina_com_as = (
                                            palavras[j + 1].strip(string.punctuation)[-2:] == 'as'
                                        )

                                        if palavra_atual == '2':
                                            if próxima_palavra_termina_com_as:
                                                palavra_atual = 'duas'
                                            else:
                                                palavra_atual = 'dois'
                            else:
                                palavra_atual = número_por_extenso

                # Atualizar palavra em 'palavras'.
                palavras[j] = palavra_atual

        # Atualizar texto_bloco.
        texto_bloco = f"{' '.join(palavras).strip()}\n"
        # Atualizar linha em 'linhas'.
        linhas_pt[i + 1] = texto_bloco

        # Se for FN, transformar em UPPER.
        if número_legenda in set_FNs:
            linhas_pt[i + 1] = texto_bloco.upper()

    return linhas_pt


# OK.
def substituir_caracteres_especiais(caractere, o_que_vai_entrar_no_lugar, linhas_pt):
    for i, linha in enumerate(linhas_pt):

        texto_bloco = linhas_pt[i]

        if re.search(caractere, texto_bloco):
            # Substituir caractere na linha.
            texto_bloco = texto_bloco.replace(caractere, o_que_vai_entrar_no_lugar)
            # Atualizar linha em linhas_pt.
            linhas_pt[i] = texto_bloco
    return linhas_pt


# OK.
# 2,5 toneladas --> duas toneladas e meia.
@loop_linhas_pt
def número_meio(i, linhas_pt, texto_bloco, número_legenda):

    encontrar_meio_na_texto_bloco = re.search(',5', texto_bloco)

    if encontrar_meio_na_texto_bloco:

        palavras = texto_bloco.split()  # Dividir linha em palavras.
        for j, plv in enumerate(palavras[0:-1], start=0):

            palavra_atual = palavras[j]

            if ',5' in palavra_atual:

                ponto = ''

                próxima_palavra = palavras[j + 1]
                próxima_palavra_termina_com_ponto = (
                    próxima_palavra[-1] in [',', '.', '?', '.', '"', ':', '¨']
                )

                if próxima_palavra_termina_com_ponto:
                    ponto = próxima_palavra[-1]

                próxima_palavra_termina_com_a_as = (
                    próxima_palavra.strip(string.punctuation).endswith(('a', 'as'))
                )
                próxima_palavra_termina_com_o_os = (
                    próxima_palavra.strip(string.punctuation).endswith(('o', 'os'))
                )

                if próxima_palavra_termina_com_a_as:
                    # Acrescentar à próxima palavra ' e meia'.
                    # --> 2,5 toneladas. --> 2 toneladas e meia.
                    próxima_palavra = f'{próxima_palavra.strip(string.punctuation)} e meia{ponto}'
                    palavra_atual = palavra_atual.replace(',5', '')

                elif próxima_palavra_termina_com_o_os:
                    próxima_palavra = f'{próxima_palavra.strip(string.punctuation)} e meio{ponto}'
                    palavra_atual = palavra_atual.replace(',5', '')

                # Atualizar palavras em 'palavras'.
                palavras[j] = palavra_atual
                palavras[j + 1] = próxima_palavra
                # Atualizar linha em 'linhas'.
                linhas_pt[i + 1] = f"{' '.join(palavras).strip()}\n"

    # Se for FN, transformar em UPPER.
    if número_legenda in set_FNs:
        linhas_pt[i + 1] = texto_bloco.upper()

    return linhas_pt


# OK.
# Remover ♪ e adicionar itálico se não tiverdef remover_caractere_música(linhas_pt):
@loop_linhas_pt
def remover_caractere_música(i, linhas_pt, texto_bloco, número_legenda):

    encontrar_caractere_música = re.search(u'\u266a', texto_bloco)

    if encontrar_caractere_música:
        # Remover caractere de música e eliminar espaços nas bordas.
        texto_bloco = re.sub(u'\u266a', '', texto_bloco).strip() + '\n'
        # Adicionar legenda atual nos sets de itálicas.
        # (geralmente quando há letra de música, fica em itálico).

        # Atualizar linha em 'linhas'.
        linhas_pt[i + 1] = texto_bloco

        linha_continua_cheia = texto_bloco.strip() != ''

        if linha_continua_cheia:
            set_abrir_itálicas.add((número_legenda, 1))
            set_fechar_itálicas.add((número_legenda, 1))

    return linhas_pt


# Remover totalmente legendas com letra de música, com o caractere ♪.
@loop_linhas_pt
def remover_legenda_música(i, linhas_pt, texto_bloco, número_legenda):
    encontrar_caractere_música = re.search(u'\u266a', texto_bloco)

    if encontrar_caractere_música:
        # Remover texto de texto_bloco para esse bloco da legenda.
        # Ser removido em seguida por uma função do decorator.
        texto_bloco = ''

        # Atualizar linha em linhas_pt.
        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# Passa número para a próxima linha se estiver no final e sem pontuação.

@loop_linhas_pt
def número_para_próxima_linha(i, linhas_pt, texto_bloco, número_legenda):

    exceções_antes_de_número = ['número', 'é']
    legenda_não_é_FN = número_legenda not in set_FNs
    próxima_legenda_não_é_FN = linhas_pt[i + 2].strip() not in set_FNs

    if legenda_não_é_FN and próxima_legenda_não_é_FN:

        for algarismo, número_por_extenso in ls.num_zero_dez:

            # Se encontrar número 0 - 10 por extenso.
            # Ou qualquer outro algarismo no fim da linha, SEM PONTO.
            if re.search(
                fr'\b{re.escape(número_por_extenso)}$|\b\d+$',
                texto_bloco, flags=re.IGNORECASE
            ):

                próxima_linha = linhas_pt[i + 4]
                palavras = texto_bloco.split()  # Dividir linha em palavras.

                if palavras[-2]:  # Se palavra anterior existe.
                    palavra_anterior = palavras[-2]
                    número = palavras[-1].strip()

                    if palavra_anterior not in exceções_antes_de_número:
                        próxima_linha = f'{número} {próxima_linha}'
                        # Remover número da primeira linha.
                        palavras[-1] = ''

                # Atualizar próxima linha.
                linhas_pt[i + 4] = próxima_linha
                # Atualizar linha atual.
                texto_bloco = f"{' '.join(palavras).strip()}\n"
                linhas_pt[i + 1] = texto_bloco
    return linhas_pt


# OK.
# Corrigir traduções 'short answers' (yes, I do, etc) do inglês.
def corrigir_traduções_de_short_answers(linhas_estr, linhas_pt):

    set_legendas_com_short_answers = set()
    # Procurar no original o termo passado na função: "Yes, I do.", "Yes, we do.", etc.

    @loop_linhas_estr
    def encontrar_short_answers_no_original(i, linhas_estr, texto_bloco_estr, número_legenda_estr):

        # Consultar as short answers da lista_short_answers.
        for i, lista in enumerate(lv.lista_short_answers):
            # Atribuir variável a cada item da lista_short_answers.
            # Para acessar o dicionário de cada short answer.
            short_answer_atual = lv.lista_short_answers[i]
            # Atribuir variável à 'short answer' do dicionário atual.
            short_answer = short_answer_atual['short_answer']

            # Procurar short answer da lista_short_answers na linha atual do original.
            if re.search(short_answer, texto_bloco_estr):
                # Salvar número da legenda.

                bloco_é_diálogo = '/' in texto_bloco_estr

                if bloco_é_diálogo:
                    linha_1 = texto_bloco_estr.split('/')[0]
                    linha_2 = texto_bloco_estr.split('/')[1]

                    short_answer_está_linha_1 = re.search(short_answer, linha_1)
                    short_answer_está_linha_2 = re.search(short_answer, linha_2)

                    if short_answer_está_linha_1:
                        set_legendas_com_short_answers.add((número_legenda_estr, 1))
                    elif short_answer_está_linha_2:
                        set_legendas_com_short_answers.add((número_legenda_estr, 2))

                else:
                    set_legendas_com_short_answers.add((número_legenda_estr, 0))

        return linhas_estr
    encontrar_short_answers_no_original(linhas_estr)

    @loop_linhas_pt
    def corrigir_tradução_short_answer_no_pt(i, linhas_pt, texto_bloco, número_legenda):

        # Definir linha anterior: se for a primeira linha de um bloco, são 4 linhas cima;.
        # Se for a segunda linha de um bloco, é uma linha acima.
        linha_anterior = linhas_pt[i - 2]
        # Pegar números das legendas detectadas no original.
        for legenda, linha in set_legendas_com_short_answers:
            # Achar número da legenda no PT.
            if número_legenda == legenda:
                # Encontrar "Sim, você faz" ou similar na legenda indicada (linhas 1 e 2).
                for j, lista in enumerate(lv.lista_short_answers):
                    # Atribuir variáveis para acessar os valores.
                    # Do dicionário de cada short answer.
                    short_answer_atual = lv.lista_short_answers[j]

                    short_answer = short_answer_atual['short_answer']
                    verbo_da_pergunta = short_answer_atual['verbo_anterior']
                    verbo_da_resposta = short_answer_atual['verbo_resposta']
                    posição = short_answer_atual['posição']

                    # Atribuir variáveis a possíveis variações da tradução literal.
                    # (com ou sem vírgula - "Sim eu faço. / Sim, eu faço.".
                    tradução_literal = short_answer_atual['tradução_literal']
                    trad_lit_sem_virg = tradução_literal.replace(',', '')
                    # (com e sem pronome - "Sim, faço.").
                    for pronome in ['eu', 'ele', 'ela', 'nós', 'eles', 'elas']:
                        trad_lit_sem_pron = tradução_literal.replace(f'{pronome} ', '')
                        trad_lit_sem_virg_e_pron = trad_lit_sem_virg.replace(f'{pronome} ', '')
                    for verbo_fazer in [
                        'faço', 'faz', 'fazemos', 'fazem', 'fiz', 'fez', 'fizemos', 'fizeram'
                    ]:
                        trad_lit_sem_verbo_fazer = tradução_literal.replace(f' {verbo_fazer}', '')

                    local_procurar_verbo_pergunta = ''
                    if linha == 0 or linha == 1:
                        local_procurar_verbo_pergunta = linha_anterior
                    elif linha == 2:
                        if '/' in texto_bloco:
                            local_procurar_verbo_pergunta = texto_bloco.split('/')[0]

                    # Procurar a tradução literal da short answer e suas varições.
                    # No texto_bloco atual.
                    if re.search(tradução_literal, texto_bloco) \
                            or re.search(trad_lit_sem_virg, texto_bloco) \
                            or re.search(trad_lit_sem_pron, texto_bloco) \
                            or re.search(trad_lit_sem_virg_e_pron, texto_bloco) \
                            or re.search(trad_lit_sem_verbo_fazer, texto_bloco):

                        # Procurar verbo na lista_geral_de_verbos_conjugados,.
                        # Que é uma lista de dicionários com a conjugação de cada verbo.
                        for k, verbo in enumerate(lv.lista_geral_de_verbos_conjugados):
                            # Atribuir variáveis para detectar os verbos.
                            # Nos tempos verbais corretos de acordo com a lista_short_answers.
                            verbo_atual = lv.lista_geral_de_verbos_conjugados[k]
                            verbo_pergunta = verbo_atual[verbo_da_pergunta]
                            verbo_resposta = verbo_atual[verbo_da_resposta]

                            # Procurar o verbo da pergunta de acordo com a linha.
                            # Guardada em set_legendas_com_short_answers.
                            # If verbo_pergunta in linha_anterior ou primeira linha de diálogo:
                            if verbo_pergunta in local_procurar_verbo_pergunta:
                                if 'Yes' in short_answer:
                                    # Posição 'pré' = (o 'sim' vem no começo).
                                    # Sim, faço. / Sim, fazemos. / etc.
                                    if posição == 'pré':
                                        resposta_pré = f'Sim, {verbo_resposta}.'
                                        # Fazer a substituição de todas as possíveis versões.
                                        # Da tradução literal pelo verbo certo.
                                        texto_bloco = (
                                            texto_bloco.replace(tradução_literal, resposta_pré)
                                            .replace(trad_lit_sem_virg, resposta_pré)
                                            .replace(trad_lit_sem_pron, resposta_pré)
                                            .replace(trad_lit_sem_virg_e_pron, resposta_pré)
                                            .replace(trad_lit_sem_verbo_fazer, resposta_pré)
                                        )
                                    # Posição 'pós' = (o 'sim' vem depois) Faz, sim.
                                    elif posição == 'pós':
                                        resposta_pós = f'{verbo_resposta.capitalize()}, sim.'
                                        texto_bloco = (
                                            texto_bloco.replace(tradução_literal, resposta_pós)
                                            .replace(trad_lit_sem_virg, resposta_pós)
                                            .replace(trad_lit_sem_pron, resposta_pós)
                                            .replace(trad_lit_sem_virg_e_pron, resposta_pós)
                                            .replace(trad_lit_sem_verbo_fazer, resposta_pós)
                                        )
                                        linhas_pt[i + 1] = texto_bloco
                                elif 'No' in short_answer:
                                    resposta_negativa = f'Não, não {verbo_resposta}.'
                                    texto_bloco = (
                                        texto_bloco.replace(tradução_literal, resposta_negativa)
                                        .replace(trad_lit_sem_virg, resposta_negativa)
                                        .replace(trad_lit_sem_pron, resposta_negativa)
                                        .replace(trad_lit_sem_virg_e_pron, resposta_negativa)
                                        .replace(trad_lit_sem_verbo_fazer, resposta_negativa)
                                    )

        linhas_pt[i + 1] = texto_bloco

        return linhas_pt

    linhas_pt = corrigir_tradução_short_answer_no_pt(linhas_pt)

    return linhas_pt


# Adiciona espaço depois de '-' nos diálogos.
@loop_linhas_pt
def diálogos_com_espaço(i, linhas_pt, texto_bloco, número_legenda):

    # Ambas as linhas dos diálogos estão na primeira linha, separadas por '\n.

    # Se a linha começar com '-'.
    if texto_bloco.startswith('-'):
        # Adicionar espaço depois de '-'.
        texto_bloco = re.sub(r'^-', r'- ', texto_bloco)
        texto_bloco = re.sub(r'\n-', r'\n- ', texto_bloco)

    # Atualizar linhas em 'linhas'.
    linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# Devolver itálicas.
@loop_linhas_pt
def devolver_itálicas(i, linhas_pt, texto_bloco, número_legenda):

    linha_1 = linhas_pt[i + 1]
    linha_2 = linhas_pt[i + 2]

    # Tag abrir itálicas <i>.
    for número, linha_abrir_itálicas in set_abrir_itálicas:
        # Se número da legenda estiver no set_abrir_itálicas.
        if número_legenda == número:
            if linha_abrir_itálicas == 1:  # Se for linha 1, abrir na linha 1.
                linha_1 = f'<i>{linha_1}'
            elif linha_abrir_itálicas == 2:  # Se for linha 2.
                # Ver se linha 2 foi removida, se sim, parar.
                if número_legenda in set_linhas_2_esvaziadas:
                    break
                # Se linha 2 estiver vazia, passar tag para a 1.
                elif linha_2.strip() == '':
                    linha_1 = f'<i>{linha_1}'
                # Se linha 2 não estiver vazia, pôr tag na 2.
                elif linha_2.strip() != '':
                    linha_2 = f'<i>{linha_2}'

            # Atualizar linhas 1 e 2 em 'linhas'.
            linhas_pt[i + 1] = linha_1
            linhas_pt[i + 2] = linha_2

    # Tag fechar itálicas </i>.
    for número, linha_fechar_itálicas in set_fechar_itálicas:

        if número_legenda == número:
            if linha_fechar_itálicas == 1:  # Linha 1.
                linha_1 = f'{linha_1.strip()}</i>\n\n'
            elif linha_fechar_itálicas == 2:  # Linha 2.
                # Ver se linha 2 foi removida, se sim, parar.
                if número_legenda.strip() in set_linhas_2_esvaziadas:
                    break
                # Se a linha 2 estiver vazia, passar para a 1.
                elif linha_2.strip() == '':
                    linha_1 = f'{linha_1.strip()}</i>\n'
                # Se a linha 2 não estiver vazia, deixar na 2.
                elif linha_2.strip() != '':
                    linha_2 = f'{linha_2.strip()}</i>\n\n'

            # Atualizar linhas 1 e 2 em 'linhas'.
            linhas_pt[i + 1] = linha_1
            linhas_pt[i + 2] = linha_2

    return linhas_pt


lista_algarismos_zero_a_dez = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

# Coloca ponto em número milhar.


@loop_linhas_pt
def tirar_espaço_milhares(i, linhas_pt, texto_bloco, número_legenda):

    padrão_milhar = r'(\d+) (\d+)'
    encontrar_milhar_texto_bloco = re.search(padrão_milhar, texto_bloco)

    if encontrar_milhar_texto_bloco:

        palavras = texto_bloco.split()
        índice_prim_núm = ''
        índice_próxima_plv = ''
        for j, plv in enumerate(palavras[:-1]):

            encontrar_número = re.search(r'^\d+$', plv)
            if encontrar_número:
                próxima_palavra = palavras[j + 1]
                próxima_palavra_strip = próxima_palavra.strip(string.punctuation)
                próxima_palavra_é_três_dígitos_milhar = (
                    re.search(r'^\d+$', próxima_palavra_strip)
                    and len(próxima_palavra_strip) == 3
                )

                if próxima_palavra_é_três_dígitos_milhar:
                    índice_prim_núm = j
                    índice_próxima_plv = j + 1
        ponto = ''
        # Se o número for de 1 a 10, deixar a próxima função escrever por extenso
        # e transformar '000' em 'mil'.
        if plv in lista_algarismos_zero_a_dez:
            próxima_plv_termina_com_ponto = (
                próxima_palavra[-1] in ['.', ',', '!', ':', '?', '¨']
            )
            if próxima_plv_termina_com_ponto:
                ponto = próxima_palavra[-1]
            próxima_palavra = f'mil{ponto}'
            # Atualizar próxima_palavra em 'palavras'.
            palavras[índice_próxima_plv] = próxima_palavra

        # Se número não for de 0 a 10, deixar como algarismo
        # e separar dos três algarismos do milhar com '.'.
        elif plv not in lista_algarismos_zero_a_dez:
            palavras[índice_prim_núm] = (
                f'{palavras[índice_prim_núm]}.{palavras[índice_próxima_plv]}'
            )
            # Deletar o item do segundo número de 'palavras'.
            del palavras[índice_próxima_plv]
        # Atualizar texto_bloco.
        texto_bloco = ' '.join(palavras)
        # Atualizar linha em linhas_pt.
        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


# OK.
# Devolver {\an8}.
@loop_linhas_pt
def devolver_top_center(i, linhas_pt, texto_bloco, número_legenda):

    for número in set_top_center:
        # Se número da legenda estiver no set_top_center.
        if número_legenda == número:
            texto_bloco = '{\\an8}' + texto_bloco  # Adicionar {\an8} à linha 1.

    # Atualizar linha 1.
    linhas_pt[i + 1] = texto_bloco
    return linhas_pt


def pôr_linha_vazia_entre_blocos(linhas_pt):
    for i, linha in enumerate(linhas_pt):
        # Definir linha do timestamp como referência.
        if '-->' in linhas_pt[i]:
            # Adicionar uma linha vazia depois de cada texto_bloco.
            linhas_pt[i - 1] = f'{linhas_pt[i - 1]}'
            linhas_pt[i] = f'{linhas_pt[i]}'
            linhas_pt[i + 1] = f'{linhas_pt[i + 1]}\n'
    return linhas_pt


@loop_linhas_pt
def quebrar_linhas_de_diálogo(i, linhas_pt, texto_bloco, número_legenda):

    # Quebrar diálogo.
    bloco_é_diálogo = '/' in texto_bloco
    if bloco_é_diálogo:

        linha_1 = texto_bloco.split('/')[0]
        linha_2 = texto_bloco.split('/')[1]
        # Tirar '/' e pôr as '-' e quebra de linha.
        texto_bloco = f'-{linha_1.strip()}\n-{linha_2.strip()}\n\n'
        # Atualizar texto_bloco em linhas_pt.
        linhas_pt[i + 1] = texto_bloco

    return linhas_pt


@loop_linhas_pt
def quebrar_linhas(i, linhas_pt, texto_bloco, número_legenda):
    tamanho_texto_bloco = len(texto_bloco)
    tamanho_máximo = int(reps.tamanho_máximo_de_linha)
    exceções_quebra = {
        # Verbos
        'apoio', 'atestado', 'como', 'entre', 'para', 'sobre', 'sua', 'vestido'}
    # Evitar os diálogos.
    if not texto_bloco.startswith('-'):
        # Ver se tamanho do texto_bloco é maior que o tamanho máximo permitido de linha.
        if tamanho_texto_bloco > tamanho_máximo:

            # Excluir o último caractere do texto_bloco (um possível ponto) e \n
            # para procurar outros pontos.
            texto_bloco_meio = texto_bloco[:-4]

            # Quebrar em algum ponto próximo do limite.
            lista_de_pontos = []
            # Procurar pontuação no meio do texto_bloco.
            for j, caractere in enumerate(texto_bloco_meio):
                for ponto in ['!', ',', '?', '.', ':', '¨']:
                    if ponto in caractere:
                        if ponto == '.':
                            caractere_anterior = texto_bloco_meio[j - 1]

                            # Variáveis com os caracteres anteriores ao ponto
                            # para evitar abreviações de títulos.
                            duas_letras_atrás_juntas = (
                                texto_bloco_meio[j - 2] + texto_bloco_meio[j - 1]
                            )
                            três_letras_atrás_juntas = (
                                texto_bloco_meio[j - 3] + texto_bloco_meio[j - 2]
                                + texto_bloco_meio[j - 1]
                            )
                            quatro_letras_atrás_juntas = (
                                texto_bloco_meio[j - 4] + texto_bloco_meio[j - 3] +
                                texto_bloco_meio[j - 2] + texto_bloco_meio[j - 1]
                            )

                            if not re.search(r'[0-9]', caractere_anterior):
                                if j + 1 < len(texto_bloco_meio):

                                    não_é_título_2 = (
                                        duas_letras_atrás_juntas.lower() not in ['dr', 'sr']
                                    )
                                    não_é_título_3 = (
                                        três_letras_atrás_juntas.lower() not in ['dra', 'sra']
                                    )
                                    não_é_título_4 = (
                                        quatro_letras_atrás_juntas.lower() not in ['srta']
                                    )
                                    if não_é_título_2 and não_é_título_3 and não_é_título_4:
                                        índice_ponto = j
                                        lista_de_pontos.append((ponto, índice_ponto))
                        # Se for outro ponto, sem ser '.'.
                        else:
                            índice_ponto = j
                            lista_de_pontos.append((ponto, índice_ponto))

            # Ver se o índice dos pontos (do fim da frase para o começo)
            # é menor que o tamanho máximo.
            for ponto, índice in reversed(lista_de_pontos):
                if índice <= tamanho_máximo:
                    # Ver se depois desse ponto o resto do texto_bloco tem tamanho permitido.
                    índice_dps_pto = índice + 1
                    índice_dps_pto_sem_espaço = índice + 2
                    texto_bloco_até_pto = f'{texto_bloco[:índice_dps_pto]}'
                    texto_bloco_dps_pto = f'{texto_bloco[índice_dps_pto_sem_espaço:]}'
                    tamanho_da_sobra_ok = len(texto_bloco_dps_pto) < tamanho_máximo
                    if tamanho_da_sobra_ok:
                        texto_bloco = f'{texto_bloco_até_pto}\n{texto_bloco_dps_pto}'
                        linhas_pt[i + 1] = f'{texto_bloco.strip()}\n\n'
                        break

            # Ver se a quebra de linha já ocorreu, procurando '\n' no texto_bloco_strip.
            if not re.search(r'\n', texto_bloco.strip()):

                # Quebrar em palavra se não tiver ponto.
                palavras = texto_bloco.split()
                soma_palavras = 0
                índice_palavra_que_excede = 0

                # Iterar nas palavras da frase para achar a palavra que excede o tamanho máximo.
                for j, plv in enumerate(palavras):
                    tamanho_palavra = len(palavras[j])
                    soma_palavras = soma_palavras + tamanho_palavra
                    # Contar número de espaços até antes da palavra que excede,.
                    # Para que o espaço depois dela não seja contado como um caractere válido.
                    espaço_entre_palavras = 1
                    soma_palavras = soma_palavras + espaço_entre_palavras
                    # Subtrair o espaço depois da palavra que excede.
                    soma_palavras_menos_último_espaço = soma_palavras - 1
                    if soma_palavras_menos_último_espaço >= tamanho_máximo:
                        índice_palavra_que_excede = j + 1
                        break

                if 'que' == palavras[j]:
                    # Se 'que' estiver entre a quarta palavra da linha e a palavra que excede.
                    índice_que = palavras[3:índice_palavra_que_excede].index('que')
                    # Quebrar antes de 'que'.
                    palavras[índice_que + 3] = '\nque'
                    # Atualizar texto_bloco.
                    texto_bloco = f'{" ".join(palavras)}\n\n'
                    # Atualizar linha em linhas_pt.
                    linhas_pt[i + 1] = texto_bloco

                # Se não tiver 'que' da quarta palavra para frente.
                else:
                    # Iterar da palavra que excede o tamanho máximo para trás.
                    for j, plv in reversed(list(enumerate(palavras[:índice_palavra_que_excede]))):
                        quebrar_em = ''

                        # Se a palavra anterior for verbo, quebrar na palavra atual.
                        if palavras[j - 1] in lv.set_geral_de_verbos_conjugados \
                                and palavras[j - 1] not in exceções_quebra:
                            quebrar_em = 'atual'

                        # Ver se a palavra atual é preposição,
                        # conjunção ou outra palavra de quebra.
                        elif palavras[j] in ls.palavras_de_quebra:
                            # Ver se a anterior também é palavra de quebra e quebrar antes dela.
                            if palavras[j - 1] in ls.palavras_de_quebra:
                                quebrar_em = 'anterior'
                            # Senão, quebrar antes da atual.
                            else:
                                quebrar_em = 'atual'

                        if quebrar_em == 'atual':
                            # Adicionar quebra antes da palavra atual.
                            palavras[j] = f'\n{palavras[j]}'
                            # Atualizar texto_bloco.
                            texto_bloco = f"{' '.join(palavras)}\n\n"
                            # Atualizar linha em linhas_pt.
                            linhas_pt[i + 1] = texto_bloco
                            break

                        elif quebrar_em == 'anterior':
                            # Adicionar quebra de linha nesta palavra.
                            palavras[j - 1] = f'\n{palavras[j - 1]}'
                            # Atualizar texto_bloco.
                            texto_bloco = f"{' '.join(palavras)}\n\n"
                            # Atualizar linha em linhas_pt.
                            linhas_pt[i + 1] = texto_bloco
                            break
    return linhas_pt


def recontar_números(linhas_pt):

    @loop_linhas_pt
    def zerar_números(i, linhas_pt, texto_bloco, número_legenda):
        número_legenda = 1
        # Atualizar número em linhas_pt.
        linhas_pt[i - 1] = f'{número_legenda}\n'
        return linhas_pt
    linhas_pt = zerar_números(linhas_pt)

    contagem = 0

    def recontar(linhas_pt, contagem):
        for i, linha in enumerate(linhas_pt):
            if '-->' in linhas_pt[i]:
                contagem = contagem + 1
                número_legenda = contagem
                número_legenda = f'{contagem}\n'
                # Atualizar número_legenda in linhas_pt.
                linhas_pt[i - 1] = número_legenda

        return linhas_pt
    recontar(linhas_pt, contagem)

    return linhas_pt
