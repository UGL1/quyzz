def rotate(pic: str) -> str:
    return pic[2] + pic[0] + pic[3] + pic[1]


def equivalents(pic: str) -> set[str]:
    return {rotate(pic), rotate(rotate(pic)), rotate(rotate(rotate(pic)))}


def display(pic: str) -> None:
    result = ''
    for y in range(2):
        for x in range(2):
            result += 'X' if pic[2 * y + x] == '1' else '.'
        result += '\n'
    print(result)


all_pics = [str(bin(i))[2:].zfill(4) for i in range(2 ** 4)]

remaining = list(all_pics)

for i in range(len(all_pics)):
    x = all_pics[i]
    print("On examine")
    display(x)
    if x in equivalents(x):
        print("On le retire car il est symétrique")
        for y in equivalents(x):
            if y in remaining:
                print("*")
                remaining.remove(y)
    else:
        print("Il n'est pas symétrique")

print(remaining)
