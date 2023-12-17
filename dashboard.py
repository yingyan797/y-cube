from flask import Flask, render_template, request
from cube import Cube

app = Flask(__name__)
sim = Cube()

@app.route('/', methods=['GET', 'POST'])    # main page
def index():
    print("request:",request.form)
    d = request.form.get("dimension")
    create = request.form.get("create")
    if create and d:
        sim.create(int(d))
    elif sim.dim == 0:
        sim.create(3)
    if request.form.get("init"):
        sim.create(sim.dim)
    elif request.form.get("random"):
        sim.randomize(False)
    if request.form.get("rec"):
        sim.rec = True
    elif request.form.get("recstop"):
        sim.rec = False
    step = request.form.get("rotate")
    if step:
        ax = step[0]
        loc = int(step[1:-1])
        drn = step[-1]
        sim.rotate(ax,loc,loc,drn)
    ax = request.form.get("axis")
    locs = []
    for i in range(sim.dim):
        if request.form.get("loc"+str(i)):
            locs.append(i)
        if len(locs) >= 3:
            break
    drn = ''
    if request.form.get("rsectl"):
        drn = 'L'
    elif request.form.get("rsectr"):
        drn = 'R'
    if ax and drn:
        if len(locs) == 1:
            loc = locs[0]
            sim.rotate(ax, int(loc), int(loc), drn)
        elif len(locs) == 2:
            sim.rotate(ax, int(locs[0]), int(locs[1]), drn)
    sim.visual()
    rec = [[sim.recwindow[i]]+[sim.recent[j][i] for j in range(4)] for i in range(len(sim.recwindow))]
    print(rec)
    return render_template('index.html', cube=sim, pos=[i for i in range(sim.dim)], recent=rec)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)