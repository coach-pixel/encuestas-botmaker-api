from datetime import date

from app.services.baserow_service import BaserowService


class SurveyService:
    def __init__(self, baserow: BaserowService):
        self.baserow = baserow

    async def create_encuesta(
        self,
        persona_id: int,
        id_empleado: str,
        session_id: str,
        tipo_encuesta: str,
        conversation_id: str,
    ):
        payload = {
            "id_persona": [persona_id],
            "id_empleado": id_empleado,
            "session_id": session_id,
            "fecha": str(date.today()),
            "tipo_encuesta": tipo_encuesta,
            "conversation_id": conversation_id,
        }
        return await self.baserow.create_encuesta(payload)

    async def create_nom50_responses(self, encuesta_id: int, answers: dict):
        payload = {
            "encuesta": [encuesta_id]
        }

        for i in range(1, 75):
            if i <= 3:
                botmaker_key = f"p{i}"
                baserow_key = f"P{i}"
            else:
                botmaker_key = f"P{i}"
                baserow_key = f"P{i}"

            value = str(answers.get(botmaker_key, "")).strip()
            if value:
                payload[baserow_key] = value

        return await self.baserow.create_respuestas_nom50(payload)

    async def create_acontecimientos_responses(self, encuesta_id: int, answers: dict):
        payload = {
            "encuesta": [encuesta_id]
        }

        allowed_fields = [
            "AcontTraum",
            "AcontTraum1", "AcontTraum2", "AcontTraum3", "AcontTraum4", "AcontTraum5",
            "AcontTraum6", "AcontTraum7", "AcontTraum8", "AcontTraum9", "AcontTraum10",
            "AcontTraum11", "AcontTraum12", "AcontTraum13", "AcontTraum14", "AcontTraum15",
            "DT1", "DT2", "DT3", "DT4", "DT5", "DT6", "DT7", "DT8", "DT9", "DT10",
            "DT11", "DT12", "DT13",
        ]

        for key in allowed_fields:
            value = str(answers.get(key, "")).strip()
            if value:
                payload[key] = value

        return await self.baserow.create_respuestas_acontecimientos(payload)