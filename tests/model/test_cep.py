from src.model.cep_types import Cep
from pydantic import TypeAdapter
import pytest

# Cep is an Annotated type — direct instantiation bypasses Pydantic validators
adapter: TypeAdapter[Cep] = TypeAdapter(Cep)


@pytest.mark.parametrize("cep", ["000000000", "0000000", "00a00000"])
def test_invalid_cep(cep: str):
    with pytest.raises(ValueError):
        adapter.validate_python(cep)


@pytest.mark.parametrize("raw_cep", ["00000-000", "00000000"])
def test_valid_cep(raw_cep: str):
    cep: Cep = adapter.validate_python(raw_cep)
    assert cep == raw_cep
