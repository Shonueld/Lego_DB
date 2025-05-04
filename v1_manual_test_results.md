# Example workflow
A user can create an account and then view their profile.

# Testing results

1. **Create a user**
**Curl:**
curl -X POST \
  https://mycoolapp.onrender.com/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com"}'

**Response:**
{
  "username": "testuser",
  "id": 1
}
