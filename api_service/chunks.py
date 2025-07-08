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
        Формирует текстовую консультацию по свободным точкам на основе правил из Rules.json (custom_points).
        Теперь выводит сначала описание точки (description), затем индивидуальную трактовку.
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
                lines.append(f"{chakra} - {aspect} - {val}:\n(Нет описания)")
                continue
            point_block = rules.get("custom_points", {}).get(point_name)
            if not point_block:
                lines.append(f"{point_name} ({val}):\n(Нет описания)")
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
                value_full = "(Нет описания)"
            if value_full:
                lines.append(f"{point_name} ({val}):\n{description}\n{value_full}")
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
                    value_full = "(Нет описания)"
                if value_full:
                    lines.append(f"{point_name} ({val}):\n{description}\n{value_full}")
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

    async def consult_compatibility(self, computed_personal: str, computed_compatibility: str, stage: str = "start") -> str:
        """
        Генерирует консультацию по совместимости на основе персональных и совместимых данных.
        stage: "start" — первый вопрос, "offer_paid" — предложение платного расчёта.
        """
        if stage == "start":
            return "Готов узнать о consult_compatibility (платно)?"
        elif stage == "offer_paid":
            return "Хочешь углублённый расчёт совместимости (платно)?\nДа\nНет"
        # дальше — обработка платного сценария

    async def ask_gpt(self, user_text: str) -> str:
        """
        Отправляет вопрос к OpenAI GPT и возвращает ответ, ограниченный тематикой Матрицы Судьбы.

        Args:
            user_text (str): Вопрос пользователя.

        Returns:
            str: Ответ языковой модели или сообщение об ошибке.
        """
        prompt = (
            "Ты — дружелюбный и вовлекающий консультант по Матрице Судьбы. "
            "Отвечай на вопросы пользователя по теме матрицы, энергий, чакр, даты рождения. "
            "Пиши простым, понятным языком, добавляй примеры, вовлекай пользователя, предлагай воспользоваться калькулятором на сайте. "
            "Если вопрос не по теме — мягко объясни, что ты консультант по Матрице Судьбы. "
            "\n\n"
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
        )
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

        # Новая обработка для общих вопросов про чакры
        if (
            "что такое чакр" in q or
            "расскажи про чакр" in q or
            "что ты знаешь про чакр" in q or
            "знаешь про чакр" in q or
            "объясни чакр" in q or
            "про чакр" in q or
            ("чакр" in q and ("что это" in q or "что значит" in q or "объясни" in q or "расскажи" in q))
        ):
            return (
                "Чакры — это энергетические центры, которые мы анализируем в вашей Матрице Судьбы. "
                "В нашей системе используются 7 чакр: Сахасрара, Аджна, Вишудха, Анахата, Манипура, Свадхистхана, Муладхара. "
                "Каждая из них отвечает за определённые аспекты вашей судьбы и энергии. "
                "Хотите узнать подробнее о какой-то из них или рассчитать свою матрицу?"
            )

        # Новая обработка для вопросов "какие чакры есть"
        if "какие чакр" in q:
            return (
                "В Матрице Судьбы используются 7 чакр:\n"
                "— Сахасрара\n"
                "— Аджна\n"
                "— Вишудха\n"
                "— Анахата\n"
                "— Манипура\n"
                "— Свадхистхана\n"
                "— Муладхара\n"
                "Каждая из них отвечает за определённые аспекты вашей судьбы и энергии. "
                "Хотите узнать подробнее о какой-то из них?"
            )
        # Новая обработка для вопросов "сколько чакр"
        if "сколько чакр" in q or "число чакр" in q or ("чакр" in q and "сколько" in q):
            return (
                "В Матрице Судьбы анализируется 7 чакр: Сахасрара, Аджна, Вишудха, Анахата, Манипура, Свадхистхана, Муладхара."
            )
        # Новая обработка для вопросов "список чакр"
        if "список чакр" in q or ("чакр" in q and "список" in q):
            return (
                "Список 7 чакр в Матрице Судьбы: Сахасрара, Аджна, Вишудха, Анахата, Манипура, Свадхистхана, Муладхара."
            )
        # Новая обработка для вопросов "какие энергии есть"
        if "какие энерг" in q or "что за энерг" in q or "список энерг" in q:
            return (
                "В Матрице Судьбы используются 22 энергии (аркана). Каждая энергия имеет своё значение и влияет на разные сферы жизни. "
                "Для индивидуального разбора просто введите вашу дату рождения в калькулятор!"
            )
        # Новая обработка для вопросов "22 энергии" и "сколько энергий"
        if "22 энергии" in q or ("энергии" in q and "сколько" in q):
            return (
                "В Матрице Судьбы используются 22 энергии (аркана). Каждая из них имеет своё значение и влияет на разные сферы жизни. "
                "Для индивидуального разбора просто введите вашу дату рождения в калькулятор!"
            )
        # Новая обработка для вопросов "что значит консультация по дате рождения"
        if "что значит консультация" in q or "что такое консультация" in q or ("консультация" in q and "что" in q):
            return (
                "Консультация по дате рождения — это индивидуальный разбор вашей Матрицы Судьбы. "
                "Я могу рассчитать вашу матрицу, объяснить значения энергий и чакр, которые связаны с вашей датой рождения, и дать рекомендации для гармонизации жизни."
            )

        # Новая обработка для вопросов "чакры это", "что такое чакры", "что значит чакры"
        if (
            ("чакр" in q and ("это" in q or "значит" in q or "что такое" in q or "что это" in q))
            or q.strip() == "чакры"
        ):
            return (
                "Чакры — это энергетические центры, которые отражают разные аспекты вашей судьбы и энергии. "
                "В Матрице Судьбы мы анализируем 7 чакр. Хотите узнать, как они проявляются именно у вас? "
                "Просто введите вашу дату рождения в калькулятор — и получите индивидуальный разбор!"
            )
        # Новая обработка для вопросов "что нужно для этого", "как получить консультацию", "как узнать свою матрицу"
        if (
            "что нужно для этого" in q
            or "как получить консультац" in q
            or "как узнать свою матрицу" in q
            or ("нужно" in q and "для этого" in q)
        ):
            return (
                "Всё очень просто! Просто введите вашу дату рождения в калькулятор на сайте — и я сразу рассчитаю вашу Матрицу Судьбы, расскажу о ваших чакрах и энергиях, и дам индивидуальные рекомендации."
            )

        if (
            ("если" in q and "дат" in q and "введ" in q)
            or ("что" in q and "узна" in q and "дат" in q)
            or ("что будет" in q and "дат" in q)
            or ("что получ" in q and "дат" in q)
        ):
            return (
                "Если вы введёте свою дату рождения, я рассчитаю вашу индивидуальную Матрицу Судьбы! "
                "Вы узнаете значения своих энергий и чакр, получите персональные рекомендации и сможете глубже понять свои сильные стороны и жизненные задачи. "
                "Попробуйте — это интересно и полезно!"
            )

        # Вопросы о стоимости
        if "сколько стоит" in q or "цена" in q or "стоимость" in q:
            return (
                "Стоимость консультации указана на сайте рядом с калькулятором. "
                "Если у вас есть вопросы по оплате — напишите, я помогу!"
            )
        # Вопросы об оплате
        if "как оплатить" in q or "оплата" in q or "оплатить" in q:
            return (
                "Оплатить консультацию можно прямо на сайте после расчёта вашей Матрицы Судьбы. "
                "Следуйте подсказкам калькулятора — всё просто и безопасно!"
            )
        # Вопросы о безопасности данных
        if "безопасн" in q and ("данн" in q or "оплат" in q):
            return (
                "Ваши данные надёжно защищены и используются только для расчёта Матрицы Судьбы. "
                "Оплата проходит через защищённый платёжный сервис."
            )
        # Вопросы о повторном расчёте или ошибках
        if "ошиб" in q or "исправ" in q or "ещё раз" in q or "повтор" in q:
            return (
                "Если вы ошиблись в дате или хотите рассчитать матрицу ещё раз — просто введите новую дату рождения в калькулятор!"
            )
        # Вопросы о времени получения результата
        if "когда" in q and ("результат" in q or "ответ" in q or "консультац" in q):
            return (
                "Результат вы получите сразу после оплаты — он появится в чате и будет доступен для скачивания!"
            )
        # Вопросы о поддержке
        if "поддержк" in q or "связаться" in q or "помощь" in q:
            return (
                "Если у вас возникли вопросы или сложности — напишите в поддержку через форму на сайте или в чат. Мы всегда готовы помочь!"
            )

        # Ответы на "да хочу", "расскажи", "хочу подробнее" после вопроса о чакрах
        if (
            q in ["да хочу", "расскажи", "хочу подробнее", "да, хочу", "да, расскажи", "да", "расскажи подробнее"]
            or ("хочу" in q and ("подробнее" in q or "узнать" in q))
        ):
            return (
                "Отлично! О какой чакре вы хотите узнать подробнее?\n"
                "Могу рассказать про любую из 7 чакр — просто напишите её название, например: 'Анахата' или 'Манипура'.\n"
                "Или введите вашу дату рождения — и я расскажу, как чакры проявляются именно у вас!"
            )

        # Обработка ввода даты рождения
        if re.match(r"^\d{2}[\.\-/]?\d{2}[\.\-/]?\d{2,4}$", q):
            return (
                f"Спасибо! Вы ввели дату рождения: {query}. "
                "Чтобы получить индивидуальный разбор, воспользуйтесь калькулятором на сайте — это быстро и удобно!"
            )

        allowed = [
            "матрица", "энерг", "чакр", "дата", "судьб", "расчёт", "консультац",
            "sahasrara", "сахасрара", "ajna", "аджна", "vishuddha", "вишудха",
            "anahata", "анахата", "manipura", "манипура", "svadhisthana", "свадхистхана",
            "muladhara", "муладхара"
        ]
        if any(word in q for word in allowed):
            return await self.ask_gpt(query)

        # Более дружелюбный fallback-ответ
        return (
            "Я консультант по Матрице Судьбы и с радостью помогу вам узнать больше о ваших энергиях, чакрах и жизненных задачах! "
            "Пожалуйста, задайте вопрос по теме или введите вашу дату рождения для индивидуального разбора."
        )

    async def consult_compatibility_full(self, partner1: dict, partner2: dict) -> str:
        """
        Формирует текст для чат-бота по совместимости двух партнёров на основе COMPATIBILITY.json.
        partner1, partner2 — dict с ключом 'chakras', где по каждой чакре массив из 3 значений.
        """
        # 1. Загрузка COMPATIBILITY.json
        compat_path = os.path.join(BASE_API_DIR, 'base', 'COMPATIBILITY.json')
        async with aiofiles.open(compat_path, 'r', encoding='utf-8') as f:
            compat_data = json.loads(await f.read())

        chakras_list = ["ajna", "anahata", "svadhisthana", "manipura", "muladhara", "sahasrara"]
        result_lines = []

        # 2. custom_points (описания и трактовки по чакрам)
        for chakra in chakras_list:
            # Найти блок custom_points для этой чакры
            block = None
            for item in compat_data.get("custom_points", []):
                if item.get("chakra", "").lower() == chakra:
                    block = item
                    break
            if not block:
                continue

            # Описание чакры
            result_lines.append(f"{chakra.capitalize()} — {block.get('description', '')}")

            # Значения для партнёров
            val1 = partner1["chakras"].get(chakra, [None, None, None])[2]
            val2 = partner2["chakras"].get(chakra, [None, None, None])[2]
            val1_str = str(val1) if val1 is not None else "?"
            val2_str = str(val2) if val2 is not None else "?"

            desc1 = block.get(val1_str, "(нет описания)")
            desc2 = block.get(val2_str, "(нет описания)")

            result_lines.append(f"Партнёр 1: {val1_str} — {desc1}")
            result_lines.append(f"Партнёр 2: {val2_str} — {desc2}")
            result_lines.append("")  # пустая строка для разделения

        # 3. recommendations (по anahata, Emociones)
        rec_block = None
        for item in compat_data.get("recommendations", []):
            if item.get("chakra", "").lower() == "anahata" and item.get("aspect", "").lower() == "emociones":
                rec_block = item
                break
        if rec_block:
            result_lines.append("Рекомендации:")
            for i, partner in enumerate([partner1, partner2], 1):
                val = partner["chakras"].get("anahata", [None, None, None])[2]
                val_str = str(val) if val is not None else "?"
                plus = rec_block.get(val_str, {}).get("плюсы", "(нет плюсов)")
                minus = rec_block.get(val_str, {}).get("минусы", "(нет минусов)")
                desc = rec_block.get("description", "")
                result_lines.append(f"Партнёр {i}: {desc}\nПлюсы: {plus}\nМинусы: {minus}")
            result_lines.append("")

        # 4. compatibility (по anahata, Emociones)
        comp_block = None
        for item in compat_data.get("compatibility", []):
            if item.get("chakra", "").lower() == "anahata" and item.get("aspect", "").lower() == "emociones":
                comp_block = item
                break
        if comp_block:
            result_lines.append("Совместимость по Anahata:")
            result_lines.append(comp_block.get("description", ""))
            v1 = partner1["chakras"].get("anahata", [None, None, None])[2]
            v2 = partner2["chakras"].get("anahata", [None, None, None])[2]
            key1 = f"{v1}-{v2}"
            key2 = f"{v2}-{v1}"
            comp = comp_block.get(key1) or comp_block.get(key2)
            if comp:
                result_lines.append(f"Пара {key1 if comp_block.get(key1) else key2}:")
                result_lines.append(f"Совместимость: {comp.get('совместимость', '')}")
                result_lines.append(f"Описание: {comp.get('описание', '')}")
            else:
                result_lines.append(f"Нет точного описания для пары {v1}-{v2}.")
            result_lines.append("")

        return "\n".join(result_lines)