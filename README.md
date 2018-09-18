# freeSteamGamesNotifier
The following repository contains a Python script to notify us, with a facebook message, whenever there is a new free Steam game on some selected sites.

# Usage Notes
Quando o script for executado pela primeira vez vai ser criada uma base de dados em SQLite com várias tabelas, se ainda não existir nenhuma base de dados. De seguida será perguntado se voce quer adicionar novos utilizadores, esses utilizadores são as pessoas que vão receber as mensagens sempre que existir um novo jogo grátis. E por ultimo irá ser pedido um nome de utilizador e a palavra pass do facebook que vai enviar as mensagens.
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
