# test_jwt_setup.py
import os
from dotenv import load_dotenv

load_dotenv()

jwt_key = os.getenv("JWT_SECRET_KEY")
if jwt_key:
    print("✅ JWT_SECRET_KEY is set")
    print(f"   Length: {len(jwt_key)} characters")
    print(f"   First 4 chars: {jwt_key[:4]}...")
else:
    print("❌ JWT_SECRET_KEY is not set!")