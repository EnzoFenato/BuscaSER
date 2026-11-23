import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# Posição (linha, coluna) de cada peça no estado objetivo
GOAL_POSITIONS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma, para cada peça (exceto o vazio),
        das distâncias horizontais e verticais até sua posição no objetivo.

        É admissível (cada movimento desloca uma única peça em 1 casa,
        então nunca superestima o custo real) e consistente.
        """
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(i, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        """Busca A*: expande o nó de menor f(n) = g(n) + h(n).

        Com heurística consistente, a primeira vez que o objetivo é
        retirado da fronteira a solução é ótima.
        """
        nodes_expanded = 0
        nodes_generated = 1

        if not initial.is_solvable:
            return SearchResult(None, 0, nodes_generated, 1, 0)

        tie = count()                # desempate estável na fila de prioridade
        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial.tiles: initial.cost}
        closed = set()
        max_frontier = 1

        while frontier:
            _, _, state = heapq.heappop(frontier)

            if state.tiles in closed:
                continue             # entrada obsoleta na fila

            if state.is_goal:
                return SearchResult(state, nodes_expanded, nodes_generated, max_frontier, state.cost)

            closed.add(state.tiles)
            nodes_expanded += 1

            for child in state.neighbors():
                if child.tiles in closed:
                    continue
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    f = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (f, next(tie), child))
                    nodes_generated += 1

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
