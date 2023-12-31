# Sets com pontuação que várias funções vão usar.
# Para facilitar, '...' serão substituídas por '¨' (trema).
set_pontuação = {'!', '.', '?', '"', '-', '¨'}

lista_pontuação_com_vírgula = ['!', '.', '?', ',', '"', '-', ':', '¨']

títulos_masculinos = {
    'Sr.', 'Dr.'}

títulos_femininos = {
    'Dona', 'Sra.', 'Srta.', 'Dra.', 'Dona'
}

títulos_extenso_e_abrv = {('senhor', 'Sr.'),
                          ('senhora', 'Sra.'),
                          ('senhorita', 'Srta.'),
                          ('doutor', 'Dr.'),
                          ('doutora', 'Dra.')}

cargos_depois_de_títulos = {'prefeito', 'prefeita', 'presidente', 'comandante',
                            'coronel', 'diretor', 'diretora', 'general', 'secretário',
                            'secretária', 'ministro', 'ministra'}


palavras_de_quebra = {
    # Preposições
    "a", "à", "às", "ante", "ao", "aos", "após", "até", "com", "contra", "daqui",
    "de", "desde", "em", "entre",     "para", "perante", "por", "sem", "sob", "sobre",
    "trás", "na", "nas", "no", "nos",
    # Artigos definidos
    "o", "a", "os", "as",
    # Artigos indefinidos
    "um", "uma", "uns", "umas",
    # Conjunções coordenativas
    "e", "mas", "ou", "porém", "todavia", "contudo", "nem", "pois",
    "porque", "como", "se", "então", "ainda",
    "do", "da", "dos", "das",
    # Conjunções subordinativas
    "que", "se", "como", "porque", "embora", "enquanto", "quando",
    "antes", "depois", "desde", "tanto", "quanto", "como",
    "para", "quando", "apesar", "porquanto", "conquanto",
    "contanto"
    # pronomes demonstrativo
    "este", "esta", "isto", "esse", "essa", "isso", "aquele", "aquela", "aquilo",
    # pronomes possessivos
    "meu", "minha", "meus", "minhas", "seu", "seus", "sua", "suas", "nosso",
    "nossos", "nossa", "nossas", "dessa", "dessas", "desse", "desses",
    # pronomes de tratamento
    # "Sr.", "Sra.", "Dr.", "Dra."
    # pronomes indefinidos
    "muitos", "muitas", "tanto", "tanta", "tantos", "tantas", "todos", "todas",
}

# set com palavras que se estiverem antes de 'você', esse pronome não será transformado em 'te'
set_exceções_antes_você = {
    'a', 'agora', 'assim', 'até', 'e', 'então', 'com', 'como', 'contra', 'de', 'desculpa',
    'em', 'enquanto', 'entre', 'forma', 'mas', 'obrigado', 'onde', 'ou', 'para',
    'perante', 'por', 'porém', 'porque', 'quando', 'que', 'se', 'sem', 'só',
    'sobre', 'tanto'
    }

# a_gente_nos
a_gente_nós_sufixos = {
    ('ar', 'armos'),
    ('ava', 'ávamos'),
    ('a', 'amos'),
    ('disse', 'dissemos'),
    ('quer', 'queremos'),
    ('quiser', 'quisermos'),
    ('er', 'ermos'),
    ('ez', 'izemos'),
    ('eu', 'emos'),
    ('e', 'emos'),
    ('foi', 'fomos'),
    ('vai', 'vamos'),
    ('ria', 'ríamos'),
    ('ia', 'íamos'),
    ('iu', 'imos'),
    ('ou', 'amos'),
    ('ôs', 'usemos'),
    ('ir', 'irmos'),
    ('unha', 'únhamos')}


# a_gente_nos
a_gente_nós_exceções = {
    # pronomes
    'eu', 'você', 'ele', 'ela', 'nós', 'eles', 'elas', 'vocês', "vai",
    # Preposições
    "ante", "após", "até", "com", "contra", "de", "desde", "em", "entre",
    "para", "perante", "por", "sem", "sob", "sobre", "trás",
    # Artigos indefinidos
    "um", "uma", "uns", "umas",
    # Conjunções coordenativas
    "mas", "ou", "porém", "todavia", "contudo", "nem", "pois", "logo",
    "porque", "como", "se", "já", "então", "ainda", "do", "da", "dos", "das",
    # Conjunções subordinativas
    "que", "se", "como", "porque", "embora", "conforme", "enquanto", "quando",
    "antes", "caso", "desde", "seja", "tanto", "quanto", "como", "para",
    "quando", "como", "apesar", "porquanto", "visto", "conquanto",
    # pronomes possessivos
    "meu", "minha", "meus", "minhas", "seu", "seus", "sua", "suas", "nosso",
    "nossos", "nossa", "nossas",
    # pronomes de tratamento
    "Sr.", "Sra.", "Dr.", "Dra."
    # pronome indefinido
    "qualquer", "quaisquer",
    # adjetivo/advérbio
    "tanto", "tanta", "tantos", "tantas",
    # adjetivos
    "bom", "boa", "bons", "boas"
}

