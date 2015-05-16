from __future__ import division
import numpy as np
import math

def nelder_mead(f, x0, tol=1e-8, maxit=1e4, iter_returns=None):
    init_guess = x0
    fx0 = f(x0)
    dist = float('inf')
    curr_it = 0

    n = np.size(x0) # dimensions count

    alpha = 1.0
    beta = 1.0 + (2.0 / n)
    gamma = 0.75 - 1.0 / (2.0 * n)
    delta = 1.0 - (1.0 / n)

    # Create the simplex points and do the initial sort
    simplex_points = np.empty((n+1, n))

    pt_fval = [(x0, fx0)]

    simplex_points[0, :] = x0

    for ind, elem in enumerate(x0):
        curr_tau = 0.05
        curr_point = np.squeeze(np.eye(1, M=n, k=ind)*curr_tau + x0)
        simplex_points[ind, :] = curr_point
        pt_fval.append((curr_point, f(curr_point)))

    if iter_returns is not None:
        ret_points = []
    else:
        ret_points = None


    # The Core of The Nelder-Mead Algorithm
    while dist>tol and curr_it<maxit:

        # 1: Sort and find new center point (excluding worst point)
        pt_fval = sorted(pt_fval, key=lambda v: v[1])
        xbar = x0 * 0

        for i in range(n):
            xbar = xbar + (pt_fval[i][0])/(n)

        if iter_returns is not None and curr_it in iter_returns:
            ret_points.append(pt_fval)

        # Define useful variables
        x1, f1 = pt_fval[0] # lowest point
        xn, fn = pt_fval[n-1] # point between lowest and highest
        xnp1, fnp1 = pt_fval[n] # highest (worst) point

        # 2: Reflect
        xr = xbar + alpha*(xbar - pt_fval[-1][0])
        fr = f(xr)

        if f1 <= fr < fn:
            # Replace the n+1 point
            xnp1, fnp1 = (xr, fr)
            pt_fval[n] = (xnp1, fnp1)

        elif fr < f1:
            # 3: expand
            xe = xbar + beta*(xr - xbar)
            fe = f(xe)

            if fe < fr:
                xnp1, fnp1 = (xe, fe)
                pt_fval[n] = (xnp1, fnp1)
            else:
                xnp1, fnp1 = (xr, fr)
                pt_fval[n] = (xnp1, fnp1)

        elif fn <= fr <= fnp1:
            # 4: outside contraction
            xoc = xbar + gamma*(xr - xbar)
            foc = f(xoc)

            if foc <= fr:
                xnp1, fnp1 = (xoc, foc)
                pt_fval[n] = (xnp1, fnp1)
            else:
                # 6: Shrink
                for i in range(1, n+1):
                    curr_pt, curr_f = pt_fval[i]
                    # Shrink the points
                    new_pt = x1 + delta*(curr_pt - x1)
                    new_f = f(new_pt)
                    # Replace
                    pt_fval[i] = new_pt, new_f

        elif fr >= fnp1:
            # 5: inside contraction
            xic = xbar - gamma*(xr - xbar)
            fic = f(xic)

            if fic <= fr:
                xnp1, fnp1 = (xic, fic)
                pt_fval[n] = (xnp1, fnp1)
            else:
                # 6: Shrink
                for i in range(1, n+1):
                    curr_pt, curr_f = pt_fval[i]
                    # Shrink the points
                    new_pt = x1 + delta*(curr_pt - x1)
                    new_f = f(new_pt)
                    # Replace
                    pt_fval[i] = new_pt, new_f

        # Compute the distance and increase iteration counter
        dist = abs(fn - f1)
        curr_it = curr_it + 1

    if curr_it == maxit:
        raise ValueError("Max iterations; Convergence failed.")

    if ret_points:
        return x1, f1, curr_it, ret_points
    else:
        return x1, f1, curr_it
