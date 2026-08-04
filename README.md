# ☀️ Ghana Solar Decision Tool

> *Should I go solar? What size? How fast does it pay for itself?*

A simple, honest calculator for a Ghanaian home or shop: enter your appliances,
and it sizes the solar system (panels, battery, inverter), estimates the cost in
GHS, and shows the payback versus your ECG bill / generator.

🧑‍💻 Built by **Collins Nyankson**, 17 — for his own home first (user #1). 🇬🇭

## 🎯 The problem it solves
Ghana has some of the strongest sunshine on earth, yet solar supplies only
~1–3% of grid electricity. Not because people don't want it — but because of
upfront-cost fear and uncertainty ("what size do I need? will it pay back?").
This tool removes that uncertainty, one household at a time.

## ▶️ Try it
👉 [Live app](https://ghana-solar-tool-pli6auappdapghergd2rfz.streamlit.app/)

## 🧮 How it works
1. **Load:** sum of (watts × quantity × hours/day) → daily kWh.
2. **Panels:** daily kWh ÷ (peak sun hours × efficiency) × safety margin.
3. **Battery:** daily kWh × days of backup ÷ depth-of-discharge (Li vs lead-acid).
4. **Inverter:** connected load × diversity, rounded to a standard size.
5. **Cost:** panels + battery + inverter + install %, in GHS (editable — plug real quotes).
6. **Payback:** total cost ÷ monthly savings (bill offset + generator fuel).

## ⚠️ Assumptions
Defaults are estimates for a typical Ghanaian home (peak sun ≈ 4.5 h,
efficiency ≈ 80%, lithium DoD 80%). Prices are placeholders — replace with 2–3
real installer quotes for accuracy. This is a decision aid, not an
engineering spec.

## 🛠️ Stack
Python · Pandas · NumPy · Streamlit

## 🔜 Next
- Real ECG tariff bands
- Region-specific sun hours
- Financing / pay-as-you-go modelling
- Lead capture for installers (the business layer)

---
*One rooftop at a time. ⚡*
