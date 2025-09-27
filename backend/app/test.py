from fastapi import APIRouter

router = APIRouter()

@router.get("/1")
async def test_health() -> dict[str, str]:
    print("Health")
    return {"message": "Healthy"}
