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
                if method(self.b):
                    break
            else:
                print 'stuck!'
                break
        if not self.b.todo:
            print 'EXCELSIOR!'

    # solve methods
    @solve_mtd
    def singles(b):
        for n in b.todo:
            if len(n.options) == 1:
                print '(%d,%d) = %d - single' % (n.x + 1, n.y +1, n.options[0] +1)
                b.setNum(n, n.options[0])
                return True

        return False
 
#    @solve_mtd
    def hidden_singles(b):
        return False
        pass
 
 
