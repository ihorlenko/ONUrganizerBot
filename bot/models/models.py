import datetime
import yaml
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Set, Literal
from datetime import time, date

Weekday = Literal['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

class Teacher(BaseModel):
    name: str
    link: Optional[str] = None

class Subject(BaseModel):
    name: str
    teacher: Teacher

class ClassTime(BaseModel):
    start_time: time
    end_time: time

class Classroom(BaseModel):
    room_number: Optional[str]

class Subgroup(BaseModel):
    number: int = Field(
        ..., 
        ge=1, 
        le=4, 
        description="Subgroup should be in range 1...4"
    )

class ClassType(BaseModel):
    class_type: Literal['lecture', 'practice']

class UniversityClass(BaseModel):
    subject: Subject
    class_time: ClassTime
    classroom: Classroom
    subgroups: List[Subgroup]
    class_type: ClassType
    date: Optional[datetime.date] = None

class DailySchedule(BaseModel):
    day: Weekday
    classes: List[UniversityClass]

class WeeklySchedule(BaseModel):
    daily_schedules: List[DailySchedule]

    @field_validator('daily_schedules')
    def validate_weekdays(cls, v):
        weekdays = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'}
        schedule_days = {schedule.day for schedule in v}
        if schedule_days != weekdays:
            raise ValueError('Schedule must include all days from Monday to Friday')
        return v


if __name__ == "__main__":

    def load_schedule_from_yaml(file_path: str) -> WeeklySchedule:
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
        
        weekly_schedule = WeeklySchedule.parse_obj(yaml_data)
        
        return weekly_schedule

    schedule = load_schedule_from_yaml('bot/resources/schedule.yaml')
    print(schedule.daily_schedules[2])