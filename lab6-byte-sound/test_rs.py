import reedsolo

def encode_message(message, n, k):
    rs = reedsolo.RSCodec(n - k)
    message_bytes = message.encode('utf-8')
    encoded_message = rs.encode(message_bytes)
    return encoded_message

def decode_message(encoded_message, n, k):
    rs = reedsolo.RSCodec(n - k)
    decoded_message = rs.decode(encoded_message)
    # 디코딩된 메시지는 튜플로 반환됩니다. 첫 번째 요소가 실제 메시지입니다.
    decoded_message = decoded_message[0]
    return decoded_message.decode('utf-8')

def introduce_errors(encoded_message, num_errors):
    import random
    encoded_message_with_error = bytearray(encoded_message)
    print(num_errors, "errors")
    postition = []
    for _ in range(num_errors):
        pos = random.randint(0, len(encoded_message_with_error) - 1)
        postition.append(pos)
        encoded_message_with_error[pos] ^= 0xFF
    print("Errors in ", postition)
    return bytes(encoded_message_with_error)

# 예제 메시지
message = "Hello, Reed-Solomon!"
n = 255  # 코드워드의 길이
k = 223  # 메시지의 길이

# 메시지 인코딩
encoded_message = encode_message(message, n, k)
print("Encoded Message:", encoded_message)
print("------------------------------------")

# 오류 삽입 (예: 16개의 오류)
encoded_message_with_error = introduce_errors(encoded_message, 16)
print("------------------------------------")
print("Error Message:", encoded_message_with_error)

# 메시지 디코딩
try:
    decoded_message = decode_message(encoded_message_with_error, n, k)
    print("------ Error recovery with RS Code, n: ",n, " k:", k , "----------")
    print("Decoded Message:", decoded_message)
except reedsolo.ReedSolomonError as e:
    print("Error decoding message:", e)
