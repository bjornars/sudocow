methods = []

def solve_mtd(mth):
    methods.append(mth)
    return mth

class Solver:
    GREEN = '\033[01;32m'
    RED = '\033[01;31m'
    RESET = '\033[00m'
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
        print '*%s(%d,%d) = %d - %s%s' % (self.GREEN, n.x + 1, n.y +1, v +1, solve, self.RESET)
        return self.b.setNum(n, v)

    def remove(self, n, v, solve):
        if self.b.removeCand(n, v):
            print '-%s(%d,%d) = %d - %s%s' % (self.RED, n.x + 1, n.y +1, v +1, solve, self.RESET)
            return True
        return False

    # solve methods
    @solve_mtd
    def singles(self):
        for n in self.b.todo:
            # if a number only has one candidates, take it
            if len(n.candidates) == 1:
                self.do(n, n.candidates[0], 'naked single')
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
                        if guess in num.candidates:
                            n += 1
                            cand = num
                    if n == 1:
                        self.do(cand, guess, 'hidden single')
                        return True

        return False
    
    @solve_mtd
    def pairs(self):
        def clear_pairs(pair, line):
            removed = False
            for num in line:
                if not num.candidates == pair:
                    removed |= self.remove(num, pair[0], 'naked pair')
                    removed |= self.remove(num, pair[1], 'naked pair')
            return removed
            
        for grp in self.b.groups.values():
            for line in grp.values():
                # for each 'line' in a group, check if a pair of candidate is unique.
                # if so, remove candiates from all other items in line
                pairs = []
                for num in line:
                    if len(num.candidates) == 2:
                        if num.candidates in pairs:
                            if clear_pairs(num.candidates[:], line):
                                return True
                        else:
                            pairs.append(num.candidates[:])

        return False

