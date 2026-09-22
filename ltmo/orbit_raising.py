"""Main program for constant-thrust orbit raising."""

import numpy as np
import matplotlib.pyplot as plt

from simulation import simulate


def main():
    history = simulate()

    time = np.array([
        item["time"] for item in history
    ])

    altitude = np.array([
        item["altitude"] for item in history
    ])

    energy = np.array([
        item["energy"] for item in history
    ])

    eccentricity = np.array([
        item["eccentricity"] for item in history
    ])

    inclination = np.rad2deg([
        item["inclination"] for item in history
    ])

    final = history[-1]

    print("\nOrbit Raising Results")
    print("---------------------")
    print(
        f"Simulation time : {final['time']:.1f} s"
    )
    print(
        f"Final altitude  : {final['altitude'] / 1e3:.2f} km"
    )
    print(
        f"Semi-major axis: {final['semi_major_axis'] / 1e3:.2f} km"
    )
    print(
        f"Eccentricity   : {final['eccentricity']:.6f}"
    )
    print(
        f"Inclination    : {np.rad2deg(final['inclination']):.3f} deg"
    )
    print(
        f"Specific energy: {final['energy']:.3e} J/kg"
    )

    # Plot results.
    fig, axes = plt.subplots(
        3,
        1,
        figsize=(9, 10),
        sharex=True,
    )

    axes[0].plot(
        time / 3600.0,
        altitude / 1e3,
    )
    axes[0].set_ylabel("Altitude [km]")
    axes[0].grid(True)

    axes[1].plot(
        time / 3600.0,
        eccentricity,
    )
    axes[1].set_ylabel("Eccentricity [-]")
    axes[1].grid(True)

    axes[2].plot(
        time / 3600.0,
        inclination,
    )
    axes[2].set_ylabel("Inclination [deg]")
    axes[2].set_xlabel("Time [h]")
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
