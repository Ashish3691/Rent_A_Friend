from fastapi import APIRouter, HTTPException
from services import verification_service

router = APIRouter()

@router.post("/")
def verify_user(pan: str, aadhar: str, driving_license: str, facial_data: str):
    """
    Four step verification:
      1. PAN/AADHAR check
      2. Driving License verification
      3. Facial Recognition check
      4. Matching of PAN/AADHAR with the person
    """
    result = verification_service.verify(pan, aadhar, driving_license, facial_data)
    if result["verified"]:
        return {"message": "User verified successfully"}
    raise HTTPException(status_code=400, detail="Verification failed")
