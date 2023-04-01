import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Define constants
# wheel_radius = 0.3  # meters
# vehicle_mass = 3500  # kg
rolling_resistance_coefficient = 0.01
air_density = 1.2  # kg/m^3
drag_coefficient = 0.5
frontal_area = 3.2  # m^2
mps_to_mph = 2.23694  # conversion factor from meters per second to miles per hour
# ram 1500 frontal area is
torque_curve = [
    (1259.232256606427, 285.776372381188),
    (1314.974846610361, 287.4040955276739),
    (1370.7174366142951, 289.10580608990904),
    (1426.4600266182294, 290.84451036001894),
    (1482.2026166221635, 292.50922721437956),
    (1537.9452066260976, 294.24793148448947),
    (1593.6877966300317, 296.17160429397273),
    (1649.430386633966, 299.75999395781656),
    (1705.1729766379, 303.5333521610338),
    (1760.9155666418342, 307.3437040721257),
    (1816.6581566457685, 311.15405598321763),
    (1872.4007466497023, 315.0014016021842),
    (1928.1433366536367, 318.7377660975268),
    (1983.885926657571, 322.54811800861864),
    (2039.6285166615048, 325.54460834646767),
    (2095.371106665439, 327.2833126165776),
    (2151.113696669373, 328.98502317881275),
    (2206.8562866733073, 330.72372744892266),
    (2262.5988766772416, 332.4994254269073),
    (2318.3414666811755, 334.20113598914253),
    (2374.0840566851098, 335.97683396712705),
    (2429.826646689044, 337.19762632699144),
    (2485.569236692978, 338.0854753159838),
    (2541.3118266969122, 338.93633059710135),
    (2597.054416700846, 339.787185878219),
    (2652.7970067047804, 340.6380411593366),
    (2708.5395967087147, 341.5258901483289),
    (2764.2821867126486, 342.3767454294465),
    (2820.024776716583, 343.22760071056405),
    (2875.767366720517, 344.1154496995564),
    (2931.509956724451, 345.7431728460422),
    (2987.2525467283854, 347.66684565552555),
    (3042.995136732319, 349.44254363351007),
    (3098.7377267362535, 351.3662164429934),
    (3154.480316740188, 353.32688296035144),
    (3210.2229067441217, 355.8054613879549),
    (3265.965496748056, 358.210052399809),
    (3321.7080867519903, 360.68863082741245),
    (3377.450676755924, 363.13021554714123),
    (3433.1932667598585, 365.57180026687007),
    (3488.935856763793, 367.9763912787242),
    (3544.6784467677267, 370.45496970632763),
    (3600.421036771661, 372.8225670103071),
    (3656.163626775595, 374.2283279095449),
    (3711.906216779529, 375.6340888087827),
    (3767.6488067834634, 376.8178874607724),
    (3823.3913967873978, 378.1496609442608),
    (3879.133986791331, 379.4074470119999),
    (3934.8765767952655, 380.665233079739),
    (3990.6191667992, 382.0340002711021),
    (4046.361756803134, 382.84292934996176),
    (4102.104346807068, 381.53828458558144),
    (4157.846936811003, 381.55308206873127),
    (4213.589526814936, 379.9993463379948),
    (4269.33211681887, 379.0005162253784),
    (4325.074706822805, 378.0016861127621),
    (4380.817296826739, 376.7808937528977),
    (4436.559886830673, 375.7820636402814),
    (4492.302476834607, 375.0051957749131),
    (4548.045066838541, 374.3023153252943),
    (4603.787656842475, 373.56244116780067),
    (4659.53024684641, 372.2063575334231),
    (4715.272836850344, 371.08386274019716),
    (4771.015426854277, 371.63876835831735),
    (4826.758016858212, 372.0087054370642),
    (4958.513229594783, 365.7937625141181),
    (5014.255819598718, 362.2053728502743),
    (5069.998409602652, 358.50600206280643),
    (5125.740999606586, 355.10258093833596),
    (5181.4835896105205, 352.4020402634845),
    (5237.226179614454, 349.96045554375564),
    (5292.968769618388, 347.48187711615213),
    (5348.711359622323, 344.85532385704994),
    (5404.453949626257, 342.3397517215718),
    (5460.196539630191, 339.787185878219),
    (5515.939129634125, 337.49357598998887),
    (5571.681719638059, 335.90284655137765),
    (5627.424309641993, 334.20113598914253),
    (5683.1668996459275, 331.57458273004033),
    (5738.909489649862, 328.91103576306347),
    (5794.652079653795, 325.76657059371576),
    (5825.057128746851, 324.47179081810197),
]
df = pd.DataFrame(torque_curve, columns=["Engine Speed (RPM)", "Engine Torque (lb-ft)"])
df["Engine Torque (Nm)"] = df["Engine Torque (lb-ft)"] * 1.35581795
# drop the lb-ft column
df.drop(columns=["Engine Torque (lb-ft)"], inplace=True)
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

    engine_power_output = engine_torque * engine_speed_rad_per_sec / 1000

    # calculate wheel speed in radians per second
    wheel_speed_rad_per_sec = engine_speed_rad_per_sec / gear_ratio / axle_ratio
    # convert wheel speed in rpm
    wheel_speed_rpm = wheel_speed_rad_per_sec * 60 / (2 * 3.14)

    # Calculate torque at wheel
    torque_at_wheel = (engine_torque * gear_ratio * axle_ratio) / 2

    # Calculate Power at wheel
    power_at_wheel = torque_at_wheel * wheel_speed_rad_per_sec / 1000
    # power_at_wheel = (engine_power_output * gear_ratio * axle_ratio) / 2

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

    return (
        torque_at_wheel,
        acceleration,
        vehicle_speed_mph,
        force_at_wheel,
        engine_power_output,
        power_at_wheel,
        wheel_speed_rpm,
    )


