from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContractAnalysis(BaseModel):
    tipo_fluxo: Optional[str]
    valor_contrato: Optional[float]
    valor_pagamento: Optional[float]
    localizacao: Optional[str]
    data_vencimento_contrato: Optional[str]
    data_vencimento_pagamento: Optional[str]
    area_responsavel: Optional[str]
    multa: Optional[float]
    risco: Optional[str]
    confianca: Optional[float]
    observacoes: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "tipo_fluxo": "RE",
                "valor_contrato": 100000.00,
                "valor_pagamento": 8333.33,
                "localizacao": "São Paulo, SP",
                "data_vencimento_contrato": "2024-12-31",
                "data_vencimento_pagamento": "2023-10-05",
                "area_responsavel": "Departamento Jurídico",
                "multa": 10.0,
                "risco": "Médio",
                "confianca": 0.85,
                "observacoes": "Contrato de locação comercial"
            }
        }