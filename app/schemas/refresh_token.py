from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4


class RefreshToken(BaseModel):
    jti : UUID
    is_revoked : bool
    created_at : datetime
    expires_at : datetime
    user_id : int



