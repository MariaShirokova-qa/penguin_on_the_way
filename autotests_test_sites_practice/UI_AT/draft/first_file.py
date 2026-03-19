
# s = 1000
#
# while 1000 <= s >= 2000:
#     if s > 0:
#         print('s')
#         s +=1
#


digs = [4, 3, 100, -53, -30, 1, 34, -8]
for i in range(len(digs)):
    num = digs[i]
    # Проверяем: двузначное ли число? (от -99 до -10 и от 10 до 99)
    if (10 <= abs(num) <= 99):
        digs[i] = 0
print(digs)