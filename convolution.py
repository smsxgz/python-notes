# I will update this script if I find more efficient methods.

import time
import numpy as np
"""
No Padding(valid)

Input:
    image:  [n, c, h, w]
    kernel: [k, c, kh, kw]
Output:
    [n, k, h - kh + 1, w - kw + 1]
"""


def convolution(image, kernel):
    # Stupid methed with three for-loops
    n, c, h, w = image.shape
    k, _c, kh, kw = kernel.shape
    assert c == _c

    out = np.zeros([n, k, h - kh + 1, w - kw + 1])
    for l in range(k):
        for i in range(h - kh + 1):
            for j in range(w - kw + 1):
                out[:, l, i, j] = np.sum(
                    image[:, :, i:i + kh, j:j + kw] * kernel[l:l + 1],
                    axis=(1, 2, 3))
    return out


def convolution2(image, kernel):
    # Better but still stupid method with one for-loop
    def func(simple_image):
        """simple_image: [c, h, w]"""
        n, c, h, w = image.shape
        k, _c, kh, kw = kernel.shape
        assert c == _c

        strides = simple_image.strides
        strided_image = np.lib.stride_tricks.as_strided(
            simple_image,
            shape=[c, h - kh + 1, w - kw + 1, kh, kw],
            strides=strides + strides[-2:])
        return np.sum(
            strided_image[np.newaxis] * kernel[:, :, np.newaxis, np.newaxis],
            axis=(1, 4, 5))

    return np.array([func(x) for x in image])


def convolution3(image, kernel):
    # This method is better
    def func(simple_image):
        """simple_image: [c, h, w]"""
        strides = simple_image.strides
        strided_image = np.lib.stride_tricks.as_strided(
            simple_image,
            shape=[c, h - kh + 1, w - kw + 1, kh, kw],
            strides=strides + strides[-2:])
        return np.einsum('ijklm, nilm -> njk', strided_image, kernel)

    return np.array([func(x) for x in image])


def convolution4(image, kernel):
    n, c, h, w = image.shape
    k, _c, kh, kw = kernel.shape
    assert c == _c

    strides = image.strides
    strided_image = np.lib.stride_tricks.as_strided(
        image,
        shape=[n, c, h - kh + 1, w - kw + 1, kh, kw],
        strides=strides + strides[-2:])
    return np.einsum('ijklmn, ojmn -> iokl', strided_image, kernel)


if __name__ == '__main__':
    n, c, h, w = 32, 6, 84, 84
    k, kh, kw = 128, 3, 3
    image = np.random.normal(size=[n, c, h, w])
    kernel = np.random.normal(size=[k, c, kh, kw])
    # image = np.ones([n, c, h, w])
    # kernel = np.array(list(range(kh * kw)) * k * c).reshape([k, c, kh, kw])

    start = time.time()
    out = convolution(image, kernel)
    print(time.time() - start)

    start = time.time()
    out2 = convolution2(image, kernel)
    print(time.time() - start)
    print(np.allclose(out, out2))

    start = time.time()
    out3 = convolution3(image, kernel)
    print(time.time() - start)
    print(np.allclose(out, out3))

    start = time.time()
    out4 = convolution4(image, kernel)
    print(time.time() - start)
    print(np.allclose(out, out4))
