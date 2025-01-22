import logging as l

def log_sim_parameters(n_steps, t_start, t_end, mesh_name, borders, writefrequency, restartfile=None):
    l.info('Simulation prameters\n')
    l.info(f"Mesh: {mesh_name}")
    if restartfile: 
        l.info(f"Restart file: {restartfile}")
    l.info(f"Number of steps: {n_steps}")
    l.info(f"Time start: {t_start}")
    l.info(f"Time end: {t_end}")
    l.info(f"Delta t: {(t_end-t_start)/n_steps}")
    l.info(f"Wrie frequency: {writefrequency}")
    l.info(f"Fishing area: {borders}\n")

def log_oil_area(amount, time):
    l.info(f"Amount of oil in area at time {time}: {amount}")