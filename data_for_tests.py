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

shop_main_page_data_test = {
    1: {
        'count': 100000,
        'name': 'Доступ к админке',
        'price': 30000,
        'description': 'Статус админа'
    },
    2: {
        'count': 15,
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
