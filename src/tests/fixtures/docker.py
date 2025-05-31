import os
import pytest

@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "src/tests", "docker-compose.yml")

@pytest.fixture(scope="session")
def docker_setup():
    return ["down -v", "up --build -d"]