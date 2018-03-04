import matplotlib.pyplot as plt

def drawPlot(x, y):
  plt.plot(x, y, 'ro')
  plt.show()

def drawTraectories(traectories):
  fig = plt.figure()
  for t in traectories:
    plt.plot(t['x'], t['y'], 'ro', markersize=3)
  plt.show() 
  fig.savefig('tra.svg', dpi=fig.dpi)
  