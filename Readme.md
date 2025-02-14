# README

This is a tool to search for the periodic distinguishers, showing all the model in the main body of our paper.

## Model

All our characterization rules are implemented in `operation_6bit_l.py`. This script allows users to run various algorithms, generating an output file named `model2.cvc`.

To obtain solutions for the model, run the command `stp model2.cvc`. The results of the model's solutions will be stored in `res.txt`.

Additionally, you can use `process_path.py` to read and interpret the information contained in the solution file.


### Key Variables

- `num_R_color`: Represents the round of the distinguisher.
- `num_R_linear`: Indicates the round of the tail linear path. (set to 0 is also valid)
- `num_pr`: Specifies the number of collisions. 
- `num_branch`: the number of tyhe branches of the structure. (no need to modify)

### Usage Instructions

1. Execute `{cipher}.py` to run the desired cipher.
2. Use the command `stp model2.cvc` to solve the model.
3. Access the solutions in `res.txt`.
4. Run `process_path.py` to extract and process the information from the solutions.

### Experiments

The experimental section `Experiments` presents the search for actual periods of various ciphers.
For Skipjack and Skipjack-B, the experiments are available at `Experiments/skipjack/test_skipjack_15r.py` and `Experiments/skipjack/test_skipjackB_16r.py`.

### STP Tool Installation and Usage

For information on installing the STP tool, please refer to: 
https://stp.readthedocs.io/en/latest/

For guidance on using the STP tool, please see: 
https://stp.readthedocs.io/en/stable/cvc-input-language.html