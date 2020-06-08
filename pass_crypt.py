def pass_crypt(o_pass: str, stored_pass=None):
    new_pass = []
    for i in o_pass:
        new_pass.append(ord(i) + len(o_pass))

    crypted_pass = '.'.join([str(x) for x in new_pass[::-1]])
    if stored_pass:
        return crypted_pass == stored_pass
    return crypted_pass


password = input()
print(pass_crypt(password))
print(pass_crypt(password, '53.53.53.53'))  # encryption for '1111'
