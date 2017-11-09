import time
import numpy as np
"""
No Padding

Input:
    image:  [n, c, h, w]
    kernel: [k, c, kh, kw]
Output:
    [n, k, h - kh + 1, w - kw + 1]
"""

n, c, h, w = 32, 4, 84, 84
k, kh, kw = 128, 3, 3
image = np.random.normal(size=[n, c, h, w])
kernel = np.random.normal(size=[k, c, kh, kw])
# image = np.ones([n, c, h, w])
# kernel = np.array(list(range(kh * kw)) * k * c).reshape([k, c, kh, kw])

# Stupid methed
# Three for-loops
start = time.time()
out = np.zeros([n, k, h - kh + 1, w - kw + 1])
for l in range(k):
    for i in range(h - kh + 1):
        for j in range(w - kw + 1):
            out[:, l, i, j] = np.sum(
                image[:, :, i:i + kh, j:j + kw] * kernel[l:l + 1],
                axis=(1, 2, 3))

print(time.time() - start)

# Better but still stupid method
start = time.time()


def func(simple_image):
    """simple_image: [c, h, w]"""
    strides = simple_image.strides
    strided_image = np.lib.stride_tricks.as_strided(
        simple_image,
        shape=[c, h - kh + 1, w - kw + 1, kh, kw],
        strides=strides + strides[-2:])
    return np.sum(
        strided_image[np.newaxis] * kernel[:, :, np.newaxis, np.newaxis],
        axis=(1, 4, 5))


out2 = np.array([func(x) for x in image])
print(time.time() - start)
print(np.allclose(out, out2))
