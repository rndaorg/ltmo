# constants.py

# Earth constants
MU_EARTH = 3.986004418e14       # m^3/s^2
R_EARTH = 6378.137e3            # m
G0 = 9.80665                     # m/s^2

# Orbit parameters
LEO_ALTITUDE = 400e3            # m
GEO_RADIUS = 42164e3            # m
TARGET_ALTITUDE = 700.0e3       # m

# Initial inclination
INITIAL_INCLINATION = np.deg2rad(28.5)

# Spacecraft parameters
INITIAL_MASS = 1000.0           # kg
THRUST = 0.20                   # N
SPECIFIC_IMPULSE = 3000.0       # s

# Simulation parameters
MAX_SIMULATION_TIME = 5 * 365.25 * 24 * 3600
MAX_STEP = 3600.0               # seconds


# Simulation
TIME_STEP = 10.0                # s
MAX_TIME = 2.0e5                # s

# Optimization weights
ENERGY_WEIGHT = 1.0
ECCENTRICITY_WEIGHT = 10.0
INCLINATION_WEIGHT = 1.0



