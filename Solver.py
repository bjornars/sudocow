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
def singles(s):
    for n in s.b.todo:
        # if a number only has one candidates, take it
        if len(n.candidates) == 1:
            s.do(n, n.candidates[0], 'naked single')
            return True

@solve_mtd
def hidden_singles(s):
    for group in s.b.groups.values():
        for line in group:
            # for each 'line' in a group, check if a candidate is unique, if so take it
            for guess in range(s.b.dim):
                n = 0
                cand = None
                for num in line:
                    if guess in num.candidates:
                        n += 1
                        cand = num
                if n == 1:
                    s.do(cand, guess, 'hidden single')
                    return True

@solve_mtd
def pairs(s):
    def clear_pairs(pair, line):
        removed = False
        for num in line:
            if not num.candidates == pair:
                removed |= s.remove(num, pair[0], 'naked pair')
                removed |= s.remove(num, pair[1], 'naked pair')
        return removed

    for group in s.b.groups.values():
        for line in group:
            # for each 'line' in a group, check if a pair of candidate is unique.
            # if so, remove candiates from all other cell in line
            pairs = []
            for num in line:
                if len(num.candidates) == 2:
                    if num.candidates in pairs:
                        if clear_pairs(num.candidates[:], line):
                            return True
                    else:
                        pairs.append(num.candidates[:])

@solve_mtd
def locked_candidates_2(s):
# TODO: locked candidates_1
    for grp in 'row', 'col':
        group = s.b.groups[grp]
        for line in group:
            # for each row or coloumn, check if all candiates for a guess are
            # contained within a single box. if so, remove the candidate from other lines within the box
            for guess in range(s.b.dim):
                boxes = [cell.group('box') for cell in line if guess in cell.candidates]
                if len( set(boxes) ) == 1:
                    # all candidates for this number in this line is in the same box
                    box = s.b.groups['box'][boxes[0]]

                    # check if there are candidates in the box outside the line
                    cands_in_box = set(cell for cell in  box if guess in cell.candidates)
                    cands_in_line = set(cell for cell in line if guess in cell.candidates)
                    if cands_in_box > cands_in_line:
                        for cell in cands_in_box - cands_in_line:
                            s.remove(cell, guess, 'locked candidates 2')
                        return True

@solve_mtd
def naked_triples(s):
    naked_tuples(s, 3)

@solve_mtd
def naked_quads(s):
    naked_tuples(s, 4)

def naked_tuples(s, n):
    for group in s.b.groups.values():
        for line in group:
            # for each 'line' in a group, check if an ntuple of candidates is contained within three cells.
            # if so, remove candiates from all other cell in line
            tups = []
            cells = filter(lambda c: len(c.candidates) <= 3 and c in s.b.todo, line)
            if len(cells) <= 3: continue
            for cell in cells:
                tups.append(set(cell.candidates))
                for tup in tups[:]:
                    new_tup = tup.intersection(cell.candidates)
                    if len( new_tup ) >=3 and new_tup not in tups:
                        tups.append(new_tup)

            for tup in tups:
                c = 0
                for cell in line:
                    if not cell in s.b.todo: continue
                    if set(cell.candidates).issubset(tup): 
                        c+= 1

                if c >= 3:
                    # 'more' than three cells were contained in a tup. try removing candidates 
                    # from everything else in the group
                    removed = False
                    for cell in line:
                        if not cell in s.b.todo: continue
                        if set(cell.candidates).issubset(tup): continue 

                        for candidate in tup:
                            removed |= s.remove(cell, candidate, 'naked %ds'% n)
                    
                    if removed: return True

