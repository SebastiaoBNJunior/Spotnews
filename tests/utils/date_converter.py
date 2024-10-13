def date_converter(data):
    partes = data.split('-')
    nova_data = f"{partes[2]}/{partes[1]}/{partes[0]}"
    return nova_data
