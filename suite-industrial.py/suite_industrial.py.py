import streamlit as st
import math

st.set_page_config(page_title="Suit Industrial", layout="wide")

st.title("Suit Industrial")
st.subheader("Elétrica | Lubrificação | Pressão | Circuitos CC")

menu = st.sidebar.selectbox(
    "Escolha a calculadora",
    ["Elétrica (NBR 5410/NR-10)",
     "Lubrificação (NBR 1409)",
     "Pressão (NR-13)",
     "Circuitos CC (Leis de Kirchhoff)"]
)

# ---------- Elétrica ----------
if menu == "Elétrica (NBR 5410/NR-10)":
    st.header("Calculadora Elétrica")
    tipo = st.selectbox("Tipo", ["Potência aparente (kVA)", "Corrente (A) - Monofásico", "Corrente (A) - Trifásico"])
    col1, col2, col3 = st.columns(3)
    with col1: P = st.number_input("Potência (kW)", 0.01, 1.0, 0.1)
    with col2: FP = st.number_input("Fator potência", 0.01, 1.0, 0.92, 0.01)
    with col3: V = st.number_input("Tensão (V)", 1, 220, 10)
    if st.button("Calcular"):
        if tipo.startswith("Potência"):
            S = P / FP
            st.write(f"**S = P/FP** = {P}/{FP} = **{S:.3f} kVA**")
        elif "Monofásico" in tipo:
            I = (P * 1000) / (V * FP)
            st.write(f"**I = (P×1000)/(V×FP)** = ({P}×1000)/({V}×{FP}) = **{I:.2f} A**")
        else:
            I = (P * 1000) / (1.732 * V * FP)
            st.write(f"**I = (P×1000)/(√3×V×FP)** = ({P}×1000)/(1,732×{V}×{FP}) = **{I:.2f} A**")

# ---------- Lubrificação ----------
elif menu == "Lubrificação (NBR 1409)":
    st.header("Calculadora de Lubrificação")
    tipo_lub = st.selectbox("Tipo", ["Troca de óleo", "Quantidade de graxa"])
    if tipo_lub == "Troca de óleo":
        cap = st.number_input("Capacidade (L)", 0.1, 10.0, 10.0)
        cons = st.number_input("Consumo (L/h)", 0.001, 0.05, 0.05, 0.01, format="%.3f")
        carga = st.slider("Fator carga", 0.1, 1.0, 0.8)
        if st.button("Calcular"):
            horas = (cap * carga) / cons
            st.write(f"**Horas = ({cap}×{carga})/{cons} = {horas:.0f} h**")
    else:
        diam = st.number_input("Diâmetro eixo (mm)", 1, 100, 50)
        larg = st.number_input("Largura mancal (mm)", 1, 100, 40)
        if st.button("Calcular"):
            g = diam * larg * 0.114
            st.write(f"**Graxa = {diam}×{larg}×0,114 = {g:.1f} g**")

# ---------- Pressão ----------
elif menu == "Pressão (NR-13)":
    st.header("Calculadora de Pressão")
    tipo_press = st.selectbox("Conversão", ["PSI → Bar", "Bar → PSI", "Força do pistão"])
    if tipo_press == "PSI → Bar":
        psi = st.number_input("PSI", 0.0, 1000.0, 100.0)
        if st.button("Converter"):
            bar = psi * 0.0689476
            st.write(f"**{psi} PSI = {bar:.3f} bar**")
    elif tipo_press == "Bar → PSI":
        bar = st.number_input("bar", 0.0, 1000.0, 6.9)
        if st.button("Converter"):
            psi = bar * 14.5038
            st.write(f"**{bar} bar = {psi:.1f} PSI**")
    else:
        pressao = st.number_input("Pressão (bar)", 0.0, 1000.0, 6.9)
        diam = st.number_input("Diâmetro pistão (cm)", 0.1, 50.0, 5.0)
        if st.button("Calcular"):
            Pa = pressao * 100000
            area = math.pi * (diam/100)**2 / 4
            F = Pa * area
            st.write(f"**Força = {F:.0f} N** ({F/9.8:.1f} kgf)")

