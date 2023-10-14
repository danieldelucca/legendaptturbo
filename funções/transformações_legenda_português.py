import reps, logo as lg, funções_de_transformações as fu
import tkinter as tk
from tkinter import filedialog


print(f'{lg.logo}\n\n')

# -------- menu de abertura dos arquivos ------- #

input('  Digite Enter para abrir a legenda em português.\n'
      '  Se você utilizou o passo 1 deste programa, selecione a legenda prévia em português.\n')

# Abrir legenda em português.
legenda_pt = fu.selecionar_arquivo_legenda('português')

print('\n  Abrir legenda em idioma estrangeiro - '
      'opcional para algumas funcionalidades (ver arquivo LEIAME.txt)\n'
      '  Se você utilizou o passo 1 deste programa, selecione a legenda prévia em idioma estrangeiro.\n')

print('    Digite:')
print("    >> A + Enter --> abrir.")
print("    >> Enter --> continuar sem legenda em idioma estrangeiro")

arquivo_leg_estrangeira = ''
não_há_legenda_estrangeira = False

# Menu para abrir legenda em idioma estrangeiro.
menu_abrir_estrangeira = input()
if menu_abrir_estrangeira.lower() == 'a':
    legenda_estrangeira = fu.selecionar_arquivo_legenda('idioma estrangeiro')
else:
    não_há_legenda_estrangeira = True
    legenda_estrangeira = legenda_pt


# ---------- menu abertura dos arquivos -------------- #

print('  Iniciando transformações...\n')

# O script irá trabalhar com duas legendas:
# - uma em outro idioma (espanhol, inglês, etc) --> "legenda estrangeira".
# - uma traduzida em português --> "legenda português".

# Função que abriga todas as funções do script.
# Em algumas funções, há um comentário com a indicação '!!!',
# apontando que a função deve vir antes ou depois de alguma outra.


