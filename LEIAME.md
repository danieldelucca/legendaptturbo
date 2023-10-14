# Legenda PT Turbo

Bem-vindo! O Legenda PT Turbo é um script em Python que faz ajustes em legendas em português brasileiro seguindo algumas especificações geralmente exigidas pelos serviços de streaming e corrige falhas comuns de tradutores automáticos, como traduções de short answers. Além disso, também prepara uma legenda em idioma estrangeiro, seguindo as mesmas especificações, para que seja traduzida pelo ChatGPT, utilizando uma conta gratuita. O script pode trabalhar de duas formas:

- apenas com uma legenda em português
- com uma legenda em outro idioma e outra em português traduzida por tradutor automático.

    **Atenção:**
    - para que o script rode corretamente, essas duas legendas devem obrigatoriamente ter o mesmo número de blocos de legenda, numerados da mesma forma e deve haver uma tradução direta;

    - ao fazer a tradução automática em um programa de legendagem como Subtitle Edit, faça-o sem a opção de juntar linhas (no caso do SE, essa opção fica na janela que executa a tradução, embaixo à esquerda);

    - caso o script seja rodado apenas com a legenda em português, algumas funcionalidades não serão executadas, como a reversão da tradução de nomes feita por tradutores automáticos.

  Há uma série de possibilidades de correções e substituições que o próprio usuário pode explorar e aprimorar utilizando os arquivos .txt da pasta "configurações".


## Instalação

1. Instale o Python no seu PC, caso ainda não esteja instalado. Para isso, entre em:
   https://www.python.org/downloads/
2. Clone este repositório ou baixe o arquivo ZIP.
3. Extraia o arquivo ZIP para uma pasta de sua escolha no seu PC.


## Uso

#### Arquivos .txt da pasta configurações
Verifique as listas de substituições dos arquivos .txt da pasta configurações. Ver seção abaixo neste documento.


#### Para traduzir uma legenda em idioma estrangeiro com uma conta gratuita no ChatGPT

1. Verifique as funcionalidades opcionais em **configurar.txt**, marcando "sim" ou "não" para ativá-las ou desativá-las.
2. Abra o arquivo **preparar_legenda_estrangeira.exe** e basta seguir as instruções.

#### Para processar a legenda traduzida em português

1. No arquivo **configurar.txt**, ajuste o número máximo de caracteres permitidos, caso saiba e deseje utilizar esse parâmetro.
Esse parâmetro servirá para que duas linhas curtas sejam unidas em uma só no mesmo bloco de legenda.
2. Verifique as funcionalidades opcionais em **configurar.txt**, marcando "sim" ou "não" para ativá-las ou desativá-las.
3. Verifique os arquivos .txt na pasta **configurações** para explorar as possibilidades de algumas das funcionalidades.
4. Execute o arquivo **legenda_pt_turbo.exe**. Além do arquivo traduzido em português, é possível abrir o arquivo em idioma estrangeiro, a partir do qual foi gerada a tradução em português, para que certas funcionalidades sejam executadas.
5. Quando o programa é rodado, ele lista os nomes próprios de personagens detectados. Se desejar, adicione nomes não detectados no arquivo **configurar.txt** e rode o programa novamente. Isso garantirá que os artigos sejam adicionados corretamente antes desses nomes.


## Funcionalidades

- **Traduções específicas de frases:**
    No arquivo _traduções_específicas_de_frases.txt_, há uma lista de frases em inglês e espanhol, juntamente com as traduções em português desejadas. Essa funcionalidade detecta essas frases nas legendas em idiomas estrangeiros e corrige suas traduções para coincidirem com as desejadas na lista. As frases devem terminar com pontuação para que esse recurso funcione.

    _"Over." --> "Câmbio."_

    O Google Tradutor, por exemplo, traduz "Over." como "Sobre." Neste caso, o programa irá substituir "Sobre." por "Câmbio."


- **Corrigir traduções de short answers do inglês**, que geralmente são traduzidas com o verbo "fazer". Uma resposta como "Yes, I do." costuma ser traduzida por tradutores automáticos como "Sim, eu faço." O programa pega o verbo da linha anterior e inclui na resposta.

    _"Você acha que eles vêm hoje?" --> "Sim, acho."_