# ---------- Circuitos CC ----------
else:
    st.header("Calculadora de Circuitos CC")
    problema = st.selectbox("Problema", [
        "Questão 1: Voltímetro (editar valores)",
        "Questão 2: Amperímetro",
        "Lei de Ohm",
        "Associação de resistores"
    ])

    if problema.startswith("Questão 1"):
        st.markdown("**Insira os valores:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            R1 = st.number_input("R1 (Ω)", 0.1, 100.0, 10.0)
            E1 = st.number_input("E1 (V)", -50.0, 50.0, 5.0)
        with col2:
            R2 = st.number_input("R2 (Ω)", 0.1, 100.0, 20.0)
            E2 = st.number_input("E2 (V)", -50.0, 50.0, 10.0)
        with col3:
            R3 = st.number_input("R3 (Ω)", 0.1, 100.0, 30.0)
            E3 = st.number_input("E3 (V)", -50.0, 50.0, 15.0)
        if st.button("Resolver"):
            fem_total = E2 + E3 - E1
            R_total = R1 + R2 + R3
            I = fem_total / R_total if R_total != 0 else 0
            Vqp = - I * R1 + E1
            st.markdown("---")
            st.markdown(f"**Corrente:** Σfem = {fem_total:.2f} V, ΣR = {R_total:.2f} Ω → I = {I:.3f} A")
            st.markdown(f"**Tensão VQP:** {Vqp:.2f} V → **Resposta: {round(Vqp)} V**")
            st.success(f"✅ {round(Vqp)} V")

    elif problema.startswith("Questão 2"):
        col1, col2 = st.columns(2)
        with col1:
            E_ger = st.number_input("Gerador (V)", 0.0, 100.0, 50.0)
            r_int = st.number_input("Resist. interna (Ω)", 0.0, 10.0, 1.0)
        with col2:
            E_rec = st.number_input("Receptor (V)", 0.0, 100.0, 20.0)
            R_out = st.number_input("Outras resist. (Ω)", 0.0, 50.0, 4.0)
        I = st.number_input("Corrente (A)", 0.1, 20.0, 5.0)
        if st.button("Calcular R"):
            R = (E_ger - E_rec)/I - (r_int + R_out)
            st.write(f"**R = {R:.2f} Ω**")
            if 7.8 < R < 8.2: st.success("Alternativa A (8 Ω)")
            elif 4.8 < R < 5.2: st.success("Alternativa B (5 Ω)")
            elif 3.8 < R < 4.2: st.success("Alternativa C (4 Ω)")

    elif problema == "Lei de Ohm":
        op = st.selectbox("Calcular", ["Tensão (V=R×I)", "Corrente (I=V/R)", "Resistência (R=V/I)"])
        if op.startswith("Tensão"):
            R = st.number_input("R (Ω)", 0.1, 1000.0, 10.0)
            I = st.number_input("I (A)", 0.1, 1000.0, 2.0)
            if st.button("Calcular"): st.write(f"V = {R*I} V")
        elif op.startswith("Corrente"):
            V = st.number_input("V (V)", 0.1, 1000.0, 12.0)
            R = st.number_input("R (Ω)", 0.1, 1000.0, 4.0)
            if st.button("Calcular"): st.write(f"I = {V/R:.2f} A")
        else:
            V = st.number_input("V (V)", 0.1, 1000.0, 12.0)
            I = st.number_input("I (A)", 0.1, 1000.0, 3.0)
            if st.button("Calcular"): st.write(f"R = {V/I:.2f} Ω")

    else:  # Associação
        st.subheader("Associação de resistores")
        tipo = st.radio("Tipo", ["Série", "Paralelo", "Misto"])
        c1, c2, c3 = st.columns(3)
        with c1: R1 = st.number_input("R1 (Ω)", 0.1, 1000.0, 10.0)
        with c2: R2 = st.number_input("R2 (Ω)", 0.1, 1000.0, 20.0)
        with c3: R3 = st.number_input("R3 (Ω)", 0.1, 1000.0, 30.0)
        if st.button("Calcular Req"):
            if tipo == "Série":
                Req = R1 + R2 + R3
            elif tipo == "Paralelo":
                Req = 1 / (1/R1 + 1/R2 + 1/R3)
            else:
                Req = (R1 + R2) * R3 / (R1 + R2 + R3)
            st.write(f"Req = {Req:.2f} Ω")

st.sidebar.markdown("---")
st.sidebar.caption("Detalhamento completo")
