from fastapi.testclient import TestClient
from server.server import app
import psycopg2
from server.models import User
import server.auth as auth

#
#def test_create_agent_state():
#    with TestClient(app) as client:
#        response = client.post(
#            "/agent_state",
#            json={
#                "agent_messages": [{"role": "user", "content": "Alice and Bob"}],
#                "sheet_status": [['']]
#            })
#        assert response.status_code == 201

# create an auth dependency
# pull the sample user from db
def pull_sample_user():
    '''
    mock pulling the sample user (the sample user has google sub '12345678')
    '''
    pg_connection_d = {
        'dbname': 'spreadsheet_agent_db',
        'user': 'zestfest123',
        'port': 5432
    }
    conn: psycopg2.extensions.connection = psycopg2.connect(**pg_connection_d)
    mock_google_sub = '12345678'
    cur = conn.cursor()
    query = "SELECT * from users where google_sub = %s;"
    
    cur.execute(query, (mock_google_sub,))
    user = cur.fetchone()
    if user:
        columns = [desc[0] for desc in cur.description]
        d = dict(zip(columns, user))
        return User(**d)
    else:
        raise Exception("Sample user not found")

def override_auth_dependency():
    return pull_sample_user()

app.dependency_overrides[auth.get_current_user] = override_auth_dependency

def test_create_sheet():
    '''
    tests creating a sheet 
    '''
    with TestClient(app) as client:
        sheet_state = [['' for x in range(24)] for y in range(40)]
        sheet_name = "Untitled"
        response = client.post(
            "/sheets",
            json={
                "sheet_status": sheet_state,
                "sheet_name": sheet_name
            }
        )
        assert response.status_code == 201 
        assert isinstance(response.json()['sheet_id'], int)

def test_put_sheet():
    with TestClient(app) as client:
        sheet_state = [['' for _ in range(24)] for y in range(40)]
        sheet_name = "Untitled"
        response = client.post(
            "/sheets",
            json={
                "sheet_status": sheet_state,
                "sheet_name": sheet_name
            }
        )
        sheet_id = response.json()["sheet_id"]

        # modify the sheet 
        sheet_state[0] = ['x' for _ in range(24)]
        put_response = client.put(
            f"/sheets/{sheet_id}",
            json={
                "sheet_status": sheet_state,
                "sheet_name": sheet_name
            }
        )
        # verify 
        assert put_response.status_code == 200
        assert isinstance(response.json()['sheet_id'], int)

app.dependency_overrides[auth.get_current_user] = override_auth_dependency

def test_get_user_sheet():
    with TestClient(app) as client:
        response = client.get(
            "/sheets/getUserSheets"
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)