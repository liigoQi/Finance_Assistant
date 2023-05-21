def bullet_format(string):
    if '•' in string:
        notes = string.split('•')
        tmp = ""
        for note in notes[1:]:
            tmp = tmp + '\n•  ' + note + '\n'
        return tmp
    if '-' in string:
        notes = string.split('-')
        tmp = ""
        for note in notes[1:]:
            tmp = tmp + '\n•  ' + note + '\n'
        return tmp
    return string 