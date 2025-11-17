import requests

BASE_URL = "http://127.0.0.1:8000/api"

# 1. Authenticate and get JWT token
auth_data = {
    "username": "your_user",
    "password": "your_password"
}
resp = requests.post(f"{BASE_URL}/token/", json=auth_data)
assert resp.status_code == 200, "Login failed"
tokens = resp.json()
access_token = tokens['access']
headers = {"Authorization": f"Bearer {access_token}"}

# 2. Create a conversation
conversation_data = {
    "title": "Project Discussion",
    "participants": [1, 2]
}
resp = requests.post(f"{BASE_URL}/chats/conversations/", json=conversation_data, headers=headers)
assert resp.status_code == 201, "Failed to create conversation"
conversation_id = resp.json()['id']

# 3. Send a message
message_data = {
    "conversation": conversation_id,
    "sender": 1,
    "content": "Hello everyone!"
}
resp = requests.post(f"{BASE_URL}/chats/messages/", json=message_data, headers=headers)
assert resp.status_code == 201, "Failed to send message"

# 4. Fetch conversations
resp = requests.get(f"{BASE_URL}/chats/conversations/", headers=headers)
assert resp.status_code == 200, "Failed to fetch conversations"
print("Conversations:", resp.json())

# 5. Fetch messages (paginated)
resp = requests.get(f"{BASE_URL}/chats/messages/?page=1", headers=headers)
assert resp.status_code == 200, "Failed to fetch messages"
print("Paginated messages:", resp.json())

# 6. Test unauthorized access (no token)
resp = requests.get(f"{BASE_URL}/chats/messages/")
assert resp.status_code == 401, "Unauthorized access test failed"
print("Unauthorized access correctly blocked")
