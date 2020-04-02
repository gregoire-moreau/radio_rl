import os
import matplotlib.pyplot as plt
from scipy.io import loadmat
import numpy as np

base_path = 'D:\Documents\data_MIRO\data_MIRO'

def list_patients():
    return os.listdir(base_path)

def patient_dates(num):
    return os.listdir(base_path+'\\Patient '+str(num).zfill(2))

def get_ct(num, date, slice_num):
    data_v = loadmat(base_path + '\\Patient ' + str(num).zfill(2) + '\\' + date + '\\data_v.mat')
    x = data_v['v']
    del data_v
    a = x.shape
    ct = np.zeros(shape=(a[0], a[1]))
    for i in range(a[0]):
        for j in range(a[1]):
            ct[i][j] = x[i][j][slice_num]
    del x
    return ct

def select_slice(y):
    b = y.shape
    slice_num = -1
    cur_best = 0
    for slice in range(b[2]):
        count = 0
        for i in range(b[0]):
            for j in range(b[1]):
                if y[i][j][slice] == 1:
                    count += 1
        if count > cur_best:
            cur_best = count
            slice_num = slice
    map = np.zeros(shape=(b[0], b[1]))
    for i in range(b[0]):
        for j in range(b[1]):
            map[i][j] = y[i][j][slice_num]
    del y
    return map, slice_num

def get_map(num, date):
    map_gtv_oar = loadmat(base_path + '\\Patient ' + str(num).zfill(2) + '\\' + date + '\\map_gtv_oar.mat')
    y = map_gtv_oar['map']
    del map_gtv_oar
    return select_slice(y)

def pretty_date(date):
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    return day+'-'+month+'-'+year

def save_scans(patient, date, ct, map):
    fig, axs = plt.subplots(1, 2)
    fig.suptitle('Patient '+str(patient) + ' on '+pretty_date(date))
    ct_plot = axs[0]
    map_plot = axs[1]
    ct_plot.set_title('CT scan')
    map_plot.set_title('Map')
    ct_plot.imshow(ct)
    ct_plot.axis('off')
    map_plot.imshow(map)
    map_plot.axis('off')
    fig.savefig('miro_images_max_s\\Patient '+str(patient).zfill(2)+'_'+date)
    np.save('miro_images_max_s\\Patient '+str(patient).zfill(2)+'_'+date+'_ct', ct)
    np.save('miro_images_max_s\\Patient '+str(patient).zfill(2)+'_'+date+'_map', map)



if __name__ == '__main__':
    #open_data(1, '20031222')
    for patient in list_patients():
        n = int(patient.split()[-1])
        for date in patient_dates(n):
            print(n, date)
            map, slice_num = get_map(n, date)
            print("Best slice =", slice_num)
            ct = get_ct(n, date, slice_num)
            save_scans(n, date, ct, map)

