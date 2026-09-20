# dynamics.py

import numpy as np

from constants import (
    MU_EARTH,
    G0,
    THRUST,
    SPECIFIC_IMPULSE
)


def calculate_exhaust_velocity():
    """
    Calculate effective exhaust velocity from specific impulse.

    Returns
    -------
    float
        Exhaust velocity in m/s.
    """

    return SPECIFIC_IMPULSE * G0


def calculate_mass_flow_rate():
    """
    Calculate propellant mass flow rate.

    Returns
    -------
    float
        Mass flow rate in kg/s.
    """

    exhaust_velocity = calculate_exhaust_velocity()

    return THRUST / exhaust_velocity


def spacecraft_dynamics(t, state):
    """
    Equations of motion for the spacecraft.

    State vector:
        [x, y, vx, vy, mass]

    Parameters
    ----------
    t : float
        Time in seconds.
    state : array-like
        Spacecraft state.

    Returns
    -------
    list
        Derivatives of the state.
    """

    x, y, vx, vy, mass = state

    # Position and velocity vectors
    position = np.array([x, y])
    velocity = np.array([vx, vy])

    # Magnitudes
    radius = np.linalg.norm(position)
    speed = np.linalg.norm(velocity)

    # Earth's gravitational acceleration
    gravity = -MU_EARTH * position / radius**3

    # Tangential thrust direction
    if speed > 0:
        thrust_direction = velocity / speed
    else:
        thrust_direction = np.zeros(2)

    # Thrust acceleration
    thrust_acceleration = (
        THRUST / mass
    ) * thrust_direction

    # Total acceleration
    acceleration = gravity + thrust_acceleration

    # Propellant mass flow
    mass_flow_rate = calculate_mass_flow_rate()

    dm_dt = -mass_flow_rate

    return [
        vx,
        vy,
        acceleration[0],
        acceleration[1],
        dm_dt
    ]
