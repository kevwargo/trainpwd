# Train Password

A small Python utility that helps you memorize a password by asking you to re-enter it at random intervals.

## How it works

1. Run the script.
2. Enter the password you want to practice.
3. The script starts a background process.
4. Every **30–60 minutes**, a KDE dialog prompts you to enter the password.
5. If the password is correct, the dialog disappears until the next prompt.
6. If it's incorrect, you'll be asked again until you enter the correct password.
7. Close the dialog or press **Cancel** to stop the training session.

## Requirements

* Python 3
* `kdialog` (KDE)

## Usage

```bash
./trainpwd.py [ID]
```

`ID` is an optional label shown in the prompt (for example, `GitHub`, `AWS`, or `Work VPN`). If omitted, `Default` is used.

## Logging

Logs are written to:

```
~/.cache/trainpwd.log
```
