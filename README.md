# Resolution-Inference
### This is an AI project using python as programming language, inplementing resolution inference algorithm to judge whether a literal can be inferred by a give set of knowledge base. 
### The program read file from a file whose name should be"input.txt".And the out put is in "output.txt".
### Format for input.txt:

#### NQ = NUMBER OF QUERIES
#### QUERY 1
#### ...
#### QUERY NQ
#### NS = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE
#### SENTENCE 1
#### ...
#### SENTENCE NS

Besides,any operator and its operands will always be surrounded by a parenthesis.

#### e.g.:
#### 1
#### Full(Sam)
#### 6
#### ((Hungry(x)&Have(x,Food))=>Eat(x,Food))
#### (Eat(x,Food)=>Full(x))
#### Hungry(Sam)
#### Have(Sam,Food)
#### (Hungry(x)=>(~Full(x)))
#### ((~Full(x))=>Hungry(x))

#### However the result does not guarantee 100% correctness for some complex logic.
There still might be some bugs.
