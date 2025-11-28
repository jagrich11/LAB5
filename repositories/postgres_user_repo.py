import psycopg
from psycopg.rows import dict_row
from typing import List, Optional
from models.user import User
from repositories.base import UserRepository

from config import DATABASE_URL


class PostgresUserRepository(UserRepository):
    def __init__(self):
        self.connection_params = DATABASE_URL

    def _get_connection(self):
        return psycopg.connect(self.connection_params)

    def create_user(self, name: str, email: str) -> User:
        with self._get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, created_at",
                    (name, email)
                )
                result = cur.fetchone()
                return User(
                    id=result['id'], 
                    name=name, 
                    email=email, 
                    created_at=result['created_at']
                )

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self._get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT * FROM users WHERE email = %s", (email,))
                row = cur.fetchone()
                if row:
                    return User(**row)
        return None

    def get_all_users(self) -> List[User]:
        with self._get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("SELECT * FROM users")
                rows = cur.fetchall()
        return [User(**row) for row in rows]