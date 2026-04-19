from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.models.schemas import Recipe, RecipeCreate
from backend.services.recipe_service import RecipeService

router = APIRouter(prefix="/api/recipes", tags=["recipes"])

recipe_service = None

def get_recipe_service():
    global recipe_service
    if recipe_service is None:
        recipe_service = RecipeService()
    return recipe_service

@router.get("")
async def list_recipes(
    status: Optional[str] = Query(None, description="按状态筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索")
):
    service = get_recipe_service()
    recipes = service.list_recipes(status=status, keyword=keyword)
    return {"recipes": recipes, "total": len(recipes)}

@router.get("/statistics")
async def get_statistics():
    service = get_recipe_service()
    stats = service.get_statistics()
    return stats

@router.get("/{recipe_id}")
async def get_recipe(recipe_id: str):
    service = get_recipe_service()
    recipe = service.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="配方不存在")
    return recipe

@router.post("")
async def create_recipe(recipe: RecipeCreate):
    service = get_recipe_service()
    new_recipe = service.create_recipe(recipe.dict())
    return new_recipe

@router.put("/{recipe_id}")
async def update_recipe(recipe_id: str, recipe_data: dict):
    service = get_recipe_service()
    updated = service.update_recipe(recipe_id, recipe_data)
    if not updated:
        raise HTTPException(status_code=404, detail="配方不存在")
    return updated

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: str):
    service = get_recipe_service()
    success = service.delete_recipe(recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="配方不存在")
    return {"message": "删除成功"}

@router.post("/{recipe_id}/tests")
async def add_test_result(recipe_id: str, test_data: dict):
    service = get_recipe_service()
    recipe = service.get_recipe(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="配方不存在")
    
    new_test = service.add_test_result(recipe_id, test_data)
    return new_test
