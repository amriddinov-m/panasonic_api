from aiogram.fsm.state import StatesGroup, State


class UploadState(StatesGroup):
    send_document = State()
    waiting_for_confirmation = State()
