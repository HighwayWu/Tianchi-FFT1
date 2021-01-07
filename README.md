# [Tianchi Competition "Forgeries and Forensics" Track 1](https://tianchi.aliyun.com/competition/entrance/531812/introduction)

An official implementation code of **Rank 1**.

## Table of Contents

- [Background](#background)
- [Demo](#demo)


## Background

<p align='center'>  
  <img src='https://github.com/HighwayWu/Tianchi-FFT1/blob/main/framework.jpg' width='500'/>
</p>
<p  align='center'>
  <em>Overview of tampering pipeline.</em>
</p>

Usually, manual modification will destroy the original structure of the image and leave traces of tampering, making the forensics algorithm locating the fake area successfully. From the attacker's point of view, one sample but efficient remedy is doing post-processing, e.g., re-compression, blurring, noising and resizing. However, extensive post-processing will cause visible flaws in the picture, which is not accepted by this competition. Here I present a new series of processes for tampering images in the stage I.

The overview of tampering pipeline is shown in above figure. For a given image and corresponding mask, where white pixel means the area needed to be modified, the major tampering steps are as follows:

    Step 1: Using Photoshop software for preliminary tampering. Specifically, use the stamp to extract the solid color background to erase the tampered area, i.e., copy-move operation, and then fill in appropriate fake texts, where the fake texts should have the same font, size, color, etc. as the original texts as possible, in order to fool the Error Level Analysis (ELA) and other forensic models.
    
    Step 2: Increasing the discontinuity of the non-text area (background) in the forged regions. Generally speaking, discontinuous areas will interfere with the forensic model, so this step adds a certain proportion of discrete original image background pixels to the tampered area. This operation is similar as adding noising and it can deceive the human eye very well, because these discrete pixels are almost the same as the tampered background.
    
    Step 3: Increasing the discontinuity of the text in the forged regions. Here we add some standard Gaussian noise to the text. Since the text is basically dark, the noise on it is not easy to detect.
    
    Step 4: Adding light yellow noise to the forged regions. Due to the visual illusion of the human eye, the discrete yellowish dots on a white background are very difficult to be found (unless the image is enlarged to some extent).

In the Track 1 of the competition, we also tried many other methods, e.g., deceive the forensic model to erase the traces introduced by the re-compression of tampered area. However, because of the diversity of the competition scoring mechanism, it is difficult to ensure the stability of its effect. In the end, we mainly adopted the processes shown in the figure. More details please refer to the code.

## Demo

To generate the forged images:
```bash
python post.py
```
Note: original images and materials please download from [here](https://drive.google.com/file/d/1rgiXdlnJhpwXD353O0PN5KYw0cPYyaf5/view?usp=sharing).
