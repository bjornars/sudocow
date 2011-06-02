GROUPS = ['row', 'col', 'box']
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
    
    @solve_mtd
    def locked_candidates_2(self):
    # TODO: locked candidates_1
        for grp in 'row', 'col':
            group = self.b.groups[grp]
            for nr, line in group.iteritems():

                # for each row or coloumn, check if all candiates for a guess are 
                # contained within a single box. if so, remove the candidate from other lines within the box
                for guess in range(self.b.dim):
                    boxes = [item.group('box') for item in line if guess in item.candidates]
                    if len( set(boxes) ) == 1: 
                        # all candidates for this number in this line is in the same box
                        box = self.b.groups['box'][boxes[0]]

                        # check if there are candidates in the box outside the line
                        cands_in_box = set(item for item in  box if guess in item.candidates)
                        cands_in_line = set(item for item in line if guess in item.candidates) 
                        if cands_in_box > cands_in_line:
                            for item in cands_in_box - cands_in_line:
                                self.remove(item, guess, 'locked candidates 2')
                            return True

                    

