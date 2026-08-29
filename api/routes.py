from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from database.database import init_db, get_connection
from database.models import ProjectCreate, ProjectUpdate, CalculatorRequest, RegionRequest
from core.planner import generate_plan
from core.projects import create_project,list_projects,get_project,update_project,delete_project
from core.components import list_components
from core.recommendations import recommend
from core.calculator import calculate
from core.pricing import PLANS, regional_price
from config.settings import settings

router=APIRouter(); init_db()
oauth = None

def get_oauth():
    global oauth
    if oauth is None:
        from authlib.integrations.starlette_client import OAuth
        oauth = OAuth()
        oauth.register(name="google",client_id=settings.google_client_id,client_secret=settings.google_client_secret,server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",client_kwargs={"scope":"openid email profile"})
    return oauth

def current_user_id(request): return request.session.get("user_id")

@router.get("/api/status")
def api_status():
    return {"name":settings.app_name,"company":settings.company_name,"version":"2.0.0","status":"online","features":{"google_oauth":bool(settings.google_client_id and settings.google_client_secret),"ai":bool(settings.openai_api_key),"payments":bool(settings.stripe_secret_key)}}

@router.get("/api/pricing")
def pricing(): return {"plans":PLANS,"payments_configured":bool(settings.stripe_secret_key and settings.stripe_monthly_price_id and settings.stripe_annual_price_id)}

@router.get("/api/auth/google")
async def google_login(request:Request):
    if not (settings.google_client_id and settings.google_client_secret): raise HTTPException(503,"Google OAuth is not configured.")
    return await get_oauth().google.authorize_redirect(request,settings.google_redirect_uri)

@router.get("/api/auth/google/callback")
async def google_callback(request:Request):
    if not (settings.google_client_id and settings.google_client_secret): raise HTTPException(503,"Google OAuth is not configured.")
    try:
        token=await get_oauth().google.authorize_access_token(request); userinfo=token.get("userinfo")
        if not userinfo: raise HTTPException(400,"Google did not return user information.")
        with get_connection() as conn:
            row=conn.execute("SELECT * FROM users WHERE google_id=? OR email=?",(userinfo["sub"],userinfo["email"])).fetchone()
            if row:
                conn.execute("UPDATE users SET google_id=?,name=?,picture=? WHERE id=?",(userinfo["sub"],userinfo.get("name"),userinfo.get("picture"),row["id"])); uid=row["id"]
            else:
                cur=conn.execute("INSERT INTO users(google_id,email,name,picture) VALUES(?,?,?,?)",(userinfo["sub"],userinfo["email"],userinfo.get("name"),userinfo.get("picture"))); uid=cur.lastrowid
            conn.commit()
        request.session["user_id"]=uid; request.session["user_email"]=userinfo["email"]
        return RedirectResponse("/")
    except HTTPException: raise
    except Exception as exc: raise HTTPException(400,f"Google sign-in failed: {exc}")

@router.post("/api/auth/logout")
def logout(request:Request): request.session.clear(); return {"ok":True}

@router.get("/api/users/me")
def me(request:Request):
    uid=current_user_id(request)
    if not uid:return {"authenticated":False,"user":None}
    with get_connection() as conn: row=conn.execute("SELECT id,email,name,picture FROM users WHERE id=?",(uid,)).fetchone()
    return {"authenticated":bool(row),"user":None if not row else dict(row)}

@router.post("/api/projects/generate")
def generate_project(payload:ProjectCreate): return generate_plan(payload.idea,payload.budget,payload.currency)

@router.get("/api/projects")
def projects(request:Request): return list_projects(current_user_id(request))

@router.post("/api/projects")
def create(payload:ProjectCreate,request:Request):
    plan=generate_plan(payload.idea,payload.budget,payload.currency)
    return create_project(payload.name,payload.idea,payload.budget,payload.currency,plan,current_user_id(request))

@router.get("/api/projects/{project_id}")
def get(project_id:int,request:Request):
    result=get_project(project_id,current_user_id(request))
    if not result: raise HTTPException(404,"Project not found")
    return result

@router.put("/api/projects/{project_id}")
def update(project_id:int,payload:ProjectUpdate,request:Request):
    result=update_project(project_id,payload.model_dump(exclude_unset=True),current_user_id(request))
    if not result: raise HTTPException(404,"Project not found")
    return result

@router.delete("/api/projects/{project_id}")
def remove(project_id:int,request:Request):
    if not delete_project(project_id,current_user_id(request)): raise HTTPException(404,"Project not found")
    return {"deleted":True}

@router.post("/api/components/recommend")
def component_recommend(payload:ProjectCreate): return recommend(payload.idea,payload.budget)
@router.get("/api/components")
def components(category:str|None=None): return {"components":list_components(category)}
@router.post("/api/calculator")
def calculator(payload:CalculatorRequest):
    result=calculate(payload.items,payload.shipping,payload.tax_percent,payload.budget); result["currency"]=payload.currency; return result

@router.post("/api/location/region")
def region(payload:RegionRequest):
    country=payload.country.upper(); return {"country":country,"region":payload.region,"location_required":False,"pricing_multiplier_example":{"IN":1.0,"US":1.25,"GB":1.20,"DE":1.22,"SG":1.10}.get(country,1.15),"precision":"coarse country/region only"}

@router.post("/api/billing/checkout")
def checkout(request:Request,plan:str):
    if not settings.stripe_secret_key: raise HTTPException(503,"Payments are not configured.")
    price_id=settings.stripe_monthly_price_id if plan=="monthly" else settings.stripe_annual_price_id if plan=="annual" else ""
    if not price_id: raise HTTPException(503,"The selected billing price is not configured.")
    import stripe
    stripe.api_key=settings.stripe_secret_key
    session=stripe.checkout.Session.create(mode="subscription",line_items=[{"price":price_id,"quantity":1}],success_url=settings.stripe_success_url,cancel_url=settings.stripe_cancel_url)
    return {"url":session.url}
