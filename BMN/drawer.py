import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from params import *
import datetime

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
  plt.subplot(111)
  for plot in plots:
    plotStyle = plotStyles.pop()
    plotLabel = '{}'.format( plot['secondaryParamValue'])
    x = plot['x'] # list of ordinates
    y = plot['y'] # list of abscises

    plt.plot(x, y, plotStyle, markersize=8, label=plotLabel)
  primaryKey = plots[0]['primaryParamKey']
  secondaryKey = plots[0]['secondaryParamKey']

  plt.xlabel(getDescription(primaryKey))
  plt.ylabel(getDescription('DISTANCE'))
  plt.legend( fontsize=12, loc="upper left", ncol=2 ,title=getDescription(secondaryKey), bbox_to_anchor=(1.05, 1))
  plt.subplots_adjust(right=0.65)
  version = int(datetime.datetime.now().strftime('%s'))
  print(staticParamsDescription(['DISTANCE', primaryKey, secondaryKey]))
  filename = 'Y_{}_prymary_{}_secondary_{}_V_{}.svg'.format('DISTANCE', primaryKey, secondaryKey, version)
  fig.savefig(filename, dpi=fig.dpi) 
  plt.show() 
    
  