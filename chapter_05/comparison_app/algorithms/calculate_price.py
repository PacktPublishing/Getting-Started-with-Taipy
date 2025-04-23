def calculate_price(buying_price, margin, vat_tax):
    final_price = buying_price * margin * vat_tax
    print(f"final price is: {final_price}")

    return final_price
