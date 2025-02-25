from typing import Callable, List, Dict

from aiogram import F, types
from aiogram.enums import ContentType
from aiogram_dialog import Window, DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.common import ManagedScroll, Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import StubScroll, Button, Group, NumberedPager, Row, Cancel, Back
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from aiogram.fsm.state import State


class MediaCollector:

    def __init__(self, can_skip: bool, back_button_on: bool = True, button_continue_text: str = 'Продолжить',
                 cancel_button_text: str = '⛔️ Завершить'):
        self.can_skip = can_skip
        self.back_button_on = back_button_on
        self.button_continue_text = button_continue_text
        self.cancel_button_text = cancel_button_text

    def predicate_when_skip(self, data: Dict, widget: Whenable, manager: DialogManager):
        return self.can_skip or manager.dialog_data.get("attachment", [])

    def predicate_when_back(self, data: Dict, widget: Whenable, manager: DialogManager):
        return self.back_button_on

    @staticmethod
    async def on_input_photo(
            message: types.Message,
            widget: MessageInput,
            dialog_manager: DialogManager,
    ):
        dialog_manager.show_mode = ShowMode.EDIT
        dialog_manager.dialog_data.setdefault("attachment", []).append(
            {
                'type': 'photo',
                'context': (message.photo[-1].file_id, message.photo[-1].file_unique_id)
            },
        )

    @staticmethod
    async def on_input_document(
            message: types.Message,
            widget: MessageInput,
            dialog_manager: DialogManager
    ):
        dialog_manager.show_mode = ShowMode.EDIT
        dialog_manager.dialog_data.setdefault("attachment", []).append(
            {
                'type': 'document',
                'context': (message.document.file_id, message.document.file_unique_id),
                'name': message.document.file_name.split('.')[0]
            }
        )

    @staticmethod
    async def on_delete(
            callback_data: types.CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager,
    ):
        scroll: ManagedScroll = dialog_manager.find("pages")
        media_number = await scroll.get_page()
        media = dialog_manager.dialog_data.get("attachment", [])
        del media[media_number]
        if media_number > 0:
            await scroll.set_page(media_number - 1)

    @staticmethod
    async def media_getter(dialog_manager: DialogManager, **kwargs) -> dict:
        scroll: ManagedScroll = dialog_manager.find("pages")
        media_number = await scroll.get_page()
        attachment = dialog_manager.dialog_data.get("attachment", [])
        media_count = len(attachment)
        dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
        if attachment:
            if media_count > 1 and media_count % 10 != 0:
                dialog_manager.show_mode = ShowMode.EDIT
            media_item = attachment[media_number]
            if media_item['type'] == "photo":
                media = MediaAttachment(
                    file_id=MediaId(*media_item["context"]),
                    type=ContentType.PHOTO,
                )
            else:
                media = MediaAttachment(
                    file_id=MediaId(*media_item["context"]),
                    type=ContentType.DOCUMENT,
                )
        else:
            media = MediaAttachment(
                path="images/NotFoundFiles.jpg",
                type=ContentType.PHOTO,
            )
        return {
            "media_count": media_count,
            "media_number": media_number + 1,
            "media": media,
        }

    def __call__(self, state: State, on_chosen_continue: Callable, continue_button_id: str,
                 widgets: List | None = None):

        if widgets is None:
            widgets = []

        return Window(
            *widgets,
            Const("\nПрикрепите нужные вложения (Поддерживаются документы и фотографии)"),
            DynamicMedia(selector="media"),
            StubScroll(id="pages", pages="media_count"),
            Button(Const(self.button_continue_text),
                   id=continue_button_id,
                   on_click=on_chosen_continue,
                   when=self.predicate_when_skip,
                   ),
            Group(
                NumberedPager(scroll="pages", when=F["pages"] > 1),
                width=5,
            ),
            Button(
                Format("🗑️ Открепить вложение #{media_number}"),
                id="del",
                on_click=self.on_delete,
                when="media_count",
            ),
            Row(
                Back(Const('Назад'), when=self.predicate_when_back),
                Cancel(Const(self.cancel_button_text))
            ),
            MessageInput(content_types=[ContentType.PHOTO], func=self.on_input_photo),
            MessageInput(content_types=[ContentType.DOCUMENT], func=self.on_input_document),
            getter=self.media_getter,
            state=state,
        )
