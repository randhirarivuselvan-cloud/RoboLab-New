from fastapi.testclient import TestClient
from main import app
client=TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='healthy'

def test_components():
    r=client.get('/api/components'); assert r.status_code==200; assert len(r.json()['components'])>0

def test_calculator():
    r=client.post('/api/calculator',json={'items':[{'name':'A','quantity':2,'unit_price':100}],'shipping':50,'tax_percent':10,'budget':300,'currency':'INR'})
    assert r.status_code==200; assert r.json()['total']==270

def test_generate():
    r=client.post('/api/projects/generate',json={'name':'x','idea':'line following robot','budget':3000,'currency':'INR'})
    assert r.status_code==200; assert 'required_components' in r.json()
