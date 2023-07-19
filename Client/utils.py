def mapOptions(option):
    host, port = option
    return f"{port}: {option}\n"

def removeValues(value):
    if value == "":
        return False
    else:
        return True