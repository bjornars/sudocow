GROUPS = ['row', 'col', 'box']

class SudokuError(Exception):
    pass

class Number:
    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y
        self.v = -1
        self.candidates = list(range(self.board.dim))

    def groups(self):
        return "(%2s, %2s, %2s)" % tuple( [ self.group(x) for x in ['row', 'col', 'box']])
    
    def __str__(self):
        if self.v >= 0:
            return str(self.v + 1)
        
        return '.'

    def group(self, i):
        if i == 'row':
            return self.y
        if i == 'col':
            return self.x
        if i == 'box':
            gx = self.x / self.board.ny
            gy = self.y / self.board.nx
            return gx * self.board.ny + gy

    def set(self, v):
        if v > self.board.dim:
            raise SudokuError()

        self.v = v

        # remove candidates from self
        self.candidates = [] 

    def removeCand(self, v):
        if v in self.candidates:
            self.candidates.remove(v)
            return True
        else:
            return False

class Board:
    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny
        self.dim = nx*ny

        # create empty groups
        self.groups = {}
        for grp in GROUPS:
            self.groups[grp] = {}
            for x in range(self.dim):
                self.groups[grp][x] = []
        
        # create empty number matrix
        self.numbers = [ [None for x in range(self.dim)] for y in range(self.dim)]
        self.todo = []

        for x in range(self.dim):
            for y in range(self.dim):
                num = Number(self, x, y)
                self.numbers[x][y] = num
                self.todo.append(num)

                # assign to groups
                for z in GROUPS:
                    self.groups[z][num.group(z)].append(num)

    def set(self, x, y, v):
        self.setNum(self.numbers[x][y], v)

    def setNum(self, num, v):
        if num.v != -1: raise SudokuError

        num.set(v)
        self.todo.remove(num)

        # remove candidates from group-mates
        for grp in GROUPS:
            for n in self.groups[grp][num.group(grp)]:
                n.removeCand(v)

        return True
    
    def removeCand(self, num, v):
        return num.removeCand(v)
    
    def display(self):
        BIG = False
        
        def make_div(ends, space, nx, ny):
            s = ends
            for j in range(ny):
                for i in range(nx):
                    s += space
                    if BIG: s += ends 
                s += ends 
            s = s[:-1]
            return s

        dn = 1
        if BIG: dn = 3

        width = 1 + (dn+1)*self.dim
        divider = make_div('+', '-' * dn, self.nx, self.ny)
        divider2 = make_div('|', ' ' * dn, self.nx, self.ny)
        divider3 = make_div('|', '%s', self.nx, self.ny)
        if BIG: divider3 = make_div('|', '%2s ', self.nx, self.ny)
        if BIG: print divider
              
        for y in range(self.dim):
            if y % self.ny == 0:
                print divider 
            if BIG: print divider2
            print divider3 % tuple([self.numbers[x][y] for x in range(self.dim)])
            if BIG: print divider2
            if BIG: print divider

if __name__ == '__main__':
    board = Board(3, 3)
    board.display()
