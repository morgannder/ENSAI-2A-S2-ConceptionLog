from unittest.mock import MagicMock

import pytest

from src.models.platforms import Platform
from src.service.platforms_service import PlatformService


# Fixtures

PLATFORM_PC = Platform(id=1, name="PC")
PLATFORM_PS5 = Platform(id=2, name="PS5")


# get_platform_by_id


def test_get_platform_by_id_ok():
    service = PlatformService()
    service.platform_dao.get_platform_by_id = MagicMock(return_value=PLATFORM_PC)

    result = service.get_platform_by_id(1)

    assert result == PLATFORM_PC
    service.platform_dao.get_platform_by_id.assert_called_once_with(1)


def test_get_platform_by_id_invalid_none():
    service = PlatformService()

    with pytest.raises(ValueError, match="entier positif"):
        service.get_platform_by_id(None)


def test_get_platform_by_id_invalid_negative():
    service = PlatformService()

    with pytest.raises(ValueError, match="entier positif"):
        service.get_platform_by_id(-1)


def test_get_platform_by_id_not_found():
    service = PlatformService()
    service.platform_dao.get_platform_by_id = MagicMock(return_value=None)

    result = service.get_platform_by_id(999)

    assert result is None
