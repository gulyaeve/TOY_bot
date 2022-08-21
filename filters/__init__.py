from aiogram import Dispatcher
from .admin_check import AdminCheck


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminCheck)
