import yaml
from datetime import datetime as dt
from loguru import logger

from aiogram.utils.text_decorations import markdown_decoration

from models.models import WeeklySchedule, DailySchedule


bells = [
    "08:00",
    "09:30",
    "11:20",
    "12:50",
    "14:20",
    "15:50",
]


def load_schedule_from_yaml(file_path: str) -> WeeklySchedule:
    with open(file_path, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)

    weekly_schedule = WeeklySchedule.parse_obj(yaml_data)

    return weekly_schedule


def escape_md(*content, sep=" "):
    """
    This function escapes prohibited
    symbols in MarkdownV2
    """

    def _join(*content, sep=" "):
        return sep.join(map(str, content))

    return markdown_decoration.quote(_join(*content, sep=sep))


def format_schedule_for_day(daily_schedule: DailySchedule) -> str:
    logger.info(f"Formatting schedule for day: {daily_schedule.day}")
    result = []
    result.append(f"*{escape_md(daily_schedule.day.upper())}:*\n")
    classes = daily_schedule.classes

    for university_class in sorted(classes, key=lambda c: c.class_time.start_time):
        subject = escape_md(university_class.subject.name)
        teacher = escape_md(university_class.subject.teacher.name)
        class_type = escape_md(university_class.class_type.class_type)
        start_time = escape_md(university_class.class_time.start_time.strftime('%H:%M'))
        end_time = escape_md(university_class.class_time.end_time.strftime('%H:%M'))
        classroom = university_class.classroom.room_number

        class_order = bells.index(start_time) + 1

        classroom = f"{escape_md(classroom)} аудиторії" if classroom != "online" else "online"
        class_type = "Лекція" if class_type == "lecture" else "Практика"
        class_type += " в" if classroom != "online" else ""

        teacher_name = escape_md(university_class.subject.teacher.name)
        if university_class.subject.teacher.link:
            teacher = f"[{teacher_name}]({university_class.subject.teacher.link})"
        else:
            teacher = teacher_name

        subgroups_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        subgroups = list(map(lambda s: subgroups_emojis[s.number - 1], university_class.subgroups))
        subgroups = ', '.join(subgroups)
        subgroups = escape_md(subgroups)

        result.append(
            f"*{class_order} пара:* {start_time}\-{end_time}\n"
            f"*{subject}* \- {teacher}\n"
            f"{class_type} {classroom}\n"
            f"*Підгрупи:* {subgroups}")

        result.append("")

    return "\n".join(result)
