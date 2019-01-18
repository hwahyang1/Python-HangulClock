# -*- coding:utf-8 -*- 

import random, datetime, os
import numpy as np
from PIL import Image

def alpha_composite(src, dst):
    src = np.asarray(src)
    dst = np.asarray(dst)
    out = np.empty(src.shape, dtype = 'float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha]/255.0
    dst_a = dst[alpha]/255.0
    out[alpha] = src_a+dst_a*(1-src_a)
    old_setting = np.seterr(invalid = 'ignore')
    out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
    np.seterr(**old_setting)
    out[alpha] *= 255
    np.clip(out,0,255)
    out = out.astype('uint8')
    out = Image.fromarray(out, 'RGBA')
    return out

def hangul_clock():
    now = datetime.datetime.now()
    filename = "%s_%s_%s_%s_%s_%s.png" % (now.year, now.month, now.day, now.hour, now.minute, now.second)

    BG = Image.open("hangul_clock_base/BG_1000_1500.png")
    ment = Image.open("hangul_clock_base/ment/ment%s_1000_1500.png" % (random.randint(1, 3)))
    one = alpha_composite(ment, BG)

    # 이거 "hangul_clock_base/BG_1000_1500.png"에 넣어도 됬었는데 이미지 작업 다하고 깨달아버려서 그냥 했습니다 ㅋㅋㅋㅋㅋㅋ
    # 속도가 너무 느리다 판단되시면 아래 두개 지우고 "hangul_clock_base/BG_1000_1500.png"로 합치시는것도 괜찮을꺼 같아여
    hour_base = Image.open("hangul_clock_base/hour/hour_base_1000_1500.png")
    two = alpha_composite(hour_base, one)

    min_base = Image.open("hangul_clock_base/minute/minute_base_1000_1500.png")
    three = alpha_composite(min_base, two)

    hour = now.hour
    if hour > 12:
        hour = now.hour - 12

    now_hour = Image.open("hangul_clock_base/hour/hour_%s_1000_1500.png" % (hour))
    four = alpha_composite(now_hour, three)

    now_minute = Image.open("hangul_clock_base/minute/minute_%s_1000_1500.png" % (now.minute))
    five = alpha_composite(now_minute, four)
 
    result = five

    result.save(filename)

    return filename