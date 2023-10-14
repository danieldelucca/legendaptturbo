import os

# detectar a pasta das funções
pasta_funções = os.path.dirname(os.path.abspath(__file__))
# detectar pasta home do script


# ler lista de verbos do arquivo configurações/lista_de_verbos.txt
# para montar as conjugações dos verbos a serem usadas nas funções
set_verbos_no_infinitivo = set()
caminho_lista_de_verbos = (
    os.path.join(pasta_funções, '..', 'configurações', 'lista_de_verbos.txt')
)
with open(caminho_lista_de_verbos, 'r', encoding='utf-8') as file:
    lista_verbos_no_inifinitivo = file.readlines()
# adicionar verbos ao set_verbos_no_infinitivo
# depois esses verbos serão conjugados e outro set será gerado
[set_verbos_no_infinitivo.add(verbo.strip()) for verbo in lista_verbos_no_inifinitivo]

# ler lista de verbos do arquivo configurações/lista_de_verbos_transitivos_diretos.txt
set_verbos_transitivos_diretos = set()
# transformar lista_de_verbos_transitivos_diretos.txt no set_verbos_tran
caminho_lista_de_verbos_trans_dir = (
    os.path.join(pasta_funções, '..', 'configurações', 'lista_de_verbos_transitivos_diretos.txt')
)
with open(caminho_lista_de_verbos_trans_dir, 'r', encoding='utf-8') as file:
    lista_verbos_trans_dir = file.readlines()
# adicionar verbos ao set_verbos_transitivos_diretos
# depois esses verbos serão conjugados e outro set será gerado
[set_verbos_transitivos_diretos.add(verbo.strip()) for verbo in lista_verbos_trans_dir]


# função para criar listas de verbos conjugados
# será criada abaixo uma lista com todos os verbos
# e outra apenas com verbos transitivos diretos
# para uso na função que transforma "peguei você" --> "te peguei"
def criar_lista_de_verbos(set_de_verbos, lista_de_verbos_conjugados):

    for verbo in set_de_verbos:
        if verbo.endswith(('ar', 'er', 'ir', 'or')):
            # verbos terminados em -AR e variações
            # -EAR, -ÇAR, etc, têm que vir antes de -AR

            # cear, cercear
            if verbo.endswith('ear'):
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}armos',
                                   'inf_3p': f'{radical}arem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}io',
                                   'pres_ind_2s': f'{radical}ias',
                                   'pres_ind_3s': f'{radical}ia',
                                   'pres_ind_1p': f'{radical}amos',
                                   'pres_ind_3p': f'{radical}iam',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}ei',
                                   'pret_per_2s': f'{radical}aste',
                                   'pret_per_3s': f'{radical}ou',
                                   'pret_per_1p': f'{radical}amos',
                                   'pret_per_3p': f'{radical}aram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ava',
                                   'pret_imp_2s': f'{radical}avas',
                                   'pret_imp_3s': f'{radical}ava',
                                   'pret_imp_1p': f'{radical}ávamos',
                                   'pret_imp_3p': f'{radical}avam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}arei',
                                   'fut_2s': f'{radical}arás',
                                   'fut_3s': f'{radical}ará',
                                   'fut_1p': f'{radical}aremos',
                                   'fut_3p': f'{radical}arão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}aria',
                                   'fut_pret_2s': f'{radical}arias',
                                   'fut_pret_3s': f'{radical}aria',
                                   'fut_pret_1p': f'{radical}aríamos',
                                   'fut_pret_3p': f'{radical}ariam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}ie',
                                   'sub_pres_2s': f'{radical}ies',
                                   'sub_pres_3s': f'{radical}ie',
                                   'sub_pres_1p': f'{radical}emos',
                                   'sub_pres_3p': f'{radical}iem',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}asse',
                                   'sub_pret_2s': f'{radical}asses',
                                   'sub_pret_3s': f'{radical}asse',
                                   'sub_pret_1p': f'{radical}ássemos',
                                   'sub_pret_3p': f'{radical}assem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ar',
                                   'sub_fut_2s': f'{radical}ares',
                                   'sub_fut_3s': f'{radical}ar',
                                   'sub_fut_1p': f'{radical}armos',
                                   'sub_fut_3p': f'{radical}arem',
                                   # imperativo
                                   'imp_2s': f'{radical}a',
                                   'imp_3s': f'{radical}e',
                                   'imp_1p': f'{radical}emos',
                                   'imp_3p': f'{radical}em',
                                   # gerúndio
                                   'ger': f'{radical}ando',
                                   # particípio
                                   'part': f'{radical}ado'
                                   }

            # almoçar, coçar, dançar
            elif verbo.endswith('çar'):     # dançar
                radical = verbo[:-2]        # danç (danço)
                radical2 = f'{verbo[:-3]}c'     # danc (dance)
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}armos',
                                   'inf_3p': f'{radical}arem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}as',
                                   'pres_ind_3s': f'{radical}a',
                                   'pres_ind_1p': f'{radical}amos',
                                   'pres_ind_3p': f'{radical}am',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical2}ei',
                                   'pret_per_2s': f'{radical}aste',
                                   'pret_per_3s': f'{radical}ou',
                                   'pret_per_1p': f'{radical}amos',
                                   'pret_per_3p': f'{radical}aram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ava',
                                   'pret_imp_2s': f'{radical}avas',
                                   'pret_imp_3s': f'{radical}ava',
                                   'pret_imp_1p': f'{radical}ávamos',
                                   'pret_imp_3p': f'{radical}avam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}arei',
                                   'fut_2s': f'{radical}arás',
                                   'fut_3s': f'{radical}ará',
                                   'fut_1p': f'{radical}aremos',
                                   'fut_3p': f'{radical}arão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}aria',
                                   'fut_pret_2s': f'{radical}arias',
                                   'fut_pret_3s': f'{radical}aria',
                                   'fut_pret_1p': f'{radical}aríamos',
                                   'fut_pret_3p': f'{radical}ariam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}e',
                                   'sub_pres_2s': f'{radical2}es',
                                   'sub_pres_3s': f'{radical2}e',
                                   'sub_pres_1p': f'{radical2}emos',
                                   'sub_pres_3p': f'{radical2}em',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}asse',
                                   'sub_pret_2s': f'{radical}asses',
                                   'sub_pret_3s': f'{radical}asse',
                                   'sub_pret_1p': f'{radical}ássemos',
                                   'sub_pret_3p': f'{radical}assem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ar',
                                   'sub_fut_2s': f'{radical}ares',
                                   'sub_fut_3s': f'{radical}ar',
                                   'sub_fut_1p': f'{radical}armos',
                                   'sub_fut_3p': f'{radical}arem',
                                   # imperativo
                                   'imp_2s': f'{radical}a',
                                   'imp_3s': f'{radical2}e',
                                   'imp_1p': f'{radical2}emos',
                                   'imp_3p': f'{radical2}em',
                                   # gerúndio
                                   'ger': f'{radical}ando',
                                   # particípio
                                   'part': f'{radical}ado'
                                   }

            # brincar, ficar
            elif verbo.endswith('car'):     # brincar
                radical = verbo[:-2]        # brinc (brinco)
                radical2 = f'{verbo[:-3]}qu'     # brinq (brinque)
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}armos',
                                   'inf_3p': f'{radical}arem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}as',
                                   'pres_ind_3s': f'{radical}a',
                                   'pres_ind_1p': f'{radical}amos',
                                   'pres_ind_3p': f'{radical}am',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical2}ei',
                                   'pret_per_2s': f'{radical}aste',
                                   'pret_per_3s': f'{radical}ou',
                                   'pret_per_1p': f'{radical}amos',
                                   'pret_per_3p': f'{radical}aram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ava',
                                   'pret_imp_2s': f'{radical}avas',
                                   'pret_imp_3s': f'{radical}ava',
                                   'pret_imp_1p': f'{radical}ávamos',
                                   'pret_imp_3p': f'{radical}avam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}arei',
                                   'fut_2s': f'{radical}arás',
                                   'fut_3s': f'{radical}ará',
                                   'fut_1p': f'{radical}aremos',
                                   'fut_3p': f'{radical}arão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}aria',
                                   'fut_pret_2s': f'{radical}arias',
                                   'fut_pret_3s': f'{radical}aria',
                                   'fut_pret_1p': f'{radical}aríamos',
                                   'fut_pret_3p': f'{radical}ariam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}e',
                                   'sub_pres_2s': f'{radical2}es',
                                   'sub_pres_3s': f'{radical2}e',
                                   'sub_pres_1p': f'{radical2}emos',
                                   'sub_pres_3p': f'{radical2}em',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}asse',
                                   'sub_pret_2s': f'{radical}asses',
                                   'sub_pret_3s': f'{radical}asse',
                                   'sub_pret_1p': f'{radical}ássemos',
                                   'sub_pret_3p': f'{radical}assem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ar',
                                   'sub_fut_2s': f'{radical}ares',
                                   'sub_fut_3s': f'{radical}ar',
                                   'sub_fut_1p': f'{radical}armos',
                                   'sub_fut_3p': f'{radical}arem',
                                   # imperativo
                                   'imp_2s': f'{radical}a',
                                   'imp_3s': f'{radical2}e',
                                   'imp_1p': f'{radical2}emos',
                                   'imp_3p': f'{radical2}em',
                                   # gerúndio
                                   'ger': f'{radical}ando',
                                   # particípio
                                   'part': f'{radical}ado'
                                   }

            # alugar, alagar
            elif verbo.endswith('gar'):     # alugar
                radical = verbo[:-2]        # alug (alugo)
                radical2 = f'{verbo[:-3]}gu'     # alugu (alugue)
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}armos',
                                   'inf_3p': f'{radical}arem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}as',
                                   'pres_ind_3s': f'{radical}a',
                                   'pres_ind_1p': f'{radical}amos',
                                   'pres_ind_3p': f'{radical}am',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical2}ei',
                                   'pret_per_2s': f'{radical}aste',
                                   'pret_per_3s': f'{radical}ou',
                                   'pret_per_1p': f'{radical}amos',
                                   'pret_per_3p': f'{radical}aram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ava',
                                   'pret_imp_2s': f'{radical}avas',
                                   'pret_imp_3s': f'{radical}ava',
                                   'pret_imp_1p': f'{radical}ávamos',
                                   'pret_imp_3p': f'{radical}avam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}arei',
                                   'fut_2s': f'{radical}arás',
                                   'fut_3s': f'{radical}ará',
                                   'fut_1p': f'{radical}aremos',
                                   'fut_3p': f'{radical}arão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}aria',
                                   'fut_pret_2s': f'{radical}arias',
                                   'fut_pret_3s': f'{radical}aria',
                                   'fut_pret_1p': f'{radical}aríamos',
                                   'fut_pret_3p': f'{radical}ariam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}e',
                                   'sub_pres_2s': f'{radical2}es',
                                   'sub_pres_3s': f'{radical2}e',
                                   'sub_pres_1p': f'{radical2}emos',
                                   'sub_pres_3p': f'{radical2}em',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}asse',
                                   'sub_pret_2s': f'{radical}asses',
                                   'sub_pret_3s': f'{radical}asse',
                                   'sub_pret_1p': f'{radical}ássemos',
                                   'sub_pret_3p': f'{radical}assem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ar',
                                   'sub_fut_2s': f'{radical}ares',
                                   'sub_fut_3s': f'{radical}ar',
                                   'sub_fut_1p': f'{radical}armos',
                                   'sub_fut_3p': f'{radical}arem',
                                   # imperativo
                                   'imp_2s': f'{radical}a',
                                   'imp_3s': f'{radical2}e',
                                   'imp_1p': f'{radical2}emos',
                                   'imp_3p': f'{radical2}em',
                                   # gerúndio
                                   'ger': f'{radical}ando',
                                   # particípio
                                   'part': f'{radical}ado'
                                   }

            # cozinhar, digitar, trabalhar, valorizar
            elif verbo.endswith('ar'):
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}armos',
                                   'inf_3p': f'{radical}arem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}as',
                                   'pres_ind_3s': f'{radical}a',
                                   'pres_ind_1p': f'{radical}amos',
                                   'pres_ind_3p': f'{radical}am',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}ei',
                                   'pret_per_2s': f'{radical}aste',
                                   'pret_per_3s': f'{radical}ou',
                                   'pret_per_1p': f'{radical}amos',
                                   'pret_per_3p': f'{radical}aram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ava',
                                   'pret_imp_2s': f'{radical}avas',
                                   'pret_imp_3s': f'{radical}ava',
                                   'pret_imp_1p': f'{radical}ávamos',
                                   'pret_imp_3p': f'{radical}avam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}arei',
                                   'fut_2s': f'{radical}arás',
                                   'fut_3s': f'{radical}ará',
                                   'fut_1p': f'{radical}aremos',
                                   'fut_3p': f'{radical}arão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}aria',
                                   'fut_pret_2s': f'{radical}arias',
                                   'fut_pret_3s': f'{radical}aria',
                                   'fut_pret_1p': f'{radical}aríamos',
                                   'fut_pret_3p': f'{radical}ariam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}e',
                                   'sub_pres_2s': f'{radical}es',
                                   'sub_pres_3s': f'{radical}e',
                                   'sub_pres_1p': f'{radical}emos',
                                   'sub_pres_3p': f'{radical}em',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}asse',
                                   'sub_pret_2s': f'{radical}asses',
                                   'sub_pret_3s': f'{radical}asse',
                                   'sub_pret_1p': f'{radical}ássemos',
                                   'sub_pret_3p': f'{radical}assem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ar',
                                   'sub_fut_2s': f'{radical}ares',
                                   'sub_fut_3s': f'{radical}ar',
                                   'sub_fut_1p': f'{radical}armos',
                                   'sub_fut_3p': f'{radical}arem',
                                   # imperativo
                                   'imp_2s': f'{radical}a',
                                   'imp_3s': f'{radical}e',
                                   'imp_1p': f'{radical}emos',
                                   'imp_3p': f'{radical}em',
                                   # gerúndio
                                   'ger': f'{radical}ando',
                                   # particípio
                                   'part': f'{radical}ado'
                                   }

                # correções de -ar
                if verbo == 'dar':
                    verbo_conjugado['pres_ind_1s'] = 'dou'
                    verbo_conjugado['pres_ind_2s'] = 'dás'
                    verbo_conjugado['pres_ind_3s'] = 'dá'
                    verbo_conjugado['sub_pres_1s'] = 'dê'
                    verbo_conjugado['sub_pres_2s'] = 'dês'
                    verbo_conjugado['sub_pres_3s'] = 'dê'
                    verbo_conjugado['imp_2s'] = 'dá'
                    verbo_conjugado['imp_3s'] = 'dê'

            # verbos terminando em -ER e variações
            # -CER, -TER, etc, têm que vir antes de -ER

            # contradizer, dizer
            elif verbo.endswith('dizer'):
                radical = verbo[:-2]    # diz (dizem, diz)
                radical2 = verbo[:-3]   # dig (digo, diga)
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}go',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical2}sse',
                                   'pret_per_2s': f'{radical2}sseste',
                                   'pret_per_3s': f'{radical2}sse',
                                   'pret_per_1p': f'{radical2}ssemos',
                                   'pret_per_3p': f'{radical2}sseram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical2}rei',
                                   'fut_2s': f'{radical2}rás',
                                   'fut_3s': f'{radical2}rá',
                                   'fut_1p': f'{radical2}remos',
                                   'fut_3p': f'{radical2}rão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical2}ria',
                                   'fut_pret_2s': f'{radical2}rias',
                                   'fut_pret_3s': f'{radical2}ria',
                                   'fut_pret_1p': f'{radical2}ríamos',
                                   'fut_pret_3p': f'{radical2}riam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}ga',
                                   'sub_pres_2s': f'{radical2}gas',
                                   'sub_pres_3s': f'{radical2}ga',
                                   'sub_pres_1p': f'{radical2}gamos',
                                   'sub_pres_3p': f'{radical2}gam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical2}ssesse',
                                   'sub_pret_2s': f'{radical2}ssesses',
                                   'sub_pret_3s': f'{radical2}ssesse',
                                   'sub_pret_1p': f'{radical2}sséssemos',
                                   'sub_pret_3p': f'{radical2}ssessem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical2}sser',
                                   'sub_fut_2s': f'{radical2}sseres',
                                   'sub_fut_3s': f'{radical2}sser',
                                   'sub_fut_1p': f'{radical2}ssermos',
                                   'sub_fut_3p': f'{radical2}sserem',
                                   # imperativo
                                   'imp_2s': f'{radical2}z',
                                   'imp_3s': f'{radical2}ga',
                                   'imp_1p': f'{radical2}gamos',
                                   'imp_3p': f'{radical2}gam',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical2}to'
                                   }

            elif verbo == 'querer':
                radical = verbo[:-2]    # quer (quero, quer, queremos)
                radical2 = 'quis'       # quis (quiser, quiserem)
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical2}',
                                   'pret_per_2s': f'{radical2}este',
                                   'pret_per_3s': f'{radical2}',
                                   'pret_per_1p': f'{radical2}emos',
                                   'pret_per_3p': f'{radical2}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}eria',
                                   'sub_pres_2s': f'{radical}erias',
                                   'sub_pres_3s': f'{radical}eria',
                                   'sub_pres_1p': f'{radical}eríamos',
                                   'sub_pres_3p': f'{radical}eriam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical2}esse',
                                   'sub_pret_2s': f'{radical2}esses',
                                   'sub_pret_3s': f'{radical2}esse',
                                   'sub_pret_1p': f'{radical2}éssemos',
                                   'sub_pret_3p': f'{radical2}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical2}er',
                                   'sub_fut_2s': f'{radical2}eres',
                                   'sub_fut_3s': f'{radical2}er',
                                   'sub_fut_1p': f'{radical2}ermos',
                                   'sub_fut_3p': f'{radical2}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}',
                                   'imp_3s': 'queira',
                                   'imp_1p': 'queiramos',
                                   'imp_3p': 'queiram',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            elif verbo == 'trazer':
                radical = 'tra'     # (trago)
                radical2 = 'troux'  # (trouxe)
                radical3 = 'traz'   # (traz, trazem)
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical3}ermos',
                                   'inf_3p': f'{radical3}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': 'trago',
                                   'pres_ind_2s': 'trazes',
                                   'pres_ind_3s': 'traz',
                                   'pres_ind_1p': 'trazemos',
                                   'pres_ind_3p': 'trazem',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical2}e',
                                   'pret_per_2s': f'{radical2}este',
                                   'pret_per_3s': f'{radical2}e',
                                   'pret_per_1p': f'{radical2}emos',
                                   'pret_per_3p': f'{radical2}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical3}ia',
                                   'pret_imp_2s': f'{radical3}ias',
                                   'pret_imp_3s': f'{radical3}ia',
                                   'pret_imp_1p': f'{radical3}íamos',
                                   'pret_imp_3p': f'{radical3}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}rei',
                                   'fut_2s': f'{radical}rás',
                                   'fut_3s': f'{radical}rá',
                                   'fut_1p': f'{radical}remos',
                                   'fut_3p': f'{radical}rão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}ria',
                                   'fut_pret_2s': f'{radical}rias',
                                   'fut_pret_3s': f'{radical}ria',
                                   'fut_pret_1p': f'{radical}ríamos',
                                   'fut_pret_3p': f'{radical}riam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}ga',
                                   'sub_pres_2s': f'{radical}gas',
                                   'sub_pres_3s': f'{radical}ga',
                                   'sub_pres_1p': f'{radical}gamos',
                                   'sub_pres_3p': f'{radical}gam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical2}esse',
                                   'sub_pret_2s': f'{radical2}esses',
                                   'sub_pret_3s': f'{radical2}esse',
                                   'sub_pret_1p': f'{radical2}éssemos',
                                   'sub_pret_3p': f'{radical2}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical2}er',
                                   'sub_fut_2s': f'{radical2}eres',
                                   'sub_fut_3s': f'{radical2}er',
                                   'sub_fut_1p': f'{radical2}ermos',
                                   'sub_fut_3p': f'{radical2}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}',
                                   'imp_3s': 'traga',
                                   'imp_1p': 'tragamos',
                                   'imp_3p': 'tragam',
                                   # gerúndio
                                   'ger': 'trazendo',
                                   # particípio
                                   'part': 'trazido'
                                   }

            # reter, ter
            elif verbo.endswith('ter'):
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}enho',
                                   'pres_ind_2s': f'{radical}ens',
                                   'pres_ind_3s': f'{radical}em',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}êm',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}ive',
                                   'pret_per_2s': f'{radical}iveste',
                                   'pret_per_3s': f'{radical}eve',
                                   'pret_per_1p': f'{radical}ivemos',
                                   'pret_per_3p': f'{radical}iveram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}inha',
                                   'pret_imp_2s': f'{radical}inhas',
                                   'pret_imp_3s': f'{radical}inha',
                                   'pret_imp_1p': f'{radical}ínhamos',
                                   'pret_imp_3p': f'{radical}inham',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}enha',
                                   'sub_pres_2s': f'{radical}enhas',
                                   'sub_pres_3s': f'{radical}enha',
                                   'sub_pres_1p': f'{radical}enhamos',
                                   'sub_pres_3p': f'{radical}enham',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}ivesse',
                                   'sub_pret_2s': f'{radical}ivesses',
                                   'sub_pret_3s': f'{radical}ivesse',
                                   'sub_pret_1p': f'{radical}ivéssemos',
                                   'sub_pret_3p': f'{radical}ivessem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}iver',
                                   'sub_fut_2s': f'{radical}iveres',
                                   'sub_fut_3s': f'{radical}iver',
                                   'sub_fut_1p': f'{radical}ivermos',
                                   'sub_fut_3p': f'{radical}iverem',
                                   # imperativo
                                   'imp_2s': f'{radical}em',
                                   'imp_3s': f'{radical}enha',
                                   'imp_1p': f'{radical}enhamos',
                                   'imp_3p': f'{radical}enham',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # desfazer, fazer, etc
            elif verbo.endswith('azer'):
                radical = verbo[:-4]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}aço',
                                   'pres_ind_2s': f'{radical}azes',
                                   'pres_ind_3s': f'{radical}az',
                                   'pres_ind_1p': f'{radical}azemos',
                                   'pres_ind_3p': f'{radical}azem',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}iz',
                                   'pret_per_2s': f'{radical}izeste',
                                   'pret_per_3s': f'{radical}ez',
                                   'pret_per_1p': f'{radical}izemos',
                                   'pret_per_3p': f'{radical}izeram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}azia',
                                   'pret_imp_2s': f'{radical}azias',
                                   'pret_imp_3s': f'{radical}azia',
                                   'pret_imp_1p': f'{radical}azíamos',
                                   'pret_imp_3p': f'{radical}azíam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}arei',
                                   'fut_2s': f'{radical}arás',
                                   'fut_3s': f'{radical}ará',
                                   'fut_1p': f'{radical}aremos',
                                   'fut_3p': f'{radical}arão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}aria',
                                   'fut_pret_2s': f'{radical}arias',
                                   'fut_pret_3s': f'{radical}aria',
                                   'fut_pret_1p': f'{radical}aríamos',
                                   'fut_pret_3p': f'{radical}ariam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}aça',
                                   'sub_pres_2s': f'{radical}aças',
                                   'sub_pres_3s': f'{radical}aça',
                                   'sub_pres_1p': f'{radical}açamos',
                                   'sub_pres_3p': f'{radical}açam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}izesse',
                                   'sub_pret_2s': f'{radical}izesses',
                                   'sub_pret_3s': f'{radical}izesse',
                                   'sub_pret_1p': f'{radical}izéssemos',
                                   'sub_pret_3p': f'{radical}izessem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}izer',
                                   'sub_fut_2s': f'{radical}izeres',
                                   'sub_fut_3s': f'{radical}izer',
                                   'sub_fut_1p': f'{radical}izermos',
                                   'sub_fut_3p': f'{radical}izerem',
                                   # imperativo
                                   'imp_2s': f'{radical}az',
                                   'imp_3s': f'{radical}aça',
                                   'imp_1p': f'{radical}açamos',
                                   'imp_3p': f'{radical}açam',
                                   # gerúndio
                                   'ger': f'{radical}azendo',
                                   # particípio
                                   'part': f'{radical}eito'
                                   }

            # saber
            elif verbo == 'saber':
                radical = verbo[:-2]
                radical2 = 'soub'
                radical3 = 'saib'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': 'sei',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical2}e',
                                   'pret_per_2s': f'{radical2}este',
                                   'pret_per_3s': f'{radical2}e',
                                   'pret_per_1p': f'{radical2}emos',
                                   'pret_per_3p': f'{radical2}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical3}a',
                                   'sub_pres_2s': f'{radical3}as',
                                   'sub_pres_3s': f'{radical3}a',
                                   'sub_pres_1p': f'{radical3}amos',
                                   'sub_pres_3p': f'{radical3}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical2}esse',
                                   'sub_pret_2s': f'{radical2}esses',
                                   'sub_pret_3s': f'{radical2}esse',
                                   'sub_pret_1p': f'{radical2}êssemos',
                                   'sub_pret_3p': f'{radical2}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical2}er',
                                   'sub_fut_2s': f'{radical2}eres',
                                   'sub_fut_3s': f'{radical2}er',
                                   'sub_fut_1p': f'{radical2}ermos',
                                   'sub_fut_3p': f'{radical2}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical3}a',
                                   'imp_1p': f'{radical3}amos',
                                   'imp_3p': f'{radical3}am',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # eleger, ranger
            elif verbo.endswith('ger'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-3]}j'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}este',
                                   'pret_per_3s': f'{radical}eu',
                                   'pret_per_1p': f'{radical}emos',
                                   'pret_per_3p': f'{radical}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}esse',
                                   'sub_pret_2s': f'{radical}esses',
                                   'sub_pret_3s': f'{radical}esse',
                                   'sub_pret_1p': f'{radical}êssemos',
                                   'sub_pret_3p': f'{radical}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}er',
                                   'sub_fut_2s': f'{radical}eres',
                                   'sub_fut_3s': f'{radical}er',
                                   'sub_fut_1p': f'{radical}ermos',
                                   'sub_fut_3p': f'{radical}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # acontecer, anoitecer, nascer
            elif verbo.endswith('cer'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-3]}ç'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}este',
                                   'pret_per_3s': f'{radical}eu',
                                   'pret_per_1p': f'{radical}emos',
                                   'pret_per_3p': f'{radical}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}esse',
                                   'sub_pret_2s': f'{radical}esses',
                                   'sub_pret_3s': f'{radical}esse',
                                   'sub_pret_1p': f'{radical}êssemos',
                                   'sub_pret_3p': f'{radical}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}er',
                                   'sub_fut_2s': f'{radical}eres',
                                   'sub_fut_3s': f'{radical}er',
                                   'sub_fut_1p': f'{radical}ermos',
                                   'sub_fut_3p': f'{radical}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # valer
            elif verbo.endswith('aler'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-3]}lh'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}este',
                                   'pret_per_3s': f'{radical}eu',
                                   'pret_per_1p': f'{radical}emos',
                                   'pret_per_3p': f'{radical}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}esse',
                                   'sub_pret_2s': f'{radical}esses',
                                   'sub_pret_3s': f'{radical}esse',
                                   'sub_pret_1p': f'{radical}êssemos',
                                   'sub_pret_3p': f'{radical}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}er',
                                   'sub_fut_2s': f'{radical}eres',
                                   'sub_fut_3s': f'{radical}er',
                                   'sub_fut_1p': f'{radical}ermos',
                                   'sub_fut_3p': f'{radical}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # poder
            elif verbo == 'poder':
                radical = 'pod'
                radical2 = 'poss'
                radical3 = 'pud'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical3}e',
                                   'pret_per_2s': f'{radical3}este',
                                   'pret_per_3s': 'pôde',
                                   'pret_per_1p': f'{radical3}emos',
                                   'pret_per_3p': f'{radical3}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}esse',
                                   'sub_pret_2s': f'{radical}esses',
                                   'sub_pret_3s': f'{radical}esse',
                                   'sub_pret_1p': f'{radical}êssemos',
                                   'sub_pret_3p': f'{radical}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}er',
                                   'sub_fut_2s': f'{radical}eres',
                                   'sub_fut_3s': f'{radical}er',
                                   'sub_fut_1p': f'{radical}ermos',
                                   'sub_fut_3p': f'{radical}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # ler, reler
            elif verbo == 'ler' or verbo == 'reler':
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}eio',
                                   'pres_ind_2s': f'{radical}ês',
                                   'pres_ind_3s': f'{radical}ê',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}eem',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}este',
                                   'pret_per_3s': f'{radical}eu',
                                   'pret_per_1p': f'{radical}emos',
                                   'pret_per_3p': f'{radical}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}eia',
                                   'sub_pres_2s': f'{radical}eias',
                                   'sub_pres_3s': f'{radical}eia',
                                   'sub_pres_1p': f'{radical}eiamos',
                                   'sub_pres_3p': f'{radical}eiam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}esse',
                                   'sub_pret_2s': f'{radical}esses',
                                   'sub_pret_3s': f'{radical}esse',
                                   'sub_pret_1p': f'{radical}êssemos',
                                   'sub_pret_3p': f'{radical}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}er',
                                   'sub_fut_2s': f'{radical}eres',
                                   'sub_fut_3s': f'{radical}er',
                                   'sub_fut_1p': f'{radical}ermos',
                                   'sub_fut_3p': f'{radical}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}ê',
                                   'imp_3s': f'{radical}eia',
                                   'imp_1p': f'{radical}eiamos',
                                   'imp_3p': f'{radical}eiam',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # escrever, receber, etc
            elif verbo.endswith('er'):
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ermos',
                                   'inf_3p': f'{radical}erem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}emos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}este',
                                   'pret_per_3s': f'{radical}eu',
                                   'pret_per_1p': f'{radical}emos',
                                   'pret_per_3p': f'{radical}eram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}erei',
                                   'fut_2s': f'{radical}erás',
                                   'fut_3s': f'{radical}erá',
                                   'fut_1p': f'{radical}eremos',
                                   'fut_3p': f'{radical}erão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}eria',
                                   'fut_pret_2s': f'{radical}erias',
                                   'fut_pret_3s': f'{radical}eria',
                                   'fut_pret_1p': f'{radical}eríamos',
                                   'fut_pret_3p': f'{radical}eriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}a',
                                   'sub_pres_2s': f'{radical}as',
                                   'sub_pres_3s': f'{radical}a',
                                   'sub_pres_1p': f'{radical}amos',
                                   'sub_pres_3p': f'{radical}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}esse',
                                   'sub_pret_2s': f'{radical}esses',
                                   'sub_pret_3s': f'{radical}esse',
                                   'sub_pret_1p': f'{radical}êssemos',
                                   'sub_pret_3p': f'{radical}essem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}er',
                                   'sub_fut_2s': f'{radical}eres',
                                   'sub_fut_3s': f'{radical}er',
                                   'sub_fut_1p': f'{radical}ermos',
                                   'sub_fut_3p': f'{radical}erem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical}a',
                                   'imp_1p': f'{radical}amos',
                                   'imp_3p': f'{radical}am',
                                   # gerúndio
                                   'ger': f'{radical}endo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # verbos terminados em -IR e variações
            # -UMIR, -EGUIR, etc, têm que vir antes de -IR

            # perseguir, prosseguir, seguir
            elif verbo.endswith('eguir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-5]}ig'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # tossir
            elif verbo.endswith('ossir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-5]}uss'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ndo'
                                   }

            # advir, intervir, vir
            elif verbo == 'ouvir':
                radical = verbo[:-2]
                radical2 = f'{verbo[:-3]}ç'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}ieste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}indo'
                                   }

            # advir, intervir, vir
            elif verbo.endswith('vir') or verbo == 'vir':
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}enho',
                                   'pres_ind_2s': f'{radical}ens',
                                   'pres_ind_3s': f'{radical}em',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}êm',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}im',
                                   'pret_per_2s': f'{radical}ieste',
                                   'pret_per_3s': f'{radical}eio',
                                   'pret_per_1p': f'{radical}iemos',
                                   'pret_per_3p': f'{radical}ieram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}inha',
                                   'pret_imp_2s': f'{radical}inhas',
                                   'pret_imp_3s': f'{radical}inha',
                                   'pret_imp_1p': f'{radical}ínhamos',
                                   'pret_imp_3p': f'{radical}inham',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}enha',
                                   'sub_pres_2s': f'{radical}enhas',
                                   'sub_pres_3s': f'{radical}enha',
                                   'sub_pres_1p': f'{radical}enhamos',
                                   'sub_pres_3p': f'{radical}enham',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}iesse',
                                   'sub_pret_2s': f'{radical}iesses',
                                   'sub_pret_3s': f'{radical}iesse',
                                   'sub_pret_1p': f'{radical}iéssemos',
                                   'sub_pret_3p': f'{radical}iessem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ier',
                                   'sub_fut_2s': f'{radical}ieres',
                                   'sub_fut_3s': f'{radical}ier',
                                   'sub_fut_1p': f'{radical}iermos',
                                   'sub_fut_3p': f'{radical}ierem',
                                   # imperativo
                                   'imp_2s': f'{radical}em',
                                   'imp_3s': f'{radical}enha',
                                   'imp_1p': f'{radical}enhamos',
                                   'imp_3p': f'{radical}enham',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}indo'
                                   }

            # pressentir, ressentir, sentir
            elif verbo.endswith('entir'):
                radical = verbo[:-2]    # sent (sente, sentem)
                radical2 = verbo[:-5]   # s
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}into',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}inta',
                                   'sub_pres_2s': f'{radical2}intas',
                                   'sub_pres_3s': f'{radical2}inta',
                                   'sub_pres_1p': f'{radical2}intamos',
                                   'sub_pres_3p': f'{radical2}intam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # atrair, retrair
            elif verbo.endswith('air'):
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}io',
                                   'pres_ind_2s': f'{radical}is',
                                   'pres_ind_3s': f'{radical}i',
                                   'pres_ind_1p': f'{radical}ímos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}í',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}ímos',
                                   'pret_per_3p': f'{radical}íram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ía',
                                   'pret_imp_2s': f'{radical}ías',
                                   'pret_imp_3s': f'{radical}ía',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}íam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}ia',
                                   'sub_pres_2s': f'{radical}ias',
                                   'sub_pres_3s': f'{radical}ia',
                                   'sub_pres_1p': f'{radical}iamos',
                                   'sub_pres_3p': f'{radical}iam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}ísse',
                                   'sub_pret_2s': f'{radical}ísses',
                                   'sub_pret_3s': f'{radical}ísse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}íssem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}i',
                                   'imp_3s': f'{radical}ia',
                                   'imp_1p': f'{radical}iamos',
                                   'imp_3p': f'{radical}iam',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ído'
                                   }

            # ferir, inserir, preferir
            elif verbo.endswith('erir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:4]}ir'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}iamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}r',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}uído'
                                   }

            # destruir, excluir, instruir
            elif verbo.endswith('uir'):
                radical = verbo[:-3]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}uirmos',
                                   'inf_3p': f'{radical}uirem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}uo',
                                   'pres_ind_2s': f'{radical}óis',
                                   'pres_ind_3s': f'{radical}ói',
                                   'pres_ind_1p': f'{radical}uímos',
                                   'pres_ind_3p': f'{radical}roem',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}uí',
                                   'pret_per_2s': f'{radical}uiste',
                                   'pret_per_3s': f'{radical}uiu',
                                   'pret_per_1p': f'{radical}uímos',
                                   'pret_per_3p': f'{radical}uíram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}uía',
                                   'pret_imp_2s': f'{radical}uías',
                                   'pret_imp_3s': f'{radical}uía',
                                   'pret_imp_1p': f'{radical}uíamos',
                                   'pret_imp_3p': f'{radical}uíam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}uirei',
                                   'fut_2s': f'{radical}uirás',
                                   'fut_3s': f'{radical}uirá',
                                   'fut_1p': f'{radical}uiremos',
                                   'fut_3p': f'{radical}uirão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}uiria',
                                   'fut_pret_2s': f'{radical}uirias',
                                   'fut_pret_3s': f'{radical}uiria',
                                   'fut_pret_1p': f'{radical}uiríamos',
                                   'fut_pret_3p': f'{radical}uiriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}ua',
                                   'sub_pres_2s': f'{radical}uas',
                                   'sub_pres_3s': f'{radical}ua',
                                   'sub_pres_1p': f'{radical}uamos',
                                   'sub_pres_3p': f'{radical}uam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}uísse',
                                   'sub_pret_2s': f'{radical}uísses',
                                   'sub_pret_3s': f'{radical}uísse',
                                   'sub_pret_1p': f'{radical}uíssemos',
                                   'sub_pret_3p': f'{radical}uíssem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}uir',
                                   'sub_fut_2s': f'{radical}uires',
                                   'sub_fut_3s': f'{radical}uir',
                                   'sub_fut_1p': f'{radical}uirmos',
                                   'sub_fut_3p': f'{radical}uirem',
                                   # imperativo
                                   'imp_2s': f'{radical}ói',
                                   'imp_3s': f'{radical}ua',
                                   'imp_1p': f'{radical}uamos',
                                   'imp_3p': f'{radical}uam',
                                   # gerúndio
                                   'ger': f'{radical}uindo',
                                   # particípio
                                   'part': f'{radical}uído'
                                   }

            # rir, sorrir
            elif verbo == 'rir' or verbo == 'sorrir':
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}io',
                                   'pres_ind_2s': f'{radical}is',
                                   'pres_ind_3s': f'{radical}i',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}iem',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}ia',
                                   'sub_pres_2s': f'{radical}ias',
                                   'sub_pres_3s': f'{radical}ia',
                                   'sub_pres_1p': f'{radical}iamos',
                                   'sub_pres_3p': f'{radical}iam',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}i',
                                   'imp_3s': f'{radical}ia',
                                   'imp_1p': f'{radical}iamos',
                                   'imp_3p': f'{radical}iam',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # subir
            elif verbo.endswith('ubir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-4]}ob'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical2}es',
                                   'pres_ind_3s': f'{radical2}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical2}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}a',
                                   'sub_pres_2s': f'{radical}as',
                                   'sub_pres_3s': f'{radical}a',
                                   'sub_pres_1p': f'{radical}amos',
                                   'sub_pres_3p': f'{radical}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical2}e',
                                   'imp_3s': f'{radical}a',
                                   'imp_1p': f'{radical}amos',
                                   'imp_3p': f'{radical}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # afligir, coagir, fingir
            elif verbo.endswith('gir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-3]}j'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # agredir, progredir, transgredir
            elif verbo.endswith('gredir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-4]}id'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical2}es',
                                   'pres_ind_3s': f'{radical2}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical2}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical2}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # impedir, medir, pedir
            elif verbo.endswith('edir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-3]}ç'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # ressarcir
            elif verbo.endswith('cir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-3]}ç'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # sumir, resumir, presumir
            elif verbo.endswith('umir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-4]}om'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}a',
                                   'sub_pres_2s': f'{radical}as',
                                   'sub_pres_3s': f'{radical}a',
                                   'sub_pres_1p': f'{radical}amos',
                                   'sub_pres_3p': f'{radical}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical}a',
                                   'imp_1p': f'{radical}amos',
                                   'imp_3p': f'{radical}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

                if verbo == 'sumir':
                    verbo_conjugado['pres_ind_2s'] = f'{radical2}es'
                    verbo_conjugado['pres_ind_3s'] = f'{radical2}e'
                    verbo_conjugado['pres_ind_3p'] = f'{radical2}em'
                    verbo_conjugado['imp_2s'] = f'{radical2}e'

            elif verbo == 'ir':
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': 'vou',
                                   'pres_ind_2s': 'vais',
                                   'pres_ind_3s': 'vai',
                                   'pres_ind_1p': 'vamos',
                                   'pres_ind_3p': 'vão',
                                   # pretérito perfeito
                                   'pret_per_1s': 'fui',
                                   'pret_per_2s': 'foste',
                                   'pret_per_3s': 'foi',
                                   'pret_per_1p': 'fomos',
                                   'pret_per_3p': 'foram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': 'ia',
                                   'pret_imp_2s': 'ias',
                                   'pret_imp_3s': 'ia',
                                   'pret_imp_1p': 'íamos',
                                   'pret_imp_3p': 'iam',
                                   # futuro do indicativo
                                   'fut_1s': 'irei',
                                   'fut_2s': 'irás',
                                   'fut_3s': 'irá',
                                   'fut_1p': 'iremos',
                                   'fut_3p': 'irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': 'iria',
                                   'fut_pret_2s': 'irias',
                                   'fut_pret_3s': 'iria',
                                   'fut_pret_1p': 'iríamos',
                                   'fut_pret_3p': 'iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': 'vá',
                                   'sub_pres_2s': 'vás',
                                   'sub_pres_3s': 'vá',
                                   'sub_pres_1p': 'vamos',
                                   'sub_pres_3p': 'vão',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': 'fosse',
                                   'sub_pret_2s': 'fosses',
                                   'sub_pret_3s': 'fosse',
                                   'sub_pret_1p': 'fôssemos',
                                   'sub_pret_3p': 'fossem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': 'for',
                                   'sub_fut_2s': 'fores',
                                   'sub_fut_3s': 'for',
                                   'sub_fut_1p': 'formos',
                                   'sub_fut_3p': 'forem',
                                   # imperativo
                                   'imp_2s': 'vai',
                                   'imp_3s': 'vá',
                                   'imp_1p': 'vamos',
                                   'imp_3p': 'vão',
                                   # gerúndio
                                   'ger': 'indo',
                                   # particípio
                                   'part': 'ido'
                                   }

            # investir, revestir, vestir, etc
            elif verbo.endswith('estir'):
                radical = verbo[:-2]
                radical2 = f'{verbo[:-5]}ist'
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical2}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical2}a',
                                   'sub_pres_2s': f'{radical2}as',
                                   'sub_pres_3s': f'{radical2}a',
                                   'sub_pres_1p': f'{radical2}amos',
                                   'sub_pres_3p': f'{radical2}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical2}a',
                                   'imp_1p': f'{radical2}amos',
                                   'imp_3p': f'{radical2}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # insistir, dividir, etc
            elif verbo.endswith('ir'):
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}irmos',
                                   'inf_3p': f'{radical}irem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}o',
                                   'pres_ind_2s': f'{radical}es',
                                   'pres_ind_3s': f'{radical}e',
                                   'pres_ind_1p': f'{radical}imos',
                                   'pres_ind_3p': f'{radical}em',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}i',
                                   'pret_per_2s': f'{radical}iste',
                                   'pret_per_3s': f'{radical}iu',
                                   'pret_per_1p': f'{radical}imos',
                                   'pret_per_3p': f'{radical}iram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}ia',
                                   'pret_imp_2s': f'{radical}ias',
                                   'pret_imp_3s': f'{radical}ia',
                                   'pret_imp_1p': f'{radical}íamos',
                                   'pret_imp_3p': f'{radical}iam',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}irei',
                                   'fut_2s': f'{radical}irás',
                                   'fut_3s': f'{radical}irá',
                                   'fut_1p': f'{radical}iremos',
                                   'fut_3p': f'{radical}irão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}iria',
                                   'fut_pret_2s': f'{radical}irias',
                                   'fut_pret_3s': f'{radical}iria',
                                   'fut_pret_1p': f'{radical}iríamos',
                                   'fut_pret_3p': f'{radical}iriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}a',
                                   'sub_pres_2s': f'{radical}as',
                                   'sub_pres_3s': f'{radical}a',
                                   'sub_pres_1p': f'{radical}amos',
                                   'sub_pres_3p': f'{radical}am',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}isse',
                                   'sub_pret_2s': f'{radical}isses',
                                   'sub_pret_3s': f'{radical}isse',
                                   'sub_pret_1p': f'{radical}íssemos',
                                   'sub_pret_3p': f'{radical}issem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}ir',
                                   'sub_fut_2s': f'{radical}ires',
                                   'sub_fut_3s': f'{radical}ir',
                                   'sub_fut_1p': f'{radical}irmos',
                                   'sub_fut_3p': f'{radical}irem',
                                   # imperativo
                                   'imp_2s': f'{radical}e',
                                   'imp_3s': f'{radical}a',
                                   'imp_1p': f'{radical}amos',
                                   'imp_3p': f'{radical}am',
                                   # gerúndio
                                   'ger': f'{radical}indo',
                                   # particípio
                                   'part': f'{radical}ido'
                                   }

            # pôr, compor, decompor, recompor, repor
            elif verbo.endswith('or'):
                radical = verbo[:-2]
                verbo_conjugado = {'infinitivo': verbo,
                                   'inf_1p': f'{radical}ormos',
                                   'inf_3p': f'{radical}orem',
                                   # presente do indicativo
                                   'pres_ind_1s': f'{radical}onho',
                                   'pres_ind_2s': f'{radical}ões',
                                   'pres_ind_3s': f'{radical}õe',
                                   'pres_ind_1p': f'{radical}omos',
                                   'pres_ind_3p': f'{radical}õem',
                                   # pretérito perfeito
                                   'pret_per_1s': f'{radical}us',
                                   'pret_per_2s': f'{radical}este',
                                   'pret_per_3s': f'{radical}ôs',
                                   'pret_per_1p': f'{radical}usemos',
                                   'pret_per_3p': f'{radical}useram',
                                   # pretérito imperfeito
                                   'pret_imp_1s': f'{radical}unha',
                                   'pret_imp_2s': f'{radical}unhas',
                                   'pret_imp_3s': f'{radical}unha',
                                   'pret_imp_1p': f'{radical}únhamos',
                                   'pret_imp_3p': f'{radical}unham',
                                   # futuro do indicativo
                                   'fut_1s': f'{radical}orei',
                                   'fut_2s': f'{radical}orás',
                                   'fut_3s': f'{radical}orá',
                                   'fut_1p': f'{radical}oremos',
                                   'fut_3p': f'{radical}orão',
                                   # futuro do pretérito
                                   'fut_pret_1s': f'{radical}oria',
                                   'fut_pret_2s': f'{radical}orias',
                                   'fut_pret_3s': f'{radical}oria',
                                   'fut_pret_1p': f'{radical}oríamos',
                                   'fut_pret_3p': f'{radical}oriam',
                                   # presente do subjuntivo
                                   'sub_pres_1s': f'{radical}onha',
                                   'sub_pres_2s': f'{radical}onhas',
                                   'sub_pres_3s': f'{radical}onha',
                                   'sub_pres_1p': f'{radical}onhamos',
                                   'sub_pres_3p': f'{radical}onham',
                                   # pretérito do subjuntivo
                                   'sub_pret_1s': f'{radical}usesse',
                                   'sub_pret_2s': f'{radical}usesses',
                                   'sub_pret_3s': f'{radical}usesse',
                                   'sub_pret_1p': f'{radical}uséssemos',
                                   'sub_pret_3p': f'{radical}usessem',
                                   # futuro do subjuntivo
                                   'sub_fut_1s': f'{radical}user',
                                   'sub_fut_2s': f'{radical}useres',
                                   'sub_fut_3s': f'{radical}user',
                                   'sub_fut_1p': f'{radical}usermos',
                                   'sub_fut_3p': f'{radical}userem',
                                   # imperativo
                                   'imp_2s': f'{radical}õe',
                                   'imp_3s': f'{radical}onha',
                                   'imp_1p': f'{radical}onhamos',
                                   'imp_3p': f'{radical}onham',
                                   # gerúndio
                                   'ger': f'{radical}ondo',
                                   # particípio
                                   'part': f'{radical}osto'
                                   }

        lista_de_verbos_conjugados.append(verbo_conjugado)


lista_geral_de_verbos_conjugados = []
lista_de_verbos_transitivos_diretos_conjugados = []

criar_lista_de_verbos(set_verbos_no_infinitivo,
                      lista_geral_de_verbos_conjugados)
criar_lista_de_verbos(set_verbos_transitivos_diretos,
                      lista_de_verbos_transitivos_diretos_conjugados)

# transformar listas em sets
# construir um set com todos os verbos conjugados (apenas os verbos, sem keys)
set_geral_de_verbos_conjugados = set()
set_de_verbos_transitivos_diretos_conjugados = set()

for i, lista in enumerate(lista_geral_de_verbos_conjugados):
    for value in lista.values():
        set_geral_de_verbos_conjugados.add(value)

for i, lista in enumerate(lista_de_verbos_transitivos_diretos_conjugados):
    for value in lista.values():
        set_de_verbos_transitivos_diretos_conjugados.add(value)

lista_short_answers = [  # afirmativa - presente
                        {'short_answer': r'Yes, I do.',
                         'tradução_literal': r'Sim, eu faço.',
                         'verbo_anterior': 'pres_ind_3s',
                         'verbo_resposta': 'pres_ind_1s',
                         'posição': 'pré'},
                        {'short_answer': r'Yes, you do.',
                         'tradução_literal': r'Sim, você faz.',
                         'verbo_anterior': 'pres_ind_1s',
                         'verbo_resposta': 'pres_ind_3s',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, he does.',
                         'tradução_literal': r'Sim, ele faz.',
                         'verbo_anterior': 'pres_ind_3s',
                         'verbo_resposta': 'pres_ind_3s',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, she does.',
                         'tradução_literal': r'Sim, ela faz.',
                         'verbo_anterior': 'pres_ind_3s',
                         'verbo_resposta': 'pres_ind_3s',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, we do.',
                         'tradução_literal': r'Sim, nós fazemos.',
                         'verbo_anterior': 'pres_ind_3p',
                         'verbo_resposta': 'pres_ind_1p',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, they do.',
                         'tradução_literal': r'Sim, eles fazem.',
                         'verbo_anterior': 'pres_ind_3p',
                         'verbo_resposta': 'pres_ind_3p',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, they do.',
                         'tradução_literal': r'Sim, elas fazem.',
                         'verbo_anterior': 'pres_ind_3p',
                         'verbo_resposta': 'pres_ind_3p',
                         'posição': 'pós'},

                        # afirmativa - pretérito perfeito
                        {'short_answer': r'Yes, I did.',
                         'tradução_literal': r'Sim, eu fiz.',
                         'verbo_anterior': 'pret_per_3s',
                         'verbo_resposta': 'pret_per_1s',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, you did.',
                         'tradução_literal': r'Sim, você fez.',
                         'verbo_anterior': 'pret_per_1s',
                         'verbo_resposta': 'pret_per_3s',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, he did.',
                         'tradução_literal': r'Sim, ele fez.',
                         'verbo_anterior': 'pret_per_3s',
                         'verbo_resposta': 'pret_per_3s',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, she did.',
                         'tradução_literal': r'Sim, ela fez.',
                         'verbo_anterior': 'pret_per_3s',
                         'verbo_resposta': 'pret_per_3s',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, we did.',
                         'tradução_literal': r'Sim, nós fizemos.',
                         'verbo_anterior': 'pret_per_3p',
                         'verbo_resposta': 'pret_per_1p',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, they did.',
                         'tradução_literal': r'Sim, eles fizeram.',
                         'verbo_anterior': 'pret_per_3p',
                         'verbo_resposta': 'pret_per_3p',
                         'posição': 'pós'},
                        {'short_answer': r'Yes, they did.',
                         'tradução_literal': r'Sim, elas fizeram.',
                         'verbo_anterior': 'pret_per_3p',
                         'verbo_resposta': 'pret_per_3p',
                         'posição': 'pós'},

                        # negativa - presente
                        {'short_answer': r"No, I don't.",
                         'tradução_literal': r'Não, eu não faço.',
                         'verbo_anterior': 'pres_ind_3s',
                         'verbo_resposta': 'pres_ind_1s',
                         'posição': 'pós'},
                        {'short_answer': r"No, you don't.",
                         'tradução_literal': r'Não, você não faz.',
                         'verbo_anterior': 'pres_ind_1s',
                         'verbo_resposta': 'pres_ind_3s',
                         'posição': 'pós'},
                        {'short_answer': r"No, he doesn't.",
                         'tradução_literal': r'Não, ele não faz.',
                         'verbo_anterior': 'pres_ind_3s',
                         'verbo_resposta': 'pres_ind_3s',
                         'posição': 'pós'},
                        {'short_answer': r"No, she doesn't.",
                         'tradução_literal': r'Não, ela não faz.',
                         'verbo_anterior': 'pres_ind_3s',
                         'verbo_resposta': 'pres_ind_3s',
                         'posição': 'pós'},
                        {'short_answer': r"No, we don't.",
                         'tradução_literal': r'Não, nós não fazemos.',
                         'verbo_anterior': 'pres_ind_3p',
                         'verbo_resposta': 'pres_ind_1p',
                         'posição': 'pós'},
                        {'short_answer': r"No, they don't.",
                         'tradução_literal': r'Não, eles não fazem.',
                         'verbo_anterior': 'pres_ind_3p',
                         'verbo_resposta': 'pres_ind_3p',
                         'posição': 'pós'},
                        {'short_answer': r"No, they don't.",
                         'tradução_literal': r'Não, elas não fazem.',
                         'verbo_anterior': 'pres_ind_3p',
                         'verbo_resposta': 'pres_ind_3p',
                         'posição': 'pós'},

                        # negativa - presente
                        {'short_answer': r"No, I didn't.",
                         'tradução_literal': r'Não, eu não fiz.',
                         'verbo_anterior': 'pret_per_3s',
                         'verbo_resposta': 'pret_per_1s',
                         'posição': 'pós'},
                        {'short_answer': r"No, you didn't.",
                         'tradução_literal': r'Não, você não fez.',
                         'verbo_anterior': 'pret_per_1s',
                         'verbo_resposta': 'pret_per_3s',
                         'posição': 'pós'},
                        {'short_answer': r"No, he didn't.",
                         'tradução_literal': r'Não, ele não fez.',
                         'verbo_anterior': 'pret_per_3s',
                         'verbo_resposta': 'pret_per_3s',
                         'posição': 'pós'},
                        {'short_answer': r"No, she didn't.",
                         'tradução_literal': r'Não, ela não fizeram.',
                         'verbo_anterior': 'pret_per_3s',
                         'verbo_resposta': 'pret_per_3s',
                         'posição': 'pós'},
                        {'short_answer': r"No, we didn't.",
                         'tradução_literal': r'Não, nós não fizemos.',
                         'verbo_anterior': 'pret_per_3p',
                         'verbo_resposta': 'pret_per_1p',
                         'posição': 'pós'},
                        {'short_answer': r"No, they didn't.",
                         'tradução_literal': r'Não, eles não fizeram.',
                         'verbo_anterior': 'pret_per_3p',
                         'verbo_resposta': 'pret_per_3p',
                         'posição': 'pós'},
                        {'short_answer': r"No, they didn't.",
                         'tradução_literal': r'Não, elas não fizeram.',
                         'verbo_anterior': 'pret_per_3p',
                         'verbo_resposta': 'pret_per_3p',
                         'posição': 'pós'},
                        ]

