
import operator
def if_(test, result, alternative):
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative
orientations = [(1,0), (0, 1), (-1, 0), (0, -1)]
def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best
class storage_MDP:
    def __init__(self, init, actlist, terminals, gamma=.9):
        update(self, init=init, actlist=actlist, terminals=terminals,
               gamma=gamma, states=set(), reward={})
    def transition_function(state, action):
        abstract
    def reward_function(self, state):
        return self.reward[state]
    def movements(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.actlist
def turn_right(orientation):
    return orientations[orientations.index(orientation)-1]
def turn_left(orientation):
    return orientations[(orientations.index(orientation)+1) % len(orientations)]
def argmax(seq, fn):
    return argmin(seq, lambda x: -fn(x))
def update(x, **entries):
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x
def vector_add(a, b):
    return tuple(map(operator.add, a, b))