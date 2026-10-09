import uvicorn
from auth import auth_app

if __name__ == "__main__":
    print("Server running and connected to Supabase")
    uvicorn.run("auth:auth_app", host="0.0.0.0", port=8000, reload=True)
