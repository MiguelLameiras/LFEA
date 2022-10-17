from lib import plotter
from file_io import *
import numpy as np
from scipy.interpolate import interp1d
import math

def T1(x):
    return 20*math.log10(pow(x,2)/math.sqrt(pow(4.5269*pow(10,8) - x**2,2) + 4.5269*pow(10,8)*pow(x,2)))
def T2(x):
    return 20*math.log10(abs((4.5269*pow(10,8))/math.sqrt(pow(4.5269*pow(10,8) - pow(x,2),2) + pow(x*2.1277*pow(10,4),2))))
def T3(x):
    return 20*math.log10(abs((2.1277*pow(10,4)*x)/math.sqrt(pow(4.5269*pow(10,8) - pow(x,2),2) + pow(x*2.1277*pow(10,4),2))))

def T11(x):
    return 20*math.log10(abs((2.1277*pow(10,4)*x)/math.sqrt(pow(4.5269*pow(10,8) - pow(x,2),2) + pow(x*2.1277*pow(10,4),2))))

def T22(x):
    return 20*math.log10(abs((4.5269*pow(10,8))/math.sqrt(pow(4.5269*pow(10,8) - pow(x,2),2) + pow(x*2.1277*pow(10,4),2))))

def T44(x):
    return 20*math.log10(24895*x/math.sqrt(pow(1570.8*x,2) + pow(3886.2*pow(10,4) - x*x,2)))


def main():
    
    x,y,errx,erry = read("data/lab4.txt",2,2*math.pi,1) #read(path to file, number of columns,x gain, y gain)

    graph = plotter.Plot(x,y,errx,erry)

    fit_type = "Interpolate" #{"Scatter", "Interpolate", "Fit", "Hist"}

    #Titles should be written in Latex -> Add an "r" before the string
    graph.Title = r"Filtro Passa-Banda de Rauch"#Dos Dois \gamma De Aniquilação Do Processo e+e^+ -> \gamma \gamma$"
    graph.xaxisTitle = r"Frequência Angular $[rad$ $s^{-1}]$"
    graph.yaxisTitle = r"Ganho $[dB]$"

    graph.datacolor = "black"
    graph.errcolor = "black"
    graph.fitcolor = "#3b8bd1" 
    graph.marker_size = 2
    graph.marker_style = "s" #https://matplotlib.org/3.3.3/api/markers_api.html

    graph.xerror = False #Show error bars 
    graph.yerror = False
    graph.xscale = "log" #Type of axis scale {"linear", "log", "symlog", "logit", ...}
    graph.yscale = "linear"
    graph.xauto = True #Auto Range of x axis 
    if not(graph.xauto): #Set manual Scale
        graph.xmin = -3
        graph.xmax = 3
        graph.xticks = 0.5
    graph.yauto = True #Auto Range of y axis 
    if not(graph.yauto): #Set manual Scale
        graph.ymin = -0.5
        graph.ymax = 0.5
        graph.yticks = 1

    if fit_type == "Fit":
        ################
        graph.expression = "a+b*x+c*x*x+d*x*x*x + e*x*x*x*x + f*x*x*x*x*x" #Function to fit data 
        graph.parameters.add('a', value=0.684)#parameters.add(string param name, intial value, min value, max value)
        graph.parameters.add('b', value=8.639)#parameters.add(string param name, intial value, min value, max value)
        graph.parameters.add('c', value=3886.2)
        graph.parameters.add('d', value=3886.2)
        graph.parameters.add('e', value=3886.2)
        graph.parameters.add('f', value=3886.2)
        ################
    
    plot = graph.Make_Plot(fit_type)

    x_continuo = np.linspace(min(x),max(x),100)
    myFn = np.vectorize(T44)
    y = myFn(x_continuo)
    plot.plot(x_continuo,y, color='black', linestyle='-', linewidth=1)

    #plot.plot([500*6.283185, 6.283185*3860], [-29.89700043, 2.04181051], color='black', linestyle='--', linewidth=1)
    #plot.plot([3860*6.283185, 6.283185*20000], [2.04181051, 2.04181051], color='black', linestyle='--', linewidth=1)

    plot.legend(["_no_legend_","Curva Experimental","Curva de Bode"], loc='best')

    #plot.arrow(0.4270506, 200, 0.1, 50, head_width=0.0005, head_length=0.1, fc='k', ec='k')
    #plot.arrow(0.550425213, 200, 0.1, 50, head_width=0.0005, head_length=0.1, fc='k', ec='k')
    #plot.annotate("(1)",(0.04,2450))
    #plot.annotate("(2)",(0.14,1200))
    #plot.annotate("(3)",(0.475,1510))
    #plot.annotate("(4)",(0.55,400))
    #plot.annotate("(5)",(0.966,400))
    #plot.annotate("(6)",(1.039,60))

    plot.grid()
    
    plot.savefig('result.png', dpi = 300)
    
main()