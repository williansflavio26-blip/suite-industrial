**Resultado:** R = **{R_calc:.2f} Ω**
""")
if abs(R_calc - 8) < 0.1:
    st.success("✅ Corresponde à alternativa A (8 Ω).")
elif abs(R_calc - 5) < 0.1:
    st.success("✅ Corresponde à alternativa B (5 Ω).")
elif abs(R_calc - 4) < 0.1:
    st.success("✅ Corresponde à alternativa C (4 Ω).")
else:
    st.info("O valor obtido pode variar conforme os dados exatos da figura.")

# --------------------------------------------------------
# LEI DE OHM
# --------------------------------------------------------
elif problema == "Lei de Ohm - Cálculo de tensão, corrente ou resistência":
ohm_op = st.selectbox("Calcular", ["Tensão (V = R × I)", "Corrente (I = V / R)", "Resistência (R = V / I)"])
if ohm_op == "Tensão (V = R × I)":
R = st.number_input("Resistência (Ω)", min_value=0.1, value=10.0)
I = st.number_input("Corrente (A)", min_value=0.1, value=2.0)
if st.button("Calcular V"):
V = R * I
st.markdown(f"**Fórmula:** V = R × I = {R} × {I} = **{V} V**")
elif ohm_op == "Corrente (I = V / R)":
V = st.number_input("Tensão (V)", min_value=0.1, value=12.0)
R = st.number_input("Resistência (Ω)", min_value=0.1, value=4.0)
if st.button("Calcular I"):
I = V / R
st.markdown(f"**Fórmula:** I = V / R = {V} / {R} = **{I:.2f} A**")
else:
V = st.number_input("Tensão (V)", min_value=0.1, value=12.0)
I = st.number_input("Corrente (A)", min_value=0.1, value=3.0)
if st.button("Calcular R"):
R = V / I
st.markdown(f"**Fórmula:** R = V / I = {V} / {I} = **{R:.2f} Ω**")

# --------------------------------------------------------
# ASSOCIAÇÃO DE RESISTORES
# --------------------------------------------------------
else:
st.subheader("Associação de resistores")
tipo_assoc = st.radio("Tipo", ["Série", "Paralelo", "Misto (2 em série + 1 em paralelo)"])
col1, col2, col3 = st.columns(3)
with col1:
R1 = st.number_input("R1 (Ω)", min_value=0.1, value=10.0)
with col2:
R2 = st.number_input("R2 (Ω)", min_value=0.1, value=20.0)
with col3:
R3 = st.number_input("R3 (Ω)", min_value=0.1, value=30.0)

if st.button("Calcular resistência equivalente"):
if tipo_assoc == "Série":
Req = R1 + R2 + R3
st.markdown(f"**Req = R1 + R2 + R3** = {R1} + {R2} + {R3} = **{Req:.2f} Ω**")
elif tipo_assoc == "Paralelo":
Req = 1 / (1/R1 + 1/R2 + 1/R3)
st.markdown(f"**1/Req = 1/R1 + 1/R2 + 1/R3** = 1/{R1} + 1/{R2} + 1/{R3} = {1/R1+1/R2+1/R3:.4f} → **Req = {Req:.2f} Ω**")
else:
# Misto: R1 e R2 em série, esse conjunto em paralelo com R3
Req = (R1 + R2) * R3 / (R1 + R2 + R3)
st.markdown(f"**Associação:** R1 e R2 em série → Rs = {R1+R2:.2f} Ω; depois Rs em paralelo com R3: Req = (Rs × R3)/(Rs+R3) = ({R1+R2:.2f} × {R3}) / ({R1+R2+R3:.2f}) = **{Req:.2f} Ω**")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para o Prof. André Gheiralde - Atualizado com detalhamento de cálculos e instrumentos de medição.")
