INPUT_DIR = 'input/'

# 输出目录
OUTPUT_DIR = 'output/'

# 输入目录1
INPUT_DIR1 = 'input/character'

# 输入目录2
INPUT_DIR2 = 'input/ner'

DYNASTY = ["元", "先秦", "南北朝", "唐", "宋", "明", "汉", "清", "辽", "金", "隋", "魏晋", "汇总"]
"""
---------------------------------------------------------
>>>     the settings for character_summary.py used
---------------------------------------------------------
"""
# top n 限制值
TOP_N = 100

# 所有可能出现的标点
MARKS = ["，", "。", "“", "”", "？", "！", "《", "》", ",", "；"]

# 所有可能出现的虚词
CLASSICAL = ["而", "何", "乎", "乃", "其", "且", "然", "若", "所", "为", "焉",
             "也", "以", "矣", "于", "之", "则", "者", "与", "欤", "因", "兮"]

"""
---------------------------------------------------------
>>>     the settings for forLatticeUse.py used
---------------------------------------------------------
"""
# 需要去除的标点
MARKS_RM = ["“", "”", "《", "》"]
# 用于分段的标点
MARKS_SEG = ["，", "。", "？", "！", ",", "；"]

"""
---------------------------------------------------------
>>>     the settings for multi_summary.py used
---------------------------------------------------------
"""
# 季节
SUMMARY_SEASON = ['春', '夏', '秋', '冬']
# 节气
SUMMARY_SOLAR_TERM = ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种', '夏至', '小暑', '大暑',
                      '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至', '小寒', '大寒']
# 意象 摘自 https://wenku.baidu.com/view/54c77d77f242336c1eb95ef6.html
SUMMARY_IMAGERY = ['柳', '梅', '菊', '松', '柏', '莲', '梧桐', '草', '芭蕉', '红豆', '豆蔻',
                   '竹', '黍离', '丁香', '叶', '花', '兰', '牡丹', '蝉', '杜鹃', '鹧鸪', '雁',
                   '鸦', '蟋蟀', '鸳鸯', '精卫', '鸟', '燕', '猿', '鱼', '月', '阳', '水', '冰',
                   '雪', '海', '江', '雨', '风', '霜', '露', '云', '天', '酒', '船', '舟', '笛',
                   '吴钩', '琴', '灯', '英雄', '小人', '南浦', '长亭', '柳营', '古迹', '乡村', '草原',
                   '城市', '市井', '仙境', '凭栏', '南山', '桃源', '西楼', '亭', '镜', '灯']
SUMMARY_IMAGERY = list(set(SUMMARY_IMAGERY))
# 颜色
SUMMARY_COLOR = {
    "白": ["白", "素", "皎", "皓", "皙"],
    "黑": ["暗", "玄", "乌", "冥", "墨", "黑", "灰", "褐", "黛", "黎", "黯", "皂", "淄", "黝"],
    "红": ["红", "丹", "朱", "赤", "绛", "赫", "彤", "绯", "赩", "茜", "骍", "赮", "殷", "赪", "檀", "纁", "缇"],
    "黄": ["黄", "缃", "黈"],
    "蓝": ["蓝", "雘", "靛"],
    "绿": ["青", "绿", "碧", "翠", "苍", "綦", "翡"],
    "紫": ["紫", "赭"],
}