# set com verbos ser e estar para juntar aos outros verbos
set_verbos_ser_estar = {
    'é', 'ser', 'sou', 'somos', 'são', 'estar', 'estou', 'está', 'estamos',
    'estivemos', 'estão', 'estará', 'estarão', 'estarei', 'estaremos'
    }

# juntar set geral de verbos com set de ser/estar
set_verbos_geral_ser_estar = set_geral_de_verbos_conjugados.union(set_verbos_ser_estar)

# criar set para pôr imperativos e infinitivos
set_imperativos_infinitivos = set()

# criar lista com infinitivos e imperativos
# para corrigir imperativos do inglês traduzidos erroneamente como infinitivos
for verbo in lista_geral_de_verbos_conjugados:
    infinitivo = verbo['infinitivo'].capitalize()
    imperativo = verbo['imp_3s'].capitalize()
    set_imperativos_infinitivos.add((infinitivo, imperativo))

# criar set apenas com verbos conjugados na 3a pessoa do singular
set_keys_verbos_3a_sing = {     # ordenar as keys da 3a pessoa do singular
    'pres_ind_3s', 'pret_per_3s', 'pret_imp_3s', 'fut_3s', 'fut_pret_3s',
    'sub_pres_3s', 'sub_pret_3s', 'sub_fut_3s'
}

