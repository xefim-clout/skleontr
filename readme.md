
# Project Skleontr

## This is a Prompt Editor for GPT-like NLP tasks. It interacts with OpenAI or similar APIs.

Skleontr is a locally working text-mode Prompt Editor. The main goal of Skleontr is to create and edit text prompts using the help of GPT type engines. User can utilize a range of commands to create and test advanced prompts easy and effectively. For example find synonyms for certain word, expand a sentence into a paragraph, or enter a chat mode with GPT engine.\
For now the program is in ROUGH sketch phase, there is a lot to be done!\
So You are welcome to help by requesting new features, pointing out bugs or contributing code.

## Links

- [Repo](https://github.com/xefim-clout/skleontr "Skleontr Repo")

- [Bugs](https://github.com/xefim-clout/skleontr/issues "Issues Page")

## Screenshots

![](/screenshots/1111.png)

## Usage

!! Note that each app user has to provide their own API key from the OpenAI. "Bring your own key" is an important concept enforced to prevent API misuse.\
\
Skleontr imports OpenAI Api key from the environment variable "API_KEY". You have to set that up beforehand in Your environment:\
export API_KEY="`<your api key>`"\
\
Use arrow keys to navigate the cursor. Cursor has highlighted text background. Cursor selects either one word or collection of words. Each separate word or, if entered, a collection of words is considered one entity.\
UP/DOWN buttons navigate through the paragraphs and LEFT/RIGHT buttons - through the words in text.\
Press SPACE to mark the starting point of selection, move cursors RIGHT/LEFT to expand selection \
and press SPACE again to mark the end of selection. \
\
Shortcut keys are: e - edit a word (interactive), c - copy, v - paste, d - delete, ESC - exit........

## Available Commands

While working in the Skleontr command line, you can run: \
\
/ed or /edit: edit selected text; /open `<filename>`: read file; /sel or /select: select text; 
/del or /delete: delete selected text; /in or /insert: insert text; /paste: paste text;
/chat: chat with OpenAI GPT (using davinci engine); /save `<filename>`: save current text buffer; /exit: exit program


## Built With

- Python3
- OpenAI library
- Curses library


## Future Updates

- [ ] Many new features

## Author

**Xefim-Clout**

- [Profile](https://github.com/xefim-clout "Xefim Clout")
- [Email]("vertinski@inbox.lv")

## 🤝 Support

Contributions, issues, and feature requests are welcome!

Give a ⭐️ if you like this project!

