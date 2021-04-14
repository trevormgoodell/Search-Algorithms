from data_structs import *
import time

def a_star_scoring(node):
    return len(node.path) + heuristic(node.name, node.goal)

def bfs_scoring(node):
    return len(node.path)

def heuristic(point_1, point_2):
    return abs(point_1[0]-point_2[0]) + abs(point_1[1] - point_2[1])


def BFS(start, end, show_steps, grid):
    init_node = Node(grid[start[0]][start[1]], end, bfs_scoring)

    frontier = PriorityQueue()
    frontier.append(init_node)

    explored = explored_set()

    if start == end:
        return init_node.path

    while frontier.count > 0:
        if show_steps:
            time.sleep(0.01)

        (_, _, node) = frontier.pop()

        if node.is_goal:
            return node.path

        explored.add(node)

        neighbors = node.generate_neighbors()

        for child_node in neighbors:
            if not (child_node in explored or child_node in frontier):
                if child_node.is_goal:
                    return child_node.path
                frontier.append(child_node)

    pass

def DFS(start, end, show_steps, grid, node = None, path = None):
    if node is None:
        node = Node(grid[start[0]][start[1]], end, bfs_scoring)
    if path is None:
        path = []

    node.curr_square.explored = True
    path.append(start)

    if start == end:
        return path   
    else:
        neighbors = node.generate_neighbors()
        for child_node in neighbors:
            child_node.curr_square.frontier = True
        for child_node in neighbors:
            if child_node.curr_square.explored == False:
                return DFS(child_node.name, end, show_steps, grid, path = path)

def A_STAR(start, end, show_steps, grid):
    init_node = Node(grid[start[0]][start[1]], end, a_star_scoring)

    frontier = PriorityQueue()
    frontier.append(init_node)

    explored = explored_set()

    if start == end:
        return init_node.path

    while frontier.count > 0:
        if show_steps:
            time.sleep(0.01)

        (_, _, node) = frontier.pop()

        if node.is_goal:
            return node.path

        explored.add(node)

        neighbors = node.generate_neighbors()

        neighbors.sort(key = lambda child: child.score)

        for child_node in neighbors:
            if not (child_node in explored or child_node in frontier):
                frontier.append(child_node)
            elif child_node in frontier:
                for frontier_node in frontier:
                    if frontier_node.name == child_node.name:
                        if child_node.score < frontier_node.score:
                            frontier.remove(frontier_node)
                            frontier.append(child_node)

    return []

def bidirectional_A_STAR(start, end, show_steps, grid):
    forward_init_node = Node(grid[start[0]][start[1]], end, a_star_scoring)

    forward_frontier = PriorityQueue()
    forward_frontier.append(forward_init_node)

    forward_explored = explored_set()

    if start == end:
        return forward_init_node.path

    backward_init_node = Node(grid[end[0]][end[1]], start, a_star_scoring)

    backward_frontier = PriorityQueue()
    backward_frontier.append(backward_init_node)

    backward_explored = explored_set()

    if start == end:
        return backward_init_node.path

    best_path = []

    forward_done = False
    backward_done = False

    while forward_frontier.count > 0 or backward_frontier.count > 0:
        if show_steps:
            time.sleep(0.01)
        if forward_done and backward_done:
            return best_path

        if forward_frontier.count > 0:
            (_, _, forward_node) = forward_frontier.pop()

            if forward_node.score > len(best_path) and best_path != []:
                forward_done = True

            if forward_node.is_goal:
                return forward_node.path

            forward_explored.add(forward_node)

            forward_neighbors = forward_node.generate_neighbors()

            forward_neighbors.sort(key = lambda child: child.score)

            for forward_child_node in forward_neighbors:
                if not (forward_child_node in forward_explored or forward_child_node in forward_frontier):
                    forward_frontier.append(forward_child_node)
                elif forward_child_node in forward_frontier:
                    for frontier_node in forward_frontier:
                        if frontier_node.name == forward_child_node.name:
                            if forward_child_node.score < frontier_node.score:
                                forward_frontier.remove(frontier_node)
                                forward_frontier.append(forward_child_node)

                if forward_child_node in backward_frontier or forward_child_node in backward_explored:
                    for node in backward_frontier:
                        if node.name == forward_child_node.name:
                            backward_list = node.path.copy()
                            backward_list.reverse()
                            temp_best_path = forward_child_node.path + backward_list[1:]
                            if len(temp_best_path) < len(best_path) or best_path == []:
                                best_path = temp_best_path

                    pass

        if backward_frontier.count > 0:
            (_, _, backward_node) = backward_frontier.pop()

            if backward_node.score > len(best_path) and best_path != []:
                backward_done = True

            if backward_node.is_goal:
                answer = backward_node.path
                answer.reverse()
                return answer

            backward_explored.add(backward_node)

            backward_neighbors = backward_node.generate_neighbors()

            backward_neighbors.sort(key = lambda child: child.score)

            for backward_child_node in backward_neighbors:
                if not (backward_child_node in backward_explored or backward_child_node in backward_frontier):
                    backward_frontier.append(backward_child_node)
                elif backward_child_node in backward_frontier:
                    for frontier_node in backward_frontier:
                        if frontier_node.name == backward_child_node.name:
                            if backward_child_node.score < frontier_node.score:
                                backward_frontier.remove(frontier_node)
                                backward_frontier.append(backward_child_node)

                if backward_child_node in forward_frontier or backward_child_node in forward_explored:
                    for node in forward_frontier:
                        if node.name == backward_child_node.name:
                            backward_list = backward_child_node.path.copy()
                            backward_list.reverse()
                            temp_best_path = node.path + backward_list[1:]
                            if len(temp_best_path) < len(best_path) or best_path == []:
                                best_path = temp_best_path
