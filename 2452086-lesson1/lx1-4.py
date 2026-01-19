def number_black_hole_6174(number):
    """
    展示6174数字黑洞：对任意四位数（各位数字不全相同），
    通过最大数-最小数的操作，最终收敛到6174
    """
    steps = []
    
    while number != 6174:
        # 将数字转换为字符串并补齐到4位
        num_str = str(number).zfill(4)
        
        # 获取组成数字的列表并排序
        digits = sorted([int(d) for d in num_str])
        
        # 构造最大数和最小数
        max_num = int(''.join(map(str, digits[::-1])))
        min_num = int(''.join(map(str, digits)))
        
        # 计算差值
        number = max_num - min_num
        
        # 格式化输出，确保所有数字显示为4位
        max_str = str(max_num).zfill(4)
        min_str = str(min_num).zfill(4)
        diff_str = str(number).zfill(4)
        
        # 记录步骤
        steps.append(f"{max_str} - {min_str} = {diff_str}")
        
        # 如果数字不足4位，补零
        number = int(str(number).zfill(4))
    
    return steps

def main():
    # 获取用户输入
    try:
        num = int(input("输入4位数字："))
        if num < 1000 or num > 9999:
            print("错误：请输入一个1000到9999之间的四位数字！")
            return
        if len(set(str(num))) == 1:
            print("警告：输入的数字各位相同，将收敛到0而非6174！")
        
        steps = number_black_hole_6174(num)
        for step in steps:
            print(step)
        print("6174")
        
    except ValueError:
        print("错误：请输入有效的整数！")

if __name__ == "__main__":
    main()