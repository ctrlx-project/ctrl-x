import pytest
def pytest_addoption(parser):
    parser.addoption("--server_ip", action="store", default="default server_ip")
    parser.addoption("--password", action="store", default="default password")
    parser.addoption("--port", action="store", default="default port")


@pytest.fixture
def server_ip(request):
    return request.config.getoption("--server_ip")


@pytest.fixture
def password(request):
    return request.config.getoption("--password")

@pytest.fixture
def port(request):
    return request.config.getoption("--port")