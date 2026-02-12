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


# get_platform_by_name


def test_get_platform_by_name_ok():
    service = PlatformService()
    service.platform_dao.get_platform_by_name = MagicMock(return_value=PLATFORM_PC)

    result = service.get_platform_by_name("pc")

    assert result == PLATFORM_PC
    service.platform_dao.get_platform_by_name.assert_called_once_with("PC")


def test_get_platform_by_name_strip_and_upper():
    service = PlatformService()
    service.platform_dao.get_platform_by_name = MagicMock(return_value=PLATFORM_PS5)

    result = service.get_platform_by_name("  ps5  ")

    assert result == PLATFORM_PS5
    service.platform_dao.get_platform_by_name.assert_called_once_with("PS5")


def test_get_platform_by_name_empty():
    service = PlatformService()

    with pytest.raises(ValueError, match="ne peut pas être vide"):
        service.get_platform_by_name("")


def test_get_platform_by_name_blank():
    service = PlatformService()

    with pytest.raises(ValueError, match="ne peut pas être vide"):
        service.get_platform_by_name("   ")


# delete_platform


def test_delete_platform_ok():
    service = PlatformService()
    service.platform_dao.delete_platform = MagicMock(return_value=True)

    result = service.delete_platform(PLATFORM_PC)

    assert result is True
    service.platform_dao.delete_platform.assert_called_once_with(PLATFORM_PC)


def test_delete_platform_none():
    service = PlatformService()

    with pytest.raises(ValueError, match="ne peut pas être None"):
        service.delete_platform(None)


# delete_platform_by_name


def test_delete_platform_by_name_ok():
    service = PlatformService()
    service.get_platform_by_name = MagicMock(return_value=PLATFORM_PC)
    service.delete_platform = MagicMock(return_value=True)

    result = service.delete_platform_by_name("pc")

    assert result is True
    service.get_platform_by_name.assert_called_once_with("pc")
    service.delete_platform.assert_called_once_with(PLATFORM_PC)


def test_delete_platform_by_name_not_found():
    service = PlatformService()
    service.get_platform_by_name = MagicMock(return_value=None)

    result = service.delete_platform_by_name("unknown")

    assert result is False


# platform_exists


def test_platform_exists_true():
    service = PlatformService()
    service.get_platform_by_name = MagicMock(return_value=PLATFORM_PC)

    assert service.platform_exists("pc") is True


def test_platform_exists_false():
    service = PlatformService()
    service.get_platform_by_name = MagicMock(return_value=None)

    assert service.platform_exists("unknown") is False


def test_platform_exists_invalid_name():
    service = PlatformService()
    service.get_platform_by_name = MagicMock(side_effect=ValueError)

    assert service.platform_exists("") is False


# platform_exists_by_id


def test_platform_exists_by_id_true():
    service = PlatformService()
    service.get_platform_by_id = MagicMock(return_value=PLATFORM_PC)

    assert service.platform_exists_by_id(1) is True


def test_platform_exists_by_id_false():
    service = PlatformService()
    service.get_platform_by_id = MagicMock(return_value=None)

    assert service.platform_exists_by_id(999) is False


def test_normalize_platform_name_basic():
    service = PlatformService()

    result = service.normalize_platform_name("pc")

    assert result == "PC"


def test_normalize_platform_name_with_spaces():
    service = PlatformService()

    result = service.normalize_platform_name("  xbox  ")

    assert result == "XBOX"


def test_normalize_platform_name_mixed_case():
    service = PlatformService()

    result = service.normalize_platform_name("PlayStation")

    assert result == "PLAYSTATION"


def test_normalize_platform_name_empty_string():
    service = PlatformService()

    result = service.normalize_platform_name("")

    assert result == ""


def test_normalize_platform_name_none():
    service = PlatformService()

    result = service.normalize_platform_name(None)

    assert result == ""


def test_normalize_platform_name_only_spaces():
    service = PlatformService()

    result = service.normalize_platform_name("   ")

    assert result == ""
