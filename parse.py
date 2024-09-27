def parsetext(text) -> list[str]:
    return text.split('	')

def getefdose(text, time) -> float:
    return text * 0.4 * 8 * (10 ** -6) * time