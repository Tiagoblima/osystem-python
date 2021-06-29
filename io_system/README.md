## Prática Gerenciamento de E/S


Individualmente (ou em dupla), implemente (com qualquer linguagem de programação a sua escolha e sem necessidade de interface gráfica) e apresente (gravando vídeo explicando código e execução):

Um "mini" simulador de gerenciamento de E/S deve ser implementado. 
Para isso, a equipe deverá simular/implementar, de modo configurável (ou comandos para usuário):

1. Informar o intervalo de blocos (e/ou setores) mínimo e máximo em disco;

2. Informar a ordem de blocos a serem visitados (ou definir aleatoriamente a partir de uma quantidade);

3. Implementar UM algoritmo de escalonamento de braço de disco (exceto FCFS, pois seria muito simples e na prática a saída seria a mesma que a entrada);

4. Exibir a ordem dos blocos visitados na prática, conforme o algoritmo implementado.

5. Exibir o tempo de seek parcial a cada requisição (considere uma unidade de tempo por bloco, ex.: para se mover do 2 ao 5, considere 3 u.t.) e, no final, o total de tempo gasto com seek.

2. 
Caso tenha implementado a prática de sistemas de arquivos (conforme a alocação feita nos blocos do disco), atualize a prática para demonstrar a alocação de UM nível de RAID escolhido
(mostrar a alocação em discos distintos). 
A quantidade de discos adicionais pode ser escolhida pelos integrantes da equipe.
A interface com o usuário deve ser manter inalterada (apenas mostrar o resultado nos discos).
Caso não tenha implementado a prática, implemente DOIS algoritmos na primeira questão (ao invés de um).

*Critérios de avaliação:*

Nível de originalidade/autenticidade
Profundidade e detalhamento das informações/explanações (pontuado individualmente).
Completude/"corretude" das implementações (quantidades, requisitos, etc.) e entregáveis (código/projeto + vídeo).
Complexidade dos algoritmos implementados (quanto mais fácil o algoritmo escolhido, menor a nota e vice-versa, pontuado individualmente).
Onde cada critério acima terá a escala: 1 - Excelente, 0,75 - Bom, 0,5 - regular, 0,25 - ruim, 0 - péssimo. A nota da atividade será individual (se feita em dupla, cada integrante deverá apresentar sua parte) com escala de 0 a 10 conforme tais critérios.

Para melhor entendimento da prática, vocês podem utilizar o simulador https://sourceforge.net/projects/oscsimulator/ - OS Sim e/ou ver o vídeo: 
