def draw_tree(node, prefix="", is_last=True):
    name = node["чел"]
    children = node["кого он пригласил"]

    if prefix:
        connector = "└─ " if is_last else "├─ "
    else:
        connector = ""
    result = f"{prefix}{connector}{name}\n"
    new_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(children):
        result += draw_tree(child, new_prefix, i == len(children) - 1)

    return result
