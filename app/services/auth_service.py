# app/services/auth_service.py - Simple authentication service

import os
from typing import Optional, Dict
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY must be set in environment variables")

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Simple authentication service using JWT tokens"""
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

# Dependency for protected routes
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current user from JWT token"""
    token = credentials.credentials
    user_data = AuthService.verify_token(token)
    
    # Extract user information
    user_id = user_data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    return {
        "user_id": user_id,
        "email": user_data.get("email"),
        "exp": user_data.get("exp")
    }

# Optional: Dependency for optional authentication
async def get_current_user_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict]:
    """Get current user if authenticated, otherwise return None"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

# Auth routes
from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

auth_router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    user_params: Optional[Dict] = None

@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login endpoint - for demo purposes, accepts any email/password"""
    # In production, verify against database
    from app.services.supabase_service import db_service
    
    try:
        # For demo: create user if doesn't exist
        user_id = await db_service.get_or_create_user(request.email)
        
        # Create access token
        access_token = AuthService.create_access_token(
            data={"sub": str(user_id), "email": request.email}
        )
        
        return LoginResponse(
            access_token=access_token,
            user_id=str(user_id),
            email=request.email
        )
        
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@auth_router.post("/register", response_model=LoginResponse)
async def register(request: RegisterRequest):
    """Register a new user"""
    from app.services.supabase_service import db_service
    
    try:
        # Create user
        user_id = await db_service.get_or_create_user(request.email)
        
        # Save user params if provided
        if request.user_params:
            await db_service.save_user_params(str(user_id), request.user_params)
        
        # Create access token
        access_token = AuthService.create_access_token(
            data={"sub": str(user_id), "email": request.email}
        )
        
        return LoginResponse(
            access_token=access_token,
            user_id=str(user_id),
            email=request.email
        )
        
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@auth_router.get("/me")
async def get_me(current_user: Dict = Depends(get_current_user)):
    """Get current user information"""
    from app.services.supabase_service import db_service
    
    try:
        user_params = await db_service.get_user_params(current_user["user_id"])
        
        return {
            "user_id": current_user["user_id"],
            "email": current_user["email"],
            "params": user_params
        }
        
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )