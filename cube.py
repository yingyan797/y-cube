import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("agg")
import time

class Cube:
    def __init__(self, colors="rybmcg"):
        axn = "zxy"
        self.axname = axn
        self.colors = colors
        self.dim = 0
        self.axmap = {axn[0]: [0,5], axn[1]: [1,3], axn[2]: [2,4]}
        u = (1,np.sqrt(3),2)
        self.unit = u
        rd = np.array([u[1], -u[0]])
        ld = np.array([-u[1], -u[0]])
        d = np.array([0,-u[2]])
        self.basis1 = [(rd,ld), (rd,d), (-ld, d)]
        self.basis2 = [self.basis1[i] for i in [2,1,0]]
        self.rec = True
        self.maxrec = 10
    
    def clearRecord(self):
        self.recent = [[] for i in range(4)]
        self.recwindow = []
        f = open("static/moves.csv","w")
        f.write("")
        f.close()

    def create(self, dim):
        self.clearRecord()
        self.dim = dim
        self.faces = [np.array([[f for i in range(dim)] for i in range(dim)]) for f in range(6)]
        if self.dim <= 10:
            self.marker = "o"
        else:
            self.marker = '.'
        u = self.unit
        self.origs1 = [np.array([self.dim*u[1], 2*self.dim*u[2]+u[0]]), 
                      np.array([0, 1.5*self.dim*u[2]]), np.array([self.dim*u[1]+u[1], self.dim*u[2]+u[0]])]
        sx = self.dim*u[2]*2.5
        shift = [np.array([sx+u[1]/2,0]), np.array([sx,u[2]]), np.array([sx-u[2],0])]
        self.origs2 = [self.origs1[i]+shift[i] for i in [1,0,2]]

    def randomize(self, rec):
        print("randomize")
        self.clearRecord()
        tmp = self.rec
        self.rec = rec
        for ite in range(max(pow(self.dim, 3), 20)):
            ax = int(3*np.random.random())
            loc = int(self.dim*np.random.random())
            drn = 'L'
            if 2*np.random.random() < 1:
                drn = 'R'
            self.rotate(self.axname[ax], loc, loc, drn)
        self.rec = tmp

    def rotate(self, ax, locf, loct, drn): # counterclockwise drn is true
        if loct < locf:
            tmp = locf
            locf = loct
            loct = tmp
        if locf < 0 or loct >= self.dim:
            return
        if self.rec:
            step = [ax,locf,loct,drn]
            for i in range(4):
                self.recent[i] = [step[i]] + self.recent[i]
            if not self.recwindow:
                self.recwindow = [1]
            else:
                self.recwindow = [self.recwindow[0]+1] + self.recwindow
            if len(self.recent[0]) > self.maxrec:
                for i in range(4):   
                    self.recent[i].pop()
                self.recwindow.pop()
            f = open("static/moves.csv", "a")
            f.write(ax+","+str(locf)+","+str(loct)+","+drn+"\n")
            f.close()
        if self.axname[0] == ax:
            fs = [1,4,3,2]
            if drn == 'R':
                fs = [2,3,4,1]
            line = self.faces[fs[0]][locf:loct+1,:].copy()
            for i in range(len(fs)-1):
                self.faces[fs[i]][locf:loct+1,:] = self.faces[fs[i+1]][locf:loct+1,:]
            self.faces[fs[-1]][locf:loct+1,:] = line
        elif self.axname[1] == ax:
            if drn == 'L':
                line = self.faces[0][self.dim-loct-1:self.dim-locf,:].copy()
                self.faces[0][self.dim-loct-1:self.dim-locf,:] = self.faces[2][:,locf:loct+1].T
                self.faces[2][:,locf:loct+1] = self.faces[5][::-1,self.dim-loct-1:self.dim-locf]
                self.faces[5][:,self.dim-loct-1:self.dim-locf] = self.faces[4][:,self.dim-loct-1:self.dim-locf]
                self.faces[4][:,self.dim-loct-1:self.dim-locf] = line.T
            else:
                line = self.faces[4][:,self.dim-loct-1:self.dim-locf].copy()
                self.faces[4][:,self.dim-loct-1:self.dim-locf] = self.faces[5][:,self.dim-loct-1:self.dim-locf]
                self.faces[5][:,self.dim-loct-1:self.dim-locf] = self.faces[2][::-1,locf:loct+1]
                self.faces[2][:,locf:loct+1] = self.faces[0][self.dim-loct-1:self.dim-locf,:].T
                self.faces[0][self.dim-loct-1:self.dim-locf,:] = line.T
        elif self.axname[2] == ax:
            if drn == 'L':
                line = self.faces[0][:,self.dim-loct-1:self.dim-locf].copy()
                self.faces[0][:,self.dim-loct-1:self.dim-locf] = self.faces[3][::-1,locf:loct+1]
                self.faces[3][:,locf:loct+1] = self.faces[5][self.dim-loct-1:self.dim-locf,::-1].T
                self.faces[5][self.dim-loct-1:self.dim-locf,:] = self.faces[1][::-1,self.dim-loct-1:self.dim-locf].T
                self.faces[1][:,self.dim-loct-1:self.dim-locf] = line
            else:
                line = self.faces[1][:,self.dim-loct-1:self.dim-locf].copy()
                self.faces[1][:,self.dim-loct-1:self.dim-locf] = self.faces[5][self.dim-loct-1:self.dim-locf,::-1].T
                self.faces[5][self.dim-loct-1:self.dim-locf,:] = self.faces[3][::-1,locf:loct+1].T
                self.faces[3][:,locf:loct+1] = self.faces[0][::-1,self.dim-loct-1:self.dim-locf]
                self.faces[0][:,self.dim-loct-1:self.dim-locf] = line
        fp = self.axmap[ax]
        if loct == self.dim-1:
            f = fp[1]
            if drn == 'L':
                self.cw(f)
            else:
                self.ccw(f)
        if locf == 0:
            f = fp[0]
            if drn == 'L':
                self.ccw(f)
            else:
                self.cw(f)

    def moveSteps(self, vis, rev):
        print("reverse", rev)
        f = open("static/moves.csv", "r")
        if not rev:
            while True:
                step = f.readline()
                if not step:
                    f.close()
                    return
                line = step.split(",")
                self.rotate(line[0], int(line[1]), int(line[2]), line[3][0])
                if vis:
                    time.sleep(0.5)
                    self.visual()
        steps = f.readlines()[::-1]
        for step in steps:
            line = step.split(",")
            drn = 'R'
            if line[3][0] == '0':
                drn = 'L'
            self.rotate(line[0], int(line[1]), int(line[2]), drn)
            if vis:
                time.sleep(0.5)
                self.visual()
        f.close()

    def cw(self, f):
        face = self.faces[f]
        newf = np.zeros((self.dim, self.dim))
        for r in range(self.dim):
            newf[:,self.dim-1-r] = face[r,:].T
        self.faces[f] = newf

    def ccw(self, f):
        face = self.faces[f]
        newf = np.zeros((self.dim, self.dim))
        for r in range(self.dim):
            newf[r,:] = face[:,self.dim-1-r].T
        self.faces[f] = newf

    def visual(self):
        # time.sleep(0.05)
        plt.xticks([])
        plt.yticks([])
        csq = []
        xs = []
        ys = []
        for f in range(6):
            face = self.faces[f]
            origs = self.origs1
            basis = self.basis1
            i = f
            if f >= 3:
                origs = self.origs2
                i = f - 3
                basis = self.basis2
            for r in range(self.dim):
                for c in range(self.dim):
                    csq.append(self.colors[int(face[r][c])])
                    coord = origs[i]+np.array(c*basis[i][0]+r*basis[i][1])
                    xs.append(coord[0])
                    ys.append(coord[1])
        plt.scatter(xs, ys, c=csq, marker=self.marker)                    
        u = self.unit
        # x2 = self.dim*u[1]
        # x5 = x2+self.shift[0]
        # y2 = self.dim*u[2]+u[0]
        # xs = np.array([u[1]/2, self.dim*u[1], u[1]/2+2*(self.dim-1)*u[1]+u[2]])
        # ys = np.array([1.5*y2,y2+u[0]/2,1.5*y2])
        # plt.plot(xs, ys, c='k')
        # plt.plot(xs+self.shift[0], ys, c='k')
        # plt.plot([x2, x2], [y2+u[0]/2, y2-u[0]-(self.dim-1)*u[2]], c='k')
        # plt.plot([x5, x5], [y2+u[0]/2, y2-u[0]-(self.dim-1)*u[2]], c='k')
        plt.savefig("static/visual.png")
        plt.clf()

# c = Cube()
# c.create(3)
# # c.randomize(True)
# # c.moveSteps(False, False)
# c.visual()


