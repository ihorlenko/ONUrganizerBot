import yaml
from datetime import datetime as dt

from aiogram import types

from models.models import WeeklySchedule


def load_schedule_from_yaml(file_path: str) -> WeeklySchedule:
    with open(file_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)
    
    weekly_schedule = WeeklySchedule.parse_obj(yaml_data)
    
    return weekly_schedule

