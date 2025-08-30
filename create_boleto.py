from PIL import Image, ImageDraw, ImageFont
import io
import base64
from datetime import datetime
from random import randint


class GeradorBoletoImagem:
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

    def criar_boleto_imagem(self, formato='PNG'):
        # Criar imagem com tamanho similar a A4 (595x842 pixels em 72 DPI)
        width, height = 595, 842
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)

        # Tentar carregar fontes
        try:
            # Para Windows
            font_bold_large = ImageFont.truetype("arialbd.ttf", 20)
            font_bold = ImageFont.truetype("arialbd.ttf", 14)
            font_normal = ImageFont.truetype("arial.ttf", 12)
            font_small = ImageFont.truetype("arial.ttf", 10)
            font_code = ImageFont.truetype("cour.ttf", 10)
        except:
            try:
                # Para Linux/Mac
                font_bold_large = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
                font_bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 14)
                font_normal = ImageFont.truetype("DejaVuSans.ttf", 12)
                font_small = ImageFont.truetype("DejaVuSans.ttf", 10)
                font_code = ImageFont.truetype("DejaVuSansMono.ttf", 10)
            except:
                # Fallback para fontes básicas (tamanhos ajustados)
                font_bold_large = ImageFont.load_default()
                font_bold = ImageFont.load_default()
                font_normal = ImageFont.load_default()
                font_small = ImageFont.load_default()
                font_code = ImageFont.load_default()

        # Posições iniciais (agora começando de cima para baixo)
        x, y = 50, 50
        line_height = 20
        section_spacing = 10

        # Título (CENTRALIZADO)
        titulo = "BOLETO BANCÁRIO FICTÍCIO"
        titulo_width = draw.textlength(titulo, font=font_bold_large)
        draw.text(((width - titulo_width) // 2, y), titulo, fill='black', font=font_bold_large)
        y += line_height * 2

        # Linha separadora
        draw.line([x, y, width - x, y], fill='black', width=1)
        y += section_spacing

        # Beneficiário
        draw.text((x, y), "Beneficiário: Banco Fictício S.A.", fill='black', font=font_bold)
        y += line_height
        draw.text((x, y), "Agência: 0001-9 / Conta: 0101010-1", fill='black', font=font_normal)
        y += line_height
        draw.text((x, y), "CNPJ: 00.000.000/0001-00", fill='black', font=font_normal)
        y += line_height * 2

        # Linha separadora
        draw.line([x, y, width - x, y], fill='black', width=1)
        y += section_spacing

        # Linha digitável
        linha_digitavel = self.gerar_linha_digitavel()
        draw.text((x, y), "Linha Digitável:", fill='black', font=font_bold)
        y += line_height
        draw.text((x, y), linha_digitavel, fill='black', font=font_code)
        y += line_height * 2

        # Linha separadora
        draw.line([x, y, width - x, y], fill='black', width=1)
        y += section_spacing

        # Dados do pagador
        draw.text((x, y), "DADOS DO PAGADOR", fill='black', font=font_bold)
        y += line_height
        draw.text((x, y), f"Nome: {self.nome}", fill='black', font=font_normal)
        y += line_height * 2

        # Linha separadora
        draw.line([x, y, width - x, y], fill='black', width=1)
        y += section_spacing

        # Informações de pagamento
        draw.text((x, y), "INFORMAÇÕES DE PAGAMENTO", fill='black', font=font_bold)
        y += line_height
        draw.text((x, y), f"Data de Emissão: {self.data_emissao}", fill='black', font=font_normal)
        y += line_height
        draw.text((x, y), f"Data de Vencimento: {self.data_vencimento}", fill='black', font=font_normal)
        y += line_height
        draw.text((x, y), f"Valor do Documento: {self.formatar_valor()}", fill='black', font=font_normal)
        y += line_height
        draw.text((x, y), f"Número do Documento: {self.numero_documento}", fill='black', font=font_normal)
        y += line_height * 2

        # Linha separadora
        draw.line([x, y, width - x, y], fill='black', width=1)
        y += section_spacing

        # Código de barras
        draw.text((x, y), "CÓDIGO DE BARRAS:", fill='black', font=font_bold)
        y += line_height
        draw.text((x, y), self.codigo_barras, fill='black', font=font_code)
        y += line_height * 2

        # Linha separadora
        draw.line([x, y, width - x, y], fill='black', width=1)
        y += section_spacing

        # Instruções
        draw.text((x, y), "INSTRUÇÕES:", fill='black', font=font_bold)
        y += line_height
        draw.text((x, y), "- Pagável em qualquer banco até o vencimento", fill='black', font=font_small)
        y += line_height
        draw.text((x, y), "- Após o vencimento, pagar apenas no Banco Fictício S.A.", fill='black', font=font_small)
        y += line_height
        draw.text((x, y), "- Não receber após 30 dias do vencimento", fill='black', font=font_small)
        y += line_height

        # Rodapé (centralizado na parte inferior)
        rodape = "Este é um boleto fictício para fins de demonstração."
        rodape_width = draw.textlength(rodape, font=font_small)
        draw.text(((width - rodape_width) // 2, height - 40), rodape, fill='gray', font=font_small)

        # Adicionar borda ao redor do boleto
        draw.rectangle([20, 20, width - 20, height - 20], outline='black', width=2)

        # Salvar em buffer
        buffer = io.BytesIO()
        if formato.upper() == 'JPG':
            img.save(buffer, format='JPEG', quality=75, optimize=True)
        else:
            img.save(buffer, format='PNG', optimize=True)

        buffer.seek(0)

        # Converter para base64
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return img_base64

    def salvar_imagem(self, filename='boleto.png'):
        """Método auxiliar para salvar a imagem diretamente"""
        img_data = self.criar_boleto_imagem()
        formato = filename.split('.')[-1].upper()

        if formato not in ['PNG', 'JPG', 'JPEG']:
            formato = 'PNG'
            filename = 'boleto.png'

        with open(filename, 'wb') as f:
            f.write(base64.b64decode(img_data))
        print(f"Imagem salva como '{filename}'")


if __name__ == "__main__":
    boleto = GeradorBoletoImagem('Marcelo Silva', 300.50, '29/08/2025')

    # Obter imagem em base64
    imagem_base64 = boleto.criar_boleto_imagem()
    print("Imagem gerada com sucesso!")

    # Salvar a imagem
    boleto.salvar_imagem('boleto.png')