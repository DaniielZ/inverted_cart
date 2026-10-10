import numpy as np

def buildStateSpace(mr, mk, Lk, rr, g):
    Ir = mr * rr**2
    me = mr + Ir / rr**2
    mT = me + mk
    print(me, mT)
    # coefficients for the linearized equations from:
    # θ″ = (mtot·g)/(mr,eff·Lk)·θ − (1/rr + mtot/(mk·Lk))/(mr,eff·Lk)·τ 
    # x″ = −(mk·g/mr,eff)·θ + (1/rr + 1/Lk)/mr,eff · τ 	
    
    th_th  =  (mT * g) / (me * Lk)                      # theta''  f(theta)
    th_tau = -(1/rr + mT/(mk*Lk)) / (me * Lk)           # theta''  f(tau)
    x_th   = -(mk * g) / me                             # x''      f(theta)
    x_tau  =  (1/rr + 1/Lk) / me                        # x''      f(tau)
    
    # z = [theta, theta_dot, x, x_dot]
    A = np.array([
        # theta, theta', x,  x'
        [0,      1,      0,  0],     # theta'  = theta'
        [th_th,  0,      0,  0],     # theta'' = th_th * theta
        [0,      0,      0,  1],     # x'      = x'
        [x_th,   0,      0,  0],     # x''     = x_th * theta
    ])

    # tau
    B = np.array([
        [0],        # theta'
        [th_tau],   # theta''
        [0],        # x'
        [x_tau],    # x''
    ])
    
    return A, B


# Test for stability
A, B = buildStateSpace(mr=2, mk=80, Lk=1.0, rr=0.2, g=9.81)
print(A)
print(B)
lam = np.linalg.eigvals(A)
print (lam)

if np.all(np.real(lam) < 0):     # any growing mode due to exponential growth offset decaying modes
    print("System is stable")  
else:
    print("System is unstable")
    