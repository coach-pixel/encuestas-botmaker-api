import random
import time

from app.schemas.surveys import PersonInput
from app.services.baserow_service import BaserowService
from app.utils.parser import get_host_url, parse_query_params_from_url, pick_value


class PersonService:
    def __init__(self, baserow: BaserowService):
        self.baserow = baserow

    def _build_person_data(
        self,
        person: PersonInput,
        session_id: str | None,
        webchathosthref: str | None,
        webchathosturl: str | None,
        webchathosturi: str | None,
    ) -> dict:
        host_url = get_host_url(webchathosthref, webchathosturl, webchathosturi)
        query_params = parse_query_params_from_url(host_url)

        raw_id_empleado = pick_value(person.cmets_id_empleado, query_params, "cmets_id_empleado")
        raw_session_id = (session_id or "").strip()

        nombre = pick_value(person.cmets_nombre, query_params, "cmets_nombre", "SIN_NOMBRE")
        apellido = pick_value(person.cmets_apellido, query_params, "cmets_apellido", "SIN_APELLIDO")
        rfc = pick_value(person.cmets_user_rfc, query_params, "cmets_user_rfc")
        id_empresa = pick_value(person.cmets_id_empresa, query_params, "cmets_id_empresa")
        empresa = pick_value(person.cmets_empresa, query_params, "cmets_empresa")

        # Regla definida:
        # convenio = cmets_id_convenio
        # convenio_desc = cmets_convenio
        convenio = pick_value(person.cmets_id_convenio, query_params, "cmets_id_convenio")
        convenio_desc = pick_value(person.cmets_convenio, query_params, "cmets_convenio")

        pcobro = pick_value(person.cmets_pcobro, query_params, "cmets_pcobro")
        sueldo = pick_value(person.cmets_sueldo, query_params, "cmets_sueldo")
        origen = (person.webchathostpagetitle or "Botmaker").strip()

        return {
            "raw_id_empleado": raw_id_empleado,
            "raw_session_id": raw_session_id,
            "nombre": nombre,
            "apellido": apellido,
            "rfc": rfc,
            "id_empresa": id_empresa,
            "empresa": empresa,
            "convenio": convenio,
            "convenio_desc": convenio_desc,
            "pcobro": pcobro,
            "sueldo": sueldo,
            "origen": origen,
        }

    async def upsert_person(
        self,
        person: PersonInput,
        session_id: str | None,
        webchathosthref: str | None,
        webchathosturl: str | None,
        webchathosturi: str | None,
    ):
        data = self._build_person_data(
            person=person,
            session_id=session_id,
            webchathosthref=webchathosthref,
            webchathosturl=webchathosturl,
            webchathosturi=webchathosturi,
        )

        raw_id_empleado = data["raw_id_empleado"]
        raw_session_id = data["raw_session_id"]

        existing = None
        if raw_id_empleado:
            existing = await self.baserow.search_person_by_id_empleado(raw_id_empleado)

        if existing:
            person_id = int(existing["id"])

            update_payload = {
                "session_id": raw_session_id,
                "nombre": data["nombre"],
                "apellido": data["apellido"],
                "rfc": data["rfc"],
                "id_empresa": data["id_empresa"],
                "empresa": data["empresa"],
                "convenio": data["convenio"],
                "convenio_desc": data["convenio_desc"],
                "pcobro": data["pcobro"],
                "sueldo": data["sueldo"],
                "origen": data["origen"],
            }

            await self.baserow.update_person(person_id, update_payload)

            final_session_id = raw_session_id
            final_id_empleado = raw_id_empleado

            if not final_session_id and final_id_empleado:
                final_session_id = f"AUTO_SESSION_{final_id_empleado}_{int(time.time() * 1000)}"

            return {
                "persona_id": person_id,
                "persona_accion": "reutilizada",
                "session_id": final_session_id,
                "id_empleado": final_id_empleado,
            }

        fallback_id = f"AUTO_{int(time.time() * 1000)}_{random.randint(10000, 99999)}"
        final_session_id = raw_session_id
        final_id_empleado = raw_id_empleado

        if not final_session_id and not final_id_empleado:
            final_session_id = fallback_id
            final_id_empleado = fallback_id
        elif not final_id_empleado and final_session_id:
            final_id_empleado = f"AUTO_EMP_{int(time.time() * 1000)}_{random.randint(10000, 99999)}"
        elif not final_session_id and final_id_empleado:
            final_session_id = f"AUTO_SESSION_{final_id_empleado}_{int(time.time() * 1000)}"

        create_payload = {
            "id_empleado": final_id_empleado,
            "session_id": final_session_id,
            "nombre": data["nombre"],
            "apellido": data["apellido"],
            "rfc": data["rfc"],
            "id_empresa": data["id_empresa"],
            "empresa": data["empresa"],
            "convenio": data["convenio"],
            "convenio_desc": data["convenio_desc"],
            "pcobro": data["pcobro"],
            "sueldo": data["sueldo"],
            "origen": data["origen"],
        }

        created = await self.baserow.create_person(create_payload)

        return {
            "persona_id": int(created["id"]),
            "persona_accion": "creada",
            "session_id": final_session_id,
            "id_empleado": final_id_empleado,
        }