# main.py

from constants import (
    INITIAL_MASS,
    THRUST,
    SPECIFIC_IMPULSE,
    R_EARTH,
    GEO_RADIUS,
    LEO_ALTITUDE
)

from dynamics import (
    calculate_exhaust_velocity,
    calculate_mass_flow_rate
)

from simulation import run_simulation

from plotting import (
    prepare_results,
    plot_trajectory,
    plot_altitude,
    plot_mass,
    plot_speed
)


def print_mission_summary(results, solution):
    """
    Print the final mission results.
    """

    final_mass = results["mass"][-1]

    propellant_used = INITIAL_MASS - final_mass

    final_altitude = results["altitude"][-1]

    final_speed = results["speed"][-1]

    if len(solution.t_events[0]) > 0:

        transfer_time = solution.t_events[0][0]

        transfer_days = transfer_time / (24 * 3600)

        print(f"Transfer time       : {transfer_days:.2f} days")

    else:

        print("GEO was not reached.")

    print()
    print(f"Initial altitude    : {LEO_ALTITUDE/1000:.1f} km")
    print(f"Final altitude      : {final_altitude/1000:.1f} km")

    print(f"Initial mass        : {INITIAL_MASS:.2f} kg")
    print(f"Final mass          : {final_mass:.2f} kg")
    print(f"Propellant used     : {propellant_used:.2f} kg")

    print(f"Thrust              : {THRUST:.3f} N")
    print(f"Specific impulse    : {SPECIFIC_IMPULSE:.0f} s")

    print(f"Final speed         : {final_speed/1000:.3f} km/s")


def main():

    print("=" * 50)
    print("       LEO -> GEO LOW-THRUST TRANSFER")
    print("=" * 50)

    # Basic propulsion information
    exhaust_velocity = calculate_exhaust_velocity()
    mass_flow_rate = calculate_mass_flow_rate()

    print(f"Exhaust velocity     : {exhaust_velocity:.2f} m/s")
    print(f"Mass flow rate       : {mass_flow_rate:.6e} kg/s")

    print("\nRunning simulation...")

    # Run numerical integration
    solution = run_simulation()

    # Process results
    results = prepare_results(solution)

    print("\nSimulation complete.\n")

    # Print final results
    print_mission_summary(
        results,
        solution
    )

    # Generate plots
    plot_trajectory(results)
    plot_altitude(results)
    plot_mass(results)
    plot_speed(results)


if __name__ == "__main__":
    main()
