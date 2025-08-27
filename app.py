import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from create_boleto import GeradorBoleto
from re import fullmatch

app = FastAPI()

@app.get('/boletos')
async def get_boleto(name: str, value: int, vencimento: str):
    print(name, value, vencimento)
    if not bool(fullmatch(r'^[\d]{2}/[\d]{2}/[\d]{4}$', vencimento)):
        return JSONResponse(status_code=400, content={"msg": "vencimento invalido favor informa no formato DD/MM/AAAA"})
    boleto = GeradorBoleto(name, value, vencimento)
    base64 = boleto.criar_boleto_base64()

    if base64:
        return JSONResponse({'base64': base64}, status_code=200)
    return {"error": "Arquivo não encontrado"}

