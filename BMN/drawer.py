import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from params import *
import datetime

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
markers = ["o", "<", "*", "D", "P","X", "^"]
plotStyles = []


def setPlotStyles():
  globals()['plotStyles'] = []
  for marker, color in zip(colors, markers):
    globals()['plotStyles'].append('{}{}-'.format(marker, color))  
  for marker, color in zip(colors[::-1], markers):
    globals()['plotStyles'].append('{}{}-'.format(marker, color)) 
     

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
  setPlotStyles()
  fig = plt.figure()
  plt.subplot(111)
  for plot in plots:
    # print(globals()['plotStyles'])
    plotStyle = globals()['plotStyles'].pop()
    plotLabel = '{}'.format( plot['secondaryParamValue'])
    x = plot['x'] # list of ordinates
    y = plot['y'] # list of abscises

    plt.plot(x, y, plotStyle, markersize=8, label=plotLabel)
  primaryKey = plots[0]['primaryParamKey']
  secondaryKey = plots[0]['secondaryParamKey']

  plt.xlabel(getDescription(primaryKey))
  plt.ylabel(getDescription('DISTANCE'))
  plt.text(0.7, 0.08, staticParamsDescription(['DISTANCE', primaryKey, secondaryKey]), ha='left', fontsize=8, transform=plt.gcf().transFigure)
  plt.legend(
    fontsize=10, 
    loc="upper left", 
    ncol=2 ,
    title=getDescription(secondaryKey), 
    bbox_to_anchor=(1.05, 1)
    )
  plt.subplots_adjust(right=0.65)
  version = int(datetime.datetime.now().strftime('%s'))
  filename = 'results/plots/Y_{}_prymary_{}_secondary_{}_V_{}'.format('DISTANCE', primaryKey, secondaryKey, version)
  fig.savefig(filename+".svg", dpi=fig.dpi) 
  fig.savefig(filename+".png", dpi=fig.dpi) 
  print(filename, ' saved')
    
  