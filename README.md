# Rhyme-Bot Description

Using a dictionary mapping words to their syllables, as well as a large list of sentences/phrases, this program uses the trie data sctructure to efficiently find the best rhyming phrases to user-inputted words/phrases.

A rhyming dictionary is provided and its location will be given as the first command line parameter. This dictionary gives the pronunciation of ~134,000 english words. Any words that are given as input and do not appear on this list will have an unknown pronunciation and do not rhyme with any other word. Note that if a sentence ends with a word with known pronunciation and contains a word with unknown pronunciation that the sentence as a whole can still rhyme with the input and be returned as output.

For the sake of speed, this program will generate save a large amount of data to the disk (approx 240mb) on its first run so that it can be read by the program very quickly on subsequent runs. The first run will be very slow. Please be patient.

# How-to

This program is run from using command-line Python using the following parameters:
```
python RhymeBot.py dictionaryFilename sentenceListFilename k user_phrase
```
This will use the dictionary and list of sentences to find the top k rhymes for the user inputted words. 

*dictionaryFilename* is the path the dictionary file. By default this is data/dictionary

*sentenceListFilename* is the path to the sentences file. By default this is data/phrases

*k* is the top number of rhymes you wish to find. The rhymes are outputted from better to worse.

*user_phrase* is the phrase inputted by that the user wishes to find rhymes for. Words must be separated by underscores.

Example: electrostatic_salad_cream will be parsed by the program as "electrostatic salad cream". If you don't use underscores the program will error.


