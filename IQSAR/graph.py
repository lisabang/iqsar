import numpy as np
import calculate
import matplotlib.pyplot as plt
def expl_graph(x,y):
# Fit the model to the sample with a straight line model
    poly_order = 1
    ab = np.polyfit(x,y, poly_order)
    # Evalute the estimated model
    y_fit = np.polyval(ab, x)
    ax=plt.subplot(title=str(x.name)+" vs. "+str(y.name))
    
    ax.scatter(x,y)
    ax.plot(x, y_fit);
    #ax.figtext
    #ax.title(str(x.name)+" vs. "+str(y.name))
    ax.figure.show()
    print "r2: "+str(calculate.r2(x,y))
    
