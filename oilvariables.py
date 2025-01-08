# u(t, x) = amount of oil at a given position x at time t
# u(t=0, x) = initial amount of oil at a given position x = exp(||(-x-xs)/0.01||)

def u(t=0, x):
    return np.exp(np.linalg.norm((-x-xs)/0.01))
