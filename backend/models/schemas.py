from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class Composition(BaseModel):
    SiO2: float
    Al2O3: float
    Na2O: float
    K2O: float
    CaO: float
    MgO: float
    Others: float

class ProcessParams(BaseModel):
    melting_temp: int
    holding_time: float
    annealing_temp: int

class TestItem(BaseModel):
    item: str
    result: str
    unit: str

class Recipe(BaseModel):
    recipe_id: str
    name: str
    created_at: str
    created_by: str
    status: str
    composition: Composition
    process_params: ProcessParams
    notes: Optional[str] = ""
    test_results: Optional[List[TestItem]] = []

class RecipeCreate(BaseModel):
    name: str
    created_by: str
    composition: Composition
    process_params: ProcessParams
    notes: Optional[str] = ""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class Source(BaseModel):
    content: str
    source: str
    page: Optional[int] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: float

class RecommendRequest(BaseModel):
    thermal_expansion: Optional[float] = None
    density: Optional[float] = None
    bending_strength: Optional[float] = None
    heat_resistance: Optional[float] = None

class RecommendResult(BaseModel):
    recipe_id: str
    name: str
    confidence: float
    composition: Dict[str, float]
    predicted_properties: Dict[str, str]
    history_count: int
