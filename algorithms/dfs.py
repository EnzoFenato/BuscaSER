from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        """Busca em Profundidade com limite de profundidade.

        Usa uma pilha LIFO como fronteira. Para evitar ciclos e trabalho
        repetido, guarda a menor profundidade em que cada estado foi
        alcançado: um estado só é revisitado se for alcançado por um
        caminho mais curto (isso mantém a busca completa dentro do limite).
        A solução encontrada NÃO é necessariamente ótima.
        """
        nodes_expanded = 0
        nodes_generated = 1

        if not initial.is_solvable:
            return SearchResult(None, 0, nodes_generated, 1, 0)

        frontier = [initial]
        best_depth = {initial.tiles: initial.cost}
        max_frontier = 1

        while frontier:
            state = frontier.pop()

            # Entrada obsoleta: o estado já foi alcançado por um caminho mais curto
            if best_depth.get(state.tiles, float("inf")) < state.cost:
                continue

            if state.is_goal:
                return SearchResult(state, nodes_expanded, nodes_generated, max_frontier, state.cost)

            if state.cost >= self.depth_limit:
                continue

            nodes_expanded += 1

            # Empilha em ordem reversa para que a primeira ação (UP) seja explorada primeiro
            for child in reversed(state.neighbors()):
                if child.cost < best_depth.get(child.tiles, float("inf")):
                    best_depth[child.tiles] = child.cost
                    nodes_generated += 1
                    # Teste de objetivo na geração: evita descer a pilha inteira
                    # quando o objetivo já é vizinho do nó atual
                    if child.is_goal:
                        return SearchResult(child, nodes_expanded, nodes_generated, max_frontier, child.cost)
                    frontier.append(child)

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
