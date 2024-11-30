# Deep Q-Learning Blackjack Agent

This project implements a Deep Q-Learning (DQN) agent to master the game of Blackjack and try to beat the dealer as often as possible. This project was made using the Flask web framework for Python, as well as simple HTML and CSS for the frontend. The DQN agent was also built using Python.

Blackjack is a very simple game. The goal is to get to a score of 21 (or as close to it as possible), but without going over, which results in a "bust". Detailed rules for the game can be found [here](https://bicyclecards.com/how-to-play/blackjack). However, the goal of our agent is to optimize it to beat the dealer as frequently as possible by either "hitting" (taking another card) or "standing" (keeping the value of our current cards). In order to calculate the most optimal move, our agent is constantly improving, by taking into consideration factors such as:
* Value of the current hand
* Whether there is an ace in our hand
* Value of the visible dealer card
* Ratio of high-value cards left in the deck
* Ratio of low-value cards left in the deck
* Ratio of aces left in the deck

Using these numbers, as well as results of the games, the agent continuously improves the probability of beating the dealer.

