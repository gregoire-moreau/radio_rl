import cv2
import numpy as np


def make_base(height, width):
    base = np.full(shape=(height, width, 3), fill_value=(255, 255, 255), dtype=np.uint8)
    base[:6, :] = (0,0,0)
    base[-6:, :] = (0,0,0)
    base[:, :6] = (0,0,0)
    base[:, -6:] = (0,0,0)
    return base


def add_tumor(base, tick, x_offset, y_offset):
    t_img = cv2.imread('tmp/t'+str(tick)+'.png')
    t_img = cv2.resize(t_img, dsize=(500, 500), interpolation=cv2.INTER_CUBIC)
    base[x_offset:x_offset+t_img.shape[0], y_offset:y_offset+t_img.shape[1]] = t_img


def add_dose_map(base, tick, x_offset, y_offset):
    t_img = cv2.imread('tmp/d'+str(tick)+'.png')
    t_img = cv2.resize(t_img[:, 55:-20], dsize=(600,540), interpolation=cv2.INTER_CUBIC)
    base[x_offset:x_offset+t_img.shape[0], y_offset:y_offset+t_img.shape[1]] = t_img


def add_images(base, ticks, pad_left=400, space_between_h=80, space_between_v=80, height=3500, width=2000):
    pad_top = int((height - 4* 500 - 3 * space_between_v) / 2)
    more=0
    higher_dose = 2
    add_tumor(base, ticks[0], pad_top, pad_left)
    add_dose_map(base, ticks[0], pad_top - higher_dose, pad_left + 500 + space_between_h+more)
    add_tumor(base, ticks[1], pad_top + 500 + space_between_v, pad_left)
    add_dose_map(base, ticks[1], pad_top + 500 + space_between_v- higher_dose, pad_left + 500 + space_between_h+more)
    add_tumor(base, ticks[2], pad_top + 1000 + 2*space_between_v, pad_left)
    add_dose_map(base, ticks[2], pad_top + 1000 + 2*space_between_v- higher_dose, pad_left + 500 + space_between_h+more)
    add_tumor(base, ticks[3], pad_top + 1500 + 3*space_between_v, pad_left)
    add_dose_map(base, ticks[3], pad_top + 1500 + 3*space_between_v- higher_dose, pad_left + 500 + space_between_h+more)
    base[int(pad_top + 500 + space_between_v/2 - 3): int(pad_top + 500 + space_between_v/2 + 3), :] = (0,0,0)
    base[int(pad_top + 1000 + 3*space_between_v/2 - 3): int(pad_top + 1000 + 3*space_between_v/2 + 3), :] = (0,0,0)
    base[int(pad_top + 1500 + 5*space_between_v/2 - 3): int(pad_top + 1500 + 5*space_between_v/2 + 3), :] = (0,0,0)
    base[:, int(pad_left - space_between_h / 2 -3):int(pad_left - space_between_h / 2 + 3)] = (0,0,0)
    base[:, int(pad_left + 500 + space_between_h / 2 - 3):int(pad_left + 500 + space_between_h / 2 +3)] = (0,0,0)


def add_images3(base, ticks, pad_left=400, space_between_h=80, space_between_v=80, height=3500, width=2000):
    pad_top = int((height - 3* 500 - 2 * space_between_v) / 2)
    more=0
    higher_dose = 2
    add_tumor(base, ticks[0], pad_top, pad_left)
    add_dose_map(base, ticks[0], pad_top - higher_dose, pad_left + 500 + space_between_h+more)
    add_tumor(base, ticks[1], pad_top + 500 + space_between_v, pad_left)
    add_dose_map(base, ticks[1], pad_top + 500 + space_between_v- higher_dose, pad_left + 500 + space_between_h+more)
    add_tumor(base, ticks[2], pad_top + 1000 + 2*space_between_v, pad_left)
    add_dose_map(base, ticks[2], pad_top + 1000 + 2*space_between_v- higher_dose, pad_left + 500 + space_between_h+more)
    base[int(pad_top + 500 + space_between_v/2 - 3): int(pad_top + 500 + space_between_v/2 + 3), :] = (0,0,0)
    base[int(pad_top + 1000 + 3*space_between_v/2 - 3): int(pad_top + 1000 + 3*space_between_v/2 + 3), :] = (0,0,0)
    #base[int(pad_top + 1500 + 5*space_between_v/2 - 3): int(pad_top + 1500 + 5*space_between_v/2 + 3), :] = (0,0,0)
    base[:, int(pad_left - space_between_h / 2 -3):int(pad_left - space_between_h / 2 + 3)] = (0,0,0)
    base[:, int(pad_left + 500 + space_between_h / 2 - 3):int(pad_left + 500 + space_between_h / 2 +3)] = (0,0,0)


def add_text3(base, ticks):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (0, 0, 0)
    lineType = 2
    cv2.putText(base, 'After '+str(ticks[0])+' hours', (75,310), font, fontScale, fontColor, lineType)
    cv2.putText(base, 'After '+str(ticks[1])+' hours', (60,890), font, fontScale, fontColor, lineType)
    cv2.putText(base, 'After '+str(ticks[2])+' hours', (60,1470), font, fontScale, fontColor, lineType)


def add_text(base, ticks):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (0, 0, 0)
    lineType = 2
    cv2.putText(base, 'After '+str(ticks[0])+' hours', (75,310), font, fontScale, fontColor, lineType)
    cv2.putText(base, 'After '+str(ticks[1])+' hours', (60,890), font, fontScale, fontColor, lineType)
    cv2.putText(base, 'After '+str(ticks[2])+' hours', (60,1470), font, fontScale, fontColor, lineType)
    cv2.putText(base, 'After '+str(ticks[3])+' hours', (60,2050), font, fontScale, fontColor, lineType)


def save_base(base, filename):
    cv2.imwrite('tmp/'+filename+'.png', base)

def make_img(ticks, name):
    height = 2350
    width = 1600
    base = make_base(height, width)
    add_images(base, ticks, height=height, width=width)
    add_text(base, ticks)
    save_base(base, name)

def make_img3(ticks, name):
    height = 1775
    width = 1600
    base = make_base(height, width)
    add_images3(base, ticks, height=height, width=width)
    add_text3(base, ticks)
    save_base(base, name)

if __name__ ==  '__main__':
    make_img([0, 216, 456, 696], 'test')
