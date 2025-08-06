# enjoy_gaming_test
Test task for Enjoy Gaming

Comments:
1. I didn't remove or restructure any class because I assume that this is business logic and lots of things may and should depend on it.
But if I would write it all from scratch I would talk through future plans on them and most probably would remove base class for games and unused model class. 
As "Composition is better than inheritance" I'd prefer having a class for each game, and come back to inheritance in future if architecture would demand it.

2. On extra task. My observations tell me that this game implementation has no loose mechanics which makes it impossible to get RTP less than 100%.
To hit such RTP I would have to partly reinvent some parts of the game and it would end in totally another game. But I'd be glad to talk about what could be done.

3. Task 2. I used Dependency Injection so that QA could pass fixed arrays of numbers when initializing Game object to control the outcome of the game.
Here also I could go deeper and separate all the usages of those numbers to funcions - it would be easier to test those logics. But I'm not sure that this is necessary in this task.

4. I fixed some typos too and renamed variables. Maybe some names are not the best, but I believe they're better than short ones. 