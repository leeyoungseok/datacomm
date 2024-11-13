
import hashlib
target = '🧡💛💚💙💜🐶🐵🐆🦜👀🦴🫤😭🤫👿👺💀👾🙈🤖💩'

def get_target(num):
    sha = hashlib.sha256(str(num).encode())
    hash_str = sha.hexdigest()
    indices = [int(c, 16) % 10 for c in hash_str]
    results = [target[i:i+1] for i in indices[:5]]
    return ''.join(results)