from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .services import ContractAnalyzerService
from .schemas import ContractAnalysis

router = APIRouter(prefix="/contracts", tags=["contracts"])
contract_service = ContractAnalyzerService()


@router.post("/analyze", response_model=ContractAnalysis)
async def analyze_contract(file: UploadFile = File(...)):
    """
    Endpoint to analyze a contract PDF file and extract relevant information.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        result = await contract_service.analyze_contract(file)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))