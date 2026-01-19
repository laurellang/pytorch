try:
    n = int(input("请输入一个小于9的数字n："))

except ValueError:
    print("无效输入，请输入一个整数。")
    
else:
    #检查输入是否符合要求
    if n > 9:
        print("数字过大，请输入小于9的数字。")
    elif n <= 0:
        print("数字过小，请输入大于0的数字。")
        
    else:
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                print(f"{j}x{i} = {j * i}", end = "  ")
            print()
            
        
