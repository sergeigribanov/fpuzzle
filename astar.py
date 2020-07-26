from queue import PriorityQueue

def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
        
    return total_path

def astar(start, goal, graph, heuristic,
          distance = lambda x, y: 1):
    closed = set()
    openedQueue = PriorityQueue()
    gScore = dict()
    gScore[start] = 0
    openedQueue.put((heuristic(start, goal), start))
    opened = {start}
    inf = float('inf')
    cameFrom = dict()
    while not openedQueue.empty():
        _, current = openedQueue.get()
        opened.remove(current)
        if current == goal:
            return reconstruct_path(cameFrom, current)

        if current in closed:
            continue

        closed.add(current)
        # print('closed:')
        # print(closed)
        for neighbor in graph(current):
            # print('neighbor : {}'.format(neighbor))
            tentative_gScore = gScore.get(current, inf) + distance(current, neighbor)
            # print('tentative_gScore : {}'.format(tentative_gScore))
            if tentative_gScore  < gScore.get(neighbor, inf):
                # print('ok 1')
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                priority = gScore.get(neighbor, inf) + heuristic(neighbor, goal)
                # print('priority : {}'.format(priority))
                if neighbor not in opened:
                    # print('ok 2')
                    openedQueue.put((priority, neighbor))
                    opened.add(neighbor)
                
    return None
