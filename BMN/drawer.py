import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
markers = []
plotStyles = []
for m in Line2D.markers:
    try:
        if len(m) == 1 and m != ' ':
            markers.append(m)
    except TypeError:
        pass

for marker, color in zip(colors, markers):
  plotStyles.append('{}{}-'.format(marker, color))  
for marker, color in zip(colors[::-1], markers):
  plotStyles.append('{}{}-'.format(marker, color))      

def drawPlot(x, y):
  plt.plot(x, y, 'ro')
  plt.show()

def drawTraectories(traectories):
  fig = plt.figure()
  for t in traectories:
    plt.plot(t['x'], t['y'], 'ro', markersize=3)
  plt.show() 
  fig.savefig('tra.svg', dpi=fig.dpi)

def drawPlots(plots):
    fig = plt.figure()
    for plot in plots:
      plotStyle = plotStyles.pop()
      plotLabel = '{}'.format( plot['secondaryParamValue'])
      x = plot['x'] # list of ordinates
      y = plot['y'] # list of abscises

      plt.plot(x, y, plotStyle, markersize=8, label=plotLabel)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend( fontsize=12, loc=1,ncol=2 ,title=r'magnetic sensitiveness,{}$-\log(\chi) $'.format(10))
    fig.savefig('plots.svg', dpi=fig.dpi) 
    plt.show() 
    
  