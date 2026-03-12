from typing import Optional
from urllib.parse import urlparse, parse_qs


def clean_dict(data: dict) -> dict:
    return {
        key: value
        for key, value in data.items()
        if value is not None and value != ""
    }


def get_host_url(
    webchathosthref: Optional[str],
    webchathosturl: Optional[str],
    webchathosturi: Optional[str],
) -> str:
    for value in (webchathosthref, webchathosturl, webchathosturi):
        if value and str(value).strip():
            return str(value).strip()
    return ""


def parse_query_params_from_url(host_url: Optional[str]) -> dict:
    if not host_url:
        return {}

    parsed = urlparse(host_url)
    query_dict = parse_qs(parsed.query)

    return {
        key: values[0]
        for key, values in query_dict.items()
        if values
    }


def pick_value(payload_value: Optional[str], query_params: dict, query_key: str, fallback: str = "") -> str:
    return str(payload_value or query_params.get(query_key) or fallback).strip()