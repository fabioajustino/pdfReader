import os
import PyPDF2
import pdfplumber
import re
from typing import Dict, Any
from fastapi import UploadFile
import openai
from core.config import get_settings

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY


class ContractAnalyzerService:
    def __init__(self):
        self.settings = get_settings()
    
    async def analyze_contract(self, file: UploadFile) -> Dict[str, Any]:
        """
        Analyze a contract PDF file and extract relevant information.
        """
        # Extract text from PDF
        text = await self._extract_text(file)
        
        # Analyze text and extract information
        result = await self._analyze_text(text)
        
        return result
    
    async def _extract_text(self, file: UploadFile) -> str:
        """
        Extract text from PDF using both PyPDF2 and pdfplumber for better accuracy.
        """
        content = await file.read()
        temp_path = f"temp_{file.filename}"
        
        try:
            # Save temporary file
            with open(temp_path, "wb") as temp_file:
                temp_file.write(content)
            
            text = ""
            
            # Try with PyPDF2 first
            with open(temp_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            # If PyPDF2 fails or returns empty text, try with pdfplumber
            if not text.strip():
                with pdfplumber.open(temp_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            
            return text
        
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    async def _analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze the extracted text using regex patterns and AI assistance.
        """
        result = {
            "tipo_fluxo": self._extract_tipo_fluxo(text),
            "valor_contrato": self._extract_valor(text, "contrato"),
            "valor_pagamento": self._extract_valor(text, "pagamento"),
            "localizacao": self._extract_localizacao(text),
            "data_vencimento_contrato": self._extract_data(text, "contrato"),
            "data_vencimento_pagamento": self._extract_data(text, "pagamento"),
            "area_responsavel": self._extract_area_responsavel(text),
            "multa": self._extract_multa(text),
            "risco": self._analyze_risco(text),
            "confianca": 0.85,  # Default confidence score
            "observacoes": self._generate_observacoes(text)
        }
        
        return result
    
    def _extract_tipo_fluxo(self, text: str) -> str:
        tipos = {
            "RE": r"real\s*estate|RE",
            "FI": r"FI|fundo\s*de\s*investimento",
            "Proposta": r"proposta",
            "Engenharia": r"engenharia",
            "RC": r"RC|responsabilidade\s*civil"
        }
        
        for tipo, pattern in tipos.items():
            if re.search(pattern, text, re.IGNORECASE):
                return tipo
        return None
    
    def _extract_valor(self, text: str, tipo: str) -> float:
        pattern = r"R\$\s*([\d.,]+)"
        matches = re.findall(pattern, text)
        if matches:
            # Convert string to float, handling Brazilian number format
            valor_str = matches[0].replace(".", "").replace(",", ".")
            return float(valor_str)
        return None
    
    def _extract_localizacao(self, text: str) -> str:
        # Basic pattern for Brazilian addresses
        pattern = r"(?i)(?:Rua|Av\.|Avenida|Alameda|Al\.|Praça)\s[^,\n]+,?\s*n°?\s*\d+[^,\n]*(?:,\s*[^,\n]+)*"
        match = re.search(pattern, text)
        if match:
            return match.group(0)
        return None
    
    def _extract_data(self, text: str, tipo: str) -> str:
        # Pattern for different date formats
        patterns = [
            r"\d{2}/\d{2}/\d{4}",
            r"\d{4}-\d{2}-\d{2}",
            r"\d{2}-\d{2}-\d{4}"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]  # Return the first found date
        return None
    
    def _extract_area_responsavel(self, text: str) -> str:
        patterns = [
            r"(?i)departamento\s+de\s+([^.,\n]+)",
            r"(?i)setor\s+de\s+([^.,\n]+)",
            r"(?i)gerência\s+de\s+([^.,\n]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
    
    def _extract_multa(self, text: str) -> float:
        pattern = r"(?i)multa\s*de\s*(\d+(?:,\d+)?)\s*%"
        match = re.search(pattern, text)
        if match:
            return float(match.group(1).replace(",", "."))
        return None
    
    def _analyze_risco(self, text: str) -> str:
        # Simple risk analysis based on keywords
        risk_indicators = {
            "Alto": ["inadimplência", "rescisão", "processo judicial", "multa alta"],
            "Médio": ["atraso", "pendência", "alteração"],
            "Baixo": ["regular", "em dia", "conforme"],
            "Crítico": ["urgente", "grave", "crítico", "emergencial"]
        }
        
        text_lower = text.lower()
        for risk, keywords in risk_indicators.items():
            if any(keyword.lower() in text_lower for keyword in keywords):
                return risk
        return "Médio"  # Default risk level
    
    def _generate_observacoes(self, text: str) -> str:
        # Use OpenAI to generate observations if API key is available
        if settings.OPENAI_API_KEY:
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Analyze this contract text and provide key observations in Portuguese:\n\n{text[:1000]}...",
                    max_tokens=150,
                    temperature=0.3
                )
                return response.choices[0].text.strip()
            except Exception:
                pass
        
        # Fallback to basic extraction
        return "Análise automática - observações não disponíveis"