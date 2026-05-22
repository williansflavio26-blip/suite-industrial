import streamlit as st
import math

st.set_page_config(page_title="Suit Industrial - Prof. André Gheiralde", layout="wide")

st.title("🏭 Suit Industrial")
st.subheader("Prof. André Gheiralde - Elétrica | Lubrificação | Pressão | Circuitos CC")

menu = st.sidebar.selectbox(
    "Escolha a calculadora",
    ["⚡ Elétrica (NBR 5410/NR-10)",
     "🛢️ Lubrificação (NBR 1409)",
     "💨 Pressão (NR-13)",
     "🔌 Circuitos CC (Leis de Kirchhoff)"]
)

# ==================== CALCULADORA ELÉTRICA ====================
if menu == "⚡ Elétrica (NBR 5410/NR-10)":
    st.header("⚡ Calculadora Elétrica")
    st.markdown("Baseada nas normas **NBR 5410** e **NR-10**.")
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
        st.subheader("📐 Resolução detalhada")
        if tipo == "Potência aparente (kVA)":
            S = P / FP
            st.markdown(f"**Fórmula:** `S = P / FP`\n\n**Dados:** P = {P} kW, FP = {FP}\n\n**Substituindo:** S = {P} / {FP} = **{S:.3f} kVA**\n\n**Significado:** Potência total que a fonte deve fornecer.")
        elif tipo == "Corrente (A) - Monofásico":
            I = (P * 1000) / (V * FP)
            st.markdown(f"**Fórmula:** `I = (P×1000)/(V×FP)`\n\n**Dados:** P={P}kW → {P*1000}W, V={V}V, FP={FP}\n\n**Substituindo:** I={P*1000}/({V}×{FP}) = **{I:.2f} A**")
        else:
            I = (P * 1000) / (math.sqrt(3) * V * FP)
            st.markdown(f"**Fórmula:** `I = (P×1000)/(√3×V×FP)`\n\n**Dados:** P={P}kW, V={V}V, FP={FP}\n\n**Substituindo:** I={P*1000}/(1,732×{V}×{FP}) = **{I:.2f} A**")
        st.info("💡 Quanto maior o FP, menor a corrente.")

# ==================== CALCULADORA DE LUBRIFICAÇÃO ====================
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
            st.markdown(f"**Fórmula:** `Horas = (Capacidade × Carga)/Consumo`\n\n**Dados:** {cap} L, {consumo} L/h, carga {carga}\n\n**Resultado:** {horas:.0f} horas")
    else:
        col1, col2 = st.columns(2)
        with col1:
            diam = st.number_input("Diâmetro do eixo (mm)", value=50)
        with col2:
            larg = st.number_input("Largura do mancal (mm)", value=40)
        if st.button("Calcular graxa"):
            gramas = diam * larg * 0.114
            st.markdown(f"**Fórmula empírica:** `Graxa (g) = Diâmetro × Largura × 0,114`\n\n**Dados:** {diam} mm, {larg} mm\n\n**Resultado:** {gramas:.1f} g")

# ==================== CALCULADORA DE PRESSÃO ====================
elif menu == "💨 Pressão (NR-13)":
    st.header("💨 Calculadora de Pressão")
    tipo_press = st.selectbox("Conversão", ["PSI → Bar", "Bar → PSI", "Força do pistão"])
    if tipo_press == "PSI → Bar":
        psi = st.number_input("PSI", value=100.0)
        if st.button("Converter"):
            bar = psi * 0.0689476
            st.markdown(f"**{psi} PSI = {bar:.3f} bar**\n\n*Fórmula: Bar = PSI × 0,0689476*")
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
            st.markdown(f"**Fórmula:** `F = P × A`\n\n**Dados:** P={pressao} bar → {Pa:.0f} Pa, diâmetro={diametro} cm → área={area:.6f} m²\n\n**Força:** {forca_N:.0f} N ≈ {forca_kgf:.1f} kgf")

# ==================== CALCULADORA DE CIRCUITOS CC ====================
else:
    st.header("🔌 Calculadora de Circuitos CC")
    problema = st.selectbox("Problema", [
        "Questão 1: Voltímetro entre Q e P (R1=10Ω, R2=20Ω, R3=30Ω; E1=5V, E2=10V, E3=15V)",
        "Questão 2: Amperímetro e resistor R (i=5A)",
        "Lei de Ohm",
        "Associação de resistores"
    ])
    if problema.startswith("Questão 1"):
        if st.button("Resolver Questão 1"):
            st.markdown("---")
            st.markdown("""
            **Instrumento:** Voltímetro ideal (R∞, ligação paralela)
            **Cálculo da corrente:**
