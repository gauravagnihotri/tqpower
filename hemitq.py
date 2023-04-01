import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# def generate_torque_curve(max_torque, peak_speed, slope):
#     # define the engine speed range
#     engine_speed_range = np.arange(1000, 7000, 100)

#     # calculate the torque at each engine speed using a sigmoid function
#     torque_curve = max_torque / (1 + np.exp(-slope * (engine_speed_range - peak_speed)))

#     # plot the torque curve
#     plt.plot(engine_speed_range, torque_curve)
#     plt.xlabel("Engine Speed (rpm)")
#     plt.ylabel("Torque (Nm)")
#     plt.show()

#     return np.column_stack((engine_speed_range, torque_curve))

# generate torque curve for 5.7L Hemi
torque_curve = [
    (0, 0),
    (1000, 200),
    (2000, 300),
    (3000, 350),
    (4000, 375),
    (5000, 380),
    (6000, 375),
    (7000, 350),
    (8000, 300),
]


def calculate_acceleration(
    engine_speed, gear_ratio, axle_ratio, vehicle_weight, wheel_radius, torque_curve
):
    # initialize variables
    wheel_torque = 0
    vehicle_speed = 0
    vehicle_acceleration = 0

    # iterate over a range of time steps
    for t in range(100):
        # interpolate the torque curve to find the maximum torque at the current engine speed
        max_torque = np.interp(engine_speed, torque_curve[:, 0], torque_curve[:, 1])

        # calculate wheel torque based on maximum torque, engine speed, gear ratio, and axle ratio
        wheel_torque = (
            max_torque * gear_ratio * axle_ratio / (60 * 2 * 3.14159) * wheel_radius
        )

        # calculate vehicle acceleration based on wheel torque, weight, and rolling resistance
        vehicle_acceleration = (
            wheel_torque - vehicle_speed * 0.01 * vehicle_weight
        ) / vehicle_weight

        # calculate vehicle speed and position based on acceleration and time step
        vehicle_speed += vehicle_acceleration * 0.1

    return vehicle_acceleration


# create a Streamlit app
st.title("Vehicle Acceleration Calculator")

st.write(
    "Input values for engine speed, gear ratio, axle ratio, vehicle weight, wheel radius, and torque curve parameters below:"
)

# define input fields
engine_speed_input = st.number_input("Engine Speed (rpm)", value=3000)
gear_ratio_input = st.number_input("Gear Ratio", value=3.5)
axle_ratio_input = st.number_input("Axle Ratio", value=4.1)
vehicle_weight_input = st.number_input("Vehicle Weight (kg)", value=1500)
wheel_radius_input = st.number_input("Wheel Radius (m)", value=0.3)
max_torque_input = st.number_input("Maximum Torque (Nm)", value=400)
peak_speed_input = st.number_input("Peak Speed (rpm)", value=4000)
slope_input = st.number_input("Slope", value=-0.05)

# generate the torque curve based on the input parameters
# torque_curve = generate_torque_curve(max_torque_input, peak_speed_input, slope_input)
# plot the torque curve in the app
fig = plt.figure()
plt.plot(torque_curve[:, 0], torque_curve[:, 1])
plt.xlabel("Engine Speed (rpm)")
plt.ylabel("Torque (Nm)")
st.pyplot(fig)

# call the calculate_acceleration function if all input fields are filled
if (
    (engine_speed_input is not None)
    and (gear_ratio_input is not None)
    and (axle_ratio_input is not None)
    and (vehicle_weight_input is not None)
    and (wheel_radius_input is not None)
):
    vehicle_acceleration = calculate_acceleration(
        engine_speed_input,
        gear_ratio_input,
        axle_ratio_input,
        vehicle_weight_input,
        wheel_radius_input,
        torque_curve,
    )

    # display the results
    st.write("Vehicle acceleration:", vehicle_acceleration, "m/s^2")
else:
    st.write("Please fill all input fields.")