set_3a_pess_sing = set()
for verbo in lista_geral_de_verbos_conjugados:
    for key, value in verbo.items():
        for vb in set_keys_verbos_3a_sing:
            set_3a_pess_sing.add(verbo[vb])

set_a_gente_nós = set()


# criar set com tuplas com verbos na 3a pessoa do singular e 1a do plural
# para a trocar de 'a gente' por 'nós'

set_keys_verbos_3a_sing_1a_pl = {
    ('pres_ind_3s', 'pres_ind_1p'),
    ('pret_per_3s', 'pret_per_1p'),
    ('pret_imp_3s', 'pret_imp_1p'),
    ('fut_3s', 'fut_1p'),
    ('fut_pret_3s', 'fut_pret_1p'),
    ('sub_pres_3s', 'sub_pres_1p'),
    ('sub_pret_3s', 'sub_pret_1p'),
    ('sub_fut_3s', 'sub_fut_1p')
}

set_a_gente_nós = set()
for verbo in lista_geral_de_verbos_conjugados:
    for key, value in verbo.items():
        for terc_pess_sing, prim_pess_pl in set_keys_verbos_3a_sing_1a_pl:
            set_a_gente_nós.add((verbo[terc_pess_sing], verbo[prim_pess_pl]))


# Criar set para a função que transforma 'para que ele faça' em 'para ele fazer'
set_pres_pret_subjuntivo = set()

