# plotting.py

import numpy as np
import matplotlib.pyplot as plt

from constants import (
    R_EARTH,
    GEO_RADIUS,
    LEO_ALTITUDE
)


def prepare_results(solution):
    """
    Extract useful quantities from the simulation.
    """

    time = solution.t

    x = solution.y[0]
    y = solution.y[1]

    vx = solution.y[2]
    vy = solution.y[3]

    mass = solution.y[4]

    radius = np.sqrt(x**2 + y**2)

    altitude = radius - R_EARTH

    speed = np.sqrt(vx**2 + vy**2)

    time_days = time / (24 * 3600)

    return {
        "time": time,
        "time_days": time_days,
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "mass": mass,
        "radius": radius,
        "altitude": altitude,
        "speed": speed
    }


def plot_trajectory(results):
    """
    Plot the spacecraft trajectory.
    """

    theta = np.linspace(0, 2 * np.pi, 500)

    earth_x = R_EARTH * np.cos(theta)
    earth_y = R_EARTH * np.sin(theta)

    leo_radius = R_EARTH + LEO_ALTITUDE

    leo_x = leo_radius * np.cos(theta)
    leo_y = leo_radius * np.sin(theta)

    geo_x = GEO_RADIUS * np.cos(theta)
    geo_y = GEO_RADIUS * np.sin(theta)

    plt.figure(figsize=(9, 9))

    # Earth
    plt.fill(
        earth_x / 1000,
        earth_y / 1000,
        color="royalblue",
        alpha=0.7,
        label="Earth"
    )

    # LEO
    plt.plot(
        leo_x / 1000,
        leo_y / 1000,
        "--",
        color="green",
        label="LEO"
    )

    # GEO
    plt.plot(
        geo_x / 1000,
        geo_y / 1000,
        "--",
        color="red",
        label="GEO"
    )

    # Spacecraft
    plt.plot(
        results["x"] / 1000,
        results["y"] / 1000,
        color="black",
        linewidth=1,
        label="Low-thrust trajectory"
    )

    plt.xlabel("x [km]")
    plt.ylabel("y [km]")
    plt.title("LEO to GEO Low-Thrust Spiral")

    plt.axis("equal")
    plt.legend()
    plt.tight_layout()

    plt.show()


def plot_altitude(results):
    """
    Plot altitude versus time.
    """

    plt.figure(figsize=(10, 5))

    plt.plot(
        results["time_days"],
        results["altitude"] / 1000,
        color="purple"
    )

    plt.axhline(
        LEO_ALTITUDE / 1000,
        color="green",
        linestyle="--",
        label="LEO"
    )

    geo_altitude = (GEO_RADIUS - R_EARTH) / 1000

    plt.axhline(
        geo_altitude,
        color="red",
        linestyle="--",
        label="GEO"
    )

    plt.xlabel("Time [days]")
    plt.ylabel("Altitude [km]")
    plt.title("Altitude During LEO-to-GEO Transfer")

    plt.legend()
    plt.tight_layout()

    plt.show()


def plot_mass(results):
    """
    Plot spacecraft mass versus time.
    """

    plt.figure(figsize=(10, 5))

    plt.plot(
        results["time_days"],
        results["mass"],
        color="darkorange"
    )

    plt.xlabel("Time [days]")
    plt.ylabel("Mass [kg]")
    plt.title("Spacecraft Mass Depletion")

    plt.tight_layout()

    plt.show()


def plot_speed(results):
    """
    Plot spacecraft speed versus time.
    """

    plt.figure(figsize=(10, 5))

    plt.plot(
        results["time_days"],
        results["speed"] / 1000,
        color="blue"
    )

    plt.xlabel("Time [days]")
    plt.ylabel("Speed [km/s]")
    plt.title("Spacecraft Speed")

    plt.tight_layout()

    plt.show()
