"""
removes 0 from dict
"""
def get_dict_of_used_currencies(curr):
    return {k: v for k, v in curr.items() if v != 0}
if __name__ == '__main__':
    d = {'foo': 0, 'bar': 1, 'baz': 0}
    d = get_dict_of_used_currencies(d)
    print(d)