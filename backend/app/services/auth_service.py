"""
Authentication Service - Handle user registration, login, and authentication
"""

import hashlib
import secrets
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import uuid
from app.database.mongodb import get_database
from app.utils.logger import setup_logger

logger = setup_logger(__name__)



class AuthService:
    """Service for user authentication and management"""

    async def delete_analysis_from_user(self, user_id: str, analysis_id: str) -> bool:
        """Delete a single analysis from user's analysis history"""
        try:
            db = await get_database()
            result = await db.users.update_one(
                {"user_id": user_id},
                {"$pull": {"analysis_history": {"analysis_id": analysis_id}}, "$set": {"updated_at": datetime.utcnow()}}
            )
            if result.modified_count > 0:
                logger.info(f"Deleted analysis {analysis_id} from user {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting analysis from user: {str(e)}")
            return False

    def __init__(self):
        self.salt_length = 16

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${password_hash.hex()}"

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_hex = password_hash.split('$')
            password_check = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return password_check.hex() == hash_hex
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False

    async def register_user(
        self,
        email: str,
        username: str,
        password: str,
        full_name: str,
        profession: str
    ) -> Dict[str, Any]:
        """
        Register a new user
        Returns user data if successful
        """
        try:
            db = await get_database()
            
            # Check if user already exists
            existing_user = await db.users.find_one({
                "$or": [
                    {"email": email.lower()},
                    {"username": username.lower()}
                ]
            })
            
            if existing_user:
                return {
                    "success": False,
                    "error": "Email or username already exists"
                }
            
            # Create new user
            user_id = str(uuid.uuid4())
            password_hash = self.hash_password(password)
            
            user_doc = {
                "user_id": user_id,
                "email": email.lower(),
                "username": username.lower(),
                "password_hash": password_hash,
                "full_name": full_name,
                "profession": profession,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "analysis_history": [],
                "is_active": True
            }
            
            await db.users.insert_one(user_doc)
            
            logger.info(f"User registered: {email}")
            return {
                "success": True,
                "user_id": user_id,
                "email": email,
                "username": username,
                "full_name": full_name,
                "profession": profession
            }
            
        except Exception as e:
            logger.error(f"Error registering user: {str(e)}")
            return {
                "success": False,
                "error": f"Registration failed: {str(e)}"
            }

    async def login_user(
        self,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """
        Login user
        Returns user data if successful
        """
        try:
            db = await get_database()
            
            # Find user by email
            user = await db.users.find_one({
                "email": email.lower()
            })
            
            if not user:
                return {
                    "success": False,
                    "error": "Invalid email or password"
                }
            
            # Verify password
            if not self.verify_password(password, user["password_hash"]):
                return {
                    "success": False,
                    "error": "Invalid email or password"
                }
            
            if not user.get("is_active", True):
                return {
                    "success": False,
                    "error": "Account is inactive"
                }
            
            logger.info(f"User logged in: {email}")
            return {
                "success": True,
                "user_id": user["user_id"],
                "email": user["email"],
                "username": user["username"],
                "full_name": user["full_name"],
                "profession": user["profession"],
                "profile_photo": user.get("profile_photo")
            }
            
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            return {
                "success": False,
                "error": f"Login failed: {str(e)}"
            }

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            db = await get_database()
            user = await db.users.find_one({"user_id": user_id})
            
            if user:
                # Return user data without password hash
                return {
                    "user_id": user["user_id"],
                    "email": user["email"],
                    "username": user["username"],
                    "full_name": user["full_name"],
                    "profession": user["profession"],
                    "profile_photo": user.get("profile_photo"),
                    "analysis_history": user.get("analysis_history", []),
                    "created_at": user["created_at"]
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return None

    async def save_analysis_to_user(
        self,
        user_id: str,
        analysis_id: str,
        model_url: str,
        report_url: str
    ) -> bool:
        """Save analysis URL to user's analysis history"""
        try:
            db = await get_database()
            
            analysis_record = {
                "analysis_id": analysis_id,
                "model_url": model_url,
                "report_url": report_url,
                "saved_at": datetime.utcnow()
            }
            
            result = await db.users.update_one(
                {"user_id": user_id},
                {
                    "$push": {"analysis_history": analysis_record},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"Saved analysis {analysis_id} for user {user_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error saving analysis to user: {str(e)}")
            return False

    async def get_user_analysis_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's analysis history"""
        try:
            db = await get_database()
            user = await db.users.find_one({"user_id": user_id})
            
            if user:
                return user.get("analysis_history", [])
            return []
            
        except Exception as e:
            logger.error(f"Error getting user analysis history: {str(e)}")
            return []

    async def update_user_profile(
        self,
        user_id: str,
        full_name: Optional[str] = None,
        profession: Optional[str] = None,
        email: Optional[str] = None,
        profile_photo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update user profile information"""
        try:
            db = await get_database()
            
            # Build update data
            update_data = {"updated_at": datetime.utcnow()}
            
            if full_name:
                update_data["full_name"] = full_name
            if profession:
                update_data["profession"] = profession
            if email:
                # Check if new email is already used
                existing = await db.users.find_one({
                    "email": email.lower(),
                    "user_id": {"$ne": user_id}
                })
                if existing:
                    return {
                        "success": False,
                        "error": "Email already in use"
                    }
                update_data["email"] = email.lower()
            if profile_photo:
                update_data["profile_photo"] = profile_photo
            
            result = await db.users.update_one(
                {"user_id": user_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"Updated profile for user {user_id}")
                
                # Return updated user data
                user = await db.users.find_one({"user_id": user_id})
                return {
                    "success": True,
                    "message": "Profile updated successfully",
                    "user": {
                        "user_id": user["user_id"],
                        "email": user["email"],
                        "username": user["username"],
                        "full_name": user["full_name"],
                        "profession": user["profession"],
                        "profile_photo": user.get("profile_photo")
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "No changes made"
                }
            
        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}")
            return {
                "success": False,
                "error": f"Update failed: {str(e)}"
            }
