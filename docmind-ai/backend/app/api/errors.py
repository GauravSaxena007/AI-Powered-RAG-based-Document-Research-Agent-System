from google.genai.errors import APIError
from langchain_google_genai._common import GoogleGenerativeAIError


def describe_google_error(
    error: APIError | GoogleGenerativeAIError,
) -> tuple[int, str]:
    cause = error
    while not isinstance(cause, APIError) and cause.__cause__ is not None:
        cause = cause.__cause__

    if isinstance(cause, APIError):
        details = cause.details
        if _has_invalid_api_key_reason(details):
            return (
                401,
                "Google rejected the API key. Create a valid Gemini API key in Google AI Studio and set it as GOOGLE_API_KEY.",
            )
        if cause.code == 429:
            return (
                429,
                "Google AI Studio quota or rate limit reached. Check your Gemini API quota and retry.",
            )
        if cause.code in {401, 403}:
            return (
                401,
                "Google rejected the API key. Check that GOOGLE_API_KEY is valid and has access to the Gemini API.",
            )
        if cause.code == 400:
            return 400, "Google Gemini rejected the request. Check the configured model names."

    if "API_KEY_INVALID" in str(error):
        return (
            401,
            "Google rejected the API key. Create a valid Gemini API key in Google AI Studio and set it as GOOGLE_API_KEY.",
        )
    if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error):
        return (
            429,
            "Google AI Studio quota or rate limit reached. Check your Gemini API quota and retry.",
        )
    return 502, "The Google Gemini request failed. Check the API configuration and retry."


def _has_invalid_api_key_reason(value: object) -> bool:
    if isinstance(value, dict):
        return value.get("reason") == "API_KEY_INVALID" or any(
            _has_invalid_api_key_reason(item) for item in value.values()
        )
    if isinstance(value, (list, tuple)):
        return any(_has_invalid_api_key_reason(item) for item in value)
    return False
