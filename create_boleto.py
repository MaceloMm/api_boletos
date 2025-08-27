from fpdf import FPDF
from datetime import datetime
import base64
import io
from random import randint


class GeradorBoleto:
    def __init__(self, nome, valor, data_vencimento):
        self.nome = nome
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.data_emissao = datetime.now().strftime("%d/%m/%Y")
        self.numero_documento = self.gerar_numero_documento()
        self.codigo_barras = self.gerar_codigo_barras()

    def gerar_numero_documento(self):
        return str(randint(100000000, 999999999))

    def gerar_codigo_barras(self):
        return str(randint(100000000000000000000000000000000000000, 999999999999999999999999999999999999999))

    def formatar_valor(self):
        return f"R$ {float(self.valor):.2f}".replace('.', ',')

    def gerar_linha_digitavel(self):
        parte1 = randint(10000, 99999)
        parte2 = randint(10000, 99999)
        parte3 = randint(10000, 99999)
        parte4 = randint(10000, 99999)
        parte5 = randint(10000, 99999)
        parte6 = randint(100, 999)

        return f"{parte1}.{parte2} {parte3}.{parte4} {parte5}.{parte6} {randint(0, 9)} {self.codigo_barras[:14]}"

    def criar_boleto_base64(self):
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()

        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_fill_color(240, 240, 240)

        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Boleto Bancário Fictício', 0, 1, 'C')
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Beneficiário: Banco Fictício S.A.', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, 'Agência: 0001-9 / Conta: 0101010-1', 0, 1)
        pdf.cell(0, 8, 'CNPJ: 00.000.000/0001-00', 0, 1)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 14)
        linha_digitavel = self.gerar_linha_digitavel()
        pdf.cell(0, 10, f'Linha Digitável: {linha_digitavel}', 0, 1)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Dados do Pagador', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f'Nome: {self.nome}', 0, 1)
        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, 'Informações de Pagamento', 0, 1)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 8, f'Data de Emissão: {self.data_emissao}', 0, 1)
        pdf.cell(0, 8, f'Data de Vencimento: {self.data_vencimento}', 0, 1)
        pdf.cell(0, 8, f'Valor do Documento: {self.formatar_valor()}', 0, 1)
        pdf.cell(0, 8, f'Número do Documento: {self.numero_documento}', 0, 1)
        pdf.ln(10)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 8, 'Código de Barras:', 0, 1)
        pdf.set_font('Courier', '', 10)
        pdf.multi_cell(0, 5, self.codigo_barras)
        pdf.ln(5)

        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 8, 'Instruções:', 0, 1)
        pdf.multi_cell(0, 5, '- Pagável em qualquer banco até o vencimento')
        pdf.multi_cell(0, 5, '- Após o vencimento, pagar apenas no Banco Fictício S.A.')
        pdf.multi_cell(0, 5, '- Não receber após 30 dias do vencimento')
        pdf.ln(5)

        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 5, 'Este é um boleto fictício para fins de demonstração.', 0, 1, 'C')

        # Salvar o PDF em memória e converter para base64
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        return pdf_base64


if __name__ == "__main__":
    boleto = GeradorBoleto('macelo', 300, '29/08/2025')
    base64_string = boleto.criar_boleto_base64()
    print("PDF em base64:")
    print(base64_string)
    with open("boleto_base64.txt", "w") as f:
        f.write(base64_string)
    print("\nBase64 salvo em 'boleto_base64.txt'")