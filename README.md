# MarplePuzzle-solver

An efficient Java program which solves any deducible marple logic game:
![X](http://www.kotiposti.net/sodacan/marple/tut/t1.png)


There are four different types of clues:

`ABC` :	"In between" clues consist of three different tiles. They indicate that the middle tile is located in between the other two tiles. It however doesn't tell the order of the other two tiles ( can be on the left side with  on the right side or  on the left side with  on the right side). Also, it does not indicate that the tiles would be located in adjacent columns (for example,  can be on the first column,  on the second column and  on the fifth column).
`A..C`:	"Left of" clues consist of two tiles with "…" in the middle. They indicate that the tile on the left has to be located left of the right side tile. They however do not indicate whether the tiles are located in adjacent columns (for example  can be on the first column with  on the fifth column).
`ABC` :	"Next to" clues consist of two tiles. They indicate that the two tiles have to be located in adjacent columns but they don't tell which one of the tiles tiles is on the left side and which one is on the right side.
`A^C` :	"Same column" clues consist of two tiles with a double headed arrow between them. They indicate that the two tiles are located in on the same column.
