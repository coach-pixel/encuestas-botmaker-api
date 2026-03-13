from urllib.parse import quote

import httpx

from app.core.config import (
    BASEROW_TOKEN,
    BASEROW_BASE_URL,
    TABLE_PERSONAS,
    TABLE_ENCUESTAS,
    TABLE_RESPUESTAS_NOM50,
    TABLE_RESPUESTAS_ACONTECIMIENTOS,
)
from app.utils.parser import clean_dict


class BaserowService:
    def __init__(self) -> None:
        self.headers = {
            "Authorization": f"Token {BASEROW_TOKEN}",
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)

    async def search_person_by_id_empleado(self, id_empleado: str):
        encoded = quote(id_empleado, safe="")
        url = (
            f"{BASEROW_BASE_URL}/{TABLE_PERSONAS}/"
            f"?user_field_names=true&filter__field_id_empleado__equal={encoded}"
        )

        response = await self.client.get(url)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        # Validación exacta en Python
        for row in results:
            row_id_empleado = str(row.get("id_empleado", "")).strip()
            if row_id_empleado == str(id_empleado).strip():
                return row

        return None

    async def create_person(self, payload: dict):
        url = f"{BASEROW_BASE_URL}/{TABLE_PERSONAS}/?user_field_names=true"
        response = await self.client.post(url, json=clean_dict(payload))
        response.raise_for_status()
        return response.json()

    async def update_person(self, person_id: int, payload: dict):
        cleaned = clean_dict(payload)
        if not cleaned:
            return {"id": person_id}

        url = f"{BASEROW_BASE_URL}/{TABLE_PERSONAS}/{person_id}/?user_field_names=true"
        response = await self.client.patch(url, json=cleaned)
        response.raise_for_status()
        return response.json()

    async def create_encuesta(self, payload: dict):
        url = f"{BASEROW_BASE_URL}/{TABLE_ENCUESTAS}/?user_field_names=true"
        response = await self.client.post(url, json=clean_dict(payload))
        response.raise_for_status()
        return response.json()

    async def create_respuestas_nom50(self, payload: dict):
        url = f"{BASEROW_BASE_URL}/{TABLE_RESPUESTAS_NOM50}/?user_field_names=true"
        response = await self.client.post(url, json=clean_dict(payload))
        response.raise_for_status()
        return response.json()

    async def create_respuestas_acontecimientos(self, payload: dict):
        url = f"{BASEROW_BASE_URL}/{TABLE_RESPUESTAS_ACONTECIMIENTOS}/?user_field_names=true"
        response = await self.client.post(url, json=clean_dict(payload))
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()