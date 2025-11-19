import heapq


class Algorithm:
    def __init__(self):
        pass

    def dijkstra_pathfinding(self, start, goal, grid):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            current_g_score, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]].color != "blue":
                    tentative_g_score = current_g_score + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        heapq.heappush(open_set, (tentative_g_score, neighbor))

        return None

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar_pathfinding(self, start, goal, grid):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            neighbors = [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
            for neighbor in neighbors:
                if 0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) and grid[neighbor[0]][neighbor[1]].color != "blue":
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

