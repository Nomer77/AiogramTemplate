import operator
from typing import Callable, Any
from aiogram_dialog.widgets.kbd import Select, Column, Cancel, ScrollingGroup
from aiogram_dialog.widgets.text import Format, Const


class BaseKeyboard:
    def __init__(self, module_name: str):
        self.module_name = module_name

    def column_select_gkbd(
            self,
            on_click: Callable,
            items_key: str
    ) -> Column:
        return Column(
            Select(
                Format("{item[1]}"),
                id=f'{self.module_name}_{items_key}_column',
                item_id_getter=operator.itemgetter(0),
                items=items_key,
                on_click=on_click,
            ),
        )

    def cancel_btn(self, text: str = '⛔️ Завершить', result: Any | None = None) -> Cancel:
        return Cancel(
            Const(text),
            id=f'__cancel__{self.module_name}',
            result=result
        )

    def scroll_group_kbd(self,
                         on_click: Callable,
                         items_key: str,
                         height: int = 10,
                         width: int = 1
                         ) -> ScrollingGroup:
        return ScrollingGroup(
            Select(
                Format("{item[1]}"),
                id=f"{self.module_name}_{items_key}_scroll",
                item_id_getter=operator.itemgetter(0),
                items=items_key,
                on_click=on_click
            ),
            id=f"{self.module_name}_{items_key}_scrolling_group",
            height=height,
            width=width
        )
