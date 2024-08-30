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