for verbo in lista_geral_de_verbos_conjugados:
    set_pres_pret_subjuntivo.add(verbo['sub_pres_1s'])
    set_pres_pret_subjuntivo.add(verbo['sub_pres_1p'])
    set_pres_pret_subjuntivo.add(verbo['sub_pres_3p'])
    set_pres_pret_subjuntivo.add(verbo['sub_pret_1s'])
    set_pres_pret_subjuntivo.add(verbo['sub_pret_1p'])
    set_pres_pret_subjuntivo.add(verbo['sub_pret_3p'])


set_sub_pres_fut = set()

for verbo in lista_geral_de_verbos_conjugados:
    # 1a e 3a p. sing do infinitivo são iguais.
    infinitivo = verbo['infinitivo']
    inf_1p = verbo['inf_1p']
    inf_3p = verbo['inf_3p']
    sub_pres_1s = verbo['sub_pres_1s']
    sub_pres_1p = verbo['sub_pres_1p']
    sub_pres_3p = verbo['sub_pres_3p']
    sub_pret_1s = verbo['sub_pret_1s']
    sub_pret_1p = verbo['sub_pret_1p']
    sub_pret_3p = verbo['sub_pret_3p']
    # 1a e 3a p. sing do subjuntivo são iguais.
    set_sub_pres_fut.add((infinitivo, sub_pres_1s))
    set_sub_pres_fut.add((inf_1p, sub_pres_1p))
    set_sub_pres_fut.add((inf_3p, sub_pres_3p))
    set_sub_pres_fut.add((infinitivo, sub_pret_1s))
    set_sub_pres_fut.add((inf_1p, sub_pret_1p))
    set_sub_pres_fut.add((inf_3p, sub_pret_3p))

