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


# `proxy.py`

This proxy server adds JSON support to the MediaServer API.  
Instead of calling the MediaServer directly like:

```
http://<yourmediaserverpc:8089>/api/apicall?Parameters
```

you can now use the proxy like this:

```
http://<yourproxypc:Port>/api/apicall?Parameters,json=[0|1]
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
   python .\proxy.py --port [port number, e.g. 8980] --srv-url [MediaServer URL with port, e.g. localhost:8089]
   ```

9. **Show help info**
   ```bash
   python .\proxy.py --help
   ```

🔄 **Note:** Keep the terminal window open while the proxy is running.

---


###





21.07.2025