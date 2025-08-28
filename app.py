import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response
from create_boleto import GeradorBoletoImagem  # Importe a nova classe
from re import fullmatch
import base64

app = FastAPI()


@app.get('/boletos')
async def get_boleto(name: str, value: float, vencimento: str):
    print(name, value, vencimento)

    # Validação do formato da data
    if not bool(fullmatch(r'^[\d]{2}/[\d]{2}/[\d]{4}$', vencimento)):
        return JSONResponse(
            status_code=400,
            content={"msg": "vencimento invalido favor informa no formato DD/MM/AAAA"}
        )

    # Validação do valor
    if value <= 0:
        return JSONResponse(
            status_code=400,
            content={"msg": "valor deve ser maior que zero"}
        )

    # Cria o boleto como imagem
    boleto = GeradorBoletoImagem(name, value, vencimento)
    imagem_base64 = boleto.criar_boleto_imagem()

    if imagem_base64:
        return JSONResponse(
            {
                'base64': imagem_base64,
                'formato': 'image/png',
                'nome_arquivo': f'boleto_{name.replace(" ", "_")}.png'
            },
            status_code=200
        )

    return JSONResponse(
        status_code=500,
        content={"error": "Erro ao gerar o boleto"}
    )