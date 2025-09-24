from fastapi.testclient import TestClient
from server.server import app
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

def test_create_sheet():
    '''
    tests creating a sheet 
    '''
    with TestClient(app) as client:
        client.cookies = {"access_token": '12345678'}
        sheet_state = [['' for x in range(24)] for y in range(40)]
        response = client.post(
            "/sheets",
            json={
                "sheet_status": sheet_state
            }
        )
        assert response.status_code == 201 
        assert isinstance(response.sheet_id, int)