import base64
import re
import os

# --- Helper Functions ---

def android_base64_decode(s: str) -> bytes:
    # Base64.DEFAULT => ignores \n, \r, whitespace
    s = s.replace("\\n", "").replace("\\r", "").strip()
    return base64.b64decode(s)

def xor_decrypt(data: bytes, key: bytes) -> str:
    out = bytearray(len(data))
    for i in range(len(data)):
        out[i] = data[i] ^ key[i % len(key)]
    return out.decode("utf-8", errors="ignore")

def stringfog_decrypt(enc_b64: str, key_b64: str) -> str:
    try:
        data = android_base64_decode(enc_b64)
        key = android_base64_decode(key_b64)
        return xor_decrypt(data, key)
    except:
        return None

def java_unescape(s: str) -> str:
    return bytes(s, "utf-8").decode("unicode_escape")

# Regex pattern to find StringFog calls
pattern = re.compile(
    r'StringFog\.decrypt\(\s*"((?:\\.|[^"])*)"\s*,\s*"((?:\\.|[^"])*)"\s*\)',
    re.DOTALL
)

def replace_callback(match):
    enc_raw, key_raw = match.groups()
    try:
        # Unescape Java string literals (e.g. \\n -> \n)
        enc = java_unescape(enc_raw)
        key = java_unescape(key_raw)
        
        plain = stringfog_decrypt(enc, key)
        
        if plain is not None:
            # Escape quotes in the result just in case
            plain_escaped = plain.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            return f"\"{plain_escaped}\""
        else:
            return match.group(0) # Return original if decrypt fails
            
    except Exception as e:
        return match.group(0)

def process_directory(root_dir):
    print(f"Searching in : {root_dir}")
    count_files = 0
    count_decrypted = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".java"):
                file_path = os.path.join(dirpath, filename)
                
                try:
                    # Read file
                    with open(file_path, "r", encoding="utf-8") as f:
                        original_content = f.read()
                    
                    # Apply decryption
                    new_content = pattern.sub(replace_callback, original_content)
                    
                    # Check if anything changed
                    if new_content != original_content:
                        # Overwrite file
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        
                        print(f"Decrypted: {file_path}")
                        count_decrypted += 1
                    
                    count_files += 1

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print("-" * 40)
    print(f"Done.")
    print(f"Found files: {count_files}")
    print(f"Decrypted files: {count_decrypted}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_directory(current_directory)
