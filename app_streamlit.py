import streamlit as st
import math

st.set_page_config(page_title="Suit Industrial", layout="wide")

st.title("🏭 Suit Industrial")
st.subheader("Elétrica | Lubrificação | Pressão | Circuitos CC")

menu = st.sidebar.selectbox(
    "Escolha a calculadora",
    ["⚡ Elétrica (NBR 5410/NR-10)",
     "🛢️ Lubrificação (NBR 1409)",
     "💨 Pressão (NR-13)",
     "🔌 Circuitos CC (Leis de Kirchhoff)"]
)

# ==================== ELÉTRICA ====================
if menu == "⚡ Elétrica (NBR 5410/NR-10)":
    st.header("⚡ Calculadora Elétrica")
    tipo = st.selectbox("Tipo de cálculo", [
        "Potência aparente (kVA)",
        "Corrente (A) - Monofásico",
        "Corrente (A) - Trifásico"
    ])
    col1, col2, col3 = st.columns(3)
    with col1:
        P = st.number_input("Potência ativa (kW)", min_value=0.01, value=1.0, step=0.1)
    with col2:
        FP = st.number_input("Fator de potência", min_value=0.01, max_value=1.0, value=0.92, step=0.01)
    with col3:
        V = st.number_input("Tensão (V)", min_value=1, value=220, step=10)

    if st.button("Calcular", type="primary"):
        st.markdown("---")
        if tipo == "Potência aparente (kVA)":
            S = P / FP
            st.markdown(f"**S = P/FP** = {P}/{FP} = **{S:.3f} kVA**")
        elif tipo == "Corrente (A) - Monofásico":
            I = (P * 1000) / (V * FP)
            st.markdown(f"**I = (P×1000)/(V×FP)** = ({P}×1000)/({V}×{FP}) = **{I:.2f} A**")
        else:
            I = (P * 1000) / (math.sqrt(3) * V * FP)
            st.markdown(f"**I = (P×1000)/(√3×V×FP)** = ({P}×1000)/(1,732×{V}×{FP}) = **{I:.2f} A**")

# ==================== LUBRIFICAÇÃO ====================
elif menu == "🛢️ Lubrificação (NBR 1409)":
    st.header("🛢️ Calculadora de Lubrificação")
    tipo_lub = st.selectbox("Tipo", ["Intervalo para troca de óleo", "Quantidade de graxa"])
    if tipo_lub == "Intervalo para troca de óleo":
        col1, col2, col3 = st.columns(3)
        with col1:
            cap = st.number_input("Capacidade do cárter (L)", value=10.0)
        with col2:
            consumo = st.number_input("Consumo de óleo (L/h)", value=0.05, step=0.01, format="%.3f")
        with col3:
            carga = st.slider("Fator de carga", 0.1, 1.0, 0.8)
        if st.button("Calcular troca"):
            horas = (cap * carga) / consumo
            st.markdown(f"**Horas = (Capacidade × Carga)/Consumo** = ({cap}×{carga})/{consumo} = **{horas:.0f} h**")
    else:
        col1, col2 = st.columns(2)
        with col1:
            diam = st.number_input("Diâmetro do eixo (mm)", value=50)
        with col2:
            larg = st.number_input("Largura do mancal (mm)", value=40)
        if st.button("Calcular graxa"):
            gramas = diam * larg * 0.114
            st.markdown(f"**Graxa (g) = Diâmetro × Largura × 0,114** = {diam}×{larg}×0,114 = **{gramas:.1f} g**")

# ==================== PRESSÃO ====================
elif menu == "💨 Pressão (NR-13)":
    st.header("💨 Calculadora de Pressão")
    tipo_press = st.selectbox("Conversão", ["PSI → Bar", "Bar → PSI", "Força do pistão"])
    if tipo_press == "PSI → Bar":
        psi = st.number_input("PSI", value=100.0)
        if st.button("Converter"):
            bar = psi * 0.0689476
            st.markdown(f"**{psi} PSI = {bar:.3f} bar**")
    elif tipo_press == "Bar → PSI":
        bar = st.number_input("bar", value=6.9)
        if st.button("Converter"):
            psi = bar * 14.5038
            st.markdown(f"**{bar} bar = {psi:.1f} PSI**")
    else:
        col1, col2 = st.columns(2)
        with col1:
            pressao = st.number_input("Pressão (bar)", value=6.9)
        with col2:
            diametro = st.number_input("Diâmetro do pistão (cm)", value=5.0)
        if st.button("Calcular força"):
            Pa = pressao * 100000
            area = math.pi * (diametro/100)**2 / 4
            forca_N = Pa * area
            forca_kgf = forca_N / 9.80665
            st.markdown(f"**F = P × A** → Força = **{forca_N:.0f} N** ≈ **{forca_kgf:.1f} kgf**")

# ==================== CIRCUITOS CC ====================
else:
    st.header("🔌 Calculadora de Circuitos CC")
    problema = st.selectbox("Problema", [
        "Questão 1: Voltímetro entre Q e P",
        "Questão 2: Amperímetro e resistor R",
        "Lei de Ohm",
        "Associação de resistores"
    ])

    # ------------------ Questão 1 ------------------
    if problema.startswith("Questão 1"):
        st.markdown("**Insira os valores do circuito:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            R1 = st.number_input("R1 (Ω)", value=10.0, step=1.0)
            E1 = st.number_input("E1 (V)", value=5.0, step=1.0)
        with col2:
            R2 = st.number_input("R2 (Ω)", value=20.0, step=1.0)
            E2 = st.number_input("E2 (V)", value=10.0, step=1.0)
        with col3:
            R3 = st.number_input("R3 (Ω)", value=30.0, step=1.0)
            E3 = st.number_input("E3 (V)", value=15.0, step=1.0)
        
        if st.button("Resolver Questão 1"):
            fem_total = E2 + E3 - E1
            R_total = R1 + R2 + R3
            I = fem_total / R_total if R_total != 0 else 0
            VQP = - (I * R1) + E1
            resposta = round(VQP)
            
            st.markdown("---")
            st.subheader("📐 Resolução detalhada")
            st.markdown(f"""
            **Instrumento:** Voltímetro ideal (R∞, paralelo)
            
            **1. Corrente na malha principal:**
