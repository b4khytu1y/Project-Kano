from aiogram import Router, types
from aiogram.filters import Command

from utils import add_task, get_user_tasks

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я Kano, твой помощник. Добавь задачи командой /addtask.')


@router.message(Command('addtask'))
async def cmd_addtask(message: types.Message):
    task = message.get_args()
    if not task:
        await message.answer('Использование: /addtask <задача>')
        return
    add_task(message.from_user.id, task)
    await message.answer('Задача добавлена!')


@router.message(Command('tasks'))
async def cmd_tasks(message: types.Message):
    tasks = get_user_tasks(message.from_user.id)
    if not tasks:
        await message.answer('У тебя пока нет задач.')
        return
    text = '\n'.join(f'- {t}' for t in tasks)
    await message.answer(f'Твои задачи:\n{text}')


@router.message()
async def emotional_support(message: types.Message):
    text = message.text.lower()
    if 'я устал' in text or 'мне грустно' in text:
        await message.answer('Держись! Ты справишься, я в тебя верю!')
