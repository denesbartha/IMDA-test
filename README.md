# Test 2 

Note: This repository contains a sample task for an interview question. The question can be found
in [AIS Test 2.docx](AIS%20Test%202.docx).

## Structure of the project

- [sampleCaptchas](http://hr-testcases.s3.amazonaws.com/2587/assets/sampleCaptchas.zip) contains
sample input and output examples for the task.
- [requirements.txt](requirements.txt) contains the packages needed for the project
- [captcha.py](captcha.py) contains the solution class for the task

## Running the project

A virtual Python environment is needed to be installed. A simple virtual environment
can be generated using the command `python -m venv venv` in a terminal.

Next step is to source the python environment in a terminal by running  the command
`source venv/bin/activate`.

Then install the requirements by running `pip install -r requirements.txt`

[captcha.py](captcha.py) can be executed by running
`python captcha.py <input_fname.jpg> <output_fname.txt>`

For example if the folder 
[sampleCaptchas](http://hr-testcases.s3.amazonaws.com/2587/assets/sampleCaptchas.zip)
already exists in the project, running the following command:

```shell
python captcha.py sampleCaptchas/input/input00.jpg sampleCaptchas/output/output00.txt
```
creates the file `sampleCaptchas/output/output00.txt` with the corresponding string output.

## Notes on the solution

### Constraints:
- All images have the same size: 30x60 pixels.
- All captcha use the same font
- The spacing between the letters are constant: 1 pixel
- All letters consists of 8x10 pixels.
- The starting position of the first letter is on the coordinate (5, 11)

###  Approach
The approach that we used here is simply to find the best matching scores for each letter that
uniquely identifies each of them. We use a statistical approach where we create a sum
by multiplying the matrix that contains the pixel values 0 or 1s of a given letter area by a matrix
that has the same dimensionality and each row `i` contains the first 8 prime numbers
`[2, 3, 5, 7, 11, 13, 17, 19]` element-wise multiplied by the weight of `11^i`.
This sum is uniquely describes each letter that we can just look up in a table in `O(1)` (if it
cannot be found, we find the closest element in the score table which takes `O(k)` where `k=36`,
that is the alphabet + # of numerical values).
Creating the score takes `O(w h)` time, where `w` is the width and `h` is the height of a letter.
In this task we fixed these values by `w=30` and `h=60`.

### Testing
I have tested the solution against the sample input and output sets. The results show identical
values for reconstructing the texts from the images.

```shell
# create a temp dir
mkdir sampleCaptchas/output2
ls sampleCaptchas/input/*.jpg | xargs -I {} sh -c 'filename=$(basename {}); numbers=$(echo $filename | grep -o "[0-9]\+"); python captcha.py {} sampleCaptchas/output2/output$numbers.txt'
ls sampleCaptchas/output/*.txt | xargs -I {} sh -c 'diff {} sampleCaptchas/output2/$(basename {})'
```
