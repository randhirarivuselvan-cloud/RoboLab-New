import json
from database.database import get_connection

def create_project(name,idea,budget,currency,plan,user_id=None):
    with get_connection() as conn:
        cur=conn.execute("INSERT INTO projects(user_id,name,idea,budget,currency,plan_json) VALUES(?,?,?,?,?,?)",(user_id,name,idea,budget,currency,json.dumps(plan)))
        conn.commit(); return get_project(cur.lastrowid,user_id)

def list_projects(user_id=None):
    with get_connection() as conn:
        if user_id is None: rows=conn.execute("SELECT * FROM projects WHERE user_id IS NULL ORDER BY updated_at DESC").fetchall()
        else: rows=conn.execute("SELECT * FROM projects WHERE user_id=? ORDER BY updated_at DESC",(user_id,)).fetchall()
        return [serialize(r) for r in rows]

def get_project(project_id,user_id=None):
    with get_connection() as conn:
        if user_id is None: row=conn.execute("SELECT * FROM projects WHERE id=? AND user_id IS NULL",(project_id,)).fetchone()
        else: row=conn.execute("SELECT * FROM projects WHERE id=? AND user_id=?",(project_id,user_id)).fetchone()
        return None if row is None else serialize(row)

def update_project(project_id,data,user_id=None):
    current=get_project(project_id,user_id)
    if not current:return None
    values={k:v for k,v in data.items() if v is not None}; fields={k:values.get(k,current[k]) for k in ["name","idea","budget","currency"]}
    with get_connection() as conn:
        conn.execute("UPDATE projects SET name=?,idea=?,budget=?,currency=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",(*fields.values(),project_id)); conn.commit()
    return get_project(project_id,user_id)

def delete_project(project_id,user_id=None):
    with get_connection() as conn:
        if user_id is None: cur=conn.execute("DELETE FROM projects WHERE id=? AND user_id IS NULL",(project_id,))
        else: cur=conn.execute("DELETE FROM projects WHERE id=? AND user_id=?",(project_id,user_id))
        conn.commit(); return cur.rowcount>0

def serialize(row):
    d=dict(row); d["plan"]=json.loads(d.pop("plan_json")); return d
