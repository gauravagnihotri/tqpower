import streamlit as st
import pandas as pd

# Define constants
# wheel_radius = 0.3  # meters
# vehicle_mass = 3500  # kg
rolling_resistance_coefficient = 0.01
air_density = 1.2  # kg/m^3
drag_coefficient = 0.5
frontal_area = 3.2  # m^2
mps_to_mph = 2.23694  # conversion factor from meters per second to miles per hour
# ram 1500 frontal area is
# Define function to calculate torque, acceleration, and vehicle speed
def calculate(
    vehicle_mass,
    wheel_radius,
    rolling_resistance_coefficient,
    air_density,
    drag_coefficient,
    frontal_area,
    engine_torque,
    gear_ratio,
    axle_ratio,
    engine_speed,
):
    # Convert engine speed to radians per second
    engine_speed_rad_per_sec = (engine_speed * 2 * 3.14) / 60

    # Calculate torque at wheel
    torque_at_wheel = (engine_torque * gear_ratio * axle_ratio) / 2

    # Calculate force at wheel
    force_at_wheel = torque_at_wheel / wheel_radius

    # Calculate total force on vehicle
    total_force = (
        force_at_wheel
        - (rolling_resistance_coefficient * vehicle_mass * 9.81)
        - (
            (0.5 * air_density * drag_coefficient * frontal_area * (0.0**2))
            * vehicle_mass
        )
    )

    # Calculate acceleration
    acceleration = total_force / vehicle_mass

    # Calculate vehicle speed in mph
    vehicle_speed_mph = (
        engine_speed_rad_per_sec / gear_ratio / axle_ratio * wheel_radius * mps_to_mph
    )

    return torque_at_wheel, acceleration, vehicle_speed_mph, force_at_wheel


