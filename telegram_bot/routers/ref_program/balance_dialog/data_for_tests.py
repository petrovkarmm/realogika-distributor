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
        'amount': 100,
        'is_accrual': True,
        'date': '26.06.2024',
        'info': 'Банковская карта.'
    },
}
