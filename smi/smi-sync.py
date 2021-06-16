#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 영상과 자막이 부분적으로 싱크 안 맞을 때 교정하는 프로그램
# 그때그때 코드를 바꿔줘야 하는 대목들
# - encoding
# - t : 시각 조정을
#   * 어느 시점부터
#   * 얼만큼

import codecs
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("srcfile", type=str)
parser.add_argument("destfile", type=str)
args = parser.parse_args()

with codecs.open(args.destfile, encoding='cp949', mode='w') as filewrite:
    with codecs.open(args.srcfile, encoding='cp949') as fileread:
        for line in fileread:
            regex = re.compile("^(<S[yY][nN][cC] Start=)([0-9]+)(>.*)$")
            m = regex.match(line)
            if m:
                t=int(m.group(2))
                if t >= 969200:
                    t += 224000
                filewrite.write(m.group(1) + str(t) + m.group(3) + "\n")
            else:
                filewrite.write(line )

fileread.close()
filewrite.close()

