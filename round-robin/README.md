# Round-Robin-python

## Explicação UNIVESP
link aulas UNIVESP SO: [Sistemas Operacionais UNIVESP TV](https://www.youtube.com/watch?v=Rl6HhDvW984&list=PLxI8Can9yAHeK7GUEGxMsqoPRmJKwI9Jw&ab_channel=UNIVESP)

[link vídeo explicativo do código](https://youtu.be/oPCXKqPVLCo)

**Command:** python main.py --config_file init.config
### Quando o Escalonador é chamado?
Um novo processo é criado
Quando um processo cria outro, qual executar? Pai ou filho?
Um processo chegou ao fim e um processo pronto deve ser executado.
Quando um processo é bloqueado (dependência de E/S), outro deve ser executado.
Executar o processo que esperava esse evento;
Continuar a executar o processo que já era executado; ou
Executar um terceiro processo que esteja pronto para ser executado.


#### Preemptivo:
Quando um processo pode, por algum motivo, perder se uso da CPU
Provoca uma interrupção forçada de um processo para que outro possa usar a CPU.
Não preemptivo:
Permite que o processo sendo executado continue a ser executado.

#### Categorias do Escalonador

Condições de parada do Não preemptivo:
termine de executar;
solicite uma operação de entrada/saída
libere explicitamente o processador, voltando à fila de prontos.


## Sistemas Interativos
### Sistemas que tem interação com o usuário.

### Round-Robin

Antigo, mais simples e mais utilizado;
Preemptivo;
Cada processo recebe um tempo de execução chamado quantum
Ao final desse tempo, o processo é suspenso e outro processo é colocado em execução;
Também suspenso em caso de interrupção;
Escalonador matém uma fila de processos prontos.
Os processos são colocados em uma fila circular (de pontos) e executados um a um.
Quando seu tempo acaba, o processo é suspenso e volta para o final da final.
Outro processo (primeiro da fila) é então colocado em execução.

Quando um processo solicita E/S, vai para a fila de bloqueado e, ao terminar a operação, volta para o final da fila de prontos.
Problema:
Tempo de chaveamento de processos;
Quantum:
Se for muito pequeno, ocorrem muitas trocas diminuindo a eficiência da CPU; Se for muito longo o tempo de reposta é comprometido.


Algoritmos com Prioridades
Cada processo possui uma prioridade
Os Processos prontos com maior prioridade são executados primeiro;
Prioridades são atribuidas dinamicamento (pelo sistema) ou estatisticamente;
Preemptivo;
Round-Robin pressupõe igual prioridade para todos os processos;
Enquanto houver processos na classe maior: rode cada um desses processos usando Round-Robin (quantum fixo de tempo).
Se essa classe não tiver mais processos; passe a de menor prioridade;
Não esqueça de ajustar as prioridades de alguma forma. Do contrário, as menos prioritárias podem nunca rodar (inanição).
