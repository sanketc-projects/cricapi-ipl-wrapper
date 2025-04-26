from cricapi_ipl.apis import set_api_key
import pytest

def test_set_api_key_not_a_string():
    with pytest.raises(TypeError):
        set_api_key(12345)  # Pass an integer instead of a string

def test_set_api_key_empty_string():
    with pytest.raises(ValueError):
        set_api_key("")  # Pass an empty string

def test_set_api_key_invalid_guid():
    with pytest.raises(ValueError):
        set_api_key("invalid-guid")  # Pass an invalid GUID format

def test_set_api_key_valid_guid():
    set_api_key("12345678-1234-1234-1234-123456789012")  # Pass a valid GUID format
    # This should not raise an exception