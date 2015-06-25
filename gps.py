# General Problem Solver, version 1 from
# "Principles of Artificial Intelligence Programming".
# Original Lisp code by Peter Norvig.
# Translated to Python by Brandon Corfman.


def is_appropriate(goal, op):
    # An op is appropriate to a goal if it is in its add list.
    return goal in op.add_list


def find_all(item, sequence, func):
    # Find all those elements of sequence that match item, according
    # to the keywords. Doesn't alter sequence.
    result = []
    for op in sequence:
        if func(item, op):
            result.append(op)
    return result


class Op:
    """ A STRIPS-like operator: holds an action, a list of preconditions,
    and an add_list and a delete_list of clauses. """
    def __init__(self, **params):
        self.action = params['action']
        self.preconds = params['preconds']
        self.add_list = params.get('add_list', [])
        self.del_list = params.get('del_list', [])


class GPS:
    def __init__(self, **params):
        self.state = set(params['state'])  # the current state: a set of conditions
        self.goals = set(params['goals'])  # list of goals to achieve
        self.ops = params['ops']      # list of available operators

    def solve(self):
        if all((self.achieve(g) for g in self.goals)):
            return "solved"
        else:
            return "can't solve"

    def achieve(self, goal):
        # A goal is achieved if it already holds,
        # or if there is an appropriate op for it that is applicable.
        return goal in self.state or any((self.apply_op(op) for op in find_all(goal, self.ops, is_appropriate)))

    def apply_op(self, op):
        # Print a message and update state if op is applicable.
        if all((self.achieve(p) for p in op.preconds)):
            print 'Executing ' + op.action
            for x in op.del_list:
                self.state.remove(x)
            for x in op.add_list:
                self.state.add(x)
            return True
        else:
            return False

