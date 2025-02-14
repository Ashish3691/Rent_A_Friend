from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def activate_sos(user_id: str, location: dict):
    """
    SOS Button endpoint:
    When activated, connects the user to support and alerts saved emergency contacts with live location.
    """
    # Implement actual SOS logic or integration with notification services here.
    return {"message": f"SOS activated for user {user_id} at location {location}"}
