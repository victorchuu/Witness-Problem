### Witness Problem

This repository contains the code articats related to the article *Complexity and resolution of spatio-temporal reasonings for criminology with greedy and evolutionary algorithms*.

The document introduces two NPO problems, WPO and WPO[1], with the aim of reconstructing the most plausible routes of the different parties involved in a crime scene, provided the testimonies of some witnesses. WPO[1] in particular, the problem studied in this repository, only one actor participates in the crime scene, so only one route shall be found.

Find more details regarding the definition of the problem, its computational complexity, and the conclussions about the experimental results int the article: TODO - Add reference


### Contents of this repository

Short-put, this repository provides:
- The different data classes that represent instances and solutions of the problem, in `src/witnessproblem/` folder
- All the instances used in the article, including the case study, in `instances`, as well as the random instance generators used to create them.
- The raw results of the experiments made in `solutions` directory, as well as the python scripts used (`run.py` and `runRealCase.py`)
- Implementations of all the proposed algorithms mentioned in the article:
  - Time-based and testimony-based **Greedy** algorithms live in `src/solutions/greedy`
  - A (computationally intensive) exact algorithm using branc-and-bound method in `src/solutions/optimal`
  - A Memetic Algorithm (that can be used as a Genetic Algorithm by setting the local search probability to 0) to obtain approximate results for the problem, defined across `src/geneticAlgorithm` and `src/geneticOperators`


### How to use this package

To evaluate the algorithms on the instances stored in `instances` folder, one needs to execute the command:
```
python run.py <startIn> <endIn> <filename> algorithm1 algorithm2 ...
```
Where `startIn` and `endIn` are integers indicating which instancess to process in the instance set, `filename` is the name of the instance set (like "I1", "I2"...).
The different kaywords for the algorithms are
- `greedy` executes both greedy algorithms
- `exact` executes the exact branch-and-bound algorithm
- `genetic` executes the Genetic Algorithm and Memetic Algorithm stopping after 100 iterations
- `genetic-timed` executes the Genetic Algorithm and Memetic Algorithm stopping after 20 seconds

Beware that some algorithms might take a long time to complete. Details on each algorithm's complecity time can be found in the article

To evaluate number of times the algorithms predict the actor's exit corner in the case study, one needs to execute the command:
```
python runRealCase.py <startIn> <endIn> algorithm1 algorithm2 ...
```