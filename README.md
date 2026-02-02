# 🌫️ StringFog Decryptor

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A lightweight Python tool designed to automatically de-obfuscate strings in Android Java source code that have been encrypted using [StringFog](https://github.com/MegatronKing/StringFog).

This script recursively scans a directory for `.java` files, identifies `StringFog.decrypt(...)` calls, decrypts the strings using the embedded logic (Base64 + XOR), and replaces the function call with the original plaintext string in the source code.

## 🚀 Features

- **Automatic Detection**: Uses Regex to find `StringFog.decrypt("encrypted_data", "key")` patterns.
- **In-place Replacement**: Directly modifies the Java files, making the code readable again immediately.
- **Recursive Scanning**: Works through all subdirectories from the script's location.
- **Java Escaping Support**: Handles special characters (like `\n`, `\"`, unicode) correctly during decryption.
- **Zero Dependencies**: Uses only Python standard libraries (`base64`, `re`, `os`).

## 🛠️ How It Works

The script looks for patterns like this in your Java code:
```java
// Before execution
String apiUrl = StringFog.decrypt("MiwSNDs=", "IzkzODs=");

// And automatically converts them to:
// After execution
String apiUrl = "https://api.example.com";
```
## 📦 Installation & Usage

1.  **Download**:
Clone this repository or download the python script.

2.  **Place the Script**:
Copy the python script into the root directory of your decompiled Android project (e.g., inside the `src` folder) or the specific package folder you want to clean up.

3.  **Run**:
Open your terminal in that directory and run:

```bash
    python main.py
```

## ⚠️ Important Warning
Backup Your Code: This script modifies files in-place (overwrites them). Always make sure you have a backup of your source code or use version control (Git) before running it.
Encoding: The script assumes source files are encoded in UTF-8.

## 🤝 Contributing
Contributions are welcome! If you find a bug or want to improve the regex pattern for edge cases, feel free to open an issue or submit a pull request.

## 📄 License
This project is open-source and available under the MIT License.
