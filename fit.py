from lib import plotter
from file_io import *

def main():
    x,y,errx,erry = read("data/calib_pulser_2.txt",4,1,1) #read(path to file, number of columns,x gain, y gain)

    graph = plotter.Plot(x,y,errx,erry)

    fit_type = "Fit" #{"Scatter", "Interpolate", "Fit"}

    #Titles should be written in Latex -> Add an "r" before the string
    graph.Title = r"Calibração Amplificador Linear"
    graph.xaxisTitle = r"Channel"
    graph.yaxisTitle = r"Energy [MeV]"

    graph.datacolor = 'black'
    graph.errcolor = "black"
    graph.fitcolor = "#ff5964"
    graph.marker_size = 1
    graph.marker_style = "s" #https://matplotlib.org/3.3.3/api/markers_api.html

    graph.xerror = True #Show error bars 
    graph.yerror = True
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

    if fit_type == "Fit":
        ################
        graph.expression = "m*x + b" #Function to fit data 
        graph.parameters.add('m', value=500)#parameters.add(string param name, intial value, min value, max value)
        graph.parameters.add('b', value=30)
        ################
    
    plot = graph.Make_Plot(fit_type)

    x,y,errx,erry = read("data/calib_nominal.txt",2,1,1) #read(path to file, number of columns,x gain, y gain)

    graph = plotter.Plot(x,y,errx,erry)

    fit_type = "Fit" #{"Scatter", "Interpolate", "Fit"}

    #Titles should be written in Latex -> Add an "r" before the string
    graph.Title = r"Calibração Amplificador de Janela"
    graph.xaxisTitle = r"Canal"
    graph.yaxisTitle = r"Energia [MeV]"

    graph.datacolor = 'black'
    graph.errcolor = "black"
    graph.fitcolor = "#38618c"
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

    if fit_type == "Fit":
        ################
        graph.expression = "m*x + b" #Function to fit data 
        graph.parameters.add('m', value=500)#parameters.add(string param name, intial value, min value, max value)
        graph.parameters.add('b', value=30)
        ################
    
    plot = graph.Make_Plot(fit_type)

    plot.legend(["Fit Pulser",'_nolegend_' ,"Fit Valores Nominais"], loc='best')

    plot.text(481.15, 5.59828,'Am-241 [5578,28 keV]',horizontalalignment='right')
    plot.text(456.77, 5.51486,'Am-241 [5534,86 keV]',horizontalalignment='right')
    plot.text(378.48, 5.40745,'Po-210 [5407,45 keV]',horizontalalignment='right')

    plot.grid()
    
    plot.savefig('result.png', dpi = 300)
    
main()