- **Detectar nomes próprios e adicionar artigos** antes deles, como se costuma usar em linguagem informal em várias regiões do Brasil. Artigos também são adicionados antes de títulos (Sr., Sra., etc).
    
    _"de João." --> "do João."_, _"Marcelo entrou na empresa ano passado." --> "O Marcelo entrou na empresa ano passado."_, _"Sra. Ana viajou ao Rio." --> "A Sra. Ana viajou ao Rio."_

    Quando o script é rodado, uma lista de nomes masculinos e femininos é apresentada. Se o usuário do script perceber que não foram detectados todos os nomes, tem a opção de consultar o site do IMBD e/ou o roteiro fornecido pelo cliente para copiar os nomes não detectados na lista de nomes em **configurar.txt** de modo que essa funcionalidade abranja o máximo de nomes possível.

- **Reverter traduções de nomes:** se o nome do personagem for John e houve a tradução, o programa converte de volta para o nome original.

    _"João" --> "John"_, _"Maria" --> "Mary"_, _"Luís" --> "Luis"_

- **Escrever por extenso números de 0 a 10.**

    _"5 pessoas..." --> "cinco pessoas..."_

- **Escrever por extenso números de 11 a 100 em começos de frases.**

    _"23 países participaram do..." --> "Vinte e três países participaram do..."_

- **Transformar ênclises em próclises.**

    _"Amo-te." --> "Te amo."_

    Este recurso faz essa transformação com "me", "te", "o", "os", "as", "a", "nos", "lhe" e "se". No caso de "lhe", o pronome utilizado na próclise é "te", mas é necessário verificar as ocorrências, pois "lhe" pode se tratar de terceira pessoa. No caso de "se", a transformação não é feita em imperativos, nos quais o "se" permanece como ênclise (_"Comporte-se."_)

- **Transformar minúsculas em maiúsculas logo depois de pontuação.**

    _"Eles chegaram. ela veio também." --> "Eles chegaram. Ela veio também."_

- **Voltar verbo para a linha anterior** se ele estiver no início de uma linha, mas não no início da frase, para que não sejam separados sujeito e verbo.

    _"Eu li o email que ele / enviou aquele dia, depois da briga." --> "Eu li o email que ele enviou / aquele dia, depois da briga"_

- **Juntar linhas que são muito curtas em uma só,** respeitando o número de caracteres máximo permitido por linha que consta em configurar.txt

    _"Eles dormiram lá mesmo. / Como conseguem?" --> "Eles dormiram lá mesmo. Como conseguem?"_

- **Remover interjeições como "ah", "oh", "ei", "ai"**, como constar no arquivo remover_ah_ai_ei.txt. Recurso opcional.
  
  _"Ah, você achou?" --> "Você achou?"_

- **Transformar gerúndio português em brasileiro.** Recurso opcional.

    _"Estava a fazer" --> "Estava fazendo"_ 

- **Consertar imperativos erroneamente traduzidos do inglês como infinitivos**
    
    _"Falar." --> "Fale."_

- **Remover "♪" e deixar a linha em itálico, se já não for.** Recurso opcional.

- **Transformar "a gente" + verbo apenas no verbo na primeira pessoa do plural**, para encurtar o texto. Recurso opcional.

    _"A gente foi ao..." --> "Fomos ao..."_

- **Juntar na mesma linha termos que não devem ser separados por quebras de linhas** listados em configurar.txt.

    _"Ele mora em São / Paulo com a família dele." --> "Ele mora em São Paulo / com a família dele."_

- **Quebrar linha antes de palavras** como preposições ("a", "com", "de", etc) e conjunções ("e", "mas", etc).

    _"Ela estava na Ásia viajando com / os amigos da família." --> "Ela estava na Ásia viajando / com os amigos da família."_

- **Transformar "você" objeto em "te".** Recurso opcional.

    _"Amo você." --> "Te amo."_

- **Trocar o caractere "½" por ",5"**
    _"2½ toneladas" --> "2,5 toneladas"_

- **Transformar números com ",5" em "e meio".**

    _"2,5 toneladas" --> "2 toneladas e meia"_

- **Remover créditos de tradução e legendagem:** são removidas linhas com termos como "Legendas por", "Tradução por", e mais o que for adicionado na parte "remover linhas com isso:" do arquivo **configurar.txt**.

