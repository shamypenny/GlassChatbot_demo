import json
import os
from typing import List, Optional, Dict
from datetime import datetime
import uuid

class RecipeService:
    def __init__(self, data_path: str = "./demo_data"):
        self.data_path = data_path
        self.recipes_file = os.path.join(data_path, "recipes.json")
        self.tests_file = os.path.join(data_path, "test_results.json")
        self._recipes = self._load_recipes()
        self._tests = self._load_tests()
    
    def _load_recipes(self) -> List[Dict]:
        if os.path.exists(self.recipes_file):
            with open(self.recipes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _load_tests(self) -> List[Dict]:
        if os.path.exists(self.tests_file):
            with open(self.tests_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _save_recipes(self):
        with open(self.recipes_file, 'w', encoding='utf-8') as f:
            json.dump(self._recipes, f, ensure_ascii=False, indent=2)
    
    def _save_tests(self):
        with open(self.tests_file, 'w', encoding='utf-8') as f:
            json.dump(self._tests, f, ensure_ascii=False, indent=2)
    
    def list_recipes(self, status: Optional[str] = None, keyword: Optional[str] = None) -> List[Dict]:
        results = self._recipes.copy()
        
        if status:
            results = [r for r in results if r.get('status') == status]
        
        if keyword:
            keyword_lower = keyword.lower()
            results = [r for r in results if 
                      keyword_lower in r.get('name', '').lower() or 
                      keyword_lower in r.get('recipe_id', '').lower()]
        
        for recipe in results:
            recipe['test_results'] = self._get_tests_for_recipe(recipe['recipe_id'])
        
        return results
    
    def get_recipe(self, recipe_id: str) -> Optional[Dict]:
        for recipe in self._recipes:
            if recipe['recipe_id'] == recipe_id:
                recipe['test_results'] = self._get_tests_for_recipe(recipe_id)
                return recipe
        return None
    
    def _get_tests_for_recipe(self, recipe_id: str) -> List[Dict]:
        tests = []
        for test in self._tests:
            if test['recipe_id'] == recipe_id:
                tests.append(test)
        return tests
    
    def create_recipe(self, recipe_data: Dict) -> Dict:
        new_id = f"PF{len(self._recipes) + 1:03d}"
        
        new_recipe = {
            "recipe_id": new_id,
            "name": recipe_data.get('name', f'新配方-{new_id}'),
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "created_by": recipe_data.get('created_by', '系统'),
            "status": "待测试",
            "composition": recipe_data.get('composition', {}),
            "process_params": recipe_data.get('process_params', {}),
            "notes": recipe_data.get('notes', '')
        }
        
        self._recipes.append(new_recipe)
        self._save_recipes()
        
        return new_recipe
    
    def update_recipe(self, recipe_id: str, recipe_data: Dict) -> Optional[Dict]:
        for i, recipe in enumerate(self._recipes):
            if recipe['recipe_id'] == recipe_id:
                self._recipes[i].update(recipe_data)
                self._save_recipes()
                return self._recipes[i]
        return None
    
    def delete_recipe(self, recipe_id: str) -> bool:
        for i, recipe in enumerate(self._recipes):
            if recipe['recipe_id'] == recipe_id:
                self._recipes.pop(i)
                self._save_recipes()
                return True
        return False
    
    def add_test_result(self, recipe_id: str, test_data: Dict) -> Dict:
        new_test = {
            "test_id": f"TS{len(self._tests) + 1:03d}",
            "recipe_id": recipe_id,
            "test_date": datetime.now().strftime("%Y-%m-%d"),
            "test_items": test_data.get('test_items', [])
        }
        
        self._tests.append(new_test)
        self._save_tests()
        
        for recipe in self._recipes:
            if recipe['recipe_id'] == recipe_id:
                recipe['status'] = '已测试'
                self._save_recipes()
                break
        
        return new_test
    
    def get_statistics(self) -> Dict:
        total = len(self._recipes)
        status_count = {}
        for recipe in self._recipes:
            status = recipe.get('status', '未知')
            status_count[status] = status_count.get(status, 0) + 1
        
        return {
            "total_recipes": total,
            "status_distribution": status_count,
            "total_tests": len(self._tests)
        }
