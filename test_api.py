from app import app

with app.test_client() as c:
    res = c.get('/api/recommend?title=Toy%20Story%20(1995)&topn=5')
    print('status', res.status_code)
    print(res.get_json())
