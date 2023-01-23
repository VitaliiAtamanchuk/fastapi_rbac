import pytest
from fastapi.testclient import TestClient

from core.database import SessionLocal
from main import app


@pytest.fixture(scope="session")
def db():
    yield SessionLocal()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# @pytest.fixture(scope="module")
# def superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers(client)


# @pytest.fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
#     return authentication_token_from_email(
#         client=client, email=settings.EMAIL_TEST_USER, db=db
#     )
