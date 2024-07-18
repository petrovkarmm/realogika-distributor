test_user_balance_movement_data = [{'id': 1,
                                    'amount': 100,
                                    'is_accrual': True
                                    },
                                   {
                                       'id': 2,
                                       'amount': 12,
                                       'is_accrual': False
                                   },
                                   {
                                       'id': 3,
                                       'amount': 12,
                                       'is_accrual': False
                                   },
                                   ]

test_full_balance_movement_info = {
    1: {
        'amount': 100,
        'is_accrual': True,
        'date': '12.01.2022',
        'info': 'Наличные.'
    },
    2: {
        'amount': 12,
        'is_accrual': False,
        'date': '24.02.2023',
        'info': 'Выставленный счёт от компании.'
    },
    3: {
        'amount': 12,
        'is_accrual': False,
        'date': '26.06.2024',
        'info': 'Банковская карта.'
    },
}

shop_main_page_data_test = [
    {
        'id': 1,
        'count': 100000,
        'name': 'Доступ к админке',
        'price': 3567,
        'description': 'Статус админа',
        'available': True
    },
    {
        'id': 2,
        'count': 1,
        'name': 'Книга Реалогика',
        'price': 2500,
        'description': 'Описание книги по реалогике.',
        'available': False
    },
    {
        'id': 3,
        'count': 8888888888,
        'name': 'Статус дистрибьютора',
        'price': 15000,
        'description': 'Позволяет стать дистрибьютором.',
        'available': True
    },
]

test_shop_item_details = {
    1: {
        'count': 100000,
        'name': 'Доступ к админке',
        'price': 3567,
        'description': 'Статус админа'
    },
    2: {
        'count': 13,
        'name': 'Книга Реалогика',
        'price': 2500,
        'description': 'Описание книги по реалогике.',
    },
    3: {
        'count': 8888888888,
        'name': 'Статус дистрибьютора',
        'price': 15000,
        'description': 'Позволяет стать дистрибьютором.',
    },
}

test_data = {'action': {'created_at': '2024-06-07T05:52:23',
                        'id': 1,
                        'name': 'Активировать роль',
                        'updated_at': '2024-06-07T05:52:23'},
             'action_id': 1,
             'additional': '1',
             'created_at': '2024-06-07T05:53:15',
             'id': 1,
             'offers': [{'category_id': 1,
                         'count': 1,
                         'created_at': '2024-06-07T05:58:43',
                         'description': 'Купить роль Дистрибьютор',
                         'duration': 30,
                         'exists_reward': True,
                         'gates': '[1,2]',
                         'id': 1,
                         'link_presentation': None,
                         'price': 150000,
                         'product_id': 1,
                         'recurrent': 0,
                         'status': 1,
                         'text_after_payment': 'Спасибо, оплата прошла успешно, доступ вам '
                                               'выдан.\r\n'
                                               'Удачного опыта использования платформы!',
                         'title': 'Купить роль Дистрибьютор',
                         'updated_at': '2024-06-07T05:58:43',
                         'url_image': None}],
             'title': 'Роль Дистрибьютор',
             'updated_at': '2024-06-07T05:53:15'}