possessivos_sing_m = {'meu', 'seu', 'nosso'}
possessivos_pl_m = {'meus', 'seus', 'nossos'}
possessivos_f = {'minha', 'minhas', 'sua', 'suas', 'nossa', 'nossas'}
possessivos_sing_f = {'minha', 'sua', 'nossa'}
possessivos_pl_f = {'minhas', 'suas', 'nossas'}

num_zero_dez = {
    ("0", "zero"), ("1", "um"), ("2", "dois"), ("3", "três"), ("4", "quatro"),
    ("5", "cinco"), ("6", "seis"), ("7", "sete"), ("8", "oito"), ("9", "nove"),
    ("10", "dez")
    }

set_0_a_100_algarismo_e_por_extenso = {
    ("11", "onze"),
    ("12", "doze"),
    ("13", "treze"),
    ("14", "catorze"),
    ("15", "quinze"),
    ("16", "dezesseis"),
    ("17", "dezessete"),
    ("18", "dezoito"),
    ("19", "dezenove"),
    ("20", "vinte"),
    ("21", "vinte e um"),
    ("22", "vinte e dois"),
    ("23", "vinte e três"),
    ("24", "vinte e quatro"),
    ("25", "vinte e cinco"),
    ("26", "vinte e seis"),
    ("27", "vinte e sete"),
    ("28", "vinte e oito"),
    ("29", "vinte e nove"),
    ("30", "trinta"),
    ("31", "trinta e um"),
    ("32", "trinta e dois"),
    ("33", "trinta e três"),
    ("34", "trinta e quatro"),
    ("35", "trinta e cinco"),
    ("36", "trinta e seis"),
    ("37", "trinta e sete"),
    ("38", "trinta e oito"),
    ("39", "trinta e nove"),
    ("40", "quarenta"),
    ("41", "quarenta e um"),
    ("42", "quarenta e dois"),
    ("43", "quarenta e três"),
    ("44", "quarenta e quatro"),
    ("45", "quarenta e cinco"),
    ("46", "quarenta e seis"),
    ("47", "quarenta e sete"),
    ("48", "quarenta e oito"),
    ("49", "quarenta e nove"),
    ("50", "cinquenta"),
    ("51", "cinquenta e um"),
    ("52", "cinquenta e dois"),
    ("53", "cinquenta e três"),
    ("54", "cinquenta e quatro"),
    ("55", "cinquenta e cinco"),
    ("56", "cinquenta e seis"),
    ("57", "cinquenta e sete"),
    ("58", "cinquenta e oito"),
    ("59", "cinquenta e nove"),
    ("60", "sessenta"),
    ("61", "sessenta e um"),
    ("62", "sessenta e dois"),
    ("63", "sessenta e três"),
    ("64", "sessenta e quatro"),
    ("65", "sessenta e cinco"),
    ("66", "sessenta e seis"),
    ("67", "sessenta e sete"),
    ("68", "sessenta e oito"),
    ("69", "sessenta e nove"),
    ("70", "setenta"),
    ("71", "setenta e um"),
    ("72", "setenta e dois"),
    ("73", "setenta e três"),
    ("74", "setenta e quatro"),
    ("75", "setenta e cinco"),
    ("76", "setenta e seis"),
    ("77", "setenta e sete"),
    ("78", "setenta e oito"),
    ("79", "setenta e nove"),
    ("80", "oitenta"),
    ("81", "oitenta e um"),
    ("82", "oitenta e dois"),
    ("83", "oitenta e três"),
    ("84", "oitenta e quatro"),
    ("85", "oitenta e cinco"),
    ("86", "oitenta e seis"),
    ("87", "oitenta e sete"),
    ("88", "oitenta e oito"),
    ("89", "oitenta e nove"),
    ("90", "noventa"),
    ("91", "noventa e um"),
    ("92", "noventa e dois"),
    ("93", "noventa e três"),
    ("94", "noventa e quatro"),
    ("95", "noventa e cinco"),
    ("96", "noventa e seis"),
    ("97", "noventa e sete"),
    ("98", "noventa e oito"),
    ("99", "noventa e nove"),
    ("100", "cem")}
