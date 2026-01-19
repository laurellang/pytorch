width = 50 #总长度
width_without = 48 #去掉*后长度

#用户输入字符串
user_input = input("请输入输入小于48个英文字母长度字符串（可中英混合）")

#计算中英文个数
cnt = 0

for char in user_input:
    # 判断是否为中文
    if '\u4e00' <= char <= '\u9fff':
        cnt += 2
    # 判断是否为英文
    elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
        cnt += 1

#写完line
konggel = (width_without - cnt) // 2
kongger = width_without - konggel - cnt
line = ' ' * konggel + user_input + ' ' * kongger

#打印
print('*' * width)
print('*' + ' ' * width_without + '*')
print('*' + ' ' * width_without + '*')
print('*' + line + '*')
print('*' + ' ' * width_without + '*')
print('*' + ' ' * width_without + '*')
print('*' * width)
