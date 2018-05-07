import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from params import *
import datetime
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from params import DEFAULT_PARAMS

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
  plt.subplot(111)
  setPlotStyles()
  for t in traectories:
    plotStyle = globals()['plotStyles'].pop()
    plt.plot(t['x'], t['y'], plotStyle, markersize=2, label=t['R'])
  plt.legend(
    fontsize=10, 
    loc="upper left", 
    ncol=2 , 
    bbox_to_anchor=(1.05, 1)
    )
  plt.subplots_adjust(right=0.65)  
  version = int(datetime.datetime.now().strftime('%s'))
  fig.savefig('results/tra/tra-{}.svg'.format(version), dpi=fig.dpi)
  fig.savefig('results/tra/tra-{}.png'.format(version), dpi=fig.dpi)
  print('saved')

def drawWalkingToChain(traectories):
  fig = plt.figure()
  plt.subplot(111)
  setPlotStyles()
  for t in traectories:
    plotStyle = globals()['plotStyles'].pop()
    plt.plot(t['x'], t['y'], plotStyle, markersize=2, label=t['R'])
  plt.legend(
    fontsize=20, 
    loc="upper left", 
    ncol=1 , 
    title="Кількість частинок \nБМН у ланцюжку",
    bbox_to_anchor=(1.05, 1)
    )
  plt.xlabel("Час подолання відстані, (ум.од.)")
  plt.ylabel('Пройдена везикулою відстань, нм')  
  plt.subplots_adjust(right=0.65)  
  version = int(datetime.datetime.now().strftime('%s'))
  fig.savefig('results/tra/WalkingToChain-{}.svg'.format(version), dpi=fig.dpi)
  fig.savefig('results/tra/WalkingToChain-{}.png'.format(version), dpi=fig.dpi)
  print('saved')

def draw3DTraectory(traectories):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  setPlotStyles()
  for t in traectories:
    plotStyle = globals()['plotStyles'].pop()
    ax.plot(t['x'], t['y'], zs=t['z'])
  N = DEFAULT_PARAMS['N']
  px, py, pz = getSpherePoints()
  for n in range(N):
    ax.plot_surface(px, py, pz+(n+1.5*n), color='b')

  ax.set_xlim(-2, 20)
  ax.set_ylim(-2, 20)
  ax.set_zlim(-40, 10)

  plt.show()

def getSpherePoints(): 
  u = np.linspace(0, np.pi, 10)
  v = np.linspace(0, 2*np.pi, 10)

  x = np.outer(np.sin(u), np.sin(v))
  y = np.outer(np.sin(u), np.cos(v))
  z = np.outer(np.cos(u), np.ones_like(v))

  return x, y, z

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
    
  