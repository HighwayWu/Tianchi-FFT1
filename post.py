import cv2
import os
import numpy as np
import copy


# For generating the mask M_g.
def generate_mask_g():
    path = './images/'
    flist = sorted(os.listdir(path + 'images_org/'))
    for file in flist:
        print(file)
        img = cv2.imread(path + 'images_org/' + file)
        rect = cv2.imread(path + 'images_rect/' + file[1:])
        img = np.int32(img)
        rect = np.int32(rect)
        rtn = abs(img - rect)
        H, W, C = rtn.shape
        for i in range(H):
            for j in range(W):
                if rtn[i, j, 0] + rtn[i, j, 1] + rtn[i, j, 2] > 150:
                    rtn[i, j, :] = 255
                else:
                    rtn[i, j, :] = 0
        # cv2.imwrite(path + 'mask_g/' + file[:-4] + '.png', rtn)
    exit()


# For generating the mask M_s
def generate_mask_s():
    path = './images/'
    flist = sorted(os.listdir(path + 'mask_g/'))
    for file in flist:
        print(file)
        mask_g = cv2.imread(path + 'mask_g/' + file)
        kernel_size = 15
        mask_s = cv2.blur(mask_g, (kernel_size, kernel_size), 0)
        # cv2.imwrite(path + 'mask_g/' + file[:-4] + '.png', mask_s)
    # It should be noted that some mask_s are further adjusted.
    exit()


# For checking whether the generated images are the same as the submitted images.
def check():
    flist = os.listdir('./images/images_final/')
    for file in flist:
        img1 = cv2.imread('./images/images_final/' + file)
        img2 = cv2.imread('./images/images_final_2079/' + file)
        difference = cv2.subtract(img1, img2)
        result = not np.any(difference)
        if result:
            print(file + ' is OK.')
        else:
            print(file + ' is WRONG !!!!')
    exit()


# If you want to generate the submitted images, please just run this main script.
# The generated images will be saved in the './images/images_final/'.
# Your may also run the 'check()' function to verify them.
if __name__ == '__main__':
    # check()
    path = './images/'

    N1 = np.uint8(cv2.imread(path + 'noise/N_3_10.png'))
    N2 = np.uint8(cv2.imread(path + 'noise/N_3_50.png'))
    N3 = np.uint8(cv2.imread(path + 'noise/N_3_70.png'))
    N4 = np.uint8(cv2.imread(path + 'noise/N_3_80.png'))
    N5 = np.uint8(cv2.imread(path + 'noise/N_3_100.png'))
    N6 = np.uint8(cv2.imread(path + 'noise/N_3_150.png'))
    N7 = np.uint8(cv2.imread(path + 'noise/N_2_10.png'))
    N_list = [N1, N2, N3, N4, N5, N6, N7]

    flist = [['b0109.jpg', 'b0110.jpg', 'd0060.jpg', 'd0063.jpg', 'f0008.jpg', 'g0011.jpg', 'g0101.jpg', 'h0173.jpg',
             'i0092.jpg', 'i0094.jpg', 'j0049.jpg'],
             ['e0006.jpg'],
             ['e0088.jpg'],
             ['a0002.jpg', 'f0139.jpg'],
             ['h0044.jpg', 'j0093.jpg'],
             ['a0102.jpg'],
             ['c0141.jpg', 'c0147.jpg']]

    for idx in range(7):
        N = N_list[idx]
        for file in flist[idx]:
            print(file)
            mname = file[1:5]

            # Step 1
            I_g = cv2.imread(path + 'images_org/' + file)
            I_f = cv2.imread(path + 'images_fake/' + file[:-4] + '.png')
            M_g = cv2.imread(path + 'mask_g/' + file[:-4] + '.png')
            I_gp = copy.deepcopy(I_g)
            H, W, C = I_g.shape

            # Special Case: Do not add any noise to 'h0044.jpg'
            if file == 'h0044.jpg':
                M_s = cv2.imread(path + 'mask_s/' + file[:-4] + '.png')
                I_g[M_s == 255] = I_f[M_s == 255]
                cv2.imwrite(path + 'images_final/' + file[:-4] + '.jpg', np.uint8(I_g),
                            [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                continue

            # Step 2
            M_1 = np.zeros((H, W), dtype=np.int32)
            tmp = np.load(path + 'noise/M_1_tmp/M_1_tmp_' + file[:-4] + '.npz')['tmp']
            M_1[tmp < 437] = 255
            tmp2 = np.int32(copy.deepcopy(I_f))
            tmp3 = tmp2[:, :, 0] + tmp2[:, :, 1] + tmp2[:, :, 2]
            M_1[tmp3 < 700] = 0
            tmp2 = np.int32(copy.deepcopy(I_gp))
            tmp3 = tmp2[:, :, 0] + tmp2[:, :, 1] + tmp2[:, :, 2]
            M_1[tmp3 < 700] = 0
            I_f[M_1 == 255] = I_gp[M_1 == 255]

            # Step 3
            if file not in ['a0002.jpg']:
                M_2 = np.zeros((H, W), dtype=np.int32)
                tmp2 = np.int32(copy.deepcopy(I_f))
                tmp3 = tmp2[:, :, 0] + tmp2[:, :, 1] + tmp2[:, :, 2]
                M_2[tmp3 < 300] = 500
                tmp2 = np.int32(copy.deepcopy(I_gp))
                tmp3 = tmp2[:, :, 0] + tmp2[:, :, 1] + tmp2[:, :, 2]
                M_2[tmp3 < 300] += 500
                tmp = np.load(path + 'noise/M_2_tmp/M_2_tmp_' + file[:-4] + '.npz')['tmp']
                M_2[tmp < 0] = 0
                I_f[M_2 == 1000] = I_gp[M_2 == 1000]

            # Step 4
            M_3 = np.zeros((H, W), dtype=np.int32)
            tmp2 = np.int32(copy.deepcopy(I_f))
            tmp3 = tmp2[:, :, 0] + tmp2[:, :, 1] + tmp2[:, :, 2]
            M_3[tmp3 < 300] += 500
            tmp2 = np.int32(copy.deepcopy(I_gp))
            tmp3 = tmp2[:, :, 0] + tmp2[:, :, 1] + tmp2[:, :, 2]
            M_3[tmp3 < 300] -= 500
            tmp = np.load(path + 'noise/M_3_tmp/M_3_tmp_' + file[:-4] + '.npz')['tmp']
            M_3[tmp < 925] = 0
            I_f[M_3 == 500] = 147

            # Step 5
            tmp = copy.deepcopy(N[:H, :W, :])
            I_f[tmp != 0] += tmp[tmp != 0]
            I_gp[tmp != 0] += tmp[tmp != 0]

            # Step 6
            M_s = cv2.imread(path + 'mask_s/' + file[:-4] + '.png')

            # Step 7
            I_g[M_g == 255] = I_gp[M_g == 255]
            I_g[M_s == 255] = I_f[M_s == 255]

            # Step 8
            cv2.imwrite(path + 'images_final/' + file[:-4] + '.jpg', np.uint8(I_g),
                        [int(cv2.IMWRITE_JPEG_QUALITY), 100])