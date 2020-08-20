# TUM NWERC Selection Tool
A tool which 
- fetches the relevant contests for the selection of the TUM NWERC teams from Codeforces and AtCoder
- calculates the score for all participants
- shows the ranking among all TUM participants.

## Usage
Install Python 3 and additionally the Python modules:
- `requests`
- `beautifulsoup4`
- `lxml`
(all available via pip).

For running the tool use `python3 main.py`. The current ranking will be printed to the console.
The `runbot.py` file is used to host a Telegram bot for which Telegram API keys are needed.

Atcoder now requires to be logged in to fetch the rankings. Therfore you need to provide valid login credentials in the file `.atcoder_config.txt`. The first line should contain the username, the second line the password.

## Contribution
Please feel free to contribute to the project by creating a pull request.
