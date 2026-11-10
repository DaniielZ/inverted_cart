import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import buildStateSpace as bsp


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


if __name__ == "__main__":
    # params in script
    rr, mr = 0.4, 2.0
    mk, Lk = 80.0, 1.0             
    g = 9.81

    state0 = [0, 0, 0.05, 0.0]
    t_span = (0, 0.3)
    sol = solve_ivp(ddx_ddtheta, t_span, state0, args=(0, mr, mk, Lk, rr, g), method="RK45", rtol=1e-8, atol=1e-10)
    plt.plot(sol.t, np.rad2deg(sol.y[2]))
    plt.xlabel("time,s")
    plt.ylabel("theta,deg")
    plt.show()


    #TODO: compare to eigenvals and linear maybe?
    # compare to eigenvals
    A, B = bsp.buildStateSpace(mr=mr, mk=mk, Lk=Lk, rr=rr, g=g)
    lam = np.linalg.eigvals(A)
    
