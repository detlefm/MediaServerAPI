24.07.2025

# MediaServerAPI
MediaServer API documentation
and proxy.py to add json support for MediaServer

##### API Documentation
./ms_docu/MediaServer_API.md
./ms_docu/MediaServer_API.html



#### AI Prompt and source files
./ai_source

### Used AI

https://www.kimi.com/chat/


#### Github Pages 

https://detlefm.github.io/MediaServerAPI/Index.html

<!-- 
# `proxy.py` 

This proxy server adds JSON support to the MediaServer API.  
Instead of calling the MediaServer directly like:

```
http://<yourmediaserverpc:8089>/api/apicall?Parameters
```

you can now use the proxy like this:

```
http://<yourproxypc:Port>/api/apicall?Parameters&json=[0|1]
```

- When `json=0`, you’ll receive the standard XML response  
- When `json=1`, the response will be in JSON format

---

## 🛠 Installation Guide

1. **Install Python**
   - Use [python.org](https://www.python.org/downloads/) or the Microsoft Store

2. **Set up your project folder**
   - Create a new directory for your proxy project

3. **Open terminal**
   - Open PowerShell or Command Prompt in your project directory

4. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

5. **Activate the virtual environment**
   - PowerShell:
     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   - Command Prompt:
     ```bash
     .\.venv\Scripts\activate.bat
     ```

6. **Add project files**
   - Place `proxy.py` and `requirements.txt` into the project directory

7. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

8. **Run the proxy**
   ```bash
   python .\proxy.py --port [port number, e.g. 8980] --server [MediaServer URL with port, e.g. localhost:8089] --cors
   ```

9. **Show help info**
   ```bash
   python .\proxy.py --help
   ```

🔄 **Note:** Keep the terminal window open while the proxy is running.

--- -->


###

---

# 🧭 `proxy.py` Overview

This lightweight proxy server adds JSON and CORS support to the MediaServer API.  
Instead of calling the MediaServer directly:

```
http://<yourmediaserverpc:8089>/api/apicall?Parameters
```

you can now use the proxy:

```
http://<yourproxypc:Port>/api/apicall?Parameters&json=1
```

- `json=0` or omitted → Response is standard XML  
- `json=1` → Response is returned in JSON format

---

## 🛠 Installation Guide

1. **Install Python**
   - Get it from [python.org](https://www.python.org/downloads/) or the Microsoft Store

2. **Create a project folder**
   - Pick or create a directory where your proxy will live

3. **Launch terminal**
   - Open PowerShell or Command Prompt in your project directory

4. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

5. **Activate the virtual environment**
   - PowerShell:
     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   - Command Prompt:
     ```bash
     .\.venv\Scripts\activate.bat
     ```

6. **Add required files**
   - Place `proxy.py` and `requirements.txt` in your project directory

7. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

8. **Start the proxy**
   ```bash
   python .\proxy.py --port [your proxy port, e.g. 8980] --server [MediaServer host:port, e.g. localhost:8089] --cors
   ```

9. **View help options**
   ```bash
   python .\proxy.py --help
   ```

🔄 **Note:** Keep your terminal session active while the proxy is running.

---

## 🌐 What Does `--cors` Do?

The `--cors` flag enables **Cross-Origin Resource Sharing (CORS)** support via FastAPI.

💡 Why it matters:
- Web apps or frontend clients hosted on different domains (e.g. `http://localhost:3000`) often need to access APIs hosted elsewhere.
- Browsers restrict cross-origin requests unless CORS headers are explicitly allowed.

✅ When you launch `proxy.py` with `--cors`, it:
- Injects `Access-Control-Allow-Origin: *` headers in every HTTP response.
- Makes your MediaServer API proxy friendly to browser-based apps or external tools.

This is especially useful during development or when integrating the proxy with single-page applications (like React, Vue, etc.).

---


