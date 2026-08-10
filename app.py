import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Solar Decision Tool — Ghana", page_icon="☀️", layout="wide")

st.title("☀️ Solar Decision Tool — Ghana Home")
st.caption("v2 · region-aware sun hours + payback from your REAL bill. Built by Collins, for his home first. 🇬🇭")

# ---------- 0. REGION -> SUN HOURS ----------
SUN = {
 "Greater Accra":4.4,"Central":4.4,"Western":4.3,"Western North":4.4,
 "Volta":4.6,"Oti":4.7,"Eastern":4.7,"Ashanti":4.8,
 "Bono":5.0,"Bono East":5.0,"Ahafo":4.8,
 "Northern":5.3,"Savannah":5.4,"North East":5.4,"Upper East":5.5,"Upper West":5.5,
}
region = st.selectbox("Your region", list(SUN.keys()))
adjust = st.slider("Sun-hours adjustment (if your area differs)", -0.5, 0.5, 0.0, 0.1)
sun_hours = round(SUN[region] + adjust, 2)
st.caption(f"Estimated peak sun hours for **{region}**: {sun_hours} (estimate — verify against irradiance data).")

# ---------- 1. APPLIANCES ----------
st.header("1️⃣ What does your home run?")
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

# ---------- 2. SIZING ----------
st.header("2️⃣ Size the system")
derate = st.slider("System efficiency (losses)", 0.6, 0.9, 0.8, 0.05)
safety = st.slider("Safety margin", 1.0, 1.5, 1.2, 0.05)
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
st.header("3️⃣ Estimate the cost (GHS) — plug real quotes")
c1,c2,c3,c4 = st.columns(4)
panel_rate = c1.number_input("Panel cost / watt (GHS)", 1, 50, 10)
batt_rate  = c2.number_input("Battery cost / kWh (GHS)", 100, 10000, 3000)
inv_rate   = c3.number_input("Inverter cost / kW (GHS)", 100, 20000, 4000)
bos_pct    = c4.number_input("Install + wiring %", 0, 100, 25)

total = (panel_kw*1000*panel_rate + battery_kwh*batt_rate + inverter_kw*inv_rate)*(1+bos_pct/100.0)
st.metric("💰 Estimated total system cost", f"GHS {total:,.0f}")

# ---------- 4. PAYBACK (v2: from your REAL bill) ----------
st.header("4️⃣ Payback — from your REAL bill")
b1,b2,b3 = st.columns(3)
monthly_bill = b1.number_input("ECG bill / month (GHS)", 0, 10000, 150)
monthly_kwh  = b2.number_input("kWh printed on bill / month", 0, 3000, 100)
gen_fuel     = b3.number_input("Generator fuel / month (GHS)", 0, 10000, 200)

eff_tariff = (monthly_bill/monthly_kwh) if monthly_kwh>0 else 0.0
monthly_demand = daily_kwh*30
monthly_gen = panel_kw*sun_hours*derate*30
covered = min(monthly_gen, monthly_demand)
bill_savings = covered*eff_tariff
monthly_savings = bill_savings + gen_fuel

if monthly_savings>0:
    p1,p2,p3,p4 = st.columns(4)
    p1.metric("🧾 Your true tariff", f"GHS {eff_tariff:.2f}/kWh")
    p2.metric("💵 Monthly savings", f"GHS {monthly_savings:,.0f}")
    p3.metric("⏳ Payback", f"{(total/monthly_savings)/12:.1f} yrs")
    p4.metric("📈 10-yr net", f"GHS {monthly_savings*120-total:,.0f}")
else:
    st.warning("Add your bill or generator spend to see payback.")

st.markdown("---")
st.caption("v2 uses your REAL bill to compute your true tariff — no invented numbers. Prices are placeholders; plug 2–3 installer quotes. One rooftop at a time. ⚡")
