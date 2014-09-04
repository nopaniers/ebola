#==============================================================================
# Ebola model
#==============================================================================
#
#  S is the number of uninfected people
#  E is the number of carriers but not yet infectious
#  I is the number of infectious people
#  R is the number of recovered people
#  D is the number of deaths
#
#==============================================================================

from pylab import *
from numpy import *
from scipy.integrate import odeint

#------------------------------------------------------------------------------
# Constants for the model
#------------------------------------------------------------------------------

N = 1000000 # Total population (set at a million for no particular reason)

sigma = 1./5.4  # Rate of becoming infections after you've contracted it
gamma = 1./5.61 # Rate of either dying or recovering
f = 0.6 # Fatality rate (as a proportion of those who contract the virus)

beta = 1.29*gamma # Rate that those with the virus infect others

print beta
print beta/gamma

#------------------------------------------------------------------------------
# ODE
#------------------------------------------------------------------------------

def D(y, t):
    """ A simple model for disease spread """
    S, E, I, R, D = y
  
    # The model equations
    dS = -beta*(S/N)*I
    dE = +beta*(S/N)*I - sigma*E
    dI = sigma*E - gamma*I
    dR = (1.0-f)*gamma*I
    dD = f*gamma*I
    return [dS, dE, dI, dR, dD]


def solve_model(T_total=365.0):
    # Initial conditions - one person infected
    y0 = [N, 1, 0, 0, 0]
    t  = np.linspace(0., T_total, 1000)
    solution = odeint(D, y0, t)

    S = solution[:,0]
    E = solution[:,1]
    I = solution[:,2]
    R = solution[:,3]
    Ds = solution[:,4]

    plt = plot

    plt(t, E+I)
    plt(t, I)
    plt(t, R)
    plt(t, Ds)
    # plt(t, S)
    # ylim(1.0)

    legend(["Currently Contracted Ebola", 
            "Currently Infectious", 
            "Recovered Patients", 
            "Deaths"], loc=2)

    show()

    # print t
