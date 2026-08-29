from core.components import recommend_components
def recommend(idea,budget=None):
    components=recommend_components(idea); total=sum(c["price"] for c in components)
    return {"recommended":components,"estimated_total":total,"budget":budget,"within_budget":None if budget is None else total<=budget}
