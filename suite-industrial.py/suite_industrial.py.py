import sys
import json
import os
from datetime import datetime, time, timedelta
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit, QGroupBox,
    QSpinBox, QDoubleSpinBox, QTextEdit, QFileDialog
)
from PyQt5.QtCore import Qt, QDate

# ==================== CALCULADORA ELÉTRICA (NBR 5410, NR-10, NR-12, IEC 60034-1) ====================

class CalculadoraEletrica(QWidget):
    """
    Calculadora para dimensionamento elétrico e de motores conforme:
    - NBR 5410: Instalações elétricas de baixa tensão[reference:0]
    - NR-10: Segurança em instalações elétricas[reference:1]
    - NR-12: Segurança em máquinas e equipamentos[reference:2]
    - IEC 60034-1: Máquinas elétricas girantes[reference:3]
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Título com referência às normas
        titulo = QLabel("⚡ Dimensionamento Elétrico e de Motores ⚡")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
        layout.addWidget(titulo)

        normas = QLabel("Baseado em: NBR 5410 | NR-10 | NR-12 | IEC 60034-1")
        normas.setAlignment(Qt.AlignCenter)
        normas.setStyleSheet("font-size: 10px; color: gray; margin-bottom: 10px;")
        layout.addWidget(normas)

        # Seleção do tipo de cálculo
        self.tipo_calculo = QComboBox()
        self.tipo_calculo.addItems([
            "Potência aparente (kVA) - Circuito monofásico",
            "Potência aparente (kVA) - Circuito trifásico",
            "Corrente nominal (A) - Motor monofásico",
            "Corrente nominal (A) - Motor trifásico",
            "Dimensionamento de condutor (mm²) - Queda de tensão"
        ])
        layout.addWidget(self.tipo_calculo)

        # Frame para parâmetros de entrada
        params_frame = QGroupBox("Parâmetros de entrada")
        params_layout = QGridLayout()
        params_frame.setLayout(params_layout)
        layout.addWidget(params_frame)

        # Campos dinâmicos (serão configurados conforme a seleção)
        self.campos = {}
        linhas = [
            ("Tensão (V):", "tensao"),
            ("Potência ativa (kW):", "potencia"),
            ("Fator de potência:", "fp"),
            ("Corrente (A):", "corrente"),
            ("Comprimento do circuito (m):", "comprimento"),
            ("Queda de tensão (%):", "queda"),
            ("Material do condutor:", "material")
        ]
        for i, (label, key) in enumerate(linhas):
            lbl = QLabel(label)
            params_layout.addWidget(lbl, i, 0)
            if key == "material":
                campo = QComboBox()
                campo.addItems(["Cobre", "Alumínio"])
            else:
                campo = QLineEdit()
                campo.setPlaceholderText("Digite o valor")
            params_layout.addWidget(campo, i, 1)
            self.campos[key] = campo

        # Botão calcular
        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        self.btn_calcular.clicked.connect(self.calcular)
        layout.addWidget(self.btn_calcular)

        # Área de resultado
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setMaximumHeight(150)
        layout.addWidget(self.resultado)

        # Observação de segurança (NR-10)
        obs = QLabel("⚠️ Conforme NR-10: toda instalação elétrica deve ser realizada por profissional qualificado e com medidas de segurança adequadas.")
        obs.setWordWrap(True)
        obs.setStyleSheet("font-size: 10px; color: #d32f2f; margin-top: 10px;")
        layout.addWidget(obs)

        self.setLayout(layout)

    def calcular(self):
        tipo = self.tipo_calculo.currentText()
        try:
            if tipo == "Potência aparente (kVA) - Circuito monofásico":
                self._calcular_potencia_monofasico()
            elif tipo == "Potência aparente (kVA) - Circuito trifásico":
                self._calcular_potencia_trifasico()
            elif tipo == "Corrente nominal (A) - Motor monofásico":
                self._calcular_corrente_monofasico()
            elif tipo == "Corrente nominal (A) - Motor trifásico":
                self._calcular_corrente_trifasico()
            elif tipo == "Dimensionamento de condutor (mm²) - Queda de tensão":
                self._dimensionar_condutor()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Falha no cálculo: {e}")

    def _calcular_potencia_monofasico(self):
        p = float(self.campos["potencia"].text())
        fp = float(self.campos["fp"].text())
        if fp <= 0 or fp > 1:
            raise ValueError("Fator de potência deve estar entre 0 e 1")
        s = p / fp  # kVA
        self.resultado.setText(f"Potência aparente (S) = {s:.3f} kVA\n\n"
                               f"Conforme NBR 5410, o dimensionamento de condutores e proteções "
                               f"deve considerar a corrente nominal I = S * 1000 / V (com V em Volts).")

    def _calcular_potencia_trifasico(self):
        p = float(self.campos["potencia"].text())
        fp = float(self.campos["fp"].text())
        if fp <= 0 or fp > 1:
            raise ValueError("Fator de potência deve estar entre 0 e 1")
        s = p / fp
        self.resultado.setText(f"Potência aparente (S) = {s:.3f} kVA\n\n"
                               f"A corrente nominal para sistema trifásico é I = S * 1000 / (√3 * V).\n"
                               f"Norma aplicável: NBR 5410 e IEC 60034-1[reference:4].")

    def _calcular_corrente_monofasico(self):
        p = float(self.campos["potencia"].text())
        v = float(self.campos["tensao"].text())
        fp = float(self.campos["fp"].text())
        if v <= 0 or fp <= 0:
            raise ValueError("Tensão e fator de potência devem ser positivos")
        i = (p * 1000) / (v * fp)
        self.resultado.setText(f"Corrente nominal (I) = {i:.2f} A\n\n"
                               f"Motores elétricos devem atender à IEC 60034-1[reference:5].\n"
                               f"NR-12 exige proteção contra sobrecorrente e partida acidental[reference:6].")

    def _calcular_corrente_trifasico(self):
        p = float(self.campos["potencia"].text())
        v = float(self.campos["tensao"].text())
        fp = float(self.campos["fp"].text())
        if v <= 0 or fp <= 0:
            raise ValueError("Tensão e fator de potência devem ser positivos")
        i = (p * 1000) / (1.732 * v * fp)
        self.resultado.setText(f"Corrente nominal (I) = {i:.2f} A\n\n"
                               f"Para motores trifásicos, a corrente de partida pode atingir de 6 a 10 vezes a nominal.\n"
                               f"Normas: NBR 5410, NR-10, NR-12 e IEC 60034-1.")

    def _dimensionar_condutor(self):
        i = float(self.campos["corrente"].text())
        l = float(self.campos["comprimento"].text())
        queda = float(self.campos["queda"].text())
        material = self.campos["material"].currentText()
        v = float(self.campos["tensao"].text())

        # Resistividade do material (Ω·mm²/m)
        if material == "Cobre":
            rho = 0.0172
        else:
            rho = 0.0282

        # Fórmula para seção mínima considerando queda de tensão em circuito monofásico
        s = (2 * rho * l * i) / (queda / 100 * v)
        s = max(s, 1.5)  # valor mínimo conforme NBR 5410

        # Padronização para bitolas comerciais (valores fictícios para exemplo)
        bitolas = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240]
        secao = next((b for b in bitolas if b >= s), 240)

        self.resultado.setText(f"Seção mínima teórica: {s:.2f} mm²\n"
                               f"Seção comercial recomendada: {secao} mm²\n\n"
                               f"✔️ Conforme NBR 5410, a queda de tensão não deve ultrapassar 7% em circuitos terminais.\n"
                               f"✔️ A instalação deve atender NR-10 (medidas de segurança contra riscos elétricos).\n"
                               f"✔️ Para máquinas, NR-12 exige dispositivos de proteção contra sobretensão[reference:7].")


# ==================== TABELA DE LUBRIFICAÇÃO (ABNT NBR 15594) ====================

class TabelaLubrificacao(QWidget):
    """
    Tabela de lubrificação baseada na ABNT NBR 15594: Gestão de lubrificação[reference:8]
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("🛢️ Tabela de Lubrificação - Plano de Manutenção 🛢️")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
        layout.addWidget(titulo)

        normas = QLabel("Baseado em: ABNT NBR 15594 (Gestão de lubrificação)")
        normas.setAlignment(Qt.AlignCenter)
        normas.setStyleSheet("font-size: 10px; color: gray; margin-bottom: 10px;")
        layout.addWidget(normas)

        # Formulário para adicionar equipamento
        form_group = QGroupBox("Adicionar/Editar Equipamento")
        form_layout = QGridLayout()
        form_group.setLayout(form_layout)

        form_layout.addWidget(QLabel("Equipamento:"), 0, 0)
        self.equipamento = QLineEdit()
        form_layout.addWidget(self.equipamento, 0, 1)

        form_layout.addWidget(QLabel("Ponto de lubrificação:"), 1, 0)
        self.ponto = QLineEdit()
        form_layout.addWidget(self.ponto, 1, 1)

        form_layout.addWidget(QLabel("Tipo de graxa/óleo:"), 2, 0)
        self.lubrificante = QComboBox()
        self.lubrificante.addItems([
            "Graxa de lítio EP2", "Graxa de cálcio", "Óleo ISO VG 32",
            "Óleo ISO VG 46", "Óleo ISO VG 68", "Graxa de molibdênio",
            "Óleo sintético 220", "Graxa para altas temperaturas"
        ])
        form_layout.addWidget(self.lubrificante, 2, 1)

        form_layout.addWidget(QLabel("Periodicidade (dias):"), 3, 0)
        self.periodicidade = QSpinBox()
        self.periodicidade.setRange(1, 365)
        self.periodicidade.setValue(30)
        form_layout.addWidget(self.periodicidade, 3, 1)

        form_layout.addWidget(QLabel("Quantidade (g ou mL):"), 4, 0)
        self.quantidade = QDoubleSpinBox()
        self.quantidade.setRange(0, 10000)
        self.quantidade.setSuffix(" g")
        form_layout.addWidget(self.quantidade, 4, 1)

        form_layout.addWidget(QLabel("Responsável:"), 5, 0)
        self.responsavel = QLineEdit()
        form_layout.addWidget(self.responsavel, 5, 1)

        # Botões de ação
        btn_layout = QHBoxLayout()
        self.btn_adicionar = QPushButton("➕ Adicionar")
        self.btn_adicionar.clicked.connect(self.adicionar_linha)
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self.editar_linha)
        self.btn_remover = QPushButton("🗑️ Remover")
        self.btn_remover.clicked.connect(self.remover_linha)
        self.btn_salvar = QPushButton("💾 Salvar em arquivo")
        self.btn_salvar.clicked.connect(self.salvar_arquivo)
        self.btn_carregar = QPushButton("📂 Carregar arquivo")
        self.btn_carregar.clicked.connect(self.carregar_arquivo)

        btn_layout.addWidget(self.btn_adicionar)
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_remover)
        btn_layout.addWidget(self.btn_salvar)
        btn_layout.addWidget(self.btn_carregar)

        form_layout.addLayout(btn_layout, 6, 0, 1, 2)

        layout.addWidget(form_group)

        # Tabela de lubrificação
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(6)
        self.tabela.setHorizontalHeaderLabels([
            "Equipamento", "Ponto", "Lubrificante", "Periodicidade (dias)",
            "Quantidade", "Responsável"
        ])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.itemSelectionChanged.connect(self.on_selecionar_linha)
        layout.addWidget(self.tabela)

        # Instrução final
        obs = QLabel("📌 A NBR 15594 recomenda manter registros atualizados e planos de lubrificação para cada ativo.")
        obs.setStyleSheet("font-size: 10px; margin-top: 8px;")
        layout.addWidget(obs)

        self.setLayout(layout)
        self.linha_selecionada = -1
        self.dados_lubrificacao = []  # lista de dicionários

    def adicionar_linha(self):
        if not self.equipamento.text():
            QMessageBox.warning(self, "Aviso", "Informe o nome do equipamento.")
            return
        if not self.ponto.text():
            QMessageBox.warning(self, "Aviso", "Informe o ponto de lubrificação.")
            return

        linha = {
            "equipamento": self.equipamento.text(),
            "ponto": self.ponto.text(),
            "lubrificante": self.lubrificante.currentText(),
            "periodicidade": self.periodicidade.value(),
            "quantidade": self.quantidade.value(),
            "responsavel": self.responsavel.text()
        }
        self.dados_lubrificacao.append(linha)
        self._atualizar_tabela()
        self._limpar_formulario()

    def _atualizar_tabela(self):
        self.tabela.setRowCount(len(self.dados_lubrificacao))
        for i, linha in enumerate(self.dados_lubrificacao):
            self.tabela.setItem(i, 0, QTableWidgetItem(linha["equipamento"]))
            self.tabela.setItem(i, 1, QTableWidgetItem(linha["ponto"]))
            self.tabela.setItem(i, 2, QTableWidgetItem(linha["lubrificante"]))
            self.tabela.setItem(i, 3, QTableWidgetItem(str(linha["periodicidade"])))
            self.tabela.setItem(i, 4, QTableWidgetItem(f"{linha['quantidade']:.1f}"))
            self.tabela.setItem(i, 5, QTableWidgetItem(linha["responsavel"]))

    def _limpar_formulario(self):
        self.equipamento.clear()
        self.ponto.clear()
        self.lubrificante.setCurrentIndex(0)
        self.periodicidade.setValue(30)
        self.quantidade.setValue(0)
        self.responsavel.clear()

    def on_selecionar_linha(self):
        selecionados = self.tabela.selectedItems()
        if selecionados:
            self.linha_selecionada = selecionados[0].row()
            dados = self.dados_lubrificacao[self.linha_selecionada]
            self.equipamento.setText(dados["equipamento"])
            self.ponto.setText(dados["ponto"])
            self.lubrificante.setCurrentText(dados["lubrificante"])
            self.periodicidade.setValue(dados["periodicidade"])
            self.quantidade.setValue(dados["quantidade"])
            self.responsavel.setText(dados["responsavel"])

    def editar_linha(self):
        if self.linha_selecionada < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma linha para editar.")
            return
        if not self.equipamento.text() or not self.ponto.text():
            QMessageBox.warning(self, "Aviso", "Preencha equipamento e ponto.")
            return
        self.dados_lubrificacao[self.linha_selecionada] = {
            "equipamento": self.equipamento.text(),
            "ponto": self.ponto.text(),
            "lubrificante": self.lubrificante.currentText(),
            "periodicidade": self.periodicidade.value(),
            "quantidade": self.quantidade.value(),
            "responsavel": self.responsavel.text()
        }
        self._atualizar_tabela()
        self._limpar_formulario()
        self.linha_selecionada = -1

    def remover_linha(self):
        if self.linha_selecionada < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma linha para remover.")
            return
        self.dados_lubrificacao.pop(self.linha_selecionada)
        self._atualizar_tabela()
        self._limpar_formulario()
        self.linha_selecionada = -1

    def salvar_arquivo(self):
        if not self.dados_lubrificacao:
            QMessageBox.warning(self, "Aviso", "Não há dados para salvar.")
            return
        caminho, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo", "", "JSON (*.json)")
        if caminho:
            with open(caminho, "w", encoding="utf-8") as f:
                json.dump(self.dados_lubrificacao, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Sucesso", f"Dados salvos em {caminho}")

    def carregar_arquivo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Carregar arquivo", "", "JSON (*.json)")
        if caminho:
            with open(caminho, "r", encoding="utf-8") as f:
                self.dados_lubrificacao = json.load(f)
            self._atualizar_tabela()
            QMessageBox.information(self, "Sucesso", "Dados carregados com sucesso.")


# ==================== CÁLCULO DE HORAS TRABALHADAS (CLT e NR-16) ====================

class CalculoHoras(QWidget):
    """
    Calculadora de horas trabalhadas conforme CLT e NR-16 (insalubridade/periculosidade).
    Base legal: CLT arts. 58 a 75[reference:9] e NR-16 (adicional de periculosidade)[reference:10]
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("⏱️ Cálculo de Horas Trabalhadas - Legislação Trabalhista ⏱️")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
        layout.addWidget(titulo)

        normas = QLabel("Baseado em: CLT (arts. 58-75) | NR-16 (insalubridade/periculosidade)")
        normas.setAlignment(Qt.AlignCenter)
        normas.setStyleSheet("font-size: 10px; color: gray; margin-bottom: 10px;")
        layout.addWidget(normas)

        # Entrada de dados
        form_group = QGroupBox("Dados da jornada")
        form_layout = QGridLayout()
        form_group.setLayout(form_layout)

        form_layout.addWidget(QLabel("Salário base (R$):"), 0, 0)
        self.salario = QLineEdit()
        self.salario.setPlaceholderText("Ex: 2500.00")
        form_layout.addWidget(self.salario, 0, 1)

        form_layout.addWidget(QLabel("Horas trabalhadas por dia:"), 1, 0)
        self.horas_dia = QDoubleSpinBox()
        self.horas_dia.setRange(0, 24)
        self.horas_dia.setSingleStep(0.5)
        self.horas_dia.setValue(8)
        form_layout.addWidget(self.horas_dia, 1, 1)

        form_layout.addWidget(QLabel("Dias trabalhados no mês:"), 2, 0)
        self.dias_mes = QSpinBox()
        self.dias_mes.setRange(0, 31)
        self.dias_mes.setValue(22)
        form_layout.addWidget(self.dias_mes, 2, 1)

        form_layout.addWidget(QLabel("Adicional noturno (20%):"), 3, 0)
        self.noturno = QComboBox()
        self.noturno.addItems(["Não", "Sim"])
        form_layout.addWidget(self.noturno, 3, 1)

        form_layout.addWidget(QLabel("Adicional de periculosidade (30% - NR-16):"), 4, 0)
        self.periculosidade = QComboBox()
        self.periculosidade.addItems(["Não", "Sim"])
        form_layout.addWidget(self.periculosidade, 4, 1)

        form_layout.addWidget(QLabel("Horas extras (50% adicional):"), 5, 0)
        self.horas_extras = QDoubleSpinBox()
        self.horas_extras.setRange(0, 100)
        self.horas_extras.setSuffix(" h")
        form_layout.addWidget(self.horas_extras, 5, 1)

        layout.addWidget(form_group)

        # Botão calcular
        self.btn_calcular = QPushButton("Calcular Remuneração")
        self.btn_calcular.clicked.connect(self.calcular)
        layout.addWidget(self.btn_calcular)

        # Resultado
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        layout.addWidget(self.resultado)

        # Observação legal
        obs = QLabel("📌 Conforme CLT, jornada normal máxima de 8h/dia ou 44h/semana. Adicional noturno (20%) para trabalho entre 22h e 5h[reference:11]. Periculosidade (30%) conforme NR-16 anexo 4[reference:12].")
        obs.setWordWrap(True)
        obs.setStyleSheet("font-size: 10px; margin-top: 8px;")
        layout.addWidget(obs)

        self.setLayout(layout)

    def calcular(self):
        try:
            salario = float(self.salario.text())
        except:
            QMessageBox.warning(self, "Erro", "Informe um salário válido.")
            return

        horas_dia = self.horas_dia.value()
        dias = self.dias_mes.value()
        horas_normais = horas_dia * dias
        valor_hora = salario / (220.0 if horas_dia <= 8 else horas_dia * dias)

        # Base
        total = salario

        # Adicional noturno (20% sobre o valor da hora)[reference:13]
        if self.noturno.currentText() == "Sim":
            adicional_noturno = valor_hora * horas_normais * 0.20
            total += adicional_noturno
        else:
            adicional_noturno = 0

        # Periculosidade (30% sobre o salário base)[reference:14]
        if self.periculosidade.currentText() == "Sim":
            periculosidade = salario * 0.30
            total += periculosidade
        else:
            periculosidade = 0

        # Horas extras (50% sobre valor da hora)
        horas_extra = self.horas_extras.value()
        adicional_extra = valor_hora * 0.50 * horas_extra
        total += adicional_extra

        self.resultado.setText(
            f"📊 Resumo da Remuneração\n"
            f"{'='*40}\n"
            f"Salário base:          R$ {salario:,.2f}\n"
            f"Horas trabalhadas:      {horas_normais:.1f} h\n"
            f"Valor da hora normal:   R$ {valor_hora:.2f}\n"
            f"\n▶️ Adicional noturno (20%):    R$ {adicional_noturno:,.2f}\n"
            f"▶️ Periculosidade (30%):        R$ {periculosidade:,.2f}\n"
            f"▶️ Horas extras (50%):          R$ {adicional_extra:,.2f}\n"
            f"{'='*40}\n"
            f"✅ TOTAL LÍQUIDO (estimado): R$ {total:,.2f}\n"
            f"{'='*40}\n\n"
            f"Legislação aplicada: CLT arts. 58 a 75 e NR-16 (Anexo 4)."
        )


# ==================== CONVERSOR DE PRESSÃO (NBR IEC e SI) ====================

class ConversorPressao(QWidget):
    """
    Conversor de unidades de pressão entre psi, bar, kPa, MPa e kgf/cm².
    Utiliza fatores de conversão comuns e respeita as unidades do Sistema Internacional (SI)[reference:15].
    """
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        titulo = QLabel("📊 Conversor de Pressão - Sistema Internacional (SI) 📊")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
        layout.addWidget(titulo)

        normas = QLabel("Baseado em: Sistema Internacional de Unidades (SI) - Portaria Inmetro 615/2023[reference:16]")
        normas.setAlignment(Qt.AlignCenter)
        normas.setStyleSheet("font-size: 10px; color: gray; margin-bottom: 10px;")
        layout.addWidget(normas)

        # Entrada
        layout.addWidget(QLabel("Valor a converter:"))
        self.valor = QLineEdit()
        layout.addWidget(self.valor)

        # Unidade de origem
        layout.addWidget(QLabel("Unidade de origem:"))
        self.de_unidade = QComboBox()
        self.de_unidade.addItems(["psi (lbf/in²)", "bar", "kPa", "MPa", "kgf/cm²"])
        layout.addWidget(self.de_unidade)

        # Unidade de destino
        layout.addWidget(QLabel("Unidade de destino:"))
        self.para_unidade = QComboBox()
        self.para_unidade.addItems(["psi (lbf/in²)", "bar", "kPa", "MPa", "kgf/cm²"])
        layout.addWidget(self.para_unidade)

        # Botão converter
        self.btn_converter = QPushButton("Converter")
        self.btn_converter.clicked.connect(self.converter)
        layout.addWidget(self.btn_converter)

        # Resultado
        self.resultado = QLabel("Resultado: ---")
        self.resultado.setStyleSheet("font-weight: bold; font-size: 14px; margin: 10px;")
        layout.addWidget(self.resultado)

        # Fatores de conversão
        layout.addWidget(QLabel("📐 Fatores de referência:"))
        info = QLabel("1 bar = 100 kPa = 0,1 MPa = 14,5038 psi = 1,01972 kgf/cm²")
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 10px; background-color: #f0f0f0; padding: 5px;")
        layout.addWidget(info)

        self.setLayout(layout)

    def converter(self):
        try:
            valor = float(self.valor.text())
        except:
            QMessageBox.warning(self, "Erro", "Digite um valor numérico.")
            return

        de = self.de_unidade.currentText()
        para = self.para_unidade.currentText()

        # Fatores de conversão para bar (como base)
        fatores = {
            "psi (lbf/in²)": 1 / 14.5038,   # 1 psi = 0.0689476 bar
            "bar": 1.0,
            "kPa": 0.001,                    # 1 kPa = 0.001 bar
            "MPa": 10.0,                     # 1 MPa = 10 bar
            "kgf/cm²": 0.980665              # 1 kgf/cm² ≈ 0.980665 bar
        }

        # Converter para bar
        em_bar = valor * fatores[de]

        # Converter de bar para unidade destino
        fatores_inv = {k: 1/f for k, f in fatores.items()}
        resultado = em_bar * fatores_inv[para]

        self.resultado.setText(f"Resultado: {valor:.4f} {de} = {resultado:.6f} {para}")


# ==================== JANELA PRINCIPAL COM ABAS ====================

class SuiteFerramentas(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏭 Suíte de Manutenção Industrial - Normas Técnicas 🏭")
        self.setGeometry(200, 200, 780, 600)

        self.addTab(CalculadoraEletrica(), "⚡ Elétrica (NBR/IEC/NR)")
        self.addTab(TabelaLubrificacao(), "🛢️ Lubrificação (NBR 15594)")
        self.addTab(CalculoHoras(), "⏱️ Horas Trabalhadas (CLT/NR)")
        self.addTab(ConversorPressao(), "📊 Conversor de Pressão (SI)")

        # Aplicar estilo global
        self.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #ccc; background: #fafafa; }
            QTabBar::tab { background: #e0e0e0; padding: 8px 16px; margin-right: 2px; }
            QTabBar::tab:selected { background: #4CAF50; color: white; }
            QPushButton { background-color: #2196F3; color: white; border: none; padding: 6px; border-radius: 4px; }
            QPushButton:hover { background-color: #0b7dda; }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox { padding: 4px; border: 1px solid #ccc; border-radius: 3px; }
        """)


# ==================== EXECUÇÃO ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ferramentas = SuiteFerramentas()
    ferramentas.show()
    sys.exit(app.exec_())