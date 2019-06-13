**Machi AI**

This project was originally made by McAndocia, his project is [here](https://github.com/mcandocia/machi_ai). Obviously, his code was written in Python 2. I forked his work and made some changes so it can be run in a python3.6 environment. I'm only a hobbyist coder, and by reading mcandocia's code I learned a lot of things. So many thanks to McAndocia.

(The following is written by McAndocia.)<br>
This is a small project that I worked on after I was wondering if I could use neural networks to simulate the game. Essentially, there are five types of decisions the AI can make, so I have five different neural networks predicting the outcome of a player winning a game at a particular point in time. In hindsight, I could have shared the networks, as most of the inputs are constant across them.

Here are a couple articles I wrote about the results:

* [General Insights](http://maxcandocia.com/article/2017/Jul/22/using-neural-networks-to-play-board-games/)

* [Strategy Extraction](http://maxcandocia.com/article/2017/Jul/30/using-ai-for-machi-koro-strategy/)

## A reminder
* This fork is for beginners who have not much experience in python.
* Pycharm IDE is recommended.
* The project can be run under Python 3.6 and tensorflow 1.13.1. Other version of Python3 and Tensorflow should work.
* McAndocia uses the number of turns in an episode to measure the AI's strength. It may have better performance metrics. 
* Althought the train will converge at 60 turns per episode, a human can beat the AI easily with cheese-factory strategy.