# A partir daqui começam sets dos verbos:

set_reflexivos_opcionais = {
    'deitar', 'abaixar', 'encontrar', 'levantar', 'agachar', 'sentar',
    'virar', 'lembrar', 'esquecer', 'cansar', 'casar', 'quebrar', 'chamar'}

# com a conjugação de pronomes específicos para que sejam removidos os pronomes reflexivos.

set_reflexivo_3a_pessoa = set()

for verbo_reflexivo in set_reflexivos_opcionais:
    for verbo in lista_geral_de_verbos_conjugados:
        if verbo['infinitivo'] == verbo_reflexivo:
            # 1a e 3a p. sing do infinitivo são iguais.
            set_reflexivo_3a_pessoa.add(verbo['inf_3p'])
            set_reflexivo_3a_pessoa.add(verbo['pres_ind_3s'])
            set_reflexivo_3a_pessoa.add(verbo['pres_ind_3p'])
            set_reflexivo_3a_pessoa.add(verbo['pret_per_3s'])
            set_reflexivo_3a_pessoa.add(verbo['pret_per_3p'])
            set_reflexivo_3a_pessoa.add(verbo['pret_imp_3s'])
            set_reflexivo_3a_pessoa.add(verbo['pret_imp_3p'])
            set_reflexivo_3a_pessoa.add(verbo['fut_3s'])
            set_reflexivo_3a_pessoa.add(verbo['fut_3p'])
            set_reflexivo_3a_pessoa.add(verbo['fut_pret_3s'])
            set_reflexivo_3a_pessoa.add(verbo['fut_pret_3p'])
            set_reflexivo_3a_pessoa.add(verbo['sub_pres_3s'])
            set_reflexivo_3a_pessoa.add(verbo['sub_pres_3p'])
            set_reflexivo_3a_pessoa.add(verbo['sub_pret_3s'])
            set_reflexivo_3a_pessoa.add(verbo['sub_pret_3p'])
            set_reflexivo_3a_pessoa.add(verbo['sub_fut_3s'])
            set_reflexivo_3a_pessoa.add(verbo['sub_fut_3p'])
            set_reflexivo_3a_pessoa.add(verbo['imp_3s'])
            set_reflexivo_3a_pessoa.add(verbo['imp_3p'])
            set_reflexivo_3a_pessoa.add(verbo['ger'])

