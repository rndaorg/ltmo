# simulation.py

import numpy as np

from scipy.integrate import solve_ivp

from constants import (
    MU_EARTH,
    R_EARTH,
    LEO_ALTITUDE,
    GEO_RADIUS,
    INITIAL_MASS,
    MAX_SIMULATION_TIME,
    MAX_STEP
)

from dynamics import spacecraft_dynamics


def calculate_circular_velocity(radius):
    """
    Calculate circular orbital velocity.

    Parameters
    ----------
    radius : float
        Orbital radius in meters.

    Returns
    -------
    float
        Circular velocity in m/s.
    """

    return np.sqrt(MU_EARTH / radius)


def create_initial_state():
    """
    Create the initial spacecraft state in LEO.

    Returns
    -------
    numpy.ndarray
        Initial state [x, y, vx, vy, mass].
    """

    leo_radius = R_EARTH + LEO_ALTITUDE

    leo_velocity = calculate_circular_velocity(
        leo_radius
    )

    x = leo_radius
    y = 0.0

    vx = 0.0
    vy = leo_velocity

    mass = INITIAL_MASS

    return np.array([
        x,
        y,
        vx,
        vy,
        mass
    ])


def geo_reached(t, state):
    """
    Event function for detecting arrival at GEO radius.
    """

    x, y = state[0], state[1]

    radius = np.sqrt(x**2 + y**2)

    return radius - GEO_RADIUS


# Stop integration when GEO is reached
geo_reached.terminal = True

# Only detect increasing radius
geo_reached.direction = 1


def run_simulation():
    """
    Run the LEO-to-GEO numerical simulation.

    Returns
    -------
    scipy.integrate.OdeResult
        Numerical integration result.
    """

    initial_state = create_initial_state()

    solution = solve_ivp(
        spacecraft_dynamics,
        [0, MAX_SIMULATION_TIME],
        initial_state,
        events=geo_reached,
        rtol=1e-8,
        atol=1e-8,
        max_step=MAX_STEP
    )

    return solution
