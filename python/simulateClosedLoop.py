import robotDynamics
import controllers
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import numpy as np



def simulateClosedLoopPD(Kp, Kd, theta_0, t_end):
    rr, mr = 0.4, 2.0
    mk, Lk = 80.0, 1.0             
    g = 9.81
    
    # x, dx, theta, dtheta
    state0 = [0, 0, theta_0, 0.0]
    t_span = (0, t_end)
    sol = solve_ivp(lambda t, state: robotDynamics.ddx_ddtheta(t, state, controllers.controllerPD(state, Kp, Kd), mr, mk, Lk, rr, g),
                    t_span, state0, method="RK45", rtol=1e-8, atol=1e-10)
    return sol

if __name__ == "__main__":

    PDs = np.array([[0.9,30],
                    [1.1,30]])
    Kp_crit = (80.0+1.0) * 9.81
    PDs[:, 0] *= Kp_crit 
    theta_0 = np.deg2rad(5) 
    t_end = 20
    for p,d in PDs:
        sol = simulateClosedLoopPD(p, d, theta_0, t_end)
        plt.plot(sol.t, np.rad2deg(sol.y[2]), label=f"Kp:{p}; Kd:{d}")
        # plt.plot(sol.t, sol.y[2], label=f"Kp:{p}; Kd:{d}")
    
    plt.xlabel("time,s")
    plt.ylabel("theta,deg")    
    plt.axhline(linestyle=":")
    plt.legend()
    plt.show()