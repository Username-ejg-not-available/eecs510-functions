from copy import deepcopy
from Util import bSort

class Graph:
    def __init__(self,v):
        self.vertices = v
        self.edges = [[] for column in range(v)]

    def add(self, edge):
        if edge[1] not in self.edges[edge[0]]:
            self.edges[edge[0]].append(edge[1])
            bSort(self.edges[edge[0]],len(self.edges[edge[0]]))
        if edge[0] not in self.edges[edge[1]]:
            self.edges[edge[1]].append(edge[0])
            bSort(self.edges[edge[1]],len(self.edges[edge[1]]))

    def remove(self,edge):
        self.edges[edge[0]].remove(edge[1])
        self.edges[edge[1]].remove(edge[0])
       
    def hasEulerCircuit(self):
        for i in self.edges:
            if len(i) % 2:
               return False
        return True

    def hasEulerPath(self):
        result = 0
        for i in self.edges:
            if len(i) % 2:
               result += 1
        if result == 2 or not result:
            return True
        return False

    def findEulerPath(self):
        if not self.hasEulerPath():
            return False
        cur = 0
        for i in range(len(self.edges)):
            if len(self.edges[i]) % 2:
                cur = i
                break
        self.eulerPathHelp(cur)

    def eulerPathHelp(self,cur):
        for i in range(0,len(self.edges[cur])):
            if not len(self.edges[cur]):
                return
            v = self.edges[cur][i]
            if self.isValid([cur,v]):
                print("[" + str(cur) + "," + str(v) + "]")
                self.remove([cur,v])
                self.eulerPathHelp(v)
                
    def isValid(self,edge):
        if len(self.edges[edge[0]]) == 1:
            return True
        vi = [False for column in range(len(self.edges))]
        c1 = self.c(edge[0], vi)
        self.remove(edge)
        for i in range(len(vi)):
            vi[i] = False
        c2 = self.c(edge[0],vi)
        self.add(edge)
        return c1 <= c2

    def c(self,v,vi):
        vi[v] = True
        count = 1
        for i in self.edges[v]:
            if not vi[i]:
                count += self.c(i,vi)
        return count

    def findHPath(self):
        r = []
        return (self.hPathHelper(0,r),r)

    def hPathHelper(self,curr,result):
        result.append(curr)
        if len(result) == self.vertices:
            return True
        z = False
        for i in range(self.vertices):
            if i not in result and i in self.edges[curr]:
                z = self.hPathHelper(i,result)
        if not z:
            del r[-1]
        return z

    def findHCircuit(self):
        r=[]
        return (self.hCircuitHelper(0,r),r)

    def hCircuitHelper(self,curr,r):
        r.append(curr)
        if len(r) == self.vertices and r[0] in self.edges[curr]:
            r.append(r[0])
            return True
        z = False
        for i in range(self.vertices):
            if i not in r and i in self.edges[curr] and not z:
                z = self.hCircuitHelper(i,r)
        if not z:
            del r[-1]
        return z

    def areIsomorphic(self,graph2):
        if self.vertices != graph2.vertices:
            print("Not isomorphic")
            return False
        sum1 = 0
        sum2 = 0
        for i in range(len(self.edges)):
            for j in self.edges[i]:
                sum1 += 1
            for j in graph2.edges[i]:
                sum2 += 1
        if sum1 != sum2:
            print("Not isomorphic")
            return False
        tester = deepcopy(graph2)
        L = [i for i in range(len(self.edges))]
        if self.isoHelp(tester,L):
            result = ""
            for i in range(len(L)):
                result += "f(u" + str(i) + ") = v" + str(L[i]) + ", "
            print(result)
            return True
        else:
            print("Not isomorphic")
            return False

    def isoHelp(self,gr,L,step = 0):
        if step == len(gr.edges):
            isCorrect = True
            for i in range(len(self.edges)):
                if len(self.edges[i]) == len(gr.edges[i]):
                    for j in range(len(self.edges[i])):
                        if self.edges[i][j] != gr.edges[i][j]:
                            isCorrect = False
                            break
                else:
                    isCorrect = False
                    break
            if isCorrect:
                return True
        for i in range(step, len(gr.edges)):
            gr.swapVertices(step,i)
            temp = L[step]
            L[step] = L[i]
            L[i] = temp
            if self.isoHelp(gr,L,step+1):
                return True
        return False

    def swapVertices(self,v1,v2):
        temp = self.edges[v1]
        self.edges[v1] = self.edges[v2]
        self.edges[v2] = temp
        for i in range(len(self.edges)):
            for j in range(len(self.edges[i])):
                if self.edges[i][j] == v1:
                    self.edges[i][j] = v2
                elif self.edges[i][j] == v2:
                    self.edges[i][j] = v1
            bSort(self.edges[i],len(self.edges[i]))

    def isBipartite(self):
        v1 = [0]
        v2 = []
        while (len(v1) + len(v2) < len(self.edges)):
            for i in v1:
                for j in self.edges[i]:
                    if j in v2:
                        continue
                    v2.append(j)
            for i in v2:
                for j in self.edges[i]:
                    if j in v1:
                        continue
                    v1.append(j)
        for i in v1:
            if i in v2:
                print("Not bipartite")
                return False
        for i in v2:
            if i in v1:
                print("Not bipartite")
                return False
        for i in v1:
            for j in v1:
                if self.edges[i] != self.edges[j]:
                    print("Bipartite")
                    return True
        print("Complete Bipartite")
        return True

    #Right example from slide 32 of intro to graph theory
    #prints whether the graph is bipartite, complete bipartite, or not
    #add in [1,6] to make graph complete bipartite
    #constructor parameter is number of vertices
    """bipart = Graph(7)
    bipart.add([0,2])
    bipart.add([0,4])
    bipart.add([0,5])
    bipart.add([0,6])
    bipart.add([1,4])
    bipart.add([1,5])
    bipart.add([1,2])
    bipart.add([3,2])
    bipart.add([3,4])
    bipart.add([3,5])
    bipart.add([3,6])
    bipart.isBipartite()"""
    
    #Example 11 from slides
    #Finds and prints one-to-one correspondence if it exists
    #literally just an overhauled string permutations function but with a list
    #the 1-1 correspondence this example gives is not the same as the one in the slides
    #However is it still a 1-1 correspondence. There can be multiple
    #constructor parameter is number of vertices
    """iso = Graph(6)
    iso.add([0,1])
    iso.add([0,3])
    iso.add([1,2])
    iso.add([1,5])
    iso.add([2,3])
    iso.add([3,4])
    iso.add([4,5])
    p = Graph(6)
    p.add([0,1])
    p.add([0,4])
    p.add([1,2])
    p.add([2,5])
    p.add([2,3])
    p.add([3,4])
    p.add([4,5])
    iso.areIsomorphic(p)"""
    
    #Dirac's Theorem example from slides except mine works 100% of the time
    #this shit is literally just the maze walker algorithm
    #both functions double as a "has" function, will return false if no path or circuit exists
    """g = Graph(5)
    g.add([0,1])
    g.add([0,2])
    g.add([0,4])
    g.add([1,4])
    g.add([1,2])
    g.add([2,4])
    g.add([2,3])
    g.add([3,4])
    print(g.findHPath())
    print(g.findHCircuit())"""
    
    #finding a Euler Circuit from 4/30 In Class Problem.
    #if no circuit exists, function will try to find a path if it exists
    #user can implicitly call gr.hasEulerCircuit() or gr.hasEulerPath()
    #again, numbering of vertices does not matter as long as user is consistent
    #in this case, a = 0, b = 1, etc.
    """gr = Graph(9)
    #[0,1] represents path from a to b, [0,3] a to d, etc.
    gr.add([0,1])
    gr.add([0,3])
    gr.add([1,2])
    gr.add([1,3])
    gr.add([1,4])
    gr.add([2,5])
    gr.add([4,5])
    gr.add([3,4])
    gr.add([3,6])
    gr.add([4,7])
    gr.add([5,8])
    gr.add([5,7])
    gr.add([6,7])
    gr.add([7,8])
    gr.findEulerPath()"""

class DirGraph(Graph):
    def __init__(self,v):
        super().__init__(v)

    def add(self,edge):
        if edge[1] not in self.edges[edge[0]]:
            self.edges[edge[0]].append(edge[1])
            bSort(self.edges[edge[0]],len(self.edges[edge[0]]))

    def remove(self,edge):
        self.edges[edge[0]].remove(edge[1])