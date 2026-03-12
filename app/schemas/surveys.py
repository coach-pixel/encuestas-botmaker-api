from typing import Optional, Dict
from pydantic import BaseModel, Field


class PersonInput(BaseModel):
    cmets_id_empleado: Optional[str] = None
    cmets_nombre: Optional[str] = None
    cmets_apellido: Optional[str] = None
    cmets_user_rfc: Optional[str] = None
    cmets_id_empresa: Optional[str] = None
    cmets_empresa: Optional[str] = None
    cmets_id_convenio: Optional[str] = None
    cmets_convenio: Optional[str] = None
    cmets_pcobro: Optional[str] = None
    cmets_sueldo: Optional[str] = None
    webchathostpagetitle: Optional[str] = None


class BaseSurveyRequest(BaseModel):
    session_id: Optional[str] = None
    conversation_id: Optional[str] = None

    webchathosthref: Optional[str] = None
    webchathosturl: Optional[str] = None
    webchathosturi: Optional[str] = None

    person: PersonInput = Field(default_factory=PersonInput)
    answers: Dict[str, str] = Field(default_factory=dict)


class Nom50Request(BaseSurveyRequest):
    tipo_encuesta: str = "NOM_50"


class AcontecimientosRequest(BaseSurveyRequest):
    tipo_encuesta: str = "ACONTECIMIENTOS_TRAUMATICOS"


class SurveyResponse(BaseModel):
    status: str
    persona_id: int
    persona_accion: str
    encuesta_id: int
    respuestas_id: int