[![Build Status](https://github.com/yakushechkin/robots-dinos/actions/workflows/main.yml/badge.svg)](https://github.com/yakushechkin/robots-dinos/actions/workflows/main.yml)


# robots-dinos
The 'robots-vs-dinos' challenge solution

## These are the features required:

- Be able to create an empty simulation space - an empty 50 x 50 grid;
- Be able to create a robot in a certain position and facing direction;
- Be able to create a dinosaur in a certain position;
- Issue instructions to a robot - a robot can turn left, turn right, move forward, move backward, and attack;
- A robot attack destroys dinosaurs around it (in front, to the left, to the right or behind);
- No need to worry about the dinosaurs - dinosaurs don't move;
- Display the simulation's current state;
- Two or more entities (robots or dinosaurs) cannot occupy the same position;
- Attempting to move a robot outside the simulation space is an invalid operation.

## Things we are looking for

- Immutability/Referential transparency;
- Idiomatic code;
- Adherence to community/standard library style guides;
- Separation of concerns;
- Unit and integration tests;
- API design;
- Domain modeling;
- Attention to possible concurrency issues;
- Error handling.
