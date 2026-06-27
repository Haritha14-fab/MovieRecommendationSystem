from app import app

with app.test_client() as c:
    print('Testing /api/recommend_hybrid for user_id=1')
    r = c.get('/api/recommend_hybrid?user_id=1&topn=5')
    print('status', r.status_code)
    print(r.get_json())
