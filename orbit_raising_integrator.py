"""Orbit-raising simulation."""

import numpy as np

from constants import (
    MU_EARTH,
    EARTH_RADIUS,
    SPACECRAFT_MASS,
    THRUST,
    INITIAL_ALTITUDE,
    TARGET_ALTITUDE,
    INITIAL_INCLINATION,
    TIME_STEP,
    MAX_TIME,
)

from dynamics import equations_of_motion
from orbital_elements import orbital_elements
from optimizer import optimize_thrust_direction


def rk4_step(state, thrust_direction, dt):
    """Fourth-order Runge-Kutta integration."""
    k1 = equations_of_motion(state, thrust_direction)

    k2 = equations_of_motion(
        state + 0.5 * dt * k1,
        thrust_direction,
    )

    k3 = equations_of_motion(
        state + 0.5 * dt * k2,
        thrust_direction,
    )

    k4 = equations_of_motion(
        state + dt * k3,
        thrust_direction,
    )

    return state + (dt / 6.0) * (
        k1 + 2.0 * k2 + 2.0 * k3 + k4
    )


def initial_state():
    """Create an initial circular orbit."""
    radius = EARTH_RADIUS + INITIAL_ALTITUDE

    circular_speed = np.sqrt(MU_EARTH / radius)

    # Start at x-axis.
    position = np.array([
        radius,
        0.0,
        0.0,
    ])

    # Velocity is tilted by the initial inclination.
    velocity = np.array([
        0.0,
        circular_speed * np.cos(INITIAL_INCLINATION),
        circular_speed * np.sin(INITIAL_INCLINATION),
    ])

    return np.concatenate((position, velocity))


def simulate():
    """Run the orbit-raising simulation."""
    state = initial_state()

    time = 0.0

    history = []

    target_radius = EARTH_RADIUS + TARGET_ALTITUDE

    while time <= MAX_TIME:

        position = state[:3]
        velocity = state[3:]

        elements = orbital_elements(
            position,
            velocity,
        )

        altitude = (
            np.linalg.norm(position)
            - EARTH_RADIUS
        )

        history.append({
            "time": time,
            "state": state.copy(),
            "altitude": altitude,
            "energy": elements["specific_energy"],
            "eccentricity": elements["eccentricity"],
            "inclination": elements["inclination"],
            "semi_major_axis": elements["semi_major_axis"],
        })

        if altitude >= TARGET_ALTITUDE:
            break

        # Optimize the thrust direction.
        direction, angles, cost = optimize_thrust_direction(
            position,
            velocity,
            target_inclination=INITIAL_INCLINATION,
        )

        # Propagate the spacecraft.
        state = rk4_step(
            state,
            direction,
            TIME_STEP,
        )

        time += TIME_STEP

    return history
