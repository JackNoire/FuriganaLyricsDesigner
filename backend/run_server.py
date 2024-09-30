import uvicorn
import webbrowser
import colorama

if __name__ == '__main__':
    colorama.init()
    webbrowser.open('http://127.0.0.1:7326')
    uvicorn.run("app:app", host="127.0.0.1", port=7326)