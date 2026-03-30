from model.external.CepApiFailure import CepApiFailure
import json as js


def test_valid_data():
    json = """
    {
        "name": "",
        "message": "",
        "type": ""
    }
    """

    raw = js.loads(json)
    response = CepApiFailure.from_json(json)

    assert raw["name"] == response.name
    assert raw["message"] == response.message
    assert raw["type"] == response.type
