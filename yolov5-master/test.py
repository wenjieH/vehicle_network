import utils.general

# 检查是否有check_requirements函数
if 'check_requirements' in dir(utils.general):
    print("check_requirements存在于utils.general模块中。")
else:
    print("check_requirements不存在于utils.general模块中。")

# 检查是否有cv2变量
if 'cv2' in dir(utils.general):
    print("cv2存在于utils.general模块中。")
else:
    print("cv2不存在于utils.general模块中。")