# Define Streamlit app
def app():
    st.title("Vehicle Performance Calculator")
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
    df1 = pd.DataFrame(
        {
            "Mu": "0.01",
            "Air Density": "1.2 kg/m^3",
            "Cd": "0.5",
            "Frontal Area": "3.2 m^2",
        },
        index=[0],
    )
    # rename index as "Parameter"
    df1.index = ["Value"]
    # display table
    # st.write("Assumptions")
    # st.dataframe(df1, use_container_width=True)
    # st.markdown("""---""")
    with st.sidebar:
        st.write("Assumptions")
        st.dataframe(df1)

        st.title("Input Parameters")
        # st.markdown("""---""")
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
        # create a new column in df for engine speed with lower precision
        df["eng_spd"] = df["Engine Speed (RPM)"].round(decimals=0)

        # engine_speed = st.number_input("Enter engine speed (RPM):", value=2000, step=100)
        engine_speed = st.select_slider(
            "Engine speed (RPM)",
            options=df["eng_spd"].values.tolist(),
        )
        engine_torque = df.loc[
            df["eng_spd"] == engine_speed, "Engine Torque (Nm)"
        ].values[0]

        # add engine power output to the dataframe
        df["Engine Power Output (kW)"] = (
            df["Engine Torque (Nm)"] * df["Engine Speed (RPM)"] * 2 * 3.14 / 60 / 1000
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
    import plotly.graph_objects as go

    # import make_subplots function from plotly.subplots
    # to make grid of plots
    from plotly.subplots import make_subplots

    # use specs parameter in make_subplots function
    # to create secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # plot a scatter chart by specifying the x and y values
    # Use add_trace function to specify secondary_y axes.
    fig.add_trace(
        go.Scatter(
            x=df["Engine Speed (RPM)"].values, y=df["Engine Torque (Nm)"], name="Torque"
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df["Engine Speed (RPM)"].values,
            y=df["Engine Power Output (kW)"],
            name="Power",
        ),
        secondary_y=True,
    )
    # Adding title text to the figure
    # fig.update_layout(title_text="Engine Torque and Power")
    # Naming x-axis
    fig.update_xaxes(title_text="Engine Speed (RPM) X - axis")
    # add a vertical line at the engine speed
    fig.add_vline(x=engine_speed, line_width=3, line_dash="dash", line_color="grey")
    # add a hovermode to at the engine speed
    fig.update_layout(hovermode="x", hoverdistance=100, spikedistance=1000)
    # Naming y-axes
    fig.update_yaxes(
        title_text="<b>Engine Torque (Nm)</b> Y - axis ", secondary_y=False
    )
    fig.update_yaxes(
        title_text="<b>Engine Power Output (kW)</b> Y - axis ", secondary_y=True
    )
    fig.update_yaxes(
        showgrid=False, gridwidth=1, gridcolor="LightPink", secondary_y=True
    )
    fig.update_xaxes(showgrid=True, gridwidth=1)

    # using hovermode add a vertical line at the engine speed
    fig.update_layout(hovermode="x", hoverdistance=100, spikedistance=1000)
    fig.update_xaxes(showspikes=True, spikemode="across", spikethickness=1)
    fig.update_xaxes(spikesnap="data")
    # add annotation at the engine speed
    fig.add_annotation(
        x=engine_speed,
        y=engine_torque,
        text="{} RPM <br> {:.2f} Nm".format(engine_speed, engine_torque),
        showarrow=True,
        arrowhead=7,
        ax=-40,
        ay=-40,
    )

    # add a vertical line at the engine speed
    # Display the plot in the Streamlit app
    # Calculate results
    (
        torque_at_wheel,
        acceleration,
        vehicle_speed_mph,
        force_at_wheel,
        engine_power_output,
        power_at_wheel,
        wheel_speed_rpm,
    ) = calculate(
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

    # add annotation for power output from df at the engine speed
    fig.add_annotation(
        x=engine_speed,
        y=engine_power_output,
        yref="y2",
        text="{} RPM <br> {:.2f} kW".format(engine_speed, engine_power_output),
        showarrow=True,
        arrowhead=7,
        ax=40,
        ay=40,
    )
    fig.update_layout(yaxis_range=[350, 550])
    fig.update_layout(yaxis2_range=[50, 300])
    fig.update_layout(xaxis_range=[1000, 6000])
    # fig.update_yaxes(automargin=True)
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

    # st.write("Output")
    # st.markdown("""---""")
    col1, col2, col6, col8 = st.columns(4)
    col1.metric("Torque at wheel:", "{:.2f} Nm".format(torque_at_wheel))
    col8.metric("Wheel Speed:", "{:.2f} RPM".format(wheel_speed_rpm))
    col6.metric("Power at wheel:", "{:.2f} kW".format(power_at_wheel))
    col2.metric("Force at wheel:", "{:.2f} Nm".format(force_at_wheel))
    col7, col5, col4, col3 = st.columns(4)
    col7.metric("Engine Speed:", "{:.2f} RPM".format(engine_speed))
    col5.metric("Engine power output:", "{:.2f} kW".format(engine_power_output))
    col4.metric("Vehicle speed:", "{:.2f} mph".format(vehicle_speed_mph))
    col3.metric("Vehicle Acceleration:", "{:.2f} m/s^2".format(acceleration))

    # Display results
    # st.write("Torque at wheel:", "{:.2f} Nm".format(torque_at_wheel))
    # st.write("Force at wheel:", "{:.2f} Nm".format(force_at_wheel))
    # st.write("Acceleration:", "{:.2f} m/s^2".format(acceleration))
    st.markdown("""---""")
    with st.expander(
        "Explanation and Equations for Vehicle Torque, Acceleration, and Speed Calculator"
    ):
        # st.title(
        #     "Explanation and Equations for Vehicle Torque, Acceleration, and Speed Calculator"
        # )
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
