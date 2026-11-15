import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import buildStateSpace as bsp
import robotDynamics as rd


if __name__ == "__main__":
    # params in script
    rr, mr = 0.4, 2.0
    mk, Lk = 80.0, 1.0             
    g = 9.81

    # x, dx, theta, dtheta
    state0 = [0, 0, 1e-4, 0.0]
    t_span = (0, 0.50)
    sol = solve_ivp(rd.ddx_ddtheta, t_span, state0, args=(0, mr, mk, Lk, rr, g), method="RK45", rtol=1e-8, atol=1e-10)
    plt.plot(sol.t, np.rad2deg(sol.y[2]), label="ODE sol")
    
    plt.xlabel("time,s")
    plt.ylabel("theta,deg")
    plt.legend()
    plt.show()
    
    # compare to eigenval 
    A, B = bsp.buildStateSpace(mr=mr, mk=mk, Lk=Lk, rr=rr, g=g)
    eigvals  = np.linalg.eigvals(A)
    lam = np.max(np.real(eigvals)) 
    
    # calculate the growth rate form ODE
    mask = sol.y[2] < 2 # unused
    # change to poly function
    # θ = θ₀·e^(λt)
    # ln θ = ln θ₀ + λt
    slope, intercept = np.polyfit(sol.t[mask], np.log(sol.y[2][mask]), 1)
    print(f"Eigenvalue lambda:   {lam:.3f} 1/s  s)")
    print(f"Fitted growth rate:  {slope:.3f} 1/s  s)")
    print(f"Difference:          {abs(slope - lam) / lam * 100:.1f} %")
    print(f"Fitted theta_0       {np.exp(intercept)}")
    
