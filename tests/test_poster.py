from app import app

with app.test_client() as c:
    title = 'Toy Story (1995)'
    r = c.get('/api/poster?title=' + title)
    print('status', r.status_code)
    print(r.get_json())
