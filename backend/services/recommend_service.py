from typing import List, Dict, Optional
import re

class RecommendService:
    def __init__(self, recipe_service):
        self.recipe_service = recipe_service
    
    def recommend(self, target_properties: Dict) -> List[Dict]:
        recipes = self.recipe_service.list_recipes()
        
        scored_recipes = []
        for recipe in recipes:
            if recipe.get('status') != '已测试':
                continue
            
            test_results = recipe.get('test_results', [])
            if not test_results:
                continue
            
            latest_test = test_results[-1] if test_results else {}
            test_items = latest_test.get('test_items', [])
            
            properties = self._parse_test_items(test_items)
            
            score = self._calculate_score(target_properties, properties)
            
            if score > 0:
                scored_recipes.append({
                    "recipe_id": recipe['recipe_id'],
                    "name": recipe['name'],
                    "confidence": round(score, 2),
                    "composition": recipe.get('composition', {}),
                    "predicted_properties": properties,
                    "history_count": len(test_results)
                })
        
        scored_recipes.sort(key=lambda x: x['confidence'], reverse=True)
        
        return scored_recipes[:3]
    
    def _parse_test_items(self, test_items: List[Dict]) -> Dict[str, float]:
        properties = {}
        
        for item in test_items:
            name = item.get('item', '')
            result = item.get('result', '')
            
            if '热膨胀' in name:
                match = re.search(r'[\d.]+', result)
                if match:
                    properties['thermal_expansion'] = float(match.group())
            
            elif '密度' in name:
                match = re.search(r'[\d.]+', result)
                if match:
                    properties['density'] = float(match.group())
            
            elif '抗弯' in name:
                match = re.search(r'[\d.]+', result)
                if match:
                    properties['bending_strength'] = float(match.group())
            
            elif '耐热' in name:
                match = re.search(r'[\d.]+', result)
                if match:
                    properties['heat_resistance'] = float(match.group())
        
        return properties
    
    def _calculate_score(self, target: Dict, actual: Dict) -> float:
        score = 0.0
        count = 0
        
        if target.get('thermal_expansion'):
            target_val = target['thermal_expansion']
            actual_val = actual.get('thermal_expansion', 0)
            if actual_val > 0:
                diff = abs(target_val - actual_val)
                item_score = max(0, 1 - diff / target_val)
                score += item_score
                count += 1
        
        if target.get('density'):
            target_val = target['density']
            actual_val = actual.get('density', 0)
            if actual_val > 0:
                diff = abs(target_val - actual_val)
                item_score = max(0, 1 - diff / target_val)
                score += item_score
                count += 1
        
        if target.get('bending_strength'):
            target_val = target['bending_strength']
            actual_val = actual.get('bending_strength', 0)
            if actual_val > 0:
                if actual_val >= target_val:
                    item_score = 1.0
                else:
                    item_score = actual_val / target_val
                score += item_score
                count += 1
        
        if target.get('heat_resistance'):
            target_val = target['heat_resistance']
            actual_val = actual.get('heat_resistance', 0)
            if actual_val > 0:
                if actual_val >= target_val:
                    item_score = 1.0
                else:
                    item_score = actual_val / target_val
                score += item_score
                count += 1
        
        return score / count if count > 0 else 0
    
    def get_similar_recipes(self, recipe_id: str, top_k: int = 3) -> List[Dict]:
        target_recipe = self.recipe_service.get_recipe(recipe_id)
        if not target_recipe:
            return []
        
        target_composition = target_recipe.get('composition', {})
        
        all_recipes = self.recipe_service.list_recipes()
        scored = []
        
        for recipe in all_recipes:
            if recipe['recipe_id'] == recipe_id:
                continue
            
            composition = recipe.get('composition', {})
            similarity = self._composition_similarity(target_composition, composition)
            
            if similarity > 0.5:
                scored.append({
                    "recipe_id": recipe['recipe_id'],
                    "name": recipe['name'],
                    "similarity": round(similarity, 2)
                })
        
        scored.sort(key=lambda x: x['similarity'], reverse=True)
        return scored[:top_k]
    
    def _composition_similarity(self, comp1: Dict, comp2: Dict) -> float:
        keys = ['SiO2', 'Al2O3', 'Na2O', 'K2O', 'CaO', 'MgO']
        
        total_diff = 0
        for key in keys:
            val1 = comp1.get(key, 0)
            val2 = comp2.get(key, 0)
            total_diff += abs(val1 - val2)
        
        max_diff = len(keys) * 100
        similarity = 1 - (total_diff / max_diff)
        
        return max(0, similarity)
