import math
from astar import astar
from idastar import idastar
import random

def state2number(state, base):
    idx = 0
    n = base**2
    power = math.ceil(math.log2(n))
    eff_base = 2**power
    for pos in range(n):
        num = state[pos] 
        idx |= pos << (num * eff_base)

    return idx

def number2state(idx, base):
    n = base**2
    power = math.ceil(math.log2(n))
    eff_base = 2**power
    match = eff_base * eff_base - 1
    state = dict()
    for num in range(n):
        pos = (idx >> (num * eff_base)) & match
        state[pos] = num

    return state

def manhattan(x, goal, base):
    maxpos = base**2 - 1
    state = number2state(x, base)
    distance = 0
    for pos, num in state.items():
        if num != 0:
            distance += abs(num - 1 - pos)
            
        # if num == 0:
        #     distance += abs(maxpos - pos)
        # else:
        #     distance += abs(num - 1 - pos)

    return distance

def neighbors(x, base):
    maxpos = base**2 - 1
    state = number2state(x, base)
    pos = None
    for pos, num in state.items():
        if num == 0:
            break

    result = set()
    if pos % base != 0:
        s = state.copy()
        s[pos], s[pos - 1] = s[pos - 1], 0
        result.add(state2number(s, base))

    if (pos + 1) % base != 0:
        s = state.copy()
        s[pos], s[pos + 1] = s[pos + 1], 0
        result.add(state2number(s, base))

    if int(pos / base) != 0:
        s = state.copy()
        s[pos], s[pos - base] = s[pos - base], 0
        result.add(state2number(s, base))

    if int(pos / base) != base - 1:
        s = state.copy()
        s[pos], s[pos + base] = s[pos + base], 0
        result.add(state2number(s, base))

    return result

def solvable(state, base):
    res = 0
    n = base**2
    zero_pos = None
    for pos1 in range(n - 1):
        if state[pos1] == 0:
            zero_pos = pos1
            continue
        
        for pos2 in range(pos1 + 1, n):
            if state[pos2] == 0:
                zero_pos = pos2
                continue
            
            if state[pos2] < state[pos1]:
                res += 1

    zero_row = base - int(zero_pos / base)
    inv_even = (res % 2 == 0)
    base_odd = (base % 2 != 0)
    even_base_case = ((res + zero_row) % 2 != 0)
    if base_odd:
        return inv_even

    return even_base_case
    

def solve(start, base=4):
    if not solvable(start, base):
        return None
    
    n = base**2
    goal = {i : i + 1 for i in range(n - 1)}
    goal[n - 1] = 0
    startState = state2number(start, base)
    goalState = state2number(goal, base)
    return astar(startState, goalState,
                 graph=lambda x: neighbors(x, base),
                 heuristic=lambda x, goal: manhattan(x, goal, base))


def solve_ida(start, base=4):
    if not solvable(start, base):
        return None
    
    n = base**2
    goal = {i : i + 1 for i in range(n - 1)}
    goal[n - 1] = 0
    startState = state2number(start, base)
    goalState = state2number(goal, base)
    return idastar(startState, goalState,
                 graph=lambda x: neighbors(x, base),
                 heuristic=lambda x, goal: manhattan(x, goal, base))



def print_state(number, base):
    state = number2state(number, base)
    n = base**2
    s = ''
    for i in range(n):
        if i != 0 and i % base == 0:
            print(s)

        if i % base == 0:
            s = '{}'.format(state[i])
        else:
            s += '\t{}'.format(state[i])

    print(s)
            
def print_solution(result, base):
    if not result:
        print('Solution not found!')
    else:
        for step, number in enumerate(result):
            print('------ step : {} ------'.format(step))
            print_state(number, base)

def test(base=4):
    n = base**2
    start = [i+1 for i in range(n)]
    start[n - 1] = 0
    # start[1], start[2] = start[2], start[1]
    # start[3], start[2] = start[2], start[3]
    random.shuffle(start)
    
    start = {i : start[i] for i in range(n)}
    print_solution(solve(start, base), base)

def test_ida(base=4):
    n = base**2
    start = [i+1 for i in range(n)]
    start[n - 1] = 0
    # start[1], start[2] = start[2], start[1]
    # start[3], start[2] = start[2], start[3]
    random.shuffle(start)
    start = {i : start[i] for i in range(n)}
    print_solution(solve_ida(start, base), base)
