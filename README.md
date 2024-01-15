# sozcukApp (terminated temporarily)
Daily word puzzle

> The game is currently terminated temporarily due to the lack of time to maintain it.

sözcük.app is a daily word game made with the inspiration of the games like Wordle, Kelime Oyunu, parolla.app, etc.  
Each day, 14 random words with different lengths are chosen from Turkish Language Association's (TDK) dictionary.  
The goal is to find the words by guessing them.

---
The game is hosted using AWS Elastic Beanstalk.  
The game uses AWS RDS for the database.
---

> I know that the repo is a mess.

## dashboard
A streamlit dashboard to see the statistics of the game, such as points, number of words remaining, visits, etc.

## data_words
You can see the full word list, as well as the process of eliminating the words that are not suitable for the game using `fuzzywuzzy` library, such as words with high similarity with the answer.

## sozcukApp
The Django project that contains the main game.  
Data is stored in a MySQL database on AWS RDS, which I did not provide the credentials for but you can find the word list in `data_words` folder.
You can also find a Slack bot that messages me whenever a new player completes the game.