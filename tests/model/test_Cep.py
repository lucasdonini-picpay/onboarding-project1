from model.Cep import Cep
import pytest


@pytest.mark.parametrize(
    "cep",
    [
        "00000-00",
        "00000-0000",
        "000000-000",
        "0000-000",
        "0a000-000",
        "000000000",
        "0000000",
        "0000a000",
    ],
)
def test_invalid_cep(cep: str):
    with pytest.raises(ValueError):
        Cep(value=cep)


def test_valid_cep():
    raw: str = "00000-000"
    cep: Cep = Cep(value=raw)

    assert cep.value == raw
