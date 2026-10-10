import numpy as np

def computeEquilibriumTorque(theta0, mr, mk, Lk, rr, g=9.81):
    # and acceleration
    Ir = mr * rr**2
    me = mr + Ir / rr**2
    mT = me + mk

    # Use previous derrived coefficients
    th_th  =  (mT * g) / (me * Lk)                      # theta''  f(theta)
    th_tau = -(1/rr + mT/(mk*Lk)) / (me * Lk)           # theta''  f(tau)
    x_th   = -(mk * g) / me                             # x''      f(theta)
    x_tau  =  (1/rr + 1/Lk) / me                        # x''      f(tau)
    # theta`` = 0, x'' = x''
    # eq 1: 0 = th_th * theta0 + th_tau * tau
    # eq 2: x'' = x_th * theta0 + x_tau * tau
    # Variables seperated into unknowns and knowns (tau, x'')
    #K (2x2) * [tau, x''] = rhs (2x1)
    # this means that for k when expaned
    # K11·τ + K12·x″ = rhs1       
    # K21·τ + K22·x″ = rhs2        
    
    K  = np.array([[th_tau,   0.0], # eq1''  th_tau * tau = -th_th * theta0 
                    [-x_tau,   1.0]  # ex2''  x''- x_tau * tau = x_th * theta0    
                    ]) 
    rhs = np.array([-th_th * theta0 , x_th * theta0]) 

    tau, a = np.linalg.solve(K, rhs)    
    return tau, a


# Test: upright, then 5 degrees
for deg in (0, 5):
    tau, a = computeEquilibriumTorque(np.deg2rad(deg), mr=2, mk=80, Lk=1.0, rr=0.2)
    print(f"theta0 = {deg} deg:  tau = {tau:.3f} N*m,  a = {a:.3f} m/s^2")