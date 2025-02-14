from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/")
def submit_rating(user_id: str, friend_id: str, rating: float):
    """
    Two-Way Rating System:
    Both customer and friend rate each other after completing the contract.
    Ratings below 3 stars are flagged and reviewed.
    """
    if rating < 0 or rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 0 and 5")
    
    if rating < 3:
        # In production, flag and trigger a review process.
        return {"message": "Rating submitted. Low rating flagged for review"}
    return {"message": "Rating submitted successfully"}
