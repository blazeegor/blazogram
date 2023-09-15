from blazogram import Router
from blazogram.types import Message
from blazogram.filters import Command, StateFilter
from blazogram.fsm import FSMContext, State


router = Router()


class MyStatesGroup:
    state = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer('<b>Hello!</b>')
    await state.set_state(MyStatesGroup.state)
    await state.update_data(NAME='NAME')


@router.message(StateFilter(MyStatesGroup.state))
async def test_func(message: Message, state: FSMContext):
    await message.answer('<b>Отлично!</b>')
    print((await state.get_data()).get('NAME'))
    await state.clear()