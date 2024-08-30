from pprint import pprint


def draw_tree(node, prefix="", is_last=True):
    name = node["чел"]
    if name is None:
        name = "<b>БЫЧИЙ КОРЕНЬ</b>"
    elif name == "Я":
        name = "<b>Я</b>"
    if prefix:
        connector = "└─ " if is_last else "├─ "
    else:
        connector = ""

    result = f"{prefix}{connector}{name}\n"

    new_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(node["кого он пригласил"]):
        result += draw_tree(child, new_prefix, i == len(node["кого он пригласил"]) - 1)

    return result


def form_invoice_data(customer_code: int, request_data: dict):
    data = {
        "Data": {
            "customerCode": customer_code,
            "amount": f"{int(float(request_data.get('amount', 0)))}.00",
            "purpose": (
                            "test1\n"
                            "test2"
                       )[:140],
            "paymentMode": [
                "sbp",
                "card"
            ],
        }
    }
    return data


def main():
    import requests
    import json

    request_data = {
        'amount': 150,
        'email': 'petrovleonid1999@mail.ru',
        'name': 'Петров Леонид Алексеевич',
        'company': 'bot2.biz',
        'product': 'Кружка пива.'
    }

    customer_code = 302755177
    jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJrYVlSdXB6WjNrVjhVOUZNRk1SSVQ0R0E0c2J6NzZHMiJ9.oUD6ircAozsxxX-nkcBi3SpSvC3TxvcUw7DI9tCgapEYtyC8kxv3Yqzu_fbce3_QCXSuB05ocbW6iJGTgMSdTRky23jWBIBzPeLLIyLvM4w2I_Kkq_GvByZa7gXgZDEODexjos8vXRtqQ-zLEqvuL-wUbZoHkkG1mkPM08PEbw7XVbkmOEhauvTAy3NSu9qFV2AhvGj2Ngxin-B4vKqWI51qMAgka1o2HMjwSntv2NKz_bIQBwfJXBbCOZJu0xYN2tA-rnQwlCR-xCNHN0VSOkmqoRVmH8reHZOJ_3knZzWM49weKF-m3w_4r2zvTTpvssYMW2RVqYOcdeg7D8egv2gE97L9At4RWVZGQKzWWlaOU3vyS5hIw9XM5nWF-F6jt3ZWnoQGCFQ_9h4fqPjpxS5ANKbIBXKGg7JfmgYOz9sARVTKJz_3_KuOjdV85_dGQLVOb6Eei9GLVCaV2nx7_psu98TvAqysHzSH1jpMxJlCkRXNsXVggx1-aFPCBwAo"

    data = form_invoice_data(customer_code=customer_code, request_data=request_data)

    url = 'https://enter.tochka.com/uapi/acquiring/v1.0/payments'
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Content-Type': 'application/json'
    }
    pprint(json.dumps(data))
    pprint(headers)
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Обработка ответа
    if response.status_code == 200:
        print("Успешно:", response.json())
    else:
        print("Ошибка:", response.status_code, response.text)


main()
