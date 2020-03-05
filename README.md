# Flappy-Bird-Genetic-Algorithm
A genetic algorithm that plays Flappy Bird

A genetic algorithm is an evolutionary algorithm, which is based on Darwin's theory of evolution.
It models the process of natural selection, where the fittest individuals of a generation are selected to produce offspring, which will constitute the next generation.
Overtime, the overall performance of each generation keeps improving, and usually at a certain point, an optimum solution for survival is found.

Flappy Bird is one of the most popular arcade games, where the aim is to try and get a yellow bird to sneak through gaps between obstacles, which are long green pipes in this case.
The game doesn't have an ending; you can only keep on improving your previous high score.

This program consists of a genetic algorithm that tries to optimise the birds to sneak through every gap that it comes across.
It begins with a generation of birds whose parametres (which instruct them on how to play the game) are set randomly. 
Then after the first generation, the process of natural selection begins: the best performing bird is picked, and its multiple copies are made.
The parametres of all the copies are altered with mutations, which are random. And then again, the birds are made to play the game, and again this time, the best performing bird is picked, and the whole process repeats again, till a certain target is reached in the game (which the user can choose to change in the code file).

Considering a target of 50 points, the birds on average take anywhere from 10-20 generations to reach there. But sometimes, they get really lucky and they manage to achieve it in the first attempt itself, and on other times, they end up taking more than 40 generations.

The program plays out almost like a video clip, so just run it, sit back, and enjoy watching the birds learn to play Flappy Bird better and better over time!

