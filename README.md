# Checkbnb

## Tools used
* https://docs.streamlit.io/get-started/installation
* https://www.npmjs.com/package/@stlite/desktop

## Developer setup

Run `python -m venv .venv`
```
A folder named ".venv" will appear in your project. This directory is where your virtual environment and its dependencies are installed.
```

Run `source .venv/bin/activate`
```
This command start the server. Once activated, you will see your environment name in parentheses before your prompt. "(.venv)"
```

Run `pip install -r requirements.txt`
```
This command install streamlit.
```

Run `streamlit app.py`
```
This command start you local app.
```

## Compile the app with electron
Run `npm run dump`
```
This dump command creates ./build directory that contains the copied Streamlit app files, dumped installed packages, Pyodide runtime, Electron app files, etc.
```

Run `npm run serve` for preview.
```
This command is just a wrapper of electron command as you can see at the "scripts" field in the package.json. It launches Electron and starts the app with ./build/electron/main.js, which is specified at the "main" field in the package.json.
```

Run `npm run app:dist` for packaging.
```
This command bundles the ./build directory created in the step above into application files (.app, .exe, .dmg etc.) in the ./dist directory. To customize the built app, e.g. setting the icon, follow the electron-builder instructions.
```

## Authors
[Aymeric](https://www.linkedin.com/in/aymeric-dominique/) & [Thomas](https://www.linkedin.com/in/thomas-d-legrand/)