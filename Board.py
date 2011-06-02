GROUPS = ['row', 'col', 'box']

class Number:
    def __init__(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y
        self.v = -1
        self.possibilites = list(range(self.board.dim))

    def groups(self):
        return "(%2s, %2s, %2s)" % tuple( [ self.getGroup(x) for x in ['row', 'col', 'box']])
    
    def __str__(self):
        if self.v >= 0:
            return str(self.v)
        
        return '.'

    def getGroup(self, i):
        if i == 'row':
            return self.x
        if i == 'col':
            return self.y
        if i == 'box':
            gx = self.x / self.board.ny
            gy = self.y / self.board.nx
            return gx * self.board.ny + gy

class Board:
    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny
        self.dim = nx*ny
        self.groups = {}
        self.groups['row'] = [None for x in range(self.dim)]
        self.groups['col'] = [None for x in range(self.dim)]
        self.groups['box'] = [None for x in range(self.dim)]
        self.numbers = [ [None for x in range(self.dim)] for y in range(self.dim)]

        for x in range(self.dim):
            for y in range(self.dim):
                for z in GROUPS:
                    num = Number(self, x, y)
                    self.groups[z][num.getGroup(z)] = num
                    self.numbers[x][y] = num

    def display(self):
        def make_div(ends, space, x, y):
            s = ends
            for i in y:
                s += space * x
                s += ends 
            s[:-1]= ''
            return s


        dn = 3
        width = 1 + (dn+1)*self.dim
        divider = '+'.join([''] + ['-' * dn for x in range(self.dim)] + [''])
        divider2 = '|'.join([''] + [' ' * dn for x in range(self.dim)] + [''])
        print divider
              
        for x in range(self.dim):
            if x % self.nx == 0:
                print divider
            print divider2
            print '|'.join([''] + ['%2s ' % self.numbers[x][y] for y in range(self.dim)] + [''])
            print divider2
            print divider
     
if __name__ == '__main__':
    board = Board(3, 3)
    board.display()