def corrigir_legenda(legenda_pt, legenda_estrangeira):

    # Listas para armazenar as legendas sem linhas vazias
    # e com as duas linhas de texto de cada bloco unificadas.
    linhas_pt = []  # Linhas da legenda PT.
    linhas_estr = []  # Linhas da legenda estrangeira.

    # Arrumar tags de itálico maiúsculas. '<I></I>' --> '<i></i>'
    # !!! Antes de registrar ocorrências de itálicas.
    legenda_pt = fu.corrigir_tags_de_itálico_maiúsculas(legenda_pt)

    # Adiciona três linhas no final.
    # (para evitar 'index error' em algumas funções).
    legenda_pt = fu.pôr_linhas_no_fim(legenda_pt)

    # Registra num set legendas com <i> e </i> e a linha do bloco em que estão.
    # !!! Depois de corrigir_tags_de_itálico_maiúsculas.
    # !!! Antes de todas as outras funções.
    fu.registrar_ocorrências_de_itálicas(legenda_pt)

    # !!! Antes de todas as funções que usem o decorator @loop_linhas_estr.
    # Junta as duas linhas de texto de cada bloco da legenda estrangeira.
    fu.juntar_linhas_de_texto(legenda_estrangeira, linhas_estr)

    # !!! Antes de todas as funções que mexam com 'linhas_pt'.
    # Junta as duas linhas de texto de cada bloco da legenda PT.
    fu.juntar_linhas_de_texto(legenda_pt, linhas_pt)

    # Remover '¡' e '¿' que pode ficar do espanhol na legenda PT.
    linhas_pt = fu.remover_pontos_invertidos_espanhol(linhas_pt)

    # Adiciona três linhas no final.
    # (para evitar 'index error' em algumas funções).
    linhas_pt = fu.pôr_linhas_no_fim(linhas_pt)

    # Substituir temporariamente '...' por '¨' (trema).
    linhas_pt = fu.subsitutir_reticências_por_trema(linhas_pt)

    # Remover temporariamente <i> e </i>.
    linhas_pt = fu.recolher_itálicas(linhas_pt)

    # !!! antes de qualquer uma que use o decorator @loops_linhas_estr.
    # Corrige espaços antes de pontos nas legendas em outro idioma.
    linhas_estr = fu.remover_closed_captions(linhas_estr)

    # !!! antes de qualquer uma que use o decorator @loops_linhas_estr...
    # Corrige espaços antes de pontos nas legendas em outro idioma.
    linhas_estr = fu.remover_nomes_closed_captions(linhas_estr)

    # Remover closed captions [] da legenda PT.
    linhas_pt = fu.remover_closed_captions(linhas_pt)

    # Tirar nomes dos personagens de antes das falas da legenda PT.
    # DAVID: Onde estou?.
    linhas_pt = fu.remover_nomes_closed_captions(linhas_pt)

    # !!! antes de qualquer uma que use o decorator @original...
    # Corrige espaços antes de pontos nas legendas em outro idioma.
    linhas_estr = fu.corrigir_espaço_pontuação_legenda_estrangeira(linhas_estr)

    # Corrige espaços antes de pontos nas legendas PT.
    linhas_pt = fu.corrigir_espaço_pontuação_legenda_pt(linhas_pt)

    # Recolher diálogos.
    # Registra num set ocorrências de diálogos e remove as '-', deixando apenas '/'.
    # Para demarcar quebra de linha.
    linhas_pt = fu.recolher_diálogos(linhas_pt)
    linhas_estr = fu.recolher_diálogos(linhas_estr)

    # Substituições sem limite de palavra (subst_sem_limite_palavra.txt).
    linhas_pt = fu.substuições_sem_limite_de_palavra(linhas_pt)

    # Remover linhas com certas palavras, créditos, etc.
    linhas_pt = fu.remover_linhas_com_créditos_e_outros(linhas_pt)

    # !!! antes das substituições case sensitive e case insensitive.
    if não_há_legenda_estrangeira is False:
        # Se não há um arquivo de legenda em outro idioma em configurar.txt.
        linhas_pt = fu.traduções_específicas_de_frases(linhas_pt, linhas_estr)

    if reps.remover_palavras_repetidas is True:
        # Remover palavras repetidas separadas por ','.
        # (Evita vícios legendas muito fiéis do espanhol.).
        linhas_pt = fu.remover_palavras_repetidas_separadas_vírgula(linhas_pt)

    # Trocar l por I em palavras totalmente maiúsculas.
    # RlTMO -> RITMO.
    linhas_pt = fu.corrigir_l_I(linhas_pt)

    # Consertar linhas apenas com "I...", do inglês,
    # Erroneamente traduzido como "EU...".
    # !!! Antes de listar_FNs.
    linhas_pt = fu.corrigir_linha_apenas_com_eu(linhas_pt)

    # !!! antes de remover_nomes_closed_captions.
    # Identificar e listar legendas FN.
    linhas_pt = fu.listar_FNs(linhas_pt)

    # Recolher {\an8} temporariamente (legenda para cima, no centro).
    linhas_pt = fu.recolher_top_center(linhas_pt)

    # Arrumar espaços duplos.
    # Eles estavam ---> Eles estavam.
    linhas_pt = fu.corrigir_espaços_duplos(linhas_pt)

    # Remover '...'.
    if reps.remover_reticências_do_começo is True:
        linhas_pt = fu.remover_reticências_começo(linhas_pt)
    if reps.remover_reticências_do_fim is True:
        linhas_pt = fu.remover_reticências_fim(linhas_pt)

    # !!! depois de recolher todas as tags.
    # Identificar nomes de pessoas, corrigir maiúsculas e destraduzir.
    linhas_pt = fu.nomes_próprios(linhas_pt, linhas_estr)

    # !!! antes das substituições.
    # Ah mas nós... --> Mas nós... / Ah, mas nós... --> Mas nós...
    if reps.remover_interjeições is True:
        linhas_pt = fu.remover_ah_ei_ai(linhas_pt)

    # Troca o gerúndio de Portugal pelo brasileiro:
    # Estava a fazer --> estava fazendo.
    if reps.transformar_gerúndio is True:
        linhas_pt = fu.transformar_gerúndio_português_em_brasileiro(linhas_pt)

    # Conserta imperativos traduzidos do inglês como infinitivos.
    # Come. --> Vir. --> Venha.
    linhas_pt = fu.corrigir_imperativos_traduzidos_como_infinitivos(linhas_pt)

    # !!! antes de remover_caractere_música.
    # Remover totalmente as legendas com letra de música com ♪.
    if reps.remover_legenda_música is True:
        linhas_pt = fu.remover_legenda_música(linhas_pt)

    # !!! antes de quebrar_antes e de números_para_próxima.
    # !!! depois de remover_levenda_música.
    # Remover ♪ e adicionar itálico se não tiver.
    if reps.remover_caract_música is True:
        linhas_pt = fu.remover_caractere_música(linhas_pt)

    # !!! antes de fix_casing.
    # !!! antes do verb back.
    # !!! antes de juntar linhas curtas.
    # A gente vai --> vamos / a gente foi --> fomos.
    if reps.transformar_a_gente_em_nos is True:
        linhas_pt = fu.transformar_a_gente_em_nós(linhas_pt)

    # NÚMEROS.

    # !!! antes das outras funções de números.
    # Tirar espaço entre números quando foram milhares.
    linhas_pt = fu.tirar_espaço_milhares(linhas_pt)

    # Trocar ½ por ,5.
    linhas_pt = fu.substituir_caracteres_especiais(u'\u00BD', ',5', linhas_pt)

    # !!! antes de num_zero_dez.
    # 2,5 toneladas --> duas toneladas e meia.
    linhas_pt = fu.número_meio(linhas_pt)

    # Escreve por extenso números de zero a dez.
    linhas_pt = fu.número_zero_dez_por_extenso(linhas_pt)

    # !!! antes de quebrar_antes.
    # !!! depois de número_zero_dez.
    # Passa número para a próxima linha se estiver no final e sem pontuação.
    linhas_pt = fu.número_para_próxima_linha(linhas_pt)

    # Escreve números por extenso de 11 a 100 em começos de frase.
    linhas_pt = fu.número_começo_por_extenso(linhas_pt)

    # Remover o pronome reflexivo 'se' dos verbos 'lembrar', 'abaixar', 'deitar'.
    if reps.remover_reflexivo is True:
        linhas_pt = fu.remover_reflexivo_opcional(linhas_pt)

    # !!! antes das substituições.
    # 'ajude-me' --> 'me ajude', 'amo-te' --> 'te amo', etc.
    #
    if reps.transformar_ênclise is True:
        linhas_pt = fu.pronomes_oblíquos_para_antes(linhas_pt)

    if não_há_legenda_estrangeira is False:
        # !!! antes das substituições.
        # Yes, I do --> sim, eu faço --> sim, eu + verbo correto.
        linhas_pt = fu.corrigir_traduções_de_short_answers(linhas_estr, linhas_pt)

    # Separa os nomes detectados em masculino e feminino para as próximas funções.
    linhas_pt = fu.separar_nomes_por_gênero(linhas_pt)

    # Abrevia títulos antes de nomes próprios.
    # Senhor João --> Sr. João.
    linhas_pt = fu.abreviar_títulos(linhas_pt)

    # Adiciona artigos antes dos nomes em certos contextos.
    # !!! antes das substituições.
    # !!! antes de corrigir_maiúsculas.
    linhas_pt = fu.pôr_artigos_antes_de_nomes_e_títulos(linhas_pt)
  
    # De João --> do João.
    if reps.transformar_de_em_do_da is True:
        linhas_pt = fu.transformar_de_em_da_ou_do(linhas_pt)

    # Para que ela faça --> para ela fazer.
    linhas_pt = fu.transformar_para_que_faça_em_para_fazer(linhas_pt)

    # Para que ela faça --> para ela fazer.
    linhas_pt = fu.transformar_sem_que_faça_em_sem_fazer(linhas_pt)

    if reps.transformar_mais_do_que_em_mais_que is True:
        # 'mais caro do que' --> 'mais caro que'
        linhas_pt = fu.transformar_mais_do_que_em_mais_que(linhas_pt)

    if reps.transformar_para_você_em_te is True:
        # Transforma 'para você' e 'a você' em 'te'.
        # 'disse a você' --> 'te disse'
        # 'devolvi para você' --> 'te devolvi'
        linhas_pt = fu.transformar_para_você_em_te(linhas_pt)

    # Substituições a serem feitas em começos de perguntas.
    # Substituições_começo_de_pergunta.txt.
    linhas_pt = fu.substituições_começo_de_pergunta(linhas_pt)

    # !!! antes de substituições_case_sensitive.
    # Faz substituições se o termo não tiver pontuação em seguida,.
    # Ou seja, se o termo não estiver no fim de uma frase.
    linhas_pt = fu.substituições_sem_pontuação(linhas_pt)

    # !!! antes de substituições_case_sensitive.
    # !!! depois de subst_sem_pontuação.
    linhas_pt = fu.substituições_case_insensitive(linhas_pt)

    # !!! antes de substituições_case_sensitive.
    # Arrumar maiúsculas depois de pontuação.
    # Ocorrência 1/2.
    if reps.corrigir_maiúsculas_pontuação is True:
        linhas_pt = fu.corrigir_maiúsculas_depois_de_pontuação(linhas_pt)

    # !!! depois de substituições_case_insensitive.
    # !!! depois de corrigir_maiúsculas_depois_de_pontuação.
    linhas_pt = fu.substituições_case_sensitive(linhas_pt)

    # !!! depois das substituições.
    # Amo você ---> Te amo.
    if reps.transformar_você is True:
        linhas_pt = fu.transformar_você_em_te(linhas_pt)

    # Põe vírgula antes da última palavra.
    linhas_pt = fu.vírgula_antes_de_sim_não_em_fim_de_frase(linhas_pt)

    # Faz substituições específicas indicadas em configurar.txt.
    linhas_pt = fu.substituições_específicas(linhas_pt)

    if reps.remover_frase_repetida is True:
        # Se houver frases repetidas, remove a primeira.
        # Não atire! Não atire! --> Não atire!.
        linhas_pt = fu.remover_frase_repetida_do_mesmo_bloco(linhas_pt)

    # !!! antes de devolver diálogos.
    # Remove linhas em que sobrou apenas um ponto.
    linhas_pt = fu.remover_linhas_só_com_um_ponto(linhas_pt)

    # Arrumar dupla pontuação .. ?? !! ,, --.
    linhas_pt = fu.corrigir_dupla_pontuação(linhas_pt)

    linhas_pt = fu.pôr_linha_vazia_entre_blocos(linhas_pt)

    # Ocorrência 2/2.
    if reps.corrigir_maiúsculas_pontuação is True:
        linhas_pt = fu.corrigir_maiúsculas_depois_de_pontuação(linhas_pt)

    if reps.transformar_reticências_em_dois_hífens is True:
        # Transformar '...' em '--'
        linhas_pt = fu.transformar_reticências_em_dois_hífens(linhas_pt)

    # Substituir de volta '¨' (trema) por '...'.
    linhas_pt = fu.devolver_reticências(linhas_pt)

    # Quebra texto_bloco em duas linhas nas legendas de texto longo.
    linhas_pt = fu.quebrar_linhas_de_diálogo(linhas_pt)

    # Põe espaço depois de '-' nos diálogos.
    if reps.diálogos_com_espaço is True:
        linhas_pt = fu.diálogos_com_espaço(linhas_pt)

    # Transformar texto_bloco em duas linhas, se ele exceder o tamanho máximo permitido.
    linhas_pt = fu.quebrar_linhas(linhas_pt)

    # !!! antes de devolver diálogos.
    # Devolver <i> e </i>.
    linhas_pt = fu.devolver_itálicas(linhas_pt)

    # Devolver {\an8}.
    linhas_pt = fu.devolver_top_center(linhas_pt)

    linhas_pt = fu.recontar_números(linhas_pt)

    return linhas_pt