- **Remover closed captions.**

    _"[PÁSSAROS CANTANDO]" --> ""_

- **Remover tags de closed captions com nomes dos personagens que estão falando.**

    _"BILL: Eles não vieram ainda." --> "Eles não vieram ainda"_

- **Arrumar diálogos desconfigurados pelo tradutor automático:** às vezes a "-" dos diálogos acaba no meio de uma das linhas e outros problemas do tipo. O programa ajusta os diálogos com as "-" no início das duas linhas do bloco da legenda.

    _"-Eles disseram que iam chegar hoje, / mas não tenho certeza. -Eu sei." --> "-Eles disseram que iam chegar hoje, mas não tenho certeza. / -Eu sei."_

- **Remover reticências do início das linhas.** Recurso opcional.

    _"...e disse que ia pensar." --> "e disse que ia pensar."_

- **Remover reticências do fim das linhas.** Recurso opcional.

    _"Ela está vindo..." --> "Ela está vindo"_

- **Remover espaços duplos.**
    
    _"Ele  chegou ontem." --> "Ele chegou ontem."_

- **Trocar l por I em palavras totalmente maiúsculas.**

    _"ClDADE" --> "CIDADE"_

- **Devolver pontuação erroneamente retirada** pelo tratudor automático
  do fim de alguns blocos de legenda.


### Listas de substituições:

Essas listas são arquivos .txt da pasta "configurações" e são organizados de modo que o usuário do programa possa editar, excluir e adicionar os termos a serem substituídos e os termos que vão entrar no lugar. Os arquivos cujo nome termina com "estrangeiro" tem as listas de substituições a serem realizadas na preparação da legenda em idioma estrangeiro. Em todas as listas da pasta configurações, cada linha é formatada da seguinte forma:

termo a ser substituído = termo para entrar no lugar

- **substituições_em_começo_de_pergunta.txt**
Nesse arquivo são listados termos a serem substituídos apenas caso a frase em questão termine com "?".

    _"Você quer um café?" --> "Quer um café?"_
    
    Neste caso, se há a frase "Você quer dinheiro.", a substituição não será feita, pois a frase não termina com "?".

- **substituições_sem_pontuação.txt**
Os termos listados nesse arquivo serão substituídos desde que não haja pontuação logo em seguida a ele.

    _"Estudei em uma escola perto daqui." --> "Estudei numa escola perto daqui."_

    Se há uma ocorrência de "em uma." (com ponto), a substituição não é feita, como em: _"Eu estudei em uma."_

- **substituições_case_sensitive.txt**
Os termos listados nesse arquivo serão substituídos apenas se as letras maiúsculas ou minúsculas forem idênticas às da lista.

    _"Muito obrigado" --> "Muito obrigado, "_

    _"Muito obrigado Paulo." --> "Muito obrigado, Paulo."_

    Isso pode servir para controlar que o termo seja substituído apenas em começos de frases, por exemplo.

    Se há a frase _"Quero dizer muito obrigado a vocês."_, a substituição não será feita, pois "muito obrigado" está minúsculo.

- **substituições_case_insensitive.txt**
Os termos listados nesse arquivo serão substituídos independente de as ocorrências na legenda estarem em maiúsculas ou minúsculas.

    _"a seu" --> "ao seu"_

    _"Diga a seu amigo que..." --> "Diga ao seu amigo que..."_

    _"A seu amigo." --> "Ao seu amigo."_

- **substituições_sem_limite_de_palavra.txt**
Os termos ou caracteres listados nesse arquivo são substituídos mesmo se estiverem dentro ou nas extremidades de uma palavra.

    _"?!" --> "?"_
    
    _"O quê?!" --> "O quê?"_

- **substituições específicas de termos listados em configurar.txt.**
Caso o tradutor automático traduza algum termo de uma forma não desejada, o termo pode ser listado nessa lista.

    Se _"pueblo"_ é traduzido como _"cidade"_, mas o tradutor deseja trocar todas as vezes _"cidade"_ por _"povoado"_.

- **remover linhas que tenham termos específicos, listados em configurar.txt.**
Se o termo _"tradução por"_ constar na lista, se uma linha tem _"Tradução por: João da Silva"_, a linha toda será eliminada.


## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

- Daniel de Lucca
- danielkdelucca@hotmail.com
