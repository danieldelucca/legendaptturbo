import subprocess
import os

pasta_do_script = os.path.dirname(os.path.abspath(__file__))

pasta_funções = os.path.join(pasta_do_script, 'funções')

def função_menu_inicial():
    print('\n  Bem-vindo ao Legenda PT Turbo!\n\n  Selecione a opção desejada:\n\n'
        '  1 + Enter --> Preparar legenda em idioma estrangeiro para tradução no ChatGPT\n'
        '  2 + Enter --> Realizar ajustes em legenda traduzida para o português\n')

    menu_inicial = input()
    if menu_inicial == '2':
        caminho_legenda_pt_turbo = os.path.join(pasta_funções, 'transformações_legenda_português.py')
        subprocess.run(['python', caminho_legenda_pt_turbo])

    elif menu_inicial == '1':
        caminho_preparar_legenda_estrangeira = (
            os.path.join(pasta_funções, 'preparar_legenda_estrangeira.py')
        )
        subprocess.run(['python', caminho_preparar_legenda_estrangeira])

    else:
        print('Digite uma opção válida.')
        função_menu_inicial()

função_menu_inicial()
