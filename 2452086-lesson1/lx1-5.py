import turtle
import random

#创建画笔
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

#构造设置随机颜色函数
def ran_col():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    # 设置画笔颜色为RGB值
    pen.pencolor(red, green, blue)  
    
#画一条射线
def draw_ray(start_x, start_y, angle, length):
 
    #移动到起点
    pen.penup()
    pen.goto(start_x, start_y)
    pen.pendown()
    
    # 箭头左半部分
    pen.left(150)
    pen.forward(15)
    pen.backward(15)  # 回到起点
    
    # 箭头右半部分
    pen.right(300) 
    pen.forward(15)
    pen.backward(15)  # 回到起点
    
    # 恢复射线方向，绘制射线主体（从起点延伸）
    pen.setheading(angle)
    pen.forward(length)
    
    #绘制射线线段
    pen.setheading(angle)
    pen.forward(length)
    
#画一个射线星图   
'''一个射线星图的：射线个数、每条射线的长度，每条射线的角度都是随机的'''
def ray_star(start_x, start_y):
    #设定随机值
    num = random.randint(25, 50) #每个星图的射线数量
    ran_col()
    pen.pensize(random.randint(1, 4))
    
    for i in range(num):
        angle = random.randint(0, 360)
        length = random.randint(1, 100)
        draw_ray(start_x, start_y, angle, length)
        
def main():
    #创建画布
    screen = turtle.Screen()
    screen.bgcolor('black')
    screen.title("射线星图")
    screen.setup(width = 800, height = 600)
    turtle.colormode(255)
    
    #设置坐标范围
    min_x, max_x = -300, 300
    min_y, max_y = -150, 150
    
    times = random.randint(5, 11) #5-10个射线星图
    for i in range (times):
        start_x = random.randint(min_x, max_x)
        start_y = random.randint(min_y, max_y)
        ray_star(start_x, start_y)
    
    turtle.down()
    
if __name__ == "__main__":
    main()