import streamlit as st
import numpy as np
import datetime

# PAGE CONFIG 
st.set_page_config(
    page_title="Smart Energy System",
    page_icon="⚡",
    layout="wide"
)

#  CUSTOM CSS (ANIMATIONS)
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    font-size:42px;
    font-weight:700;
    text-align:center;
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: fadeIn 1.5s ease-in-out;
}

.card {
    padding:25px;
    border-radius:18px;
    background:white;
    box-shadow:0 10px 25px rgba(0,0,0,0.08);
    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px) scale(1.01);
}

.big-number {
    font-size:30px;
    font-weight:700;
    color:#0072ff;
}

.stButton>button {
    background: linear-gradient(90deg,#0072ff,#00c6ff);
    color:white;
    border:none;
    border-radius:10px;
    padding:12px 25px;
    font-size:16px;
    font-weight:600;
    transition:0.3s;
}

.stButton>button:hover{
    transform:scale(1.05);
}

@keyframes fadeIn {
    from {opacity:0; transform:translateY(-20px);}
    to {opacity:1; transform:translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# HEADER 
st.markdown('<p class="main-title">⚡ Smart Energy Management System</p>', unsafe_allow_html=True)
st.write("### AI-Powered Energy Forecast + Cost Analysis")

# TABS 
tab1, tab2, tab3 = st.tabs(["🔮 Predictor", "🔌 Device Calculator", "💡 Energy Tips"])

# TAB 1 — PREDICTOR
with tab1:

    st.subheader("Energy Consumption Predictor")

    col1, col2 = st.columns(2)

    with col1:
        hour = st.slider("Hour of Day", 0, 23, 14)
        day = st.selectbox("Day of Week",
                           ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    with col2:
        month = st.selectbox("Month",
                             ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
        doy = st.slider("Day of Year",1,365,180)

    predict = st.button("⚡ Predict Energy")

    if predict:

        # ---- FAKE MODEL (Demo Logic) ----
        base = 12000
        peak = 4000 if 18 <= hour <= 22 else 0
        weekend = -1500 if day in ["Saturday","Sunday"] else 0

        prediction = base + peak + weekend + np.random.randint(-500,500)

        energy_kwh = prediction
        cost = energy_kwh * 0.12

        c1,c2,c3 = st.columns(3)

        c1.markdown(f'<div class="card"><center>Predicted Load<br><div class="big-number">{prediction:.0f} kWh</div></center></div>',unsafe_allow_html=True)
        c2.markdown(f'<div class="card"><center>Hourly Cost<br><div class="big-number">${cost:.2f}</div></center></div>',unsafe_allow_html=True)
        c3.markdown(f'<div class="card"><center>Daily Cost<br><div class="big-number">${cost*24:.2f}</div></center></div>',unsafe_allow_html=True)

        st.divider()

        if prediction > 15000:
            st.error("⚠️ High Consumption Predicted — Reduce heavy appliances")
        elif prediction < 12000:
            st.success("✅ Low Consumption — Good time to use heavy devices")
        else:
            st.info("Moderate usage expected")

# TAB 2 — DEVICE CALCULATOR
with tab2:

    st.subheader("Device Cost Calculator")

    devices = {
        "Air Conditioner":1500,
        "Refrigerator":200,
        "Washing Machine":500,
        "Water Heater":2000,
        "Television":120
    }

    device = st.selectbox("Select Device", list(devices.keys()))
    hours = st.slider("Hours Used Per Day",0.5,24.0,1.0)

    if st.button("Calculate Cost"):

        power = devices[device]
        energy = power/1000 * hours
        cost = energy * 0.12

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Daily kWh",f"{energy:.2f}")
        c2.metric("Daily Cost",f"${cost:.2f}")
        c3.metric("Monthly",f"${cost*30:.2f}")
        c4.metric("Yearly",f"${cost*365:.2f}")

        if cost*365 > 500:
            st.warning("⚠️ High yearly cost device")
        else:
            st.success("Efficient usage level")

# TAB 3 — ENERGY TIPS
with tab3:

    st.subheader("Energy Saving Recommendations")

    tips = [
        "Use LED lights instead of bulbs",
        "Run appliances during off-peak hours",
        "Keep AC at 24-26°C",
        "Wash clothes in cold water",
        "Unplug devices when not in use",
        "Use natural daylight",
        "Seal windows to prevent heat loss",
        "Run full laundry loads",
        "Maintain appliances regularly",
        "Use solar panels if possible"
    ]

    for tip in tips:
        st.markdown(f"✅ {tip}")

    st.success("Following these tips can reduce your electricity bill by up to 35%")
