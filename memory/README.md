Individualmente (ou em dupla), implemente (com qualquer linguagem de programação a sua escolha e sem necessidade de interface gráfica) e apresente (gravando video explicando código e execução):

1. A alocação de memória usando partições fixas ou variáveis/segmentação (UMA à sua escolha). Deve ser possível configurar/alterar (ou dar opção ao usuário):

a. Estabelecer o tamanho máximo de memória física (em qualquer unidade, MB, KB, etc.)

b. Se partições fixas, definir previamente o tamanho das partições (na mesma unidade que a memória física)

c. Definir um processo de duração “infinita" (thread ou simulado) com nome, ID, tamanho (na mesma unidade que a memória física), etc.

d. A partir da ordem de criação dos processos (FIFO) e DOIS algoritmos de alocação na memória (first-fit, best-fit, worst-fit, etc.), mostrar a alocação da memória (seu estado/capacidade, se há fragmentação interna e/ou externa, além das posições livres/alocadas, etc.)

e. A cada nova alocação, caso a memória esteja cheia, realizar compactação (apenas se as partições forem dinâmicas/segmentação) e, persistindo a falta de memória, retirar aleatoriamente um processo, que irá para a memória secundária (swapping).


2. A alocação de memória usando paginação. Deve ser possível configurar/alterar (ou dar opção ao usuário):

a. Estabelecer o tamanho máximo de memória física (em qualquer unidade, MB, KB, etc.)

b. Estabelecer o tamanho máximo de memória virtual (maior que a memória física e na mesma unidade)

c. Definir previamente o tamanho das páginas (na mesma unidade que a memória física/virtual) e calcular/alocar a quantidade de páginas necessárias a um processo a depender de seu tamanho

d. Definir um processo de duração "infinita" (thread ou simulado) com nome, ID, tamanho (na mesma unidade que a memória física), etc.

e. A partir da ordem de criação dos processos (FIFO) e DOIS algoritmos de substituição de páginas (FIFO, LRU, Relógio, SC, etc. e em caso de algoritmos que verifiquem bits, de tempos em tempos, devem ser alterados/resetados), mostrar a alocação da memória (seu estado/capacidade, se há fragmentação interna, além das páginas livres/alocadas, etc.)

f. A cada nova alocação, caso a memória esteja cheia, aplicar um algoritmo de substituição de páginas (UM selecionado) e substituir uma página (de qualquer processo).

g. Ao final da execução calcule e exiba a quantidade de "page miss" que cada algoritmo sofre no total.

### Critérios de avaliação:

Nível de originalidade/autenticidade
Profundidade e detalhamento das informações/explanações (pontuado individualmente).
Completude/"corretude" das implementações (quantidades, requisitos, etc.) e entregáveis (código/projeto + vídeo).
Complexidade dos algoritmos implementados (quanto mais fácil o algoritmo escolhido, menor a nota e vice-versa, pontuado individualmente).
Onde cada critério acima terá a escala: 1 - Excelente, 0,75 - Bom, 0,5 - regular, 0,25 - ruim, 0 - péssimo. A nota da atividade será individual (se feita em dupla, cada integrante deverá apresentar sua parte) com escala de 0 a 10 conforme tais critérios.

Para melhor entendimento da prática, vocês podem utilizar o simulador https://sourceforge.net/projects/oscsimulator/ - OS Sim e/ou ver o
