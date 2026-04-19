import os
from typing import List, Dict
from openai import OpenAI
from config.settings import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.ZHIPU_API_KEY
        self.api_base = settings.ZHIPU_API_BASE
        
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base
            )
        else:
            self.client = None
            print("警告：未配置API Key，将使用模拟回答")
    
    def chat(self, messages: List[Dict], temperature: float = 0.7) -> str:
        if not self.client:
            return self._mock_response(messages[-1]['content'] if messages else "")
        
        try:
            response = self.client.chat.completions.create(
                model="glm-4",
                messages=messages,
                temperature=temperature,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM调用失败: {e}")
            return self._mock_response(messages[-1]['content'] if messages else "")
    
    def chat_with_context(self, question: str, context: str) -> str:
        system_prompt = """你是一个玻璃材料领域的专业助手。请根据以下参考文档回答用户的问题。

回答要求：
1. 基于参考文档回答，不要编造信息
2. 如果参考文档中没有相关信息，请明确说明
3. 回答要专业、准确、简洁
4. 在回答中适当引用来源，如"根据《玻璃材料学基础》..." """

        user_prompt = f"""【参考文档】
{context}

【用户问题】
{question}

请基于以上参考文档回答问题。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.chat(messages, temperature=0.3)
    
    def _mock_response(self, question: str) -> str:
        mock_answers = {
            "热膨胀系数": "根据文献资料，高铝硅酸盐玻璃的热膨胀系数通常在(3-5)×10⁻⁶/℃范围内。具体数值受Al₂O₃含量、碱金属氧化物含量等因素影响。当Al₂O₃含量从10%增加到20%时，热膨胀系数可从5.5×10⁻⁶/℃降至4.0×10⁻⁶/℃。",
            "降低": "降低玻璃热膨胀系数的方法包括：\n1. 增加SiO₂含量\n2. 添加Al₂O₃、B₂O₃等网络形成氧化物\n3. 减少碱金属氧化物含量\n4. 采用适当的退火工艺\n\n通过优化成分配比，可以将玻璃的热膨胀系数从8×10⁻⁶/℃降至3×10⁻⁶/℃以下。",
            "Al₂O₃": "Al₂O₃对玻璃性能的影响主要体现在以下几个方面：\n1. 降低热膨胀系数：Al₂O₃的加入可以填充玻璃网络结构中的空隙，使结构更加紧密\n2. 提高化学稳定性：Al₂O₃可以增强玻璃网络的连接强度\n3. 改善机械性能：Al₂O₃可以提高玻璃的硬度和抗弯强度\n\n实验数据表明，当Al₂O₃含量从10%增加到20%时，玻璃的热膨胀系数从5.5×10⁻⁶/℃降至4.0×10⁻⁶/℃。",
            "熔制温度": "玻璃的熔制温度通常在1400-1600℃之间，具体温度取决于玻璃的成分配比：\n- 普通钠钙玻璃：1450-1500℃\n- 高铝硅酸盐玻璃：1550-1650℃\n- 硼硅酸盐玻璃：1500-1600℃\n\n熔制过程中需要严格控制温度曲线和保温时间，以确保玻璃的均匀性和质量。",
            "退火": "退火是玻璃制造过程中的重要环节，目的是消除玻璃内部的热应力。退火温度通常在玻璃转变温度以下50-100℃。退火工艺包括：\n1. 升温至退火温度\n2. 保温一段时间（根据玻璃厚度确定）\n3. 缓慢冷却至室温\n\n良好的退火可以提高玻璃的机械强度和热稳定性。",
            "密度": "玻璃密度通常在2.2-2.8g/cm³范围内，主要受化学成分影响：\n- SiO₂：密度约2.2g/cm³，增加SiO₂含量会降低玻璃密度\n- Al₂O₃：密度约3.9g/cm³\n- CaO：密度约3.35g/cm³\n\n高铝硅酸盐玻璃的密度通常在2.40-2.55g/cm³之间。",
            "抗弯强度": "玻璃的抗弯强度通常在60-100MPa范围内。提高抗弯强度的方法包括：\n1. 增加Al₂O₃含量\n2. 适量添加CaO和MgO\n3. 控制碱金属氧化物含量\n4. 良好的退火处理\n5. 表面处理（如酸洗、钢化）\n\n通过优化成分配比和热处理工艺，可以将抗弯强度提高到100MPa以上。",
            "耐热": "玻璃的耐热性能评估方法包括：\n1. 热稳定性测试：加热后急冷，观察是否开裂\n2. 热膨胀系数测定：使用热膨胀仪测量\n3. 软化温度测定：测定玻璃开始软化的温度\n4. 耐热冲击性测试：循环加热和冷却\n\n高铝硅酸盐玻璃的耐热温度通常在500℃以上，热膨胀系数越低，耐热性能越好。",
            "碱金属": "碱金属氧化物（Na₂O、K₂O）的主要作用：\n1. 助熔作用：降低玻璃的熔制温度\n2. 对热膨胀系数的影响：会提高热膨胀系数\n3. 对化学稳定性的影响：过量会降低化学稳定性\n\n在玻璃配方设计中，需要平衡碱金属氧化物的含量。对于高铝硅酸盐玻璃，Na₂O含量通常控制在8-12%。",
            "化学稳定性": "提高玻璃化学稳定性的方法：\n1. 增加SiO₂含量\n2. 添加Al₂O₃\n3. 减少碱金属氧化物含量\n4. 添加CaO、MgO等二价金属氧化物\n\n高铝硅酸盐玻璃具有优异的化学稳定性，耐水性和耐酸性都很好。"
        }
        
        for keyword, answer in mock_answers.items():
            if keyword in question:
                return answer
        
        return "根据文献资料，这是一个关于玻璃材料的专业问题。建议您查阅相关技术文档获取详细信息，或咨询材料专家。"
