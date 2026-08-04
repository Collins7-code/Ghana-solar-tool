import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Solar Decision Tool — Ghana Home", page_icon="☀️", layout="wide")

st.title("☀️ Solar Decision Tool — Ghana Home")
st.caption("Size a home solar system, estimate the cost, and see the payback. Built by Collins, for his home first. 🇬🇭")

# ---------- 1. YOUR HOME'S APPLIANCES ----------
st.header("1️⃣ What does your home run?")
st.caption("Edit quantities & hours to match YOUR home. Add rows for anything missing (AC, freezer, iron...).")

default_appliances = pd.DataFrame({
    "Appliance": ["LED bulb","Fridge","TV","Standing fan","Phone charger","Radio","Water pump","Air conditioner"],
    "Watts_each": [10,150,80,60,10,15,300,1000],
    "Quantity":   [6,1,1,2,3,1,1,0],
    "Hours_per_day":[5,8,5,6,3,4,0.5,0],
})

appliances = st.data_editor(default_appliances, num_rows="dynamic", use_container_width=True)

daily_wh = (appliances["Watts_each"]*appliances["Quantity"]*appliances["Hours_per_day"]).sum()
daily_kwh = daily_wh/1000.0
connected_w = (appliances["Watts_each"]*appliances["Quantity"]).sum()

# ---------- 2. SIZE THE SYSTEM ----------
st.header("2️⃣ Size the system")
colA,colB,colC = st.columns(3)
sun_hours = colA.slider("Peak sun hours (Ghana ≈ 4–5)", 3.0, 6.0, 4.5, 0.1)
derate   = colB.slider("System efficiency (losses)", 0.6, 0.9, 0.8, 0.05)
safety   = colC.slider("Safety margin", 1.0, 1.5, 1.2, 0.05)

panel_kw = (daily_kwh/(sun_hours*derate))*safety

battery_type = st.radio("Battery type", ["Lithium (LiFePO4)","Lead-acid / Gel"], horizontal=True)
dod = 0.8 if battery_type.startswith("Lithium") else 0.5
autonomy = st.slider("Days of backup (autonomy)", 1, 3, 1)
battery_kwh = (daily_kwh*autonomy)/dod

inverter_kw = max(1.0, np.ceil((connected_w*0.7)/1000.0))

m1,m2,m3 = st.columns(3)
m1.metric("☀️ Panels", f"{panel_kw:.2f} kW")
m2.metric("🔋 Battery", f"{battery_kwh:.1f} kWh")
m3.metric("⚡ Inverter", f"{inverter_kw:.0f} kW")

# ---------- 3. COST ----------
st.header("3️⃣ Estimate the cost (GHS) — edit with real quotes")
c1,c2,c3,c4 = st.columns(4)
panel_rate = c1.number_input("Panel cost / watt (GHS)", 1, 50, 10)
batt_rate  = c2.number_input("Battery cost / kWh (GHS)", 100, 10000, 3000)
inv_rate   = c3.number_input("Inverter cost / kW (GHS)", 100, 20000, 4000)
bos_pct    = c4.number_input("Install + wiring %", 0, 100, 25)

panel_cost = panel_kw*1000*panel_rate
batt_cost  = battery_kwh*batt_rate
inv_cost   = inverter_kw*inv_rate
subtotal   = panel_cost+batt_cost+inv_cost
total      = subtotal*(1+bos_pct/100.0)

st.metric("💰 Estimated total system cost", f"GHS {total:,.0f}")
st.caption(f"Panels {panel_cost:,.0f} + Battery {batt_cost:,.0f} + Inverter {inv_cost:,.0f}, +{bos_pct}% install.")

# ---------- 4. PAYBACK ----------
st.header("4️⃣ What does it replace? (payback)")
p1,p2,p3 = st.columns(3)
ecg_bill   = p1.number_input("Current ECG bill / month (GHS)", 0, 5000, 150)
offset_pct = p2.slider("% of bill solar replaces", 0, 100, 50)
gen_fuel   = p3.number_input("Generator fuel / month (GHS)", 0, 5000, 200)

monthly_savings = ecg_bill*(offset_pct/100.0)+gen_fuel
if monthly_savings>0:
    payback_months = total/monthly_savings
    st.metric("⏳ Payback", f"{payback_months/12.0:.1f} years")
    st.caption(f"10-year net benefit: GHS {monthly_savings*120-total:,.0f}")
else:
    st.warning("Add what solar replaces (bill or generator) to see payback.")

st.markdown("---")
st.caption("User #1 is Collins' own home. Prices are estimates — plug in 2–3 real installer quotes to make it exact. This is what changing how Ghana generates energy looks like: one rooftop at a time. ⚡")
