"""
author: ww
"""
import time
import math
import numpy as np
from dtw import *  # pip install dtw-python


def dtw_matching(query, reference, keep_internals=False):
    alignment = dtw(query, reference, keep_internals=keep_internals, step_pattern=symmetric1)
    return alignment, alignment.distance


def dtw_distance(s1, s2):
    """
    s1: query series
    s2: reference series
    """
    length1 = len(s1)
    length2 = len(s2)
    if length1 == 0 or length2 == 0:
        return -1
    dp = [[float('inf')] * (length2 + 1) for _ in range(length1 + 1)]  # 初始化一个 (length2+1)列 (length1+1)行 的矩阵
    dp[0][0] = 0
    for k1 in range(1, length1 + 1):
        for k2 in range(1, length2 + 1):
            cost = abs(s1[k1-1] - s2[k2-1])
            dp[k1][k2] = cost + min(dp[k1-1][k2], dp[k1][k2-1], dp[k1-1][k2-1])
    return dp[-1][-1]
