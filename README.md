Exercises in Programming Style
==============================

Comprehensive collection of well-known, and not so well-known, programming
styles using a simple computational task, term frequency. All programs run 
with the following command line:

```bash
python tf-NN.py ../pride-and-prejudice.txt
```

NOTE: the code in the master branch is written for Python 3. If you are looking
for a version for Python 2.7, check out the 2.7 branch or the v1.0 release.

Explanations and historical context for all these styles can be found in the
companion book [Exercises in Programming Style](http://www.amazon.com/Exercises-Programming-Style-Cristina-Videira/dp/1482227371/).

Additions are welcome! 

You can contribute: 
- new exercises related to the existing styles
- an entirely new programming style
- new names for the existing styles
- discussion of names, pros and cons of each style

Because this project and the companion book are used in courses, at the
suggestion of several students I am no longer accepting contributions 
of the existing styles written in different programming languages. 
That is the first exercise that the students do. Having the solutions
easily available here will rob future students of the learning experience!

Please follow the conventions suggested by the existing code base,
specifically, if you are contributing a new style, make a new folder called
nn-funname and add an example program in that folder called
tf-nn.ext. (nn is the next avalaible number in the collection)
Additionally, add a README.md file that clearly describes the
contraints for writing programs in that style. I will only consider
new styles corresponding to constraints that are clearly different
from the ones that already exist in the collection. (different
programs written in existing styles are exercises for students, and
should not be here)

Contributions of new names and discussion should be done under Issues
or on the Wiki part of this repo.

To test your work, make sure your script is executable and then run:

```
./test/test.sh NN
```

Where `NN` is the number prefix of the directory you're adding.

Never stop exercising!

Love,
Crista

P.S. Inspiration for this collection: http://en.wikipedia.org/wiki/Exercises_in_Style

