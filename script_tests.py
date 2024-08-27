def draw_tree(node, prefix="", is_last=True):
    name = node["чел"]
    children = node["кого он пригласил"]

    # Определяем префикс для текущего узла
    if prefix:
        connector = "└─ " if is_last else "├─ "
    else:
        connector = ""

    # Формируем строку для текущего узла
    result = f"{prefix}{connector}{name}\n"

    # Новый префикс для потомков
    new_prefix = prefix + ("   " if is_last else "│  ")

    # Рекурсивно добавляем строки для всех потомков
    for i, child in enumerate(children):
        result += draw_tree(child, new_prefix, i == len(children) - 1)

    return result
