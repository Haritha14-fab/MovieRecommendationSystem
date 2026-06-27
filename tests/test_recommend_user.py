from app import app

with app.test_client() as c:
    print('Testing /api/recommend_user (global top 5)')
    r = c.get('/api/recommend_user?topn=5')
    print('status', r.status_code)
    print(r.get_json())

    print('\nTesting /api/recommend_user for user_id=1')
    r2 = c.get('/api/recommend_user?user_id=1&topn=5')
    print('status', r2.status_code)
    print(r2.get_json())
