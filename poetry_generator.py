"""
Nicole Nigro
CSCI 3725
M6: Poetry Slam
4/16/21

Generates and evaluates poems in the tanka form.

Dependencies: nltk, glob, os, random, re, string, num2words, syllapy, text2emotion, textstat
"""


import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import glob, os, random, re, string
import num2words
import syllapy
import text2emotion as te
import textstat


class Tanka():
    def __init__(self):
        """
        Initializes a Tanka object with 5 lines (since it's a 5 line poem, typically with a 5-7-5-7-7 syllable pattern),
        a bigrams dictionary, an all_words list, a last_words tuple, a syllable_pattern, an emotions
        dictionary, a boolean grammar_correct, an understandability_score, and an understandability_category.
        Args: 
            None
        Return:
            None
        """
        self.line_1 = ""
        self.line_2 = ""
        self.line_3 = ""
        self.line_4 = ""
        self.line_5 = ""
        self.bigrams = dict()
        self.all_words = []
        self.last_words = ()
        self.syllable_pattern = ""
        self.emotions = dict()
        self.grammar_correct = False
        self.understandability_score = 0
        self.understandability_category = ""
        
    def read_files(self, input_dir):
        """
        Read in the files from the inspiring set.
        Arg:
            input_dir (str): name of directory the inspiring set of poems are in
        Return:
            None
        """
        for filename in glob.glob(input_dir):
            with open(os.path.join(filename), encoding='utf-8') as f:
                poem_words = []
                for word in f.read().split():
                    #keeps and, inserts space wherever there is a --, gets rid of odd punctuations ’ “ ”
                    prep_word = word.lower().replace("&", "and").replace("--", " ").replace("’", "").replace("“", "").replace("”", "")

                    #removes punctuation except for -
                    exclude = string.punctuation.replace("-", "")
                    table = str.maketrans('', '', exclude)
                    cleaned_word = prep_word.translate(table)

                    #replaces numbers with their words
                    num_free_word = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), cleaned_word) 
                    
                    if num_free_word not in self.all_words:
                        self.all_words.append(num_free_word)

                    poem_words.append(num_free_word)
                
                #create bigrams using the words in the current poem
                self.create_bigrams(poem_words)

    def create_bigrams(self, words):
        """
        Creates 2-word ngrams and adds them and the words that follow after with their frequencies
        to the bigrams dictionary. 
        Arg:
            words (list): list of words in a poem
        Return:
            None
        """
        for i in range(len(words)-2):
            ngram = (words[i], words[i+1])
            next_word = words[i+2]

            #update frequency count if next_word is already in the dictionary of values for ngram
            if ngram in self.bigrams and next_word in self.bigrams[ngram]:
                self.bigrams[ngram][next_word] += 1
            
            #if ngram is in bigrams, but next_word isn't in the dictionary of values, add next_word with a frequency of 1
            elif ngram in self.bigrams:
                self.bigrams[ngram][next_word] = 1
            
            #add ngram to bigrams as the key and {next_word: 1} as the value
            else:
                self.bigrams[ngram] = dict()
                self.bigrams[ngram][next_word] = 1
            
    def syllables(self, word):
        """
        Counts the number of syllables in a word/phrase using the syllapy package.
        Arg:
            word (str): the word or phrase
        Return:
            word_syllables (int): the number of syllables in the word or phrase
        """
        word_syllables =  syllapy.count(word)
        return word_syllables
    
    def get_next_word(self, word_pair):
        """
        Gets the next word based on the frequencies of the words following the current pair of words.
        Arg:
            word_pair (tuple): the current pair of words
        Return:
            next_word (str): the word chosen to follow next in the poem
        """
        if word_pair in self.bigrams:
            #select a word with word_frequencies used to weight the decision
            word_options = list(self.bigrams[word_pair].keys())
            word_frequencies = [self.bigrams[word_pair][i] for i in word_options]
            next_word = random.choices(population=word_options, weights=word_frequencies, k=1)[0]
        else:
            #randomly select a word from the all_words list
            word_index = random.randint(0, len(self.all_words)-1)
            next_word = self.all_words[word_index]
        return next_word
    
    def write_kaminoku(self):
        """
        Writes the first 3 parts of a tanka in 5-7-5 syllable pattern.
        Args:
            None
        Return:
            None
        """
        ready = False

        while not ready:
            #randomly select a pair of words to start the tanka
            start_index = random.randint(0, len(self.bigrams)-1)
            current_pair = tuple(list(self.bigrams)[start_index])

            #first word shouldn't be an article because they reduce poetic compression and weaken the poetic impact of the form
            if pos_tag(word_tokenize(current_pair[0]))[0][1] != "DT" and pos_tag(word_tokenize(current_pair[0]))[0][1] != "WDT" \
                 and self.syllables(str(current_pair)) <= 5:
                ready = True

        self.line_1 += current_pair[0] + " " + current_pair[1] + " "

        #keep writing (selecting the next word and adding it to the line) as long as the syllable count is less than 5
        while self.syllables(self.line_1) < 5:
            next_word = self.get_next_word(current_pair)
            self.line_1 += next_word + " "
            current_pair = (current_pair[1], next_word)

        while self.syllables(self.line_2) < 7:
            next_word = self.get_next_word(current_pair)
            self.line_2 += next_word + " "
            current_pair = (current_pair[1], next_word)

        while self.syllables(self.line_3) < 5:
            next_word = self.get_next_word(current_pair)
            self.line_3 += next_word + " "
            current_pair = (current_pair[1], next_word)
        
        self.last_words = current_pair

    def write_shimonoku(self):
        """
        Writes the last 2 parts of a tanka in 7-7 syllable pattern.
        Args:
            None
        Return:
            None
        """
        current_pair = self.last_words

        while self.syllables(self.line_4) < 7:
            next_word = self.get_next_word(current_pair)
            self.line_4 += next_word + " "
            current_pair = (current_pair[1], next_word)
        
        while self.syllables(self.line_5) < 7:
            next_word = self.get_next_word(current_pair)
            self.line_5 += next_word + " "
            current_pair = (current_pair[1], next_word)

    def edit_tanka(self):
        """
        After having a rough draft of the tanka, edit to make sure it fits a tanka syllable pattern.
        Args:
            None
        Return:
            None
        """
        if self.syllables(self.line_1) == 5 and self.syllables(self.line_2) == 7 and self.syllables(self.line_3) == 5 and \
            self.syllables(self.line_4) == 8 and self.syllables(self.line_5) == 7:
            self.syllable_pattern = "ji-amari (exceeds the typical syllable count) - 5-7-5-8-7"
        elif self.syllables(self.line_1) == 5 and self.syllables(self.line_2) == 7 and self.syllables(self.line_3) == 5 and \
            self.syllables(self.line_4) == 7 and self.syllables(self.line_5) == 6:
            self.syllable_pattern = "ji-tarazu (runs short) - 5-7-5-7-6"
        elif self.syllables(self.line_1) == 5 and self.syllables(self.line_2) == 7 and self.syllables(self.line_3) == 5 and \
            self.syllables(self.line_4) == 9 and self.syllables(self.line_5) == 5:
            self.syllable_pattern = "ku-ware (splitting) - 5-7-5-9-5"
        elif self.syllables(self.line_1) == 8 and self.syllables(self.line_2) == 4 and self.syllables(self.line_3) == 5 and \
            self.syllables(self.line_4) == 7 and self.syllables(self.line_5) == 7:
            self.syllable_pattern = "ku-matagari (straddling) - 8-4-5-7-7"
        elif self.syllables(self.line_1) == 5 and self.syllables(self.line_2) == 7 and self.syllables(self.line_3) == 5 and \
            self.syllables(self.line_4) == 7 and self.syllables(self.line_5) == 7:
            self.syllable_pattern = "standard - 5-7-5-7-7" 
        else: 
            pass
    
    def write_tanka(self):
        """
        Writes a complete tanka, consisting of the kami-no-ku and shimo-no-ku, and then edits it.
        Args:
            None
        Return:
            poem (str): the completed tanka
        """
        self.write_kaminoku()
        self.write_shimonoku()
        self.edit_tanka()

        poem = self.line_1 + self.line_2 + self.line_3 + self.line_4 + self.line_5

        return poem

    def export_poem(self):
        """
        Exports a poem to an output folder.
        Args:
            None
        Return:
            None
        """
        output_path = os.path.join("output", "tanka5.txt")
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(self.line_1.strip() + "\n")
            f.write(self.line_2.strip()  + "\n")
            f.write(self.line_3.strip()  + "\n")
            f.write(self.line_4.strip()  + "\n")
            f.write(self.line_5.strip())
        
    def export_pos_tags(self):
        """
        Exports a file with all the words that are of a specified part of speech.
        Args:
            None
        Return:
            None
        """
        output_path = os.path.join("pos_tags", "WRB.txt")
        with open(output_path, "w", encoding='utf-8') as f:
            for word in self.all_words:
                if len(pos_tag(word_tokenize(word))) == 0:
                    pass
                elif pos_tag(word_tokenize(word))[0][1] == "WRB":
                    f.write("'" + str(pos_tag(word_tokenize(word))[0][0] + "'" + " | "))
                else:
                    pass

    def perform_poem(self, poem):
        """
        Performs a tanka out loud.
        Arg:
            poem (str): the tanka to be performed
        Return:
            None
        """
        #randomly selects one of four voices
        voices = ["Samantha", "Victoria", "Alex", "Fred"]
        speaker = random.choice(voices)

        os.system("say -v " + speaker + " " + poem)
    
    def evaluate_emotions(self, poem):
        """
        Evaluates the emotions of a poem (happy, angry, surprise, sad, fear) using the text2emotion package.
        Arg:
            poem (str): the poem to evaluate
        Return
            emotions (dict): a dictionary with the 5 emotions and the poem's score for each
        """
        self.emotions = te.get_emotion(poem)
        return self.emotions
    
    def evaluate_grammar(self, poem):
        """
        Evaluates the grammar of a poem. Uses code from: https://www.fireblazeaischool.in/blogs/grammar-checking-using-nltk/
        Arg:
            poem (str): the poem to evaluate
        Return:
            grammar_correct (bool): whether or not the poem is gramatically corect (T/F)
        """
        load_grammar = nltk.data.load('file:grammar.cfg')
        wrong_syntax = 1
        poem_split = poem.split()
        rd_parser = nltk.RecursiveDescentParser(load_grammar)
        for tree_struc in rd_parser.parse(poem_split):
            s = tree_struc
            wrong_syntax = 0 
            self.grammar_correct = True
        if wrong_syntax == 1:
            self.grammar_correct = False
        return self.grammar_correct

    def evaluate_understandability(self, poem):
        """
        Evalautes the understandability using the textstat package. The flesch_reading_ease() method
        is used to measure the readability of a poem.
        Arg:
            poem (str): the poem to evaluate
        Return:
            understandability (float): the flesch reading ease score
        """
        self.understandability_score = textstat.flesch_reading_ease(poem)

        #categorize the score into the different Flesch Reading Ease Score categories
        if self.understandability_score >= 90.0:
            self.understandability_category = "Very Easy"
        elif 80.0 <= self.understandability_score <= 89.99:
            self.understandability_category = "Easy"
        elif 70.0 <= self.understandability_score <= 79.99:
            self.understandability_category = "Fairly Easy"
        elif 60.0 <= self.understandability_score <= 69.99:
            self.understandability_category = "Standard"
        elif 50.0 <= self.understandability_score <= 59.99:
            self.understandability_category = "Fairly Difficult"
        elif 30.0 <= self.understandability_score <= 49.99:
            self.understandability_category = "Difficult"
        else:
            self.understandability_category = "Very Confusing"

        return self.understandability_score

    def export_metrics(self):
        """
        Exports the the syllable pattern and metrics from evaluation of the tanka: emotions, grammar,
        understandability.
        Args:
            None
        Return:
            None
        """
        output_path = os.path.join("metrics", "tanka5-metrics.txt")
        with open(output_path, "w", encoding='utf-8') as f:
            f.write("Syllable Pattern: " + self.syllable_pattern + "\n")
            f.write("Emotions: " + str(self.emotions) + "\n")
            f.write("Grammar Correct: " + str(self.grammar_correct) + "\n")
            f.write("Understandability: " + str(self.understandability_score) + " (" + self.understandability_category + ") \n")
    
    def __str__(self):
        """
        Returns a string representation of this Tanka
        Args:
            None
        Return:
            output (str): the string representing a Tanka object
        """
        output = self.line_1 + "\n" + self.line_2 + "\n" + self.line_3 + "\n" + self.line_4 + "\n" + self.line_5
        return output

    def __repr__(self):
        """
        Returns a representation of a Tanka object
        Args:
            None
        Return:
            the string representing a Tanka object
        """
        return "Tanka('{0}', '{1}', '{2}', '{3}', '{4}')".format(self.line_1, self.line_2, self.line_3, self.line_4, self.line_5)


def main():
    ready = False

    #generate tankas until there is one that is understandable enough and follows one of the syllable patterns
    while not ready:
        t = Tanka()
        t.read_files("input/*")
        p = t.write_tanka()
        t.evaluate_emotions(p)
        t.evaluate_grammar(p)
        t.evaluate_understandability(p)
        if t.understandability_score >= 60.0 and t.syllable_pattern != "":
            t.perform_poem(p)
            t.export_poem()
            t.export_metrics()
            print(t.__str__())
            ready = True

if __name__ == "__main__":
    main()