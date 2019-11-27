import  text2dimacs

class Sokoban():
    def __init__(self, filename,state):
        self.map = []
        self.states = state
        self.player = []
        self.boxesstart = []
        self.boxesgoal = []
        self.walls=[]

        with open(filename,'r') as file:
            for line in file:
                self.map.append(list(line[:len(line)-1]))

        self.map[len(self.map)-1] = ''.join(self.map[len(self.map)-1])
       # player = self.map[len(self.map)-1].split(" ")

       # self.player.append(int(player[0]))
       # self.player.append(int(player[1]))
       # self.map.pop(len(self.map)-1)


        # urcit kde su boxy a ich finish a player
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == "o":
                    self.boxesstart.append([i,j])
                elif self.map[i][j] == "_":
                    self.boxesgoal.append([i,j])
                elif self.map[i][j] == "H":
                    self.player.append([i,j])
                elif self.map[i][j] == "X":
                    self.walls.append([i, j])
    def get_map(self):
        return self.map

    def get_stats(self):
        return self.states

    def solve(self):
        self.generate_minisat_input()

    def generate_minisat_input(self):
        with open("minisat_input", 'w') as out:
            self.generate_background_kwn(out)
            self.generate_exclusuivity(out)
            self.generaete_frame_probme(out)
            self.generate_initial_state(out)
            self.generate_actions(out)
            self.generate_goal_state(out)

    def generate_initial_state(self, out):
        # initial state
        out.write("c INITIAL STATE\n")
        out.write("\n")

        # player at his position at start
        out.write("c player at start\n")
        for i in self.player:
            out.write("at(p,{},{},0)".format(i[0], i[1]))
            out.write("\n")

        # boxes at start
        out.write("\n")
        out.write("c boxes at start\n")
        for i in self.boxesstart:
            out.write("at(b,{},{},0)".format( i[0], i[1]))
            out.write("\n")


        # player not at start
        out.write("\n")
        out.write("c player not at start\n")
        for i in range(1, len(self.map) - 1):
            for j in range(1, len(self.map[i]) - 1):
                if (self.map[i][j] != "x" and self.map[i][j] != "H"):
                     out.write("-at(p,{},{},0)".format(i, j))
                     out.write("\n")

        # boxes not at start
        out.write("\n")
        out.write("c boxes not at start\n")
        for box in self.boxesstart:
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    if (self.map[i][j] != "x" and self.map[i][j] != "o"):
                        out.write("-at(b,{},{},0)".format(i, j))
                        out.write("\n")


        out.write("\n")
    def generate_goal_state(self, out):
        # goal state
        out.write("c GOAL STATE\n")
        out.write("\n")

        # boxes at goal
        out.write("\n")
        out.write("c boxes at goal\n")
        for i in self.boxesgoal:
            out.write("at(b,{},{},{})".format( i[0], i[1], self.states))
            out.write("\n")




    def generate_actions(self, out):
        out.write("\n")
        out.write("c ACTIONS")
        out.write("\n")


        out.write("c player moves ")
        out.write("\n")
        for n in range(1,int(self.states)):
            for i in range(1,len(self.map)-1):
                for j in range(1, len(self.map[i])-1):
                    if self.map[i][j] !="x":
                        for s in 'udlr':
                            #move player up
                            if s == "u" and self.map[i-1][j] != "x" :
                                out.write("-move(p,{},{},{},{},{})".format(i-1, j, i , j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(p,{},{},{})\n".format(i, j, n-1))
                                # that step
                                out.write("-move(p,{},{},{},{},{})".format(i-1, j, i , j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i-1, j, n))
                                # ze sa pohol z tadial kde bol
                                out.write("-move(p,{},{},{},{},{})".format(i-1, j, i , j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(p,{},{},{},{},{})".format(i-1, j, i , j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i-1, j, n))
                                # stena ak bude boxa
                                out.write("-move(p,{},{},{},{},{})".format(i-1, j, i , j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i-2, j, n))
                                #boxa
                                out.write("-move(p,{},{},{},{},{})".format(i-1, j, i , j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i-1, j, n))
                            elif s == "d" and self.map[i+1][j] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(p,{},{},{})\n".format(i, j, n - 1))
                                # that step
                                out.write("-move(p,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i + 1, j, n))
                                # ze sa pohol z tadial kde bol
                                out.write("-move(p,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(p,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i + 1, j, n))
                                # stena ak bude boxa
                                out.write("-move(p,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i + 2, j, n))
                                # boxa
                                out.write("-move(p,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i + 1, j, n))
                            elif s == "l" and self.map[i-1][j] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(p,{},{},{})\n".format(i, j, n - 1))
                                # that step
                                out.write("-move(p,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i , j-1, n))
                                # ze sa pohol z tadial kde bol
                                out.write("-move(p,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(p,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i, j - 1, n))
                                # stena ak bude boxa
                                out.write("-move(p,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i - 2, j, n))
                                # boxa
                                out.write("-move(p,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j - 1, n))
                            elif s == "r" and self.map[i][j+1] != "x":
                                out.write("-move(p,{},{},{},{},{})".format(i, j +1, i, j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(p,{},{},{})\n".format(i, j, n +1))
                                # that step
                                out.write("-move(p,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i , j+1, n))
                                # ze sa pohol z tadial kde bo
                                out.write("-move(p,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(p,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i, j + 1, n))
                                # stena ak bude boxa
                                out.write("-move(p,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i + 2, j, n))
                                # boxa
                                out.write("-move(p,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j + 1, n))


        out.write("c boxes moves ")
        out.write("\n")
        for n in range(1, int(self.states)):
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    if self.map[i][j] != "x":
                        for s in 'udlr':
                            # move player up
                            if s == "u" and self.map[i - 1][j] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i - 1, j, i, j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(b,{},{},{})\n".format(i, j, n - 1))
                                # that step
                                out.write("-move(b,{},{},{},{},{})".format(i - 1, j, i, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i - 1, j, n))
                                # ze sa pohol z tadial kde bol
                                out.write("-move(b,{},{},{},{},{})".format(i - 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(b,{},{},{},{},{})".format(i - 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i - 1, j, n))
                                # player je pred boxov krok pred
                                out.write("-move(b,{},{},{},{},{})".format(i - 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i+1 , j, n-1))
                                # player je na mieste boxy
                                out.write("-move(b,{},{},{},{},{})".format(i - 1, j, i, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i , j, n))
                            elif s == "d" and self.map[i + 1][j] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(b,{},{},{})\n".format(i, j, n - 1))
                                # that step
                                out.write("-move(b,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i + 1, j, n))
                                # ze sa pohol z tadial kde bol
                                out.write("-move(b,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(b,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i + 1, j, n))
                                # stena ak bude boxa
                                out.write("-move(b,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i -1, j, n))
                                # boxa
                                out.write("-move(b,{},{},{},{},{})".format(i + 1, j, i, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i , j, n))
                            elif s == "l" and self.map[i - 1][j] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(b,{},{},{})\n".format(i, j, n - 1))
                                # that step
                                out.write("-move(b,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j - 1, n))
                                # ze sa pohol z tadial kde bol
                                out.write("-move(b,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(b,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i, j - 1, n))
                                # stena ak bude boxa
                                out.write("-move(b,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i , j+1, n))
                                # boxa
                                out.write("-move(b,{},{},{},{},{})".format(i, j - 1, i, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j , n))
                            elif s == "r" and self.map[i][j + 1] != "x":
                                out.write("-move(b,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                # player step before
                                out.write("at(b,{},{},{})\n".format(i, j, n + 1))
                                # that step
                                out.write("-move(b,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("at(b,{},{},{})\n".format(i, j + 1, n))
                                # ze sa pohol z tadial kde bo
                                out.write("-move(b,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(b,{},{},{})\n".format(i, j, n))
                                # stena
                                out.write("-move(b,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(w,{},{},{})\n".format(i, j + 1, n))
                                # stena ak bude boxa
                                out.write("-move(b,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("-at(p,{},{},{})\n".format(i , j-1, n))
                                # boxa
                                out.write("-move(b,{},{},{},{},{})".format(i, j + 1, i, j, n))
                                out.write(" v ")
                                out.write("at(p,{},{},{})\n".format(i, j , n))


    def generate_exclusuivity(self, out):
        out.write("\n")
        out.write("c EXCLUSIVITY")
        out.write("\n")

        # player at only one place/state
        out.write("\n")
        out.write("c player at only one place/state")
        out.write("\n")
        for n in range(1, int(self.states )+ 1):
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j] != "x":
                        for k in range(len(self.map)):
                            for l in range(len(self.map[k])):
                                if self.map[k][l] != "x":
                                    if i != k or j != l:
                                        out.write("-at(p,{},{},{}) v -at(p,{},{},{})\n".format(i, j, n, k, l, n))
        out.write("\n")

        # one from player,box,empty at place/state
        out.write("\n")
        out.write("c player or box only one place/state")
        out.write("\n")
        for n in range(1, int(self.states)+ 1):
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j] != "x":
                        out.write("-at(b,{},{},{}) v -at(p,{},{},{})\n".format(i, j, n, i, j, n))
        out.write("\n")

        # player moves exlusvity
        out.write("\n")

        out.write("c player moves exlusivity")
        out.write("\n")
        for n in range(1, int(self.states) + 1):
            for i in range(1, len(self.map) - 1):
                for j in range(1, len(self.map[i]) - 1):
                    if self.map[i][j] != "x":
                        way = []
                        for s in 'udlr':
                            if s == "u" and self.map[i - 1][j] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i-1, j, i , j, n))
                            elif s == "d" and self.map[i + 1][j] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i+1, j, i, j, n))

                            elif s == "l" and self.map[i][j - 1] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i, j-1, i, j, n))

                            elif s == "r" and self.map[i][j + 1] != "x":
                                way.append("-move(p,{},{},{},{},{})".format(i, j+1, i, j, n))
                        for s1 in way:
                            for s2 in way:
                                if s1 != s2:
                                    out.write(s1 + " v " + s2 + "\n")

        out.write("\n")
        # box moves exlusivity
        out.write("c box moves exclusivity")
        out.write("\n")

        out.write("\n")
        for n in range(1, int (self.states) + 1):
            for i in range(1, len(self.map)-1):
                for j in range(1, len(self.map[i])-1):
                    if self.map[i][j] != "x":
                        way = []
                        for s in 'udlr':
                            if s == "u" and self.map[i - 1][j] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i-1, j, i, j, n))
                            elif s == "d" and self.map[i + 1][j] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i+1, j, i, j, n))

                            elif s == "l" and self.map[i][j - 1] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i, j-1, i, j, n))

                            elif s == "r" and self.map[i][j + 1] != "x":
                                way.append("-move(b,{},{},{},{},{})".format(i, j+1, i, j, n))
                        for s1 in way:
                            for s2 in way:
                                if s1 != s2:
                                    out.write(s1 + " v " + s2 + "\n")

        out.write("\n")
        out.write("\n")
    def generate_background_kwn(self,out):
        # player nemoze byt na dvoch poziciach naraz
        out.write("c Player at more positions at the same time \n")
        out.write("\n")
        for n in range(0, int(self.states) ):
            for i in range(0, len(self.map) ):
                for j in range(0, len(self.map[i]) ):
                    if self.map[i][j] != "x":
                        out.write("\n")
                        out.write(" at(p,{},{},{}) ".format(i,j,n))
                        for k in range(0, len(self.map)):
                            for l in range(0, len(self.map[i])):
                              if k!=i  & l!=j :
                                out.write(" v ")
                                out.write(" -at(p,{},{},{}) ".format(k, l, n))
        #boxa nemoze byt na dvoch poziciach naraz
        out.write("\n")
        out.write("c Boxes on more positions\n")
        out.write("\n")
        for n in range(0, int(self.states) ):
            for i in range(0, len(self.map) ):
                for j in range(0, len(self.map[i]) ):
                    if self.map[i][j] != "x":
                        out.write("\n")
                        out.write(" at(b,{},{},{}) ".format(i,j,n))
                        for k in range(0, len(self.map)):
                            for l in range(0, len(self.map[i])):
                              if k!=i  & l!=j :
                                out.write(" v ")
                                out.write(" -at(b,{},{},{}) ".format(k, l, n))
    def generaete_frame_probme(self,out):
        out.write("c FRAME PROBLEM\n")
        out.write("\n")

        #ak je player na nejakom mieste a a neni tam stena a neni krok 0 tak sa tam musel nejako dostat
        out.write("c player frame problem")
        out.write("\n")
        for n in range(1, int (self.states) ):
            for i in range(0, len(self.map)):
                for j in range(0, len(self.map[i])):
                    if self.map[i][j] != "x":
                        out.write("at(p,{},{},{})".format(i,j,n))
                        out.write("v -move(p,{},{},{},{},{}) ".format(i , j, i+1, j, n-1))
                        out.write("v -move(p,{},{},{},{},{}) ".format(i , j, i-1, j, n-1))
                        out.write("v -move(p,{},{},{},{},{}) ".format(i, j, i, j+1, n-1))
                        out.write("v -move(p,{},{},{},{},{}) ".format(i, j + 1, i, j-1, n-1))

                    out.write("\n")

                #to co s playerom len s boxou
                out.write("c player frame problem")
                out.write("\n")
                for n in range(1, int(self.states) ):
                    for i in range(0, len(self.map)):
                        for j in range(0, len(self.map[i])):
                            if self.map[i][j] != "x":
                                out.write("at(b,{},{},{})".format(i, j, n))
                                out.write("-move(b,{},{},{},{},{}) ".format(i, j, i + 1, j, n - 1))
                                out.write("v -move(b,{},{},{},{},{}) ".format(i, j, i - 1, j, n - 1))
                                out.write("v -move(b,{},{},{},{},{}) ".format(i, j, i, j + 1, n - 1))
                                out.write("v -move(b,{},{},{},{},{}) ".format(i, j + 1, i, j - 1, n - 1))

                            out.write("\n")


if __name__ == '__main__':

    import sys
    inp =sys.stdin
    filename =sys.argv[1]

   # states = "12"
    states = sys.argv[2]

    print filename
    print "..Generating input for Minisat.."
    Sokoban = Sokoban(filename, states)
    Sokoban.solve()
    inf = open('minisat_input', 'r')

    outf = sys.stdout
    outf = open('tosat', 'w')

    print "..Converting result for minisat.."
    text2dimacs.translate(inf, outf)

    #os.system(minisat "tosat" "result")

