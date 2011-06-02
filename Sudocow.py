from Board import Board

def read_board(filename):
    with open(filename) as f:
        data = f.readlines()
        nx = 0
        ny = 0
        
        first_col = data[1].index('|')
        nx = data[1][first_col:].index('|', 1) -1 

        data2 = []
        for line in data:
            data2.append(''.join([x for x in line if x in '1234567890.']))
        
        data2 = [x for x in data2 if x]
        ny = len(data2) / nx
        # print nx, ny
        # print '\n'.join(data2)

        board = Board(nx, ny)
        for y, line in enumerate(data2):
            for x, value in enumerate(line):
                if value in '123456789':
                    board.set(x, y, int(value)-1)
        
        return board

b = read_board('boards/test1.ss')
b.display()
print b.numbers[0][0].options
print b.numbers[1][0].options
print b.numbers[2][0].options
print b.numbers[3][0].options
print b.numbers[4][0].options
print b.numbers[5][0].options
print b.numbers[6][0].options
print b.numbers[7][0].options
print b.numbers[8][0].options

b.solve()


# b.display()