set_reflexivo_1a_pess_sing = set()

for verbo_reflexivo in set_reflexivos_opcionais:
    for verbo in lista_geral_de_verbos_conjugados:
        if verbo['infinitivo'] == verbo_reflexivo:
            # 1a e 3a p. sing do infinitivo são iguais.
            set_reflexivo_1a_pess_sing.add(verbo['pres_ind_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['pret_per_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['pret_imp_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['fut_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['fut_pret_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['sub_pres_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['sub_pret_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['sub_fut_1s'])
            set_reflexivo_1a_pess_sing.add(verbo['ger'])


set_reflexivo_1a_pess_pl = set()

for verbo_reflexivo in set_reflexivos_opcionais:
    for verbo in lista_geral_de_verbos_conjugados:
        if verbo['infinitivo'] == verbo_reflexivo:
            # 1a e 3a p. sing do infinitivo são iguais.
            set_reflexivo_1a_pess_pl.add(verbo['inf_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['pres_ind_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['pret_per_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['pret_imp_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['fut_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['fut_pret_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['sub_pres_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['sub_pret_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['sub_fut_1p'])
            set_reflexivo_1a_pess_pl.add(verbo['ger'])


set_reflexivos_opcionais_gerúndio = set()

for verbo_reflexivo in set_reflexivos_opcionais:
    for verbo in lista_geral_de_verbos_conjugados:
        if verbo['infinitivo'] == verbo_reflexivo:
            set_reflexivo_1a_pess_pl.add(verbo['ger'])

# Set com todos os verbos conjgados em todos os tempos na terceira pessoa.
set_terceira_pessoa = set()
for verbo in lista_geral_de_verbos_conjugados:
    # set_terceira_pessoa.add(verbo['inf_3p'])
    set_terceira_pessoa.add(verbo['pres_ind_3s'])
    set_terceira_pessoa.add(verbo['pres_ind_3p'])
    set_terceira_pessoa.add(verbo['pret_per_3s'])
    set_terceira_pessoa.add(verbo['pret_per_3p'])
    set_terceira_pessoa.add(verbo['pret_imp_3s'])
    set_terceira_pessoa.add(verbo['pret_imp_3p'])
    set_terceira_pessoa.add(verbo['fut_3s'])
    set_terceira_pessoa.add(verbo['fut_3p'])
    set_terceira_pessoa.add(verbo['fut_pret_3s'])
    set_terceira_pessoa.add(verbo['fut_pret_3p'])
    set_terceira_pessoa.add(verbo['sub_pres_3s'])
    set_terceira_pessoa.add(verbo['sub_pres_3p'])
    set_terceira_pessoa.add(verbo['sub_pret_3s'])
    set_terceira_pessoa.add(verbo['sub_pret_3p'])
    set_terceira_pessoa.add(verbo['sub_fut_3s'])
    set_terceira_pessoa.add(verbo['sub_fut_3p'])
    set_terceira_pessoa.add(verbo['imp_2s'])
    set_terceira_pessoa.add(verbo['imp_3s'])
    set_terceira_pessoa.add(verbo['imp_3p'])


# Preparação dos sets para a função que transforma 'para você' em 'te', dependendo do verbo.
set_verbos_transformar_para_você_em_te = {
    'consultar', 'contar', 'dar', 'devolver', 'dizer', 'emprestar', 'entregar', 'enviar',
    'falar', 'lembrar', 'levar', 'mandar', 'pagar', 'pedir', 'perguntar', 'propor', 'recordar',
    'responder', 'revelar', 'trazer'
    }

set_verbos_conjugados_transformar_para_você_em_te = set()

for verbo_para_você in set_verbos_transformar_para_você_em_te:
    for verbo in lista_geral_de_verbos_conjugados:
        if verbo['infinitivo'] == verbo_para_você:
            # 1a e 3a p. sing do infinitivo são iguais.
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['infinitivo'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['inf_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['pres_ind_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['pres_ind_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['pret_per_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['pret_per_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['pret_imp_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['pret_imp_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['fut_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['fut_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['fut_pret_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['fut_pret_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['sub_pres_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['sub_pres_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['sub_pret_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['sub_pret_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['sub_fut_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['sub_fut_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['imp_3s'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['imp_3p'])
            set_verbos_conjugados_transformar_para_você_em_te.add(verbo['ger'])
