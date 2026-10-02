# 1. Фикстура, которая поднимает реальный Postgres в Docker
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.storage.SqlAlchemyBase import Base


