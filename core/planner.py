import json
from core.components import recommend_components
from config.settings import settings

def starter_plan(idea,budget=None,currency="INR"):
    components=recommend_components(idea); estimated=round(sum(c["price"] for c in components),2); low=idea.lower()
    difficulty="Intermediate / Advanced" if any(k in low for k in ["quadruped","computer vision","autonomous","robot arm","drone"]) else "Beginner / Intermediate"
    return {"project_overview":f"Engineering starting plan for: {idea}","required_components":components,"estimated_cost":estimated,"currency":currency,"budget":budget,"budget_status":None if budget is None else ("within estimate" if estimated<=budget else "over estimate"),"difficulty":difficulty,"architecture":["Requirements","Mechanical design","Electronics","Power","Firmware","Software","Testing","Documentation"],"controller":"Choose from the recommended controller based on I/O, compute and connectivity needs.","power":"Size the battery and regulator from measured current draw and required runtime.","wiring":"Controller → sensors/driver → actuators; use appropriate regulation and common ground where required.","safety":["Verify voltage/current ratings.","Secure moving mechanisms before testing.","Use current-limited or otherwise suitable power during first tests.","Test one subsystem at a time."],"next_steps":["Review the component list","Check the budget","Build a wiring diagram","Prototype one subsystem","Test incrementally"],"engine_status":"starter planner"}

def generate_plan(idea,budget=None,currency="INR"):
    if not settings.openai_api_key:
        return starter_plan(idea,budget,currency)
    try:
        from openai import OpenAI
        client=OpenAI(api_key=settings.openai_api_key)
        prompt=("Create a concise robotics engineering plan as JSON. Do not claim live prices, stock, CAD, simulation, or hardware validation. "
                "Include overview, assumptions, components, estimated_cost, architecture, power, testing, safety, next_steps. "
                f"Idea: {idea}\nBudget: {budget} {currency}")
        response=client.chat.completions.create(model=settings.openai_model,messages=[{"role":"system","content":"You are a careful robotics planning assistant."},{"role":"user","content":prompt}],temperature=0.2,response_format={"type":"json_object"})
        data=json.loads(response.choices[0].message.content)
        data["engine_status"]="OpenAI-powered planner"
        data["currency"]=currency; data["budget"]=budget
        return data
    except Exception:
        return starter_plan(idea,budget,currency)
