# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

base = os.getenv('OPENCV_TEST_PATH', 'images')

img1 = cv2.imread(os.path.join(base, os.getenv('OPENCV_TEST_QUERY', 'pig.jpg')), 0)
img2 = cv2.imread(os.path.join(base, os.getenv('OPENCV_TEST_BASE', 'normal.png')), 0)


def draw_matches(img1, kp1, img2, kp2, matches, **kwargs):
    """
    http://stackoverflow.com/a/26227854
    """

    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1, rows2]), cols1+cols2, 3), dtype='uint8')

    out[:rows1,:cols1,:] = np.dstack([img1, img1, img1])

    out[:rows2, cols1:cols1+cols2,:] = np.dstack([img2, img2, img2])

    for mat in matches:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        (x1, y1) = kp1[img1_idx].pt
        (x2, y2) = kp2[img2_idx].pt

        cv2.circle(out, (int(x1), int(y1)), 4, (255, 0, 0), 1)
        cv2.circle(out, (int(x2)+cols1, int(y2)), 4, (255, 0, 0), 1)

        cv2.line(out, (int(x1), int(y1)), (int(x2)+cols1, int(y2)), (255, 0, 0), 1)

    return out


def orb_matcher():
    orb = cv2.ORB_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)

    # Draw first 10 matches.
    img3 = draw_matches(img1, kp1, img2, kp2, matches, flags=2)

    plt.imshow(img3), plt.show()


FLANN_INDEX_KDTREE = 0


def flann_matcher():
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    # FLANN parameters
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # Need to draw only good matches, so create a mask
    matches_mask = [[0, 0] for _ in xrange(len(matches))]

    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matches_mask[i] = [1, 0]

    draw_params = dict(
        matchColor=(0, 255, 0),
        singlePointColor = (255, 0, 0),
        matchesMask = matches_mask,
        flags = 0
    )

    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)

    plt.imshow(img3,), plt.show()


if __name__ == '__main__':
    mode = os.getenv('OPENCV_TEST_MODE', 'flann')
    {'flann': flann_matcher, 'orb': orb_matcher}.get(mode, lambda: None)()