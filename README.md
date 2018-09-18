# freeSteamGamesNotifier
The following repository contains a Python script to notify us, with a facebook message, whenever there is a new free Steam game on some selected sites.

# Usage Notes
When the script is run for the first time a database will be created in SQLite with multiple tables if no database exists yet. You will then be asked if you want to add new users, these users are the people who will receive the messages whenever there is a new game for free. And lastly you will be asked for a username and the facebook pass word that will send the messages.

  #Attention
    - Users have to be friends on Facebook who will send the message.
    - When you enter a new user, what you have to insert is the Facebook name of the person who will receive the notification message.
      e.g.: Mark Zuckerberg
    - After the script is working if you want to re-add more users just press Ctrl + c and the question will again appear to add more user.
    - In this version if you want to change Facebook that will send the messages or delete users you have to delete the database and start all over again or edit directly in the database.
    - I am not responsible if the Facebook that sends the messages take a block by initiating too many conversations simultaneously.

# Dependencies
 - Python 3.x.x
 - BeautifulSoup
 - fbchat
 - Requests
 - sqlite3


Made with ❤️ in Portugal
