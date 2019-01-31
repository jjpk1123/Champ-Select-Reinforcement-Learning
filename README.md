# Reinforcement Learning Project for League of Legends Champion Select
by Julien Pecquet, December 11th, 2018
# Introduction
League of Legends (A.K.A. LoL or League) is an Multiplayer Online Battle Arena (MOBA) game, where teams of 5 fight each other with the goal of destroying the opposing teams nexus (home base). [The League of Legends wikipedia](https://en.wikipedia.org/wiki/League_of_Legends) notes that in September 2016, the company who owns LoL, Riot Games, estimated that there are over 100 million active players each month. Currently, the 2018 World Championship is ongoing, which featured teams from North America, Europe, Latin America, South Korea, China, Taiwan, and many more. Last year's championship boasted 60 million unique viewers and a total prize pool of over 4 million USD. Needless to say, the pay off for succeeding in the League of Legends esports scene is enormous, and noticed by a huge population. This is one of my motivations for solving this problem.    
While it would be incredible to focus on a program who could play the real-time game against real people, this would be an incredibly deep problem requiring much more resources. This is in fact the part of the game which most people think of when they think about LoL. This being said, the portion of the game I want to focus on is similar to a card game. It is known as Champion Select. Before players can get to the MOBA action, they go through a turn-based game which takes about 5 minutes to decide which champions they get to play. It has many formats and I want to explore them all to see what my implementation will think is best within each format. I also am very excited to compare what my program will value as opposed to what players come up in different countries and different ranks, to my own ideas, and also to professional play. 
Before I dive into the specifics, let's think for a moment about the space complexity of this problem given the different drafts. There are (as of December 5th, 2018) 142 Champions in the League. Basic rules of league's interactive draft state that you can only have unique champions in the pick/bans. There are 5 bans per team, 5 champions per team. So there are (142 choose 20)=1.12 * 10^24 possible board states.<br>

Now, how do we cut this number up so that this problem is doable? We can potentially completely remove ban's from the game, when training. This would mean that the problem goes to (142 choose 10)=6.64 * 10^14, significantly smaller! Something else to note is that not every champion can play in every role. Some champions only play in 1 role, so once that role is chosen they no longer are a choice for that game state. Implied in this statement is the fact that each team needs 1 and only 1 of each role. From data gathered using methods defined below, there are 107 top laners, 86 junglers, 101 mid laners, 84 duo_carries, 83 duo_supports. This drastically reduces the space of the problem to be less than before. Perhaps it would work something like this:

((142) * (141) * (140) * (139) * (138) * (137) * (136) * (135) * (107) * (107))/(10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * (142-10)) = 3,232,609,275,050

My reasoning is that the first 4 choices per team (8 choices total) will, at worst, still allow choices of every remaining champion. But once you get to your last choice, you only have one role. I'm assuming the worst again, in that the last role picked is Top. 
How can we make the players pick things more randomly in a way that reflects a real game? We could have a mechanism for banning either a high general win-rate champ, or a random champ. This would mean that the most overpowered compositions would be found less often, and we wouldnt adhere to the meta quite as much. Making bans random would also reduce the amount of choices by a very significant amount. We can also make the opponent player randomly pick champions in order to increase processing time.

((132) * (131) * (130) * (129) * (128) * (127) * (126) * (125) * (107) * (107)) / (10 * 9 * 8 * 7 * 6 * 5 * 4 * 3 * 2 * (132-10)) = 1,920,070,742,519


My naivete brought me into this project thinking "it won't be so bad, what could go wrong?".
Well I'll tell you right now, the experiment failed because the problem is just too large to train the AI in a decent amount of time given the methods, organization, etc that I came up with. 
This project is still ongoing, but as it stands, this is what I've got!

# Outside Tools

The outside tools I am using are:
   * Champion.gg: Documentation found here: http://api.champion.gg/docs/#api-Champions
        * This tool is my primary one, which will get me an enormous amount of statistics for different champions in different roles with different other champions as their teammates or enemies. It has *almost* everything I need for the project.
   * Riot Games' Data Dragon: Documentation found here: https://developer.riotgames.com/static-data.html
        * This tool will allow me to do a great number of things to make my software easily usable (for me) and to make the output pretty! This service allows me to get images of champions, abilities, etc and more importantly for development it will allow me to get champion's descriptions by id (given to me from champion.gg requests).
   * Reinforcement Learning Algorithm: Taken from Dr. Andersons Fall 2018 'Intro to Artificial Intelligence' course at Colorado State University, and altered to fit my programs needs.  
