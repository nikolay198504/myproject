import os
import json
import aiofiles
from typing import List, Dict, Any
from dotenv import load_dotenv
import openai

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
BASE_API_DIR = os.getenv("API_BASE_DIR")
if BASE_API_DIR is None:
    BASE_API_DIR = os.path.dirname(os.path.abspath(__file__))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Chunk:
    """
    Класс для работы с консультациями по Матрице Судьбы, включая генерацию текстов по правилам и интеграцию с OpenAI.
    """
    def __init__(self):
        """
        Инициализация класса Chunk.
        """
        print("[DEBUG] Chunk init: Правка для consult_personal — теперь используется computed_data.")

    async def get_rules_json(self) -> dict:
        """
        Асинхронно загружает и возвращает содержимое файла Rules.json с описаниями энергий и аспектов.

        Returns:
            dict: Словарь с правилами для трактовки энергий.
        Raises:
            FileNotFoundError: Если файл не найден.
        """
        rules_path = os.path.join(BASE_API_DIR, 'base', 'Rules.json')
        if not os.path.exists(rules_path):
            raise FileNotFoundError(f"Файл {rules_path} не найден.")
        async with aiofiles.open(rules_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        return json.loads(content)

    # Сопоставление (chakra, aspect) -> point_name для custom_points
    CHAKRA_ASPECT_TO_POINT = {
        ("Muladhara", "Energía"): "Recurso interior",
        ("Ajna", "Energía"): "Talento",
        ("Anahata", "Emociones"): "Zona de confort",
        ("Muladhara", "Física"): "Cola kármica general",
        ("Svadhisthana", "Emociones"): "Cola kármica del amor",
        ("Anahata", "Energía"): "Amor y dinero",
        ("Vishuddha", "Física"): "Dirección de vida profesional",
        ("Manipura", "Energía"): "Fuente de ingresos",
        ("Svadhisthana", "Energía"): "Bloqueo financiero",
        ("Ajna", "Física"): "Energía masculina",
        ("Anahata", "Física"): "Energía femenina",
    }

    async def consult_personal(self, free_points: List[Dict[str, Any]]) -> str:
        """
        Формирует текстовую консультацию по свободным точкам на основе правил из Rules.json (custom_points).
        Теперь выводит сначала описание точки (description), затем индивидуальную трактовку.
        """
        rules = await self.get_rules_json()
        lines = []
        for point in free_points:
            chakra = point.get("chakra")
            aspect = point.get("aspect")
            val = point.get("value")
            val_str = str(val)
            point_name = self.CHAKRA_ASPECT_TO_POINT.get((chakra, aspect))
            if not point_name:
                lines.append(f"{chakra} - {aspect} - {val}:\n(Нет описания)")
                continue
            point_block = rules.get("custom_points", {}).get(point_name)
            if not point_block:
                lines.append(f"{point_name} ({val}):\n(Нет описания)")
                continue
            description = point_block.get("description", "")
            value_text = point_block.get("values", {}).get(val_str)
            if value_text:
                lines.append(f"{point_name} ({val}):\n{description}\n{value_text}")
            else:
                lines.append(f"{point_name} ({val}):\n{description}\n(Нет описания)")
        return "\n\n".join(lines)

    async def consult_paid(self, points: List[Dict[str, Any]], date: str = None) -> str:
        """
        Формирует расширенную консультацию по точкам с возможностью указания даты (custom_points).
        Теперь, если в точке нет поля name, точка пропускается (никакой fallback по chakra+aspect).
        """
        print("DEBUG paidPoints:", points)  # В начало функции
        rules = await self.get_rules_json()
        lines = []
        for point in points:
            point_name = point.get("name")
            val = point.get("value")
            val_str = str(val)
            if point_name:
                point_block = rules.get("custom_points", {}).get(point_name)
                if not point_block:
                    lines.append(f"{point_name} ({val}):\n(Нет описания)")
                    continue
                description = point_block.get("description", "")
                value_text = point_block.get("values", {}).get(val_str)
                if value_text:
                    lines.append(f"{point_name} ({val}):\n{description}\n{value_text}")
                else:
                    lines.append(f"{point_name} ({val}):\n{description}\n(Нет описания)")
            # Если нет имени, точка пропускается
            # continue
        print("DEBUG lines:", lines)  # Перед формированием final_text
        final_text = "\n\n".join(lines)
        print("DEBUG final_text:", final_text)  # Перед return
        if date:
            final_text = f"Расширенная интерпретация для даты {date}:\n\n{final_text}"
        return final_text

    async def consult_compatibility(self, computed_personal: str, computed_compatibility: str) -> str:
        """
        Генерирует консультацию по совместимости на основе персональных и совместимых данных.

        Args:
            computed_personal (str): Персональные данные.
            computed_compatibility (str): Данные по совместимости.

        Returns:
            str: Текст консультации (пока не реализовано).
        """
        return "Пока не реализовано: consult_compatibility."

    async def ask_gpt(self, user_text: str) -> str:
        """
        Отправляет вопрос к OpenAI GPT и возвращает ответ, ограниченный тематикой Матрицы Судьбы.

        Args:
            user_text (str): Вопрос пользователя.

        Returns:
            str: Ответ языковой модели или сообщение об ошибке.
        """
        prompt = (
            "Ты — консультант по Матрице Судьбы. "
            "Отвечай только на вопросы по Матрице Судьбы, энергиям, чакрам, дате рождения, трактовкам. "
            "Чакры, которые используются в Матрице Судьбы:\n"
            "— Sahasrara (Сахасрара): чакра высшего сознания, связь с высшими смыслами.\n"
            "— Ajna (Аджна): чакра интуиции, внутреннего видения и мудрости.\n"
            "— Vishuddha (Вишудха): чакра коммуникации, самовыражения и честности.\n"
            "— Anahata (Анахата): чакра любви, гармонии и сострадания.\n"
            "— Manipura (Манипура): чакра воли, самооценки и личной силы.\n"
            "— Svadhisthana (Свадхистхана): чакра эмоций, творчества и удовольствия.\n"
            "— Muladhara (Муладхара): чакра стабильности, безопасности и жизненной энергии.\n"
            "Если пользователь спрашивает о значении или роли любой из этих чакр — отвечай кратко по описанию выше.\n"
            "Если пользователь хочет узнать подробнее о себе, своей матрице или энергиях — предложи воспользоваться калькулятором для расчёта по дате рождения.\n"
            "Если вопрос не по теме — напиши: 'Я могу отвечать только на вопросы по Матрице Судьбы, энергиям и консультациям по дате рождения.'"
        )
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_text}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print("Ошибка в ask_gpt:", e)
            return "Извините, произошла ошибка при обращении к языковой модели. Попробуйте позже."

    async def get_answer_async(self, query: str) -> str:
        """
        Обрабатывает пользовательский запрос: приветствия, благодарности, тематические вопросы.
        Для тематических вопросов вызывает ask_gpt.

        Args:
            query (str): Входящий текстовый запрос пользователя.

        Returns:
            str: Ответ на запрос.
        """
        q = query.lower().strip()
        greetings = [
            "привет", "здравствуйте", "добрый день", "добрый вечер", "hello", "hi", "хай", "доброго времени суток"
        ]
        farewells = [
            "пока", "до свидания", "bye", "goodbye", "до встречи", "увидимся", "спокойной ночи"
        ]
        thanks = [
            "спасибо", "благодарю", "thank you", "мерси", "спс", "спасибо большое"
        ]

        if any(word in q for word in greetings):
            return "Здравствуйте! Я консультант по Матрице Судьбы. Могу рассчитать вашу матрицу, объяснить значения энергий и дать рекомендации. Просто введите вашу дату рождения в калькулятор!"
        if any(word in q for word in farewells):
            return "Всего доброго! Если будут вопросы по Матрице Судьбы — обращайтесь."
        if any(word in q for word in thanks):
            return "Пожалуйста! Если нужна консультация по Матрице Судьбы — я всегда на связи."
        if "что ты можешь" in q or "что умеешь" in q or "твои возможности" in q or "кто ты" in q:
            return "Я — консультант по Матрице Судьбы. Могу рассчитать вашу матрицу, объяснить значения энергий и дать рекомендации. Просто введите вашу дату рождения в калькулятор!"

        # Вот сюда добавьте:
        allowed = [
            "матрица", "энерг", "чакр", "дата", "судьб", "расчёт", "консультац",
            "sahasrara", "сахасрара", "ajna", "аджна", "vishuddha", "вишудха",
            "anahata", "анахата", "manipura", "манипура", "svadhisthana", "свадхистхана",
            "muladhara", "муладхара"
        ]
        if any(word in q for word in allowed):
            return await self.ask_gpt(query)

        return "Я могу отвечать только на вопросы по Матрице Судьбы, энергиям и консультациям по дате рождения."