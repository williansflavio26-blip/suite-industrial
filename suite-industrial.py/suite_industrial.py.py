import streamlit as st
import math

st.set_page_config(page_title="Suit Industrial - Prof. André Gheiralde", layout="wide")

st.title("🏭 Suit Industrial")
st.subheader("- Elétrica | Lubrificação | Pressão | Circuitos CC")

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
        "Questão 1: Voltímetro entre Q e P (R1=10Ω, R2=20Ω, R3=30Ω; E1=5V, E2=10V, E3=15V)",
        "Questão 2: Amperímetro e resistor R (i=5A)",
        "Lei de Ohm",
        "Associação de resistores"
    ])
    if problema.startswith("Questão 1"):
        if st.button("Resolver Questão 1"):
            st.markdown("""
            **Instrumento:** Voltímetro ideal (R∞, paralelo)
            **Corrente:** Σfem = 10+15-5 = 20V, ΣR = 60Ω → I = 20/60 = 0,333A
            **Tensão VQP:** 11V (alternativa A)
            """)
            st.success("✅ Resposta: 11 V")
    elif problema.startswith("Questão 2"):
        st.info("Informe os dados do circuito (conforme a imagem da prova)")
        col1, col2 = st.columns(2)
        with col1:
            E_ger = st.number_input("Tensão do gerador (V)", value=50.0)
            r_int = st.number_input("Resistência interna (Ω)", value=1.0)
        with col2:
            E_rec = st.number_input("Tensão do receptor (V)", value=20.0)
            R_outras = st.number_input("Outras resistências (Ω)", value=4.0)
        I = st.number_input("Corrente medida (A)", value=5.0)
        if st.button("Calcular R"):
            R_calc = (E_ger - E_rec) / I - (r_int + R_outras)
            st.markdown(f"**R = {R_calc:.2f} Ω**")
            if 7.8 < R_calc < 8.2:
                st.success("Alternativa A (8 Ω)")
            elif 4.8 < R_calc < 5.2:
                st.success("Alternativa B (5 Ω)")
            elif 3.8 < R_calc < 4.2:
                st.success("Alternativa C (4 Ω)")
    elif problema == "Lei de Ohm":
        ohm_op = st.selectbox("Calcular", ["Tensão (V=R×I)", "Corrente (I=V/R)", "Resistência (R=V/I)"])
        if ohm_op == "Tensão (V=R×I)":
            R = st.number_input("R (Ω)", value=10.0)
            I = st.number_input("I (A)", value=2.0)
            if st.button("Calcular V"):
                st.markdown(f"**V = {R} × {I} = {R*I} V**")
        elif ohm_op == "Corrente (I=V/R)":
            V = st.number_input("V (V)", value=12.0)
            R = st.number_input("R (Ω)", value=4.0)
            if st.button("Calcular I"):
                st.markdown(f"**I = {V} / {R} = {V/R:.2f} A**")
        else:
            V = st.number_input("V (V)", value=12.0)
            I = st.number_input("I (A)", value=3.0)
            if st.button("Calcular R"):
                st.markdown(f"**R = {V} / {I} = {V/I:.2f} Ω**")
    else:  # Associação de resistores
        st.subheader("Associação de resistores")
        tipo_assoc = st.radio("Tipo", ["Série", "Paralelo", "Misto (série+paralelo)"])
        c1, c2, c3 = st.columns(3)
        with c1:
            R1 = st.number_input("R1 (Ω)", value=10.0)
        with c2:
            R2 = st.number_input("R2 (Ω)", value=20.0)
        with c3:
            R3 = st.number_input("R3 (Ω)", value=30.0)
        if st.button("Calcular Req"):
            if tipo_assoc == "Série":
                Req = R1 + R2 + R3
                st.markdown(f"**Req = {R1} + {R2} + {R3} = {Req:.2f} Ω**")
            elif tipo_assoc == "Paralelo":
                Req = 1 / (1/R1 + 1/R2 + 1/R3)
                st.markdown(f"**1/Req = 1/{R1} + 1/{R2} + 1/{R3}** → Req = **{Req:.2f} Ω**")
            else:
                Rs = R1 + R2
                Req = (Rs * R3) / (Rs + R3)
                st.markdown(f"**Série R1+R2 = {Rs:.2f} Ω** → Paralelo com R3: Req = **{Req:.2f} Ω**")

st.sidebar.markdown("---")
st.sidebar.caption("Prof. André Gheiralde - Detalhamento completo")
