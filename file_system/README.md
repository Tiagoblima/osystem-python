## Prática de Sistema de Arquivos


**Comandos**

Criar um arquivo

    --path usr/myfile.txt --size 10 

Ver um arquivo

    --path usr/myfile.txt --get_file

Listar diretório

    --path usr/ --list_dir

Criar diretório

    --path usr/new_folder --is_folder

Deletar arquivo ou diretório

    --path usr/myfile.txt --delete


Individualmente (ou em dupla), implemente (com qualquer linguagem de programação a sua escolha e sem necessidade de interface gráfica) e apresente (gravando vídeo explicando código e execução):

Um "mini" simulador de sistemas de arquivos deve ser implementado. Para isso, a equipe deverá simular UM mecanismo de alocação a sua escolha (encadeada, indexada, FAT, NTFS, etc.) e permitir que um usuário:

1. Crie e exclua arquivos e diretórios;

2. Realize a listagem de arquivos de um diretório;

3. A cada operação realizada pelo usuário, a alocação deve ser simulada (não apenas mostrar a interface para o usuário, mas também como ficaria em baixo nível - alocação no SA);

4. As informações dos arquivos e diretórios devem conter, pelo menos, nome e tamanho

5. Para facilitar, não permitir arquivos e diretórios com nomes iguais e não precisa implementar várias hierarquias de árvore de diretórios (bastaria dois níveis - um para a raiz e outro para alocar arquivos em um diretório criado).

6. Estabelecer o tamanho máximo de memória física (em qualquer unidade, MB, KB, etc.) e tamanho dos blocos (na mesma unidade da memória física, para facilitar);

7. Indicar se há fragmentação interna ou externa (quando ocorrer).





**Critérios de avaliação:**

Nível de originalidade/autenticidade
Profundidade e detalhamento das informações/explanações (pontuado individualmente).
Completude/"corretude" das implementações (quantidades, requisitos, etc.) e entregáveis (código/projeto + vídeo).
Complexidade dos algoritmos implementados (quanto mais fácil o algoritmo escolhido, menor a nota e vice-versa, pontuado individualmente).
Onde cada critério acima terá a escala: 1 - Excelente, 0,75 - Bom, 0,5 - regular, 0,25 - ruim, 0 - péssimo. A nota da atividade será individual (se feita em dupla, cada integrante deverá apresentar sua parte) com escala de 0 a 10 conforme tais critérios.

Para melhor entendimento da prática, vocês podem utilizar o simulador https://sourceforge.net/projects/oscsimulator/ - OS Sim e/ou ver o vídeo: 


