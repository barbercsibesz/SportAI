import streamlit as st
import math

st.set_page_config(
page_title="Sport AI Tippelő",
page_icon="⚽",
layout="wide"
)

st.title("⚽ Sport AI Tippelő")
st.write("Futballmérkőzések statisztikai elemzése és valószínűségi becslése.")

st.warning(
"A becslések matematikai modelleken alapulnak, "
"nem garantálják az eredményt."
)

st.header("📊 Mérkőzés elemzése")

col1, col2 = st.columns(2)

with col1:
home = st.text_input("Hazai csapat", "Liverpool")
home_goals = st.number_input(
"Hazai csapat várható góljai",
min_value=0.0, max_value=6.0,
value=1.8, step=0.1
)

with col2:
away = st.text_input("Vendégcsapat", "Chelsea")
away_goals = st.number_input(
"Vendégcsapat várható góljai",
min_value=0.0, max_value=6.0,
value=1.1, step=0.1
)

def poisson(k, lam):
return (math.exp(-lam) * lam**k / math.factorial(k))

if st.button("🔍 Mérkőzés elemzése", type="primary"):
if not home.strip() or not away.strip():
st.error("Add meg mindkét csapat nevét!")
else:
max_goals = 10
p_home = 0.0
p_draw = 0.0
p_away = 0.0
p_btts = 0.0
p_over25 = 0.0

for h in range(max_goals + 1):
for a in range(max_goals + 1):
p = poisson(h, home_goals) * poisson(a, away_goals)

if h > a:
p_home += p
elif h == a:
p_draw += p
else:
p_away += p

if h > 0 and a > 0:
p_btts += p

if h + a >= 3:
p_over25 += p

st.subheader(f"{home} – {away}")

c1, c2, c3 = st.columns(3)
c1.metric("Hazai győzelem", f"{p_home:.1%}")
c2.metric("Döntetlen", f"{p_draw:.1%}")
c3.metric("Vendég győzelem", f"{p_away:.1%}")

c4, c5 = st.columns(2)
c4.metric("Mindkét csapat gólt szerez", f"{p_btts:.1%}")
c5.metric("Több mint 2,5 gól", f"{p_over25:.1%}")

st.info(
"Ez egy egyszerű Poisson-modell. "
"A becslés a megadott várható gólszámoktól függ, "
"és nem használ automatikusan friss csapatstatisztikákat."
)
