from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.com"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseModel):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()





