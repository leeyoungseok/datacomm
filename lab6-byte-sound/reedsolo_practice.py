from reedsolo import RSCodec, ReedSolomonError

# 예시 데이터 (17바이트)
data = b'202150835'
print(f"Original Data : {data}")

# RSCodec 객체 생성 (k=n-4)
k = 6
rs = RSCodec(k)

# 인코딩
encoded_data = rs.encode(data)
print(f"Encoded data (length n={len(encoded_data)}): {encoded_data}")

# 3바이트 오류 추가
corrupted_data = bytearray(encoded_data)
corrupted_data[2] = 255
corrupted_data[4] = 255
corrupted_data[6] = 255
print(f"Corrupted data with 3 bytes: {corrupted_data}")

# 디코딩
try:
    decoded_data = rs.decode(corrupted_data)
    print(f"Decoding Success")
    print(f"Decoded data: {decoded_data[0]}")
except ReedSolomonError as e:
    print(f"k number : {k}, Decoding Failed")