# Define Streamlit app
def app():
    st.title(
        "Kevin and Evan's Dilemma - Vehicle Torque, Acceleration, and Speed Calculator"
    )
    # st.table(
    #     {
    #         "Vehicle Mass": "3500 kg (~7700 lbs))",
    #         "Rolling Resistance Coefficient": "0.01",
    #         "Air Density": "1.2 kg/m^3",
    #         "Drag Coefficient": "0.5",
    #         "Frontal Area": "3.2 m^2",
    #     }
    # )
    # generate above table as dataframe
    df = pd.DataFrame(
        {
            "Rolling Resistance Coefficient": "0.01",
            "Air Density": "1.2 kg/m^3",
            "Drag Coefficient": "0.5",
            "Frontal Area": "3.2 m^2",
        },
        index=[0],
    )
    # rename index as "Parameter"
    df.index = ["Parameters"]
    # display table
    st.write("Assumptions")
    st.dataframe(df, use_container_width=True)
    # st.markdown("""---""")
    st.title("Input Parameters")
    st.markdown("""---""")
    # Get inputs from user
    # wheel_radius = st.number_input("Enter wheel radius (m):", value=0.43, step=0.01)
    vehicle_mass = st.slider(
        "Enter Vehicle Mass (lbs):",
        min_value=0.0,
        max_value=10000.0,
        value=7700.0,
        step=10.0,
    )
    # convert vehicle mass to kg
    vehicle_mass = vehicle_mass * 0.453592
    wheel_radius = st.slider(
        "Enter Wheel Radius (m):",
        min_value=0.0,
        max_value=1.0,
        value=0.43,
        step=0.01,
    )
    st.write("Ram 1500 wheel radius is 0.43 m for 275/55R20 tires")

    # engine_torque = st.number_input("Enter engine torque (Nm):", value=200.0, step=10.0)

    # st.write("Ram 1500 engine torque is 200 bcoz MDS")
    # gear_ratio = st.number_input("Enter gear ratio:", value=1.67, step=0.01)

    # selected_gear = st.selectbox(
    #     "Select gear:",
    #     ("1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"),
    #     index=3,
    # )
    # if selected_gear == "1st":
    #     gear_ratio = 4.71
    # elif selected_gear == "2nd":
    #     gear_ratio = 3.14
    # elif selected_gear == "3rd":
    #     gear_ratio = 2.10
    # elif selected_gear == "4th":
    #     gear_ratio = 1.67
    # elif selected_gear == "5th":
    #     gear_ratio = 1.29
    # elif selected_gear == "6th":
    #     gear_ratio = 1.00
    # elif selected_gear == "7th":
    #     gear_ratio = 0.84
    # elif selected_gear == "8th":
    #     gear_ratio = 0.67

    # engine_speed = st.number_input("Enter engine speed (RPM):", value=2000, step=100)
    engine_speed = st.slider(
        "Enter Engine Speed (RPM):",
        min_value=0.0,
        max_value=7000.0,
        value=2000.0,
        step=100.0,
    )
    engine_torque = st.slider(
        "Enter Engine Torque (Nm):",
        min_value=0.0,
        max_value=550.0,
        value=200.0,
        step=10.0,
    )

    # st.write(
    #     "ZF 8HP70 Gear Ratios: 1st: 4.71, 2nd: 3.14, 3rd: 2.10, 4th: 1.67, 5th: 1.29, 6th: 1.00, 7th: 0.84, 8th: 0.67"
    # )
    # generate gear dataframe columnwise
    gear_ratios = pd.DataFrame(
        {
            "1st": [4.71],
            "2nd": [3.14],
            "3rd": [2.10],
            "4th": [1.67],
            "5th": [1.29],
            "6th": [1.00],
            "7th": [0.84],
            "8th": [0.67],
        }
    )
    # rename gear_ratios first row to gear
    gear_ratios = gear_ratios.rename(index={0: "Reduction Ratio"})
    # rename header row to 'gear'
    gear_ratios.index.name = "Gear"

    st.dataframe(gear_ratios, use_container_width=True)
    ###
    selected_gear = st.radio(
        "Select gear:",
        ("1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"),
        index=3,
        horizontal=True,
    )
    if selected_gear == "1st":
        gear_ratio = 4.71
    elif selected_gear == "2nd":
        gear_ratio = 3.14
    elif selected_gear == "3rd":
        gear_ratio = 2.10
    elif selected_gear == "4th":
        gear_ratio = 1.67
    elif selected_gear == "5th":
        gear_ratio = 1.29
    elif selected_gear == "6th":
        gear_ratio = 1.00
    elif selected_gear == "7th":
        gear_ratio = 0.84
    elif selected_gear == "8th":
        gear_ratio = 0.67
    # axle_ratio = st.number_input("Enter axle ratio:", value=3.92, step=0.01)
    axle_ratio = st.select_slider(
        "Select axle ratio:", options=[3.21, 3.55, 3.92, 4.10], value=3.92
    )

    # Calculate results
    torque_at_wheel, acceleration, vehicle_speed_mph, force_at_wheel = calculate(
        vehicle_mass,
        wheel_radius,
        rolling_resistance_coefficient,
        air_density,
        drag_coefficient,
        frontal_area,
        engine_torque,
        gear_ratio,
        axle_ratio,
        engine_speed,
    )
    st.title("Output")
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    col1.metric("Torque at wheel:", "{:.2f} Nm".format(torque_at_wheel))
    col2.metric("Force at wheel:", "{:.2f} Nm".format(force_at_wheel))
    st.markdown("""---""")
    col3, col4 = st.columns(2)
    col3.metric("Acceleration:", "{:.2f} m/s^2".format(acceleration))
    col4.metric("Vehicle speed:", "{:.2f} mph".format(vehicle_speed_mph))

    # Display results
    # st.write("Torque at wheel:", "{:.2f} Nm".format(torque_at_wheel))
    # st.write("Force at wheel:", "{:.2f} Nm".format(force_at_wheel))
    # st.write("Acceleration:", "{:.2f} m/s^2".format(acceleration))
    st.markdown("""---""")
    st.title(
        "Explanation and Equations for Vehicle Torque, Acceleration, and Speed Calculator"
    )
    st.write("Vehicle Acceleration is calculated using the following equation:")
    st.latex(
        r"""
        a = \frac{F_{wheel} - F_{rolling resistance} - F_{drag}}{m}
        """
    )
    st.write("Vehicle Speed is calculated using the following equation:")
    st.latex(
        r"""
        v = \frac{\omega_{engine} * R_{wheel}}{GR * AR} * \frac{3600}{1609.34}
        """
    )
    st.write("where:")
    st.latex(
        r"""
        \omega_{engine} = \frac{2 * \pi * N_{engine}}{60}
        """
    )
    st.write("and:")
    st.latex(
        r"""
        F_{wheel} = \frac{T_{engine} * GR * AR}{2 * R_{wheel}}
        """
    )
    st.write("and:")
    st.latex(
        r"""
        F_{rolling resistance} = \mu_{rolling resistance} * m * g
        """
    )
    st.write("and:")
    st.latex(
        r"""
        F_{drag} = \frac{1}{2} * \rho * C_{drag} * A_{frontal} * v^2
        """
    )


# plot acceleration vs engine speed for each gear


if __name__ == "__main__":
    app()
