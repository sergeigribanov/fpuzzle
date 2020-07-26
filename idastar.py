
def search(path, g, bound, goal, graph,
           heuristic, distance):
    node = path[-1]
    f = g + heuristic(node, goal)
    if f > bound:
        return f

    if node == goal:
        return 'FOUND'

    minval = float('inf')
    for neighbor in graph(node):
        if neighbor not in path:
            path.append(neighbor)
            t = search(path, g + distance(node, neighbor), bound,
                       goal, graph, heuristic, distance)
            if t == 'FOUND':
                return 'FOUND'

            if t < minval:
                minval = t

            path.pop()

    return minval


def idastar(start, goal, graph, heuristic,
            distance = lambda x, y: 1):
    bound = heuristic(start, goal)
    path = [start]
    while True:
        t = search(path, 0, bound, goal,
                   graph, heuristic, distance)
        if t == 'FOUND':
            return path
        
        if t ==  float('inf'):
            return None

        bound = t
