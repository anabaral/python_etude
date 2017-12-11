#
# 동영상 자막파일(.smi) 의 아래와 같은 부분을 변환하는 스크립트.
# &#45348;&#45448;&#46308;&#51060;&#45264;? ==> 네놈들이냐?
# 특정 플레이어 (LG smart tv) 의 자막 인식기능이 저급하여 어쩔 수 없이 변환함.
#
import re, os
enc_charset = "utf-16le"
src_dir_path = "E:/download/1/오늘부터신령님2기자막_/"
dest_dir_path = src_dir_path[0:-2] + "/"

for dirname, dirnames, filenames in os.walk(src_dir_path):
    # print (dirname, dirnames, filenames)
    for filename in filenames:
        file_read_object = open(src_dir_path + filename, "r", encoding=enc_charset)
        data = file_read_object.readlines()
        file_write_object = open(dest_dir_path + filename, "w", encoding=enc_charset)
        for line in data:
            # 개선하고 싶은 점:
            # 각 라인에서 regex match 되는 부분을 한개씩 찾아 라인 전체를 바꾸고 반복하는 동작을
            # 각 부분을 바꾼 부분으로 만들어 조립하는 식으로 바꾸고 싶음.
            while True :
                match = re.search("[&][#]([0-9]+);", line)
                if match:
                    possible_number = int(match.group(1))
                    bytes = bytearray([(possible_number % 256), int(possible_number / 256)])
                    line = line[0:match.start(1)-2] + bytes.decode(enc_charset) + line[match.end(1)+1:]
                else:
                    break
            file_write_object.write(line)
        file_write_object.close()
        file_read_object.close()
