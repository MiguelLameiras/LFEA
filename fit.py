from lib import plotter
from file_io import *

def main():
    x,y,errx,erry = read("data/cesium_6.txt",2,1.59222,1/43161) #read(path to file, number of columns,x gain, y gain)

    graph = plotter.Plot(x,y,errx,erry)

    fit_type = "Scatter" #{"Scatter", "Interpolate", "Fit"}

    #Titles should be written in Latex -> Add an "r" before the string
    graph.Title = r"Energy Spectrum"
    graph.xaxisTitle = r"Energy [keV]"
    graph.yaxisTitle = r"Events"

    graph.datacolor = "#e41a1c"
    graph.fitcolor = "#034"
    graph.marker_size = 1
    graph.marker_style = "s" #https://matplotlib.org/3.3.3/api/markers_api.html

    graph.xerror = False #Show error bars 
    graph.yerror = False
    graph.xscale = "linear" #Type of axis scale {"linear", "log", "symlog", "logit", ...}
    graph.yscale = "linear"
    graph.xauto = True #Auto Range of x axis 
    if not(graph.xauto): #Set manual Scale
        graph.xmin = 0
        graph.xmax = 1024
        graph.xticks = 100
    graph.yauto = True #Auto Range of y axis 
    if not(graph.yauto): #Set manual Scale
        graph.ymin = -0.5
        graph.ymax = 0.5
        graph.yticks = 1
    
    plot = graph.Make_Plot(fit_type)

    plot.legend(["Cesium-137","Cobalt-60","Background"], loc='best')

    plot.grid()
    
    plot.savefig('result.png', dpi = 300)
    
main()