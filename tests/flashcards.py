def rotate(pic: str) -> str:
    return pic[6] + pic[3] + pic[0] + pic[7] + pic[4] + pic[1] + pic[8] + pic[5] + pic[2]


def display(pic: str) -> None:
    result = ''
    for y in range(3):
        for x in range(3):
            result += 'X' if pic[3 * y + x] == '1' else '.'
        result += '\n'
    print(result)


def equiv(pic: str) -> set:
    result = set()
    tmp = pic
    for i in range(3):
        tmp = rotate(tmp)
        result.add(tmp)
    return result


def fits(pic: int) -> bool:
    pic = str(bin(pic))[2:].zfill(9)
    pic = [int(x) for x in pic]
    return (pic[4] == 1) and \
    (2== pic[0] + pic[1] + pic[2]) and \
    (2==  pic[6] + pic[7] + pic[8]) and \
    (2==  pic[0] + pic[3] + pic[6]) and \
    (2==  pic[2] + pic[6] + pic[8])



all_pics = {str(bin(i))[2:].zfill(9) for i in range(2 ** 9) if fits(i)}
print(len(all_pics))

for x in all_pics:
    display(x)