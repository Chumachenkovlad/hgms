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

def drawPlots(plots_data):
    fig = plt.figure()
    for key in plots_data.keys():
      x = plots_data[key]['x'];
      y = plots_data[key]['y'];
      plt.plot(x, y, 'r--', markersize=4)
    plt.show() 
    fig.savefig('plots.svg', dpi=fig.dpi)  
  