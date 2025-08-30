import os
import json
import aiofiles
from typing import List, Dict, Any
from dotenv import load_dotenv
import openai
import re

# load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
BASE_API_DIR = os.getenv("API_BASE_DIR")
if BASE_API_DIR is None:
    BASE_API_DIR = os.path.dirname(os.path.abspath(__file__))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Chunk:
    """
    Clase para trabajar con consultas de la Matriz del Destino, incluida la generación de textos por reglas e integración con OpenAI.
    """
    def __init__(self):
        """
        Inicialización de la clase Chunk.
        """
        print("[DEBUG] Chunk init: Corrección para consult_personal — ahora se usa computed_data.")

    async def get_rules_json(self) -> dict:
        """
        Carga de forma asíncrona y devuelve el contenido del archivo Rules.json con descripciones de energías y aspectos.

        Returns:
            dict: Diccionario con las reglas para la interpretación de energías.
        Raises:
            FileNotFoundError: Si no se encuentra el archivo.
        """
        rules_path = os.path.join(BASE_API_DIR, 'base', 'Rules.json')
        if not os.path.exists(rules_path):
            raise FileNotFoundError(f"Archivo {rules_path} no encontrado.")
        async with aiofiles.open(rules_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        return json.loads(content)

    # Mapeo (chakra, aspect) -> point_name para custom_points
    CHAKRA_ASPECT_TO_POINT = {
        ("Anahata", "Fisica"): "Zona de confort",
        ("Sahasrara", "Fisica"): "Recurso interior",
        ("Sahasrara", "Energia"): "Talento",
        ("Muladhara", "Fisica"): "Cola kármica general",
        ("Svadhisthana", "Emociones"): "Cola kármica del amor",
        ("Muladhara", "Emociones"): "Pareja kármica en el amor",
        ("Manipura", "Emociones"): "Amor y dinero",
        ("Manipura", "Fisica"): "Dirección de vida profesional",
        ("Manipura", "Energia"): "Fuente de ingresos",
        ("Muladhara", "Energia"): "Bloqueo financiero",
        
    }

    def normalize(self, val):
        if not isinstance(val, str):
            return val
        return (
            val.replace("í", "i")
               .replace("é", "e")
               .replace("ó", "o")
               .replace("Í", "I")
               .replace("É", "E")
               .replace("Ó", "O")
        )

    async def consult_personal(self, free_points: List[Dict[str, Any]]) -> str:
        """
        Forma una consulta textual sobre puntos libres basada en las reglas de Rules.json (custom_points).
        Ahora primero muestra la descripción del punto (description) y después la interpretación individual.
        """
        rules = await self.get_rules_json()
        lines = []
        for point in free_points:
            chakra = point.get("chakra")
            aspect = self.normalize(point.get("aspect"))
            val = point.get("value")
            val_str = str(val)
            point_name = self.CHAKRA_ASPECT_TO_POINT.get((chakra, aspect))
            if not point_name:
                lines.append(f"{chakra} - {aspect} - {val}:\n(Sin descripción)")
                continue
            point_block = rules.get("custom_points", {}).get(point_name)
            if not point_block:
                lines.append(f"{point_name} ({val}):\n(Sin descripción)")
                continue
            description = point_block.get("description", "")
            value_block = point_block.get(val_str)
            if isinstance(value_block, dict):
                value_title = value_block.get("title")
                value_text = value_block.get("text")
                if value_title and value_text:
                    value_full = f"{value_title}. {value_text}"
                elif value_title:
                    value_full = value_title
                elif value_text:
                    value_full = value_text
                else:
                    value_full = str(value_block)
            elif isinstance(value_block, str):
                value_full = value_block
            else:
                value_full = "(Sin descripción)"
            if value_full:
                lines.append(f"{point_name} ({val}):\n{description}\n{value_full}")
            else:
                lines.append(f"{point_name} ({val}):\n{description}\n(Sin descripción)")
        return "\n\n".join(lines)

    async def consult_paid(self, points: List[Dict[str, Any]], date: str = None) -> str:
        """
        Forma una consulta ampliada por puntos con posibilidad de indicar fecha (custom_points).
        Ahora, si en el punto no hay campo name, el punto se omite (sin fallback por chakra+aspect).
        """
        print("DEBUG paidPoints:", points)  # Al inicio de la función
        rules = await self.get_rules_json()
        lines = []
        for point in points:
            point_name = point.get("name")
            val = point.get("value")
            val_str = str(val)
            if point_name:
                point_block = rules.get("custom_points", {}).get(point_name)
                if not point_block:
                    lines.append(f"{point_name} ({val}):\n(Sin descripción)")
                    continue
                description = point_block.get("description", "")
                if point_name == "Energía masculina":
                    value_block = point_block.get("Línea paterna", {}).get(val_str)
                elif point_name == "Energía femenina":
                    value_block = point_block.get("Línea materna", {}).get(val_str)
                else:
                    value_block = point_block.get(val_str)
                if isinstance(value_block, dict):
                    value_title = value_block.get("title")
                    value_text = value_block.get("text")
                    if value_title and value_text:
                        value_full = f"{value_title}. {value_text}"
                    elif value_title:
                        value_full = value_title
                    elif value_text:
                        value_full = value_text
                    else:
                        value_full = str(value_block)
                elif isinstance(value_block, str):
                    value_full = value_block
                else:
                    value_full = "(Sin descripción)"
                if value_full:
                    lines.append(f"{point_name} ({val}):\n{description}\n{value_full}")
                else:
                    lines.append(f"{point_name} ({val}):\n{description}\n(Sin descripción)")
            # Si no hay name, el punto se omite
            # continue
        print("DEBUG lines:", lines)  # Antes de formar final_text
        final_text = "\n\n".join(lines)
        print("DEBUG final_text:", final_text)  # Antes de return
        if date:
            final_text = f"Interpretación ampliada para la fecha {date}:\n\n{final_text}"
        return final_text

    async def consult_compatibility(self, computed_personal: str, computed_compatibility: str, stage: str = "start") -> str:
        """
        Genera una consulta sobre compatibilidad basada en datos personales y de pareja.
        stage: "start" — primera pregunta, "offer_paid" — oferta de cálculo de pago.
        """
        if stage == "start":
            return "¿Listo para conocer consult_compatibility (de pago)?"
        elif stage == "offer_paid":
            return "¿Quieres un cálculo profundo de compatibilidad (de pago)?\nSí\nNo"
        # a continuación: procesamiento del escenario de pago

    async def ask_gpt(self, user_text: str) -> str:
        """
        Envía una pregunta a OpenAI GPT y devuelve la respuesta, limitada a la temática de la Matriz del Destino.

        Args:
            user_text (str): Pregunta del usuario.

        Returns:
            str: Respuesta del modelo o mensaje de error.
        """
        prompt = (
            "Eres un asesor amable y participativo de la Matriz del Destino. "
            "Responde a las preguntas del usuario sobre la matriz, energías, chakras y fecha de nacimiento. "
            "Escribe en lenguaje simple y claro, añade ejemplos, involucra al usuario y sugiere usar la calculadora del sitio. "
            "Si la pregunta no es del tema, explica suavemente que eres asesor de la Matriz del Destino. "
            "\n\n"
            "Chakras utilizados en la Matriz del Destino:\n"
            "— Sahasrara: chakra de la conciencia superior, conexión con significados elevados.\n"
            "— Ajna: chakra de la intuición, visión interior y sabiduría.\n"
            "— Vishuddha: chakra de la comunicación, autoexpresión y honestidad.\n"
            "— Anahata: chakra del amor, la armonía y la compasión.\n"
            "— Manipura: chakra de la voluntad, autoestima y poder personal.\n"
            "— Svadhisthana: chakra de las emociones, la creatividad y el placer.\n"
            "— Muladhara: chakra de la estabilidad, la seguridad y la energía vital.\n"
            "Si el usuario pregunta por el significado o el papel de cualquiera de estos chakras — responde brevemente con la descripción anterior.\n"
            "Si el usuario quiere saber más sobre sí mismo, su matriz o energías — sugiere usar la calculadora para el cálculo por fecha de nacimiento.\n"
        )
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_text + "\n\nPor favor, da una respuesta completa y detallada y asegúrate de concluir la idea."}
            ],
            max_tokens=1200
        )
        return response.choices[0].message.content.strip()

    async def get_answer_async(self, query: str) -> str:
        """
        Procesa la solicitud del usuario: saludos, agradecimientos, preguntas temáticas.
        Para preguntas temáticas llama a ask_gpt.

        Args:
            query (str): Entrada de texto del usuario.

        Returns:
            str: Respuesta.
        """
        q = query.lower().strip()
        greetings = [
            "hola", "buenas", "buenos días", "buenas tardes", "buenas noches", "hello", "hi"
        ]
        farewells = [
            "adiós", "hasta luego", "bye", "goodbye", "nos vemos", "hasta pronto", "buenas noches"
        ]
        thanks = [
            "gracias", "muchas gracias", "thank you", "mil gracias"
        ]

        if any(word in q for word in greetings):
            return "¡Hola! Soy asesor de la Matriz del Destino. Puedo calcular tu matriz, explicar el significado de las energías y dar recomendaciones. ¡Solo introduce tu fecha de nacimiento en la calculadora!"
        if any(word in q for word in farewells):
            return "¡Todo lo mejor! Si tienes preguntas sobre la Matriz del Destino — aquí estaré."
        if any(word in q for word in thanks):
            return "¡Con gusto! Si necesitas una consulta sobre la Matriz del Destino — siempre estoy a tu disposición."
        if "qué puedes" in q or "qué sabes hacer" in q or "tus capacidades" in q or "quién eres" in q:
            return "Soy asesor de la Matriz del Destino. Puedo calcular tu matriz, explicar los significados de las energías y darte recomendaciones. ¡Solo introduce tu fecha de nacimiento en la calculadora!"

        # Nueva gestión para preguntas generales sobre chakras
        if (
            "qué es chakr" in q or
            "cuéntame de chakr" in q or
            "qué sabes de chakr" in q or
            "sabes de chakr" in q or
            "explica chakr" in q or
            "sobre chakr" in q or
            ("chakr" in q and ("qué es" in q or "qué significa" in q or "explica" in q or "cuéntame" in q))
        ):
            return (
                "Los chakras son centros energéticos que analizamos en tu Matriz del Destino. "
                "En nuestro sistema usamos 7 chakras: Sahasrara, Ajna, Vishuddha, Anahata, Manipura, Svadhisthana, Muladhara. "
                "Cada uno responde por aspectos específicos de tu destino y energía. "
                "¿Quieres saber más de alguno o calcular tu matriz?"
            )

        # Nueva gestión para “qué chakras hay”
        if "qué chakr" in q:
            return (
                "En la Matriz del Destino se usan 7 chakras:\n"
                "— Sahasrara\n"
                "— Ajna\n"
                "— Vishuddha\n"
                "— Anahata\n"
                "— Manipura\n"
                "— Svadhisthana\n"
                "— Muladhara\n"
                "Cada uno responde por aspectos específicos de tu destino y energía. "
                "¿Quieres saber más de alguno?"
            )
        # “cuántos chakras”
        if "cuántos chakr" in q or "número de chakr" in q or ("chakr" in q and "cuántos" in q):
            return "En la Matriz del Destino se analizan 7 chakras: Sahasrara, Ajna, Vishuddha, Anahata, Manipura, Svadhisthana, Muladhara."
        # “lista de chakras”
        if "lista de chakr" in q or ("chakr" in q and "lista" in q):
            return "Lista de 7 chakras en la Matriz del Destino: Sahasrara, Ajna, Vishuddha, Anahata, Manipura, Svadhisthana, Muladhara."
        # “qué energías hay”
        if "qué energ" in q or "lista de energ" in q:
            return (
                "En la Matriz del Destino se usan 22 energías (arcanos). Cada energía tiene su propio significado e impacta diferentes áreas de la vida. "
                "Para un análisis individual introduce tu fecha de nacimiento en la calculadora."
            )
        # “22 energías” / “cuántas energías”
        if "22 energías" in q or ("energías" in q and "cuántas" in q):
            return (
                "En la Matriz del Destino se usan 22 energías (arcanos). Cada una tiene su significado e influencia. "
                "Para un análisis individual introduce tu fecha de nacimiento en la calculadora."
            )
        # “tarea de vida”
        if "tarea de vida" in q or ("tarea" in q and "vida" in q):
            return (
                "La tarea de vida es el propósito principal con el que una persona llega a este mundo. En la Matriz del Destino se determina por la fecha de nacimiento y ayuda a entender tu vocación principal, lecciones y pruebas. ¿Quieres conocer la tuya? ¡Introduce tu fecha en la calculadora!"
            )
        # “qué significa consulta por fecha”
        if "qué significa consulta" in q or "qué es consulta" in q or ("consulta" in q and "qué" in q):
            return (
                "La consulta por fecha de nacimiento es el análisis individual de tu Matriz del Destino. "
                "Puedo calcular tu matriz, explicar el significado de tus energías y chakras y darte recomendaciones para armonizar tu vida."
            )

        # “chakras es”, “qué son chakras”
        if (
            ("chakr" in q and ("es" in q or "significa" in q or "qué es" in q or "qué son")) 
            or q.strip() == "chakras"
        ):
            return (
                "Los chakras son centros energéticos que reflejan distintos aspectos de tu destino y energía. "
                "En la Matriz del Destino analizamos 7 chakras. ¿Quieres saber cómo se manifiestan en ti? "
                "Introduce tu fecha de nacimiento en la calculadora — ¡y obtendrás tu análisis!"
            )
        # “qué necesito”, “cómo obtener consulta”, “cómo saber mi matriz”
        if (
            "qué necesito" in q
            or "cómo obtener consulta" in q
            or "cómo saber mi matriz" in q
            or ("necesito" in q and "para esto" in q)
        ):
            return (
                "¡Muy simple! Introduce tu fecha de nacimiento en la calculadora del sitio — y enseguida calcularé tu Matriz del Destino, te contaré sobre tus chakras y energías, y te daré recomendaciones."
            )

        if (
            ("si" in q and "fecha" in q and "introdu" in q)
            or ("qué" in q and "sabr" in q and "fecha" in q)
            or ("qué pasará" in q and "fecha" in q)
            or ("qué obtengo" in q and "fecha" in q)
        ):
            return (
                "Si introduces tu fecha de nacimiento, ¡calcularé tu Matriz del Destino individual! "
                "Conocerás el significado de tus energías y chakras, recibirás recomendaciones y comprenderás mejor tus fortalezas y tareas de vida. "
                "¡Pruébalo — es interesante y útil!"
            )

        # Precio
        if "cuánto cuesta" in q or "precio" in q or "coste" in q or "costo" in q:
            return (
                "El precio de la consulta está indicado en el sitio junto a la calculadora. "
                "Si tienes preguntas sobre el pago — ¡escríbeme y te ayudo!"
            )
        # Pago
        if "cómo pagar" in q or "pago" in q or "pagar" in q:
            return (
                "Puedes pagar la consulta directamente en el sitio después del cálculo de tu Matriz del Destino. "
                "Sigue las indicaciones de la calculadora — ¡todo es simple y seguro!"
            )
        # Seguridad de datos
        if "segurid" in q and ("datos" in q or "pago" in q):
            return (
                "Tus datos están protegidos y se usan solo para el cálculo de la Matriz del Destino. "
                "El pago se procesa mediante un servicio de pago seguro."
            )
        # Repetir cálculo / errores
        if "error" in q or "correg" in q or "otra vez" in q or "repet" in q:
            return (
                "Si te equivocaste en la fecha o quieres recalcular — ¡simplemente introduce una nueva fecha en la calculadora!"
            )
        # Cuándo llega el resultado
        if "cuándo" in q and ("resultado" in q or "respuesta" in q or "consulta" in q):
            return "El resultado lo recibirás inmediatamente tras el pago — aparecerá en el chat y estará disponible para descargar."
        # Soporte
        if "soporte" in q or "contactar" in q or "ayuda" in q:
            return "Si tienes dudas o dificultades — escribe al soporte mediante el formulario del sitio o en el chat. ¡Siempre estamos listos para ayudar!"

        # Respuestas a “sí, quiero”, “cuenta”, “más detalles”
        if (
            q in ["sí quiero", "cuenta", "quiero más", "sí, quiero", "sí, cuéntame", "sí", "cuéntame más"]
            or ("quiero" in q and ("más" in q or "saber" in q))
        ):
            return (
                "¡Genial! ¿Sobre qué chakra quieres saber más?\n"
                "Puedo contarte sobre cualquiera de los 7 — escribe su nombre, por ejemplo: 'Anahata' o 'Manipura'.\n"
                "O introduce tu fecha de nacimiento — ¡y te contaré cómo se manifiestan en ti!"
            )

        # Detección simple de fecha
        if re.match(r"^\d{2}[\.\-/]?\d{2}[\.\-/]?\d{2,4}$", q):
            return (
                f"¡Gracias! Has introducido la fecha de nacimiento: {query}. "
                "Para obtener un análisis individual, usa la calculadora del sitio — ¡es rápido y cómodo!"
            )

        allowed = [
            "matriz", "energ", "chakr", "fecha", "destino", "cálculo", "consulta",
            "sahasrara", "ajna", "vishuddha",
            "anahata", "manipura", "svadhisthana",
            "muladhara"
        ]
        if any(word in q for word in allowed):
            return await self.ask_gpt(query)

        # Respuesta fallback más amistosa
        return (
            "Soy asesor de la Matriz del Destino y con gusto te ayudaré a saber más sobre tus energías, chakras y tareas de vida. "
            "Por favor, haz una pregunta del tema o introduce tu fecha de nacimiento para un análisis individual."
        )

    async def consult_compatibility_full(self, partner1: dict, partner2: dict) -> str:
        """
        Forma el texto para el chatbot sobre la compatibilidad de dos parejas basado en COMPATIBILITY.json.
        partner1, partner2 — dict con clave 'chakras', donde por cada chakra hay un array de 3 valores.
        """
        # 1. Carga de COMPATIBILITY.json
        compat_path = os.path.join(BASE_API_DIR, 'base', 'COMPATIBILITY.json')
        async with aiofiles.open(compat_path, 'r', encoding='utf-8') as f:
            compat_data = json.loads(await f.read())

        chakras_list = ["ajna", "anahata", "svadhisthana", "manipura", "muladhara", "sahasrara"]
        result_lines = []

        # 2. custom_points (descripciones e interpretaciones por chakras)
        for chakra in chakras_list:
            # Buscar bloque custom_points para este chakra
            block = None
            for item in compat_data.get("custom_points", []):
                if item.get("chakra", "").lower() == chakra:
                    block = item
                    break
            if not block:
                continue

            # Descripción del chakra
            result_lines.append(f"{chakra.capitalize()} — {block.get('description', '')}")

            # Valores para las parejas
            val1 = partner1["chakras"].get(chakra, [None, None, None])[2]
            val2 = partner2["chakras"].get(chakra, [None, None, None])[2]
            val1_str = str(val1) if val1 is not None else "?"
            val2_str = str(val2) if val2 is not None else "?"

            desc1 = block.get(val1_str, "(sin descripción)")
            desc2 = block.get(val2_str, "(sin descripción)")

            result_lines.append(f"Pareja 1: {val1_str} — {desc1}")
            result_lines.append(f"Pareja 2: {val2_str} — {desc2}")
            result_lines.append("")  # línea en blanco para separar

        # 3. recommendations (para anahata, Emociones)
        rec_block = None
        for item in compat_data.get("recommendations", []):
            if item.get("chakra", "").lower() == "anahata" and item.get("aspect", "").lower() == "emociones":
                rec_block = item
                break
        if rec_block:
            result_lines.append("Recomendaciones:")
            for i, partner in enumerate([partner1, partner2], 1):
                val = partner["chakras"].get("anahata", [None, None, None])[2]
                val_str = str(val) if val is not None else "?"
                # Nota: si en tu JSON cambiaste 'плюсы'/'минусы' a 'pros'/'contras', ajusta estas claves:
                plus = rec_block.get(val_str, {}).get("плюсы", "(sin pros)")
                minus = rec_block.get(val_str, {}).get("минусы", "(sin contras)")
                desc = rec_block.get("description", "")
                result_lines.append(f"Pareja {i}: {desc}\nPros: {plus}\nContras: {minus}")
            result_lines.append("")

        # 4. compatibility (para anahata, Emociones)
        comp_block = None
        for item in compat_data.get("compatibility", []):
            if item.get("chakra", "").lower() == "anahata" and item.get("aspect", "").lower() == "emociones":
                comp_block = item
                break
        if comp_block:
            result_lines.append("Compatibilidad por Anahata:")
            result_lines.append(comp_block.get("description", ""))
            v1 = partner1["chakras"].get("anahata", [None, None, None])[2]
            v2 = partner2["chakras"].get("anahata", [None, None, None])[2]
            key1 = f"{v1}-{v2}"
            key2 = f"{v2}-{v1}"
            comp = comp_block.get(key1) or comp_block.get(key2)
            if comp:
                result_lines.append(f"Pareja {key1 if comp_block.get(key1) else key2}:")
                # Nota: si en tu JSON cambiaste 'совместимость'/'описание' a 'compatibilidad'/'descripcion', ajusta estas claves:
                result_lines.append(f"Compatibilidad: {comp.get('совместимость', '')}")
                result_lines.append(f"Descripción: {comp.get('описание', '')}")
            else:
                result_lines.append(f"No hay una descripción exacta para la pareja {v1}-{v2}.")
            result_lines.append("")

        return "\n".join(result_lines)
