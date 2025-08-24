from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    full_name = State()
    date_birth = State()
    number = State()
    
    
class UserApplications(StatesGroup):
    service = State()
    description = State()
    technologies = State()
    deadline = State()
    
    
class UserMailing(StatesGroup):
    message = State()
