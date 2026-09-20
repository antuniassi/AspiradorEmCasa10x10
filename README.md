# Aspirador de Pó com A*

Implementação do robô aspirador de pó utilizando o algoritmo de busca A*.

O mapa é gerado aleatoriamente e possui 50% das células sujas. O aspirador começa na posição (0, 0) e pode se mover para cima, baixo, esquerda e direita, além de limpar a célula em que está.

## Algoritmo

O algoritmo utilizado é o A*. Ele escolhe quais estados explorar utilizando:

```text
f(n) = g(n) + h(n)
```

Onde:

* `g(n)` representa o custo das ações realizadas até o estado atual.
* `h(n)` é uma estimativa do custo que ainda falta para limpar o mapa.

Para tornar a busca mais eficiente, a heurística utilizada combina três informações:

```text
h(n) = sujeiras restantes + distância até a sujeira mais próxima + MST
```

### Distância Manhattan

A distância Manhattan calcula a distância entre duas posições considerando apenas movimentos horizontais e verticais:

```text
distância = |linha1 - linha2| + |coluna1 - coluna2|
```

Ela é utilizada para descobrir a distância do aspirador até a sujeira mais próxima.

### MST

A MST (Minimum Spanning Tree / Árvore Geradora Mínima) estima o deslocamento necessário para conectar todas as células que ainda estão sujas.

O algoritmo encontra conexões de menor distância entre as sujeiras utilizando a distância Manhattan. Isso fornece ao A* uma estimativa melhor de quanto o aspirador ainda precisará se deslocar para alcançar todas elas.

Assim, a heurística considera: Quantidade de limpezas que ainda precisam ser feitas + Distância até a sujeira mais próxima + Distância mínima para conectar todas as sujeiras


Com isso, o A* consegue priorizar estados mais promissores e evitar explorar desnecessariamente uma grande quantidade de possibilidades.

Ao executar o programa, o mapa gerado é mostrado no terminal e, ao final, é informado se uma solução foi encontrada e quanto tempo o algoritmo levou para encontrá-la.

Caso o tempo de busca ultrapasse 5 minutos, a execução é interrompida (timeout).