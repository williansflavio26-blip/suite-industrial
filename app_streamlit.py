import streamlit as st

st.set_page_config(page_title="Suíte Industrial", layout="centered")
st.title("🏭 Suíte de Ferramentas Industriais")
st.caption("Baseado em NBR, NR, CLT, IEC")

aba = st.tabs(["⚡ Elétrica", "🛢️ Lubrificação", "⏱️ Horas Trabalhadas", "📊 Pressão"])

# ==================== ELÉTRICA ====================
with aba[0]:
    st.subheader("Calculadora Elétrica (NBR 5410 / NR-10)")
    tipo = st.selectbox("Tipo de cálculo", [
        "Potência aparente (kVA) - Monofásico",
        "Corrente nominal (A) - Motor monofásico"
    ])
    potencia = st.number_input("Potência ativa (kW)", value=1.0, step=0.1)
    fp = st.number_input("Fator de potência", value=0.92, min_value=0.0, max_value=1.0, step=0.01)
    if tipo == "Corrente nominal (A) - Motor monofásico":
        tensao = st.number_input("Tensão (V)", value=220.0, step=10.0)
        if st.button("Calcular Corrente"):
            if tensao > 0 and fp > 0:
                i = (potencia * 1000) / (tensao * fp)
                st.success(f"Corrente = {i:.2f} A")
            else:
                st.error("Valores inválidos")
    else:
        if st.button("Calcular Potência"):
            if fp > 0:
                s = potencia / fp
                st.success(f"Potência aparente = {s:.3f} kVA")
            else:
                st.error("Fator de potência deve ser > 0")

# ==================== LUBRIFICAÇÃO ====================
with aba[1]:
    st.subheader("Tabela de Lubrificação (NBR 15594)")
    equip = st.text_input("Equipamento")
    ponto = st.text_input("Ponto de lubrificação")
    lub = st.selectbox("Lubrificante", ["Graxa de lítio EP2", "Óleo ISO VG 46", "Graxa para altas temperaturas"])
    periodicidade = st.number_input("Periodicidade (dias)", value=30, step=1)
    if st.button("Registrar"):
        if equip and ponto:
            st.info(f"✅ {equip} - {ponto} lubrificado com {lub} a cada {periodicidade} dias.")
        else:
            st.warning("Preencha equipamento e ponto.")

# ==================== HORAS TRABALHADAS ====================
with aba[2]:
    st.subheader("Cálculo de Horas (CLT / NR-16)")
    salario = st.number_input("Salário base (R$)", value=2500.0, step=100.0)
    horas_dia = st.number_input("Horas por dia", value=8.0, step=0.5)
    dias = st.number_input("Dias trabalhados no mês", value=22, step=1)
    periculosidade = st.checkbox("Adicional de periculosidade (30%)")
    horas_extras = st.number_input("Horas extras (50%)", value=0.0, step=1.0)
    if st.button("Calcular Salário"):
        valor_hora = salario / (220 if horas_dia == 8 else horas_dia * dias)
        total = salario
        if periculosidade:
            total += salario * 0.30
        total += valor_hora * 0.5 * horas_extras
        st.success(f"Total estimado: R$ {total:,.2f}")
        st.caption(f"Valor da hora normal: R$ {valor_hora:.2f}")

# ==================== PRESSÃO ====================
with aba[3]:
    st.subheader("Conversor de Pressão (SI)")
    valor = st.number_input("Valor", value=1.0, step=0.1)
    de = st.selectbox("De", ["psi", "bar", "kPa", "MPa", "kgf/cm²"])
    para = st.selectbox("Para", ["psi", "bar", "kPa", "MPa", "kgf/cm²"])
    fatores = {"psi": 1/14.5038, "bar": 1.0, "kPa": 0.001, "MPa": 10.0, "kgf/cm²": 0.980665}
    if st.button("Converter"):
        em_bar = valor * fatores[de]
        resultado = em_bar / fatores[para]
        st.success(f"{valor} {de} = {resultado:.6f} {para}")