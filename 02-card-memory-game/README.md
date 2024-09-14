# FastHTML Memory Card Game

This example app demonstrates a simple memory card game using TailwindCSS, AlpineJS inside a FastHTML app.

## Running Locally

To run the app locally:

1. Clone the repository
2. Navigate to the project directory
3. [optional] Install the standalone TailwindCSS CLI (see below).
4. Create a new Python environment if you wish.
5. Install the project dependencies: `pip install  -r requirements.txt`
6. In one terminal start the Python server: `python main.py`
7. If you wish to edit the Tailwind styles then, in another terminal watch and compile the app CSS file: `tailwindcss -i ./src/app.css -o ./public/app.css --watch`

## Installing the TailwindCSS Standalone CLI

There are three main methods for installing the standalone CLI.

### 1. PyPi

`pip install pytailwindcss`

I had issues getting this to work on Windows WSL though.

### 2. Installing Manually

You can download the standalone CLI manually with the following commands:

```
wget https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.10/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
sudo mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss
```

### 3. NPM

Perhaps the easiest method is to just install TailwindCSS via npm, if you don't mind using npm that is. It's only for local development and there is no need to run npm/Node on the server when you deploy your app in production.

```
npm install -D tailwindcss
```

### Testing TailwindCSS CLI

Once intstalled, test that you can run the TailwindCSS standalone CLI via:

```
tailwindcss
```

You should see the current TailwindCSS CLI version and some usage instructions.

### Installing TailwindCSS Plugins

If you use the standalone TailwindCSS CLI then you can still use any 3rd party Tailwind plugin such as DasiyUI. Simply install the plugin via npm in the usual way and update `tailwind.config.js` accordingly.
