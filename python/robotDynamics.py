import numpy as np

def ddx_ddtheta(t, state, u, mr, mk, Lk, rr, g):
    x, dx, theta, dtheta = state
    
    Ir = mr * rr**2
    me = mr + Ir / rr**2
    mT = me + mk
    
    # Check derivation in report
    # A @ [ddx, ddtheta] = B
    A = np.array(
        [[mT, mk * Lk * np.cos(theta)],
        [mk * Lk * np.cos(theta), mk * Lk**2]])
    
    B = np.array(
        [u + mk * Lk * dtheta**2 * np.sin(theta),
        mk * g * Lk * np.sin(theta) - u*rr])
    
    ddx, ddtheta = np.linalg.solve(A, B)
    
    return [dx, ddx, dtheta, ddtheta]
