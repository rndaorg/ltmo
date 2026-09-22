"""Simple thrust-direction optimization."""

import numpy as np

from orbital_elements import (
    specific_energy,
    eccentricity,
    inclination,
)


def unit_vector(vector):
    """Normalize a vector."""
    norm = np.linalg.norm(vector)

    if norm == 0.0:
        raise ValueError("Cannot normalize zero vector.")

    return vector / norm


def local_frame(position, velocity):
    """
    Construct the local orbital frame.

    Returns:
        radial   : outward direction
        tangential: direction of motion
        normal   : orbit-normal direction
    """
    radial = unit_vector(position)

    h = np.cross(position, velocity)
    normal = unit_vector(h)

    tangential = unit_vector(np.cross(normal, radial))

    return radial, tangential, normal


def thrust_direction(position, velocity, flight_path_angle, normal_angle):
    """
    Construct a thrust direction.

    flight_path_angle:
        0 rad = purely tangential

        positive = partly radial outward

    normal_angle:
        rotates part of the thrust toward the
        orbital-normal direction.
    """
    radial, tangential, normal = local_frame(position, velocity)

    in_plane = (
        np.cos(flight_path_angle) * tangential
        + np.sin(flight_path_angle) * radial
    )

    direction = (
        np.cos(normal_angle) * in_plane
        + np.sin(normal_angle) * normal
    )

    return unit_vector(direction)


def objective(
    position,
    velocity,
    direction,
    target_eccentricity=0.0,
    target_inclination=None,
):
    """
    Evaluate a thrust direction.

    Lower objective is better.

    The energy term is negative because increasing
    orbital energy is desirable.
    """
    dt = 1.0

    old_energy = specific_energy(position, velocity)

    acceleration = direction

    # Approximate velocity change from unit thrust acceleration.
    # The optimizer mainly compares directions, not magnitude.
    new_velocity = velocity + acceleration * dt

    new_energy = specific_energy(position, new_velocity)

    energy_gain = new_energy - old_energy

    e = eccentricity(position, new_velocity)

    cost = -energy_gain

    cost += 10.0 * (e - target_eccentricity) ** 2

    if target_inclination is not None:
        inc = inclination(position, new_velocity)
        cost += (inc - target_inclination) ** 2

    return cost


def optimize_thrust_direction(
    position,
    velocity,
    target_inclination=None,
):
    """
    Beginner-friendly grid-search optimizer.

    Searches over radial/tangential flight-path angles
    and out-of-plane angles.
    """
    best_cost = np.inf
    best_direction = None
    best_angles = None

    flight_path_angles = np.deg2rad(
        np.linspace(-20.0, 20.0, 17)
    )

    normal_angles = np.deg2rad(
        np.linspace(-10.0, 10.0, 9)
    )

    for gamma in flight_path_angles:
        for beta in normal_angles:

            direction = thrust_direction(
                position,
                velocity,
                gamma,
                beta,
            )

            cost = objective(
                position,
                velocity,
                direction,
                target_inclination=target_inclination,
            )

            if cost < best_cost:
                best_cost = cost
                best_direction = direction
                best_angles = (gamma, beta)

    return best_direction, best_angles, best_cost
