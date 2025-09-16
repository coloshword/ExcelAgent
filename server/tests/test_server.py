#from fastapi.testclient import TestClient
#from server.server import app
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