def change_table_style(table_html, html_class="text-center thead-light"):
    return table_html.replace("<thead>", f"<thead class='{html_class}>'")


def change_table_align(table_html, align="center"):
    return table_html.replace("text-align: right;", f"text-align: {align};")
