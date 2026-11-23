from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        """Busca em Largura (busca em grafo).

        Usa uma fila FIFO como fronteira, garantindo que os nós sejam
        expandidos por ordem de profundidade. Como todas as ações têm
        custo 1, a primeira solução encontrada é ótima.
        """
        nodes_expanded = 0
        nodes_generated = 1          # o estado inicial conta como gerado

        if not initial.is_solvable:
            return SearchResult(None, 0, nodes_generated, 1, 0)

        if initial.is_goal:
            return SearchResult(initial, nodes_expanded, nodes_generated, 1, initial.cost)

        frontier = deque([initial])
        reached = {initial.tiles}    # estados já gerados (na fronteira ou expandidos)
        max_frontier = 1

        while frontier:
            state = frontier.popleft()
            nodes_expanded += 1

            for child in state.neighbors():
                if child.tiles in reached:
                    continue
                nodes_generated += 1
                # Teste de objetivo na geração: válido para BFS com custo uniforme
                if child.is_goal:
                    return SearchResult(child, nodes_expanded, nodes_generated, max_frontier, child.cost)
                reached.add(child.tiles)
                frontier.append(child)

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
