from fastapi import APIRouter, HTTPException
from typing import List
from backend.models.schemas import RecommendRequest, RecommendResult
from backend.services.recipe_service import RecipeService
from backend.services.recommend_service import RecommendService

router = APIRouter(prefix="/api/recommend", tags=["recommend"])

recipe_service = None
recommend_service = None

def get_services():
    global recipe_service, recommend_service
    if recipe_service is None:
        recipe_service = RecipeService()
    if recommend_service is None:
        recommend_service = RecommendService(recipe_service)
    return recipe_service, recommend_service

@router.post("", response_model=List[RecommendResult])
async def recommend(request: RecommendRequest):
    _, recommend_svc = get_services()
    
    target_properties = {}
    if request.thermal_expansion:
        target_properties['thermal_expansion'] = request.thermal_expansion
    if request.density:
        target_properties['density'] = request.density
    if request.bending_strength:
        target_properties['bending_strength'] = request.bending_strength
    if request.heat_resistance:
        target_properties['heat_resistance'] = request.heat_resistance
    
    if not target_properties:
        raise HTTPException(status_code=400, detail="请至少提供一个目标性能指标")
    
    results = recommend_svc.recommend(target_properties)
    
    return results

@router.get("/similar/{recipe_id}")
async def get_similar(recipe_id: str, top_k: int = 3):
    _, recommend_svc = get_services()
    
    similar = recommend_svc.get_similar_recipes(recipe_id, top_k)
    return {"similar_recipes": similar}
