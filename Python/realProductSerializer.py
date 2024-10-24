import json
import dictionarySorter

def serialize_real_products_to_json(real_products):
    real_products_json = []

    for key in real_products:
        real_product = real_products[key]
        serialized_real_product = real_product.to_json()
        real_product_json_data = json.loads(serialized_real_product)
        real_products_json.append(real_product_json_data)

    real_products_json = dictionarySorter.sort(real_products_json, "score")
    return real_products_json