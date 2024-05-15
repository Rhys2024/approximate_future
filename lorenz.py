from scipy.integrate import solve_ivp
import numpy as np


sigma = 10
beta = 8/3
rho = 28


def Lorenz(t, point, sigma, beta, rho):
    
    x, y, z = point

    dx_dt = sigma*(y - x)
    dy_dt = (x*(rho - z)) - y
    dz_dt = (x*y) - (beta*z)
    
    return np.array([dx_dt, dy_dt, dz_dt])




def system_solutions(initial_conds, lorenz_params = [10, 8/3, 28], 
                     n_trajectories=3, 
                     cloud_size = 1,
                     travel_time = 100,
                     depth=10_000):
    
    x0, y0, z0 = initial_conds

    initial_conds = [
        [x0 + np.random.uniform(-cloud_size, cloud_size), 
         y0 + np.random.uniform(-cloud_size, cloud_size), 
         z0 + np.random.uniform(-cloud_size, cloud_size)]
        for _ in range(n_trajectories)
    ]

    t_span = (0, travel_time)
    t_eval = np.linspace(*t_span, depth)

    lorenz_solutions = []
    for conds in initial_conds:
        sol = solve_ivp(Lorenz, t_span, conds, t_eval=t_eval, 
                        args = lorenz_params)
        lorenz_solutions.append(sol.y)

    return np.array(lorenz_solutions)