linhas_pt = corrigir_legenda(legenda_pt, legenda_estrangeira)

print('\n\n  >> Nomes masculinos identificados:')
for i, nome in enumerate(reps.set_nomes_masculinos):
    if i == 0:
        print('  ', end='')
    else:
        print(',', end=' ')
    print(nome, end='')

print('\n\n  >> Nomes femininos identificados:')
for i, nome in enumerate(reps.set_nomes_femininos):
    if i == 0:
        print('  ', end='')
    else:
        print(',', end=' ')
    print(nome, end='')

print('\n\n  Agora vamos salvar o arquivo da legenda final.\n')
input('  Digite Enter para continuar.\n')


def salvar_srt():
    novo_arquivo = (
        filedialog.asksaveasfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
    )

    if novo_arquivo:
        with open(novo_arquivo, "w", encoding='utf-8') as file:
            file.write(legenda_final)
            print(f'  Arquivo salvo com sucesso:\n  {novo_arquivo}')

    else:
        print('  Salve o arquivo .srt na janela que vamos abrir.')
        input('  Digite Enter para continuar.\n')
        salvar_srt()
legenda_final = ''.join(linhas_pt)


salvar_srt()

print('\n\n  Caso deseje, adicione em configurar.txt nomes não detectados pelo programa\n'
      '  e rode-o novamente para que sejam adicionados artigos corretamente.\n\n')
input('  Obrigado por usar o Legenda PT Turbo.\n  Digite Enter para sair.')
exit()
