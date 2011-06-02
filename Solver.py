methods = []

def solve_mtd(mth):
    methods.append(mth)
    return mth

class Solver:
    def __init__(self, board):
        self.b = board

    def solve(self):
        todo = self.b.todo
        while self.b.todo:
            deadlock = True
            for method in methods:
                if method(self):
                    break
            else:
                print 'stuck!'
                break
        if not self.b.todo:
            print 'EXCELSIOR!'

    def do(self, n, v, solve):
        print '(%d,%d) = %d - %s' % (n.x + 1, n.y +1, v +1, solve)
        self.b.setNum(n, v)

    # solve methods
    @solve_mtd
    def singles(self):
        for n in self.b.todo:
            # if a number only has one options, take it
            if len(n.options) == 1:
                self.do(n, n.options[0], 'single')
                return True

        return False
 
    @solve_mtd
    def hidden_singles(self):
        for grp in self.b.groups.values():
            for line in grp.values():
                # for each 'line' in a group, check if a candidate is unique, if so take it

                for guess in range(self.b.dim):
                    n = 0
                    cand = None
                    for num in line:
                        if guess in num.options:
                            n += 1
                            cand = num
                    if n == 1:
                        self.do(cand, guess, 'hidden single')
                        return True

        return False
 
