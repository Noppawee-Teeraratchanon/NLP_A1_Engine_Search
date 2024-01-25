# NLP_A1_Engine_Search

To run app, 
1. Load the files from this repository
2. Run
```sh
python app/app.py
```
3. Access the app with http://127.0.0.1:5000  (but the app has not finished yet)

Data directory:
1. capital-common-countries.txt (from https://www.fit.vutbr.cz/~imikolov/rnnlm/word-test.v1.txt ) used for calculating semantic accuracy of each model
2. past-tense.text (from https://www.fit.vutbr.cz/~imikolov/rnnlm/word-test.v1.txt ) used for calculating syntactic accuracy of each model
3. wordsim353.txt (from http://alfonseca.org/eng/research/wordsim353.html) used for finding the correlation between model and human judgment

Dataset that I used to train: categories news data from nltk (brown)