
def validate_address(symbol, address):

    if symbol == "TNBC":
        if len(address) == 64:
            return True

    return False
