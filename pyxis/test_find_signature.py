from unittest.mock import patch, MagicMock

from find_signature import (
    find_signature_using_reference,
)

mock_pyxis_graphql_api = "https://graphql.redhat.com/api"

SIGNATURE_ID = "67033c8d76860bfe6a094ecf"
SIGNATURE_ID2 = "67033c8d76860bfe6a094ecg"


@patch("pyxis.graphql_query")
def test_signature_exists(graphql_query):
    # Arrange
    args = MagicMock()
    args.pyxis_graphql_api = mock_pyxis_graphql_api
    args.manifest_digest = "some_digest"
    args.reference = "quay.io/scoheb/a:latest"

    # signature exists
    signature1 = generate_signatures(SIGNATURE_ID)
    signature2 = generate_signature(SIGNATURE_ID, args.reference)
    graphql_query.side_effect = [
        generate_pyxis_response("find_signature_data_by_index", signature1),
        generate_pyxis_response("get_signature", signature2),
    ]

    # Act
    found = find_signature_using_reference(
        args.pyxis_graphql_api, args.reference, args.manifest_digest
    )
    assert found


@patch("pyxis.graphql_query")
def test_signature_notfound(graphql_query):
    # Arrange
    args = MagicMock()
    args.pyxis_graphql_api = mock_pyxis_graphql_api
    args.manifest_digest = "some_digest"
    args.reference = "quay.io/scoheb/a:latest"
    another_reference = "quay.io/scoheb/a:oldest"

    # signature does not exist
    signature1 = generate_signatures(SIGNATURE_ID)
    signature2 = generate_signature(SIGNATURE_ID, another_reference)
    graphql_query.side_effect = [
        generate_pyxis_response("find_signature_data_by_index", signature1),
        generate_pyxis_response("get_signature", signature2),
        generate_pyxis_response("find_signature_data_by_index", []),
    ]

    # Act
    found = find_signature_using_reference(
        args.pyxis_graphql_api, args.reference, args.manifest_digest
    )
    assert not found


def generate_pyxis_response(query_name, data):
    response_json = {
        query_name: {
            "data": data,
            "error": None,
        }
    }

    return response_json


def generate_signatures(id):
    signatures = [
        {
            "_id": id,
        }
    ]
    return signatures


def generate_signature(id, reference):
    signature = {
        "_id": id,
        "reference": reference,
    }
    return signature
