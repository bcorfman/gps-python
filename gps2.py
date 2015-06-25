# General Problem Solver, version 2 from
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
            print "solved"
        else:
            print "can't solve"

    def achieve_all(self):
        # Try to achieve each goal, then make sure they still hold.
        return all((self.achieve(x) for x in self.goals)) and self.goals.issubset(self.state)

    def achieve(self, goal):
        # A goal is achieved if it already holds,
        # or if there is an appropriate op for it that is applicable.
        return goal in self.state or any((self.apply_op(op) for op in find_all(goal, self.ops, is_appropriate)))

    def apply_op(self, op):
        # Print a message and update state if op is applicable.
        if all((self.achieve_all(p) for p in op.preconds)):
            print 'Executing ' + op.action
            for x in op.del_list:
                self.state.remove(x)
            for x in op.add_list:
                self.state.add(x)
            return True
        else:
            return False

def main():
    school_ops = [Op(action='drive-son-to-school',
                     preconds=['son-at-home', 'car-works'],
                     add_list=['son-at-school'],
                     del_list=['son-at-home']),
                  Op(action='shop-installs-battery',
                     preconds=['car-needs-battery', 'shop-knows-problem', 'shop-has-money'],
                     add_list=['car-works']),
                  Op(action='tell-shop-problem',
                     preconds=['in-communication-with-shop'],
                     add_list=['shop-knows-problem']),
                  Op(action='telephone-shop',
                     preconds=['know-phone-number'],
                     add_list=['in-communication-with-shop']),
                  Op(action='look-up-number',
                     preconds=['have-phone-book'],
                     add_list=['know-phone-number']),
                  Op(action='give-shop-money',
                     preconds=['have-money'],
                     add_list=['shop-has-money'],
                     del_list=['have-money'])]
    gps = GPS(state=['son-at-home', 'car-needs-battery', 'have-money', 'have-phone-book'],
              goals=['son-at-school'],
              ops=school_ops)
    gps.solve()
    print
    gps = GPS(state=['son-at-home', 'car-needs-battery', 'have-money'],
              goals=['son-at-school'],
              ops=school_ops)
    gps.solve()
    print 
    gps = GPS(state=['son-at-home', 'car-works'],
              goals=['son-at-school'],
              ops=school_ops)
    gps.solve()

if __name__ == '__main__':
    main()
