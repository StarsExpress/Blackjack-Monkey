from configs.output_config import INCOME_SUB_SCOPES
from configs.input_config import INCOME_DICT
from pywebio.output import put_scope, put_button, popup, put_datatable


def show_income(income_list: list[dict[str, str]]):
    put_button(label=INCOME_DICT['label'], color=INCOME_DICT['color'],
               onclick=lambda: popup(INCOME_DICT['title'],
                                     put_scope(INCOME_SUB_SCOPES['content'],
                                               put_datatable(records=income_list,
                                                             instance_id=f"{INCOME_SUB_SCOPES['content']}_table",
                                                             column_order=INCOME_SUB_SCOPES['columns'],
                                                             theme='balham', scope=INCOME_SUB_SCOPES['content'])
                                               ),
                                     INCOME_DICT['size'], True),
               scope=INCOME_SUB_SCOPES['income'])
