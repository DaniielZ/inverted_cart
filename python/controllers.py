def controllerPD(state, Kp, Kd):
    x, dx, theta, dtheta = state
    
    u = Kp * theta + Kd * dtheta
    
    return u
    