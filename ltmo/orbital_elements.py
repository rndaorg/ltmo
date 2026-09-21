"""Orbital mechanics calculations."""

import numpy as np
from constants import MU_EARTH


def specific_energy(position, velocity):
    """Specific orbital energy [J/kg]."""
    r = np.linalg.norm(position)
    v = np.linalg.norm(velocity)

    return 0.5 * v**2 - MU_EARTH / r


def angular_momentum(position, velocity):
    """Specific angular momentum [m^2/s]."""
    return np.cross(position, velocity)


def eccentricity_vector(position, velocity):
    """Return eccentricity vector."""
    r = np.linalg.norm(position)
    h = angular_momentum(position, velocity)

    return np.cross(velocity, h) / MU_EARTH - position / r


def eccentricity(position, velocity):
    """Return orbital eccentricity."""
    return np.linalg.norm(eccentricity_vector(position, velocity))


def inclination(position, velocity):
    """Return inclination [rad]."""
    h = angular_momentum(position, velocity)

    return np.arccos(
        np.clip(h[2] / np.linalg.norm(h), -1.0, 1.0)
    )


def semi_major_axis(position, velocity):
    """Return semi-major axis [m]."""
    energy = specific_energy(position, velocity)

    return -MU_EARTH / (2.0 * energy)


def orbital_elements(position, velocity):
    """Return the main orbital elements."""
    return {
        "specific_energy": specific_energy(position, velocity),
        "eccentricity": eccentricity(position, velocity),
        "inclination": inclination(position, velocity),
        "semi_major_axis": semi_major_axis(position, velocity),
    }
