"""Robots bez regulatora (tau = 0): pilnais nelinearais modelis, ritenis + korpuss.
Stavokli y = [x, xd, theta, thetad]. Ieeja: moments tau."""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")          # noņem šo rindu, ja grafiku vajag redzēt uz ekrāna
import matplotlib.pyplot as plt
 
# Parametri
rr, mr, Ir = 0.4, 2.0, 0.32    # ritenis: radiuss [m], masa [kg], inerce [kg*m^2]
mk, Lk = 80.0, 1.0             # korpuss: masa [kg], garums [m]
g = 9.81
mT = mr + mk + Ir / rr**2      # = 84 kg (ar bezslides efektivo masu)
 
 
def robot_dynamics(t, y, tau=0.0):
    """y' = f(t, y); x'' un theta'' no 2x2 linearas sistemas A @ acc = b."""
    theta, thetad = y[2], y[3]
 
    A = np.array([[mT,                    mk * Lk * np.cos(theta)],
                  [mk * Lk * np.cos(theta), mk * Lk**2           ]])
    b = np.array([tau / rr + mk * Lk * thetad**2 * np.sin(theta),
                  mk * g * Lk * np.sin(theta) - tau])
 
    acc = np.linalg.solve(A, b)          # acc[0] = x'', acc[1] = theta''
    return [y[1], acc[0], y[3], acc[1]]
 
 
if __name__ == "__main__":
    # Funkcijas parbaude
    chk = robot_dynamics(0, [0, 0, 0.1, 0], tau=0.0)
    print("robot_dynamics parbaude:", np.round(chk, 4))      # [0, -16.25, 0, 17.15]
 
    # Simulacija bez regulatora (ode45 ekvivalents: RK45)
    y0 = [0.0, 0.0, 0.05, 0.0]
    sol = solve_ivp(robot_dynamics, (0, 0.3), y0, method="RK45",
                    rtol=1e-8, atol=1e-10, dense_output=True)
    t = np.linspace(0, 0.3, 301)
    theta = sol.sol(t)[2]
 
    # Linearizetais modelis un ipasvertiba
    lam = np.sqrt(mT * g / ((mT - mk) * Lk))                 # 14.35 1/s
    theta_lin = y0[2] * np.cosh(lam * t)
    print(f"lambda = {lam:.2f} 1/s")
    print(f"theta(0.3 s): nelinearais = {theta[-1]:.4f} rad, linearizetais = {theta_lin[-1]:.4f} rad")
 
    # Efektivais krisanas atrums: theta = theta0*cosh(lambda_sim*t)
    for tt in (0.05, 0.1, 0.2, 0.3):
        th = sol.sol(tt)[2]
        print(f"t = {tt:.2f} s: lambda_sim = {np.arccosh(th / y0[2]) / tt:.2f} 1/s")
 
    # Grafiks
    plt.figure()
    plt.plot(t, theta, label="nelineārais modelis")
    plt.plot(t, theta_lin, "--", label=r"$\theta_0\cosh(\lambda t)$")
    plt.xlabel("t [s]"); plt.ylabel(r"$\theta$ [rad]")
    plt.title("Robots bez regulatora, $\\tau = 0$")
    plt.grid(True); plt.legend()
    plt.savefig("theta_t.png", dpi=150)
 
