import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.surveys import (
    Nom50Request,
    AcontecimientosRequest,
    SurveyResponse,
)
from app.services.baserow_service import BaserowService
from app.services.person_service import PersonService
from app.services.survey_service import SurveyService

router = APIRouter()


@router.post("/nom50", response_model=SurveyResponse)
async def save_nom50(payload: Nom50Request):
    baserow = BaserowService()
    person_service = PersonService(baserow)
    survey_service = SurveyService(baserow)

    try:
        person_result = await person_service.upsert_person(
            person=payload.person,
            session_id=payload.session_id,
            webchathosthref=payload.webchathosthref,
            webchathosturl=payload.webchathosturl,
            webchathosturi=payload.webchathosturi,
        )

        encuesta = await survey_service.create_encuesta(
            persona_id=person_result["persona_id"],
            id_empleado=person_result["id_empleado"],
            session_id=person_result["session_id"],
            tipo_encuesta="NOM_50",
            conversation_id=payload.conversation_id or "AUTO_CONV_NOM50",
        )

        respuestas = await survey_service.create_nom50_responses(
            encuesta_id=int(encuesta["id"]),
            answers=payload.answers,
        )

        return SurveyResponse(
            status="ok",
            persona_id=person_result["persona_id"],
            persona_accion=person_result["persona_accion"],
            encuesta_id=int(encuesta["id"]),
            respuestas_id=int(respuestas["id"]),
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"Baserow error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await baserow.close()


@router.post("/acontecimientos", response_model=SurveyResponse)
async def save_acontecimientos(payload: AcontecimientosRequest):
    baserow = BaserowService()
    person_service = PersonService(baserow)
    survey_service = SurveyService(baserow)

    try:
        person_result = await person_service.upsert_person(
            person=payload.person,
            session_id=payload.session_id,
            webchathosthref=payload.webchathosthref,
            webchathosturl=payload.webchathosturl,
            webchathosturi=payload.webchathosturi,
        )

        encuesta = await survey_service.create_encuesta(
            persona_id=person_result["persona_id"],
            id_empleado=person_result["id_empleado"],
            session_id=person_result["session_id"],
            tipo_encuesta="ACONTECIMIENTOS_TRAUMATICOS",
            conversation_id=payload.conversation_id or "AUTO_CONV_ACONTECIMIENTOS",
        )

        respuestas = await survey_service.create_acontecimientos_responses(
            encuesta_id=int(encuesta["id"]),
            answers=payload.answers,
        )

        return SurveyResponse(
            status="ok",
            persona_id=person_result["persona_id"],
            persona_accion=person_result["persona_accion"],
            encuesta_id=int(encuesta["id"]),
            respuestas_id=int(respuestas["id"]),
        )

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail=f"Baserow error: {e.response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await baserow.close()