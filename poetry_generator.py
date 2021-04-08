"""
M6: Poetry Slam
CSCI 3725
Nicole Nigro
4/8/21

Dependencies: glob, os, random, string, syllapy, nltk, text2emotion, textstat

TODO: 
* fix if statements functions so that syllable counts match 5/7/5/7/7 syllable pattern
* lines should not begin with articles <- implement for last 4 lines
* PROCESS: What contextual information might inspire your computational poet? How might it move from inspiration to planning to creation?
    * have the first 2 line adress the experience of the poet (what they saw, heard, felt, etc.)
    * have the third line (turn/pivot) change the tone of the poem, relating to 2 lines above and below
    * have final 2 lines express a profound transcendental meaning that prompts reflection
    * Conceptual and syntactical knowledge bases
        * SYNTACTICAL:
            * must obey linguistic conventions, prescribed by a given grammar and lexicon (grammaticality)
        * CONCEPTUAL:
            * must convey a conceptual message, meaningful under some interpretation (meaningfulness)
* EVALUATION
    * grammar
    * unity?
    * message?
* display poem on the screen
    * implement Deepmoji: https://medium.com/@b.terryjack/nlp-pre-trained-sentiment-analysis-1eb52a9d742c
* incorporate more creativity theory from class

TANKA INFO
Third line is a turn/pivotal image, which marks the transition from the examination of an image to the examination of the personal response.
In its purest form, tanka poems are most commonly written as expressions of gratitude, love, or self-reflection. Suitors would send
a tanka to a woman the day after a date, and she would reply in kind. These were short messages (like secret letters) expressing love,
desire, meaning, or gratitude. These poems often culminated in a transcendental message. Because tanka poems are meant to be given to
someone, they are written from the viewpoint of the poet. That does not mean they must be written in the first person, but the poet is
ever-present, always writing to express personal feelings about the subject. Like any constrained poem, lines should not begin with
articles (e.g., “a” or “the”) because articles reduce poetic compression and weaken the poetic impact of the form. In terms of content,
the kami-no-ku and shimo-no-ku tend to make a pair. Tanka is more likely to have transitions in narrative or mood. Traditionally, tanka has
addressed a limited number of themes, from seasons to love to travel to death, but contemporary tanka has tackled a much wider range of topics
within the age-old form.

TANKA RECIPE
Start with two lines addressing the experience of the poet, what they saw, heard, felt, tasted, smelled etc.
Add a third line (called the turn or pivot) which changes the tone of the poem. It should relate separately to the two lines above and below.
Finish with two lines which express a profound transcendental meaning that prompts reflection.
"""

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import glob, os, random, string, syllapy
import text2emotion as te
import textstat

class Tanka():
    def __init__(self):
        """
        Initializes a Tanka object with 5 lines (since it's a 5 line poem with a 5-7-5-7-7 syllable pattern),
        a last_words tuple, a ngrams dictionary, and an all_words list.
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
        self.last_words = ()
        self.ngrams = dict()
        self.all_words = []
        self.pos_tags = []
        
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
                    prep_word = word.lower().replace("&", "and").replace("--", "")
                    exclude = string.punctuation.replace("'", "").replace("-", "")
                    table = str.maketrans('', '', exclude) #removes punctuation (except ' and -)
                    cleaned_word = prep_word.translate(table)
                    if word not in self.all_words:
                        self.all_words.append(cleaned_word)
                    poem_words.append(cleaned_word)
                self.create_ngrams(poem_words)

    def create_ngrams(self, words):
        """
        Creates 2-word ngrams.
        Arg:
            words (list): list of words in a poem
        Return:
            ngrams (dict): 2-word ngrams and the words that follow after and their frequencies
        """
        for i in range(len(words)-2):
            ngram = (words[i], words[i+1])
            next_word = words[i+2]
            if ngram in self.ngrams and next_word in self.ngrams[ngram]:
                self.ngrams[ngram][next_word] += 1
            elif ngram in self.ngrams:
                self.ngrams[ngram][next_word] = 1
            else:
                self.ngrams[ngram] = dict()
                self.ngrams[ngram][next_word] = 1
        return self.ngrams

    def tag_words(self):
        """
        Tags every word with a part of speech
        Args:
            None
        Return:
            None
        """
        for word in self.all_words:
            self.pos_tags.append(pos_tag(word_tokenize(word)))

    def syllables(self, word):
        """
        Counts the number of syllables in a word.
        Arg:
            word (str): the word
        Return:
            word_syllables (int): the number of syllables in the word
        """
        word_syllables = syllapy.count(word)
        return word_syllables
    
    def get_next_word(self, word_pair):
        """
        Gets the next word based on the frequencies of the words following the current pair of words.
        Arg:
            word_pair (tuple): the current pair of words
        Return:
            next_word (str): the word chosen to follow next in the poem
        """
        if word_pair in self.ngrams:
            word_options = list(self.ngrams[word_pair].keys())
            word_frequencies = [self.ngrams[word_pair][i] for i in word_options]
            next_word = random.choices(population=word_options, weights=word_frequencies, k=1)[0]
        else:
            word_index = random.randint(0, len(self.all_words)-1)
            next_word = self.all_words[word_index]
        return next_word

    def write_kaminoku(self, current_pair):
        """
        Writes the first 3 parts of a tanka in 5-7-5 syllable pattern.
        Args:
            current_pair (tuple): the current pair of words used to start writing the kami-no-ku
        Return:
            None
        """
        self.line_1 += current_pair[0] + " " + current_pair[1] + " "
        syllable_count = self.syllables(str(current_pair))

        while syllable_count < 5:
            next_word = self.get_next_word(current_pair)
            word_syllables = self.syllables(next_word)

            #if (word_syllables + syllable_count) <= 5:
            self.line_1 += next_word + " "
            current_pair = (current_pair[1], next_word)
            syllable_count += word_syllables
        
        syllable_count = 0

        while syllable_count < 7:
            next_word = self.get_next_word(current_pair)
            word_syllables = self.syllables(next_word)

            #if (word_syllables + syllable_count) <= 7:
            self.line_2 += next_word + " "
            current_pair = (current_pair[1], next_word)
            syllable_count += word_syllables

        syllable_count = 0

        while syllable_count < 5:
            next_word = self.get_next_word(current_pair)
            word_syllables = self.syllables(next_word)

            #if (word_syllables + syllable_count) <= 5:
            self.line_3 += next_word + " "
            current_pair = (current_pair[1], next_word)
            syllable_count += word_syllables
        
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
        syllable_count = 0

        while syllable_count < 7:
            next_word = self.get_next_word(current_pair)
            word_syllables = self.syllables(next_word)

            if (word_syllables + syllable_count) > 7:
                next_word = self.get_next_word(current_pair)
            
            self.line_4 += next_word + " "
            current_pair = (current_pair[1], next_word)
            syllable_count += word_syllables
            
        syllable_count = 0

        while syllable_count < 7:
            next_word = self.get_next_word(current_pair)
            word_syllables = self.syllables(next_word)

            if (word_syllables + syllable_count) > 7:
                next_word = self.get_next_word(current_pair)
                word_syllables = self.syllables(next_word)
            
            self.line_5 += next_word + " "
            current_pair = (current_pair[1], next_word)
            syllable_count += word_syllables

    def write_tanka(self):
        """
        Writes a complete tanka, consisting of the kami-no-ku and shimo-no-ku.
        Args:
            None
        Return:
            poem (str): the 5-line tanka
        """
        start_index = random.randint(0, len(self.ngrams)-1)
        start_pair = tuple(list(self.ngrams)[start_index])

        if pos_tag(word_tokenize(start_pair[0]))[0][1] == "DT": #first word of a line shouldn't be an article
            start_index = random.randint(0, len(self.ngrams)-1)
            start_pair = tuple(list(self.ngrams)[start_index])

        self.write_kaminoku(start_pair)
        self.write_shimonoku()

        poem = self.line_1 + self.line_2 + self.line_3 + self.line_4 + self.line_5
        return poem

    def export_poem(self):
        """
        Exports the poem to an output folder.
        Args:
            None
        Return:
            None
        """
        output_path = os.path.join("output", "tanka2.txt")
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(self.line_1 + "\n")
            f.write(self.line_2 + "\n")
            f.write(self.line_3 + "\n")
            f.write(self.line_4 + "\n")
            f.write(self.line_5)

    def perform_poem(self, poem):
        """
        Performs a tanka out loud.
        Args:
            poem (str): the tanka to be performed
        Return:
            None
        """
        voices = ["Samantha", "Victoria", "Alex", "Fred"]
        speaker = random.choice(voices)
        os.system("say -v " + speaker + " " + poem)
    
    def evaluate_emotions(self, poem):
        """
        Evaluates the emotions of a poem (happy, angry, surprise, sad, fear) using the text2emotion package.
        Args:
            poem (str): the poem to evaluate
        Return
            emotions (dict): a dictionary with the 5 emotions and the poem's score for each
        """
        emotions = te.get_emotion(poem)
        return emotions
    
    def evaluate_grammar(self, poem):
        """
        """
        # CC	coordinating conjunction
        # CD	cardinal digit
        # DT	determiner
        # EX	existential there
        # FW	foreign word
        # IN	preposition/subordinating conjunction
        # JJ	This NLTK POS Tag is an adjective (large)
        # JJR	adjective, comparative (larger)
        # JJS	adjective, superlative (largest)
        # LS	list market
        # MD	modal (could, will)
        # NN	noun, singular (cat, tree)
        # NNS	noun plural (desks)
        # NNP	proper noun, singular (sarah)
        # NNPS	proper noun, plural (indians or americans)
        # PDT	predeterminer (all, both, half)
        # POS	possessive ending (parent\ 's)
        # PRP	personal pronoun (hers, herself, him,himself)
        # PRP$	possessive pronoun (her, his, mine, my, our )
        # RB	adverb (occasionally, swiftly)
        # RBR	adverb, comparative (greater)
        # RBS	adverb, superlative (biggest)
        # RP	particle (about)
        # TO	infinite marker (to)
        # UH	interjection (goodbye)
        # VB	verb (ask)
        # VBG	verb gerund (judging)
        # VBD	verb past tense (pleaded)
        # VBN	verb past participle (reunified)
        # VBP	verb, present tense not 3rd person singular(wrap)
        # VBZ	verb, present tense with 3rd person singular (bases)
        # WDT	wh-determiner (that, what)
        # WP	wh- pronoun (who)
        # WRB	wh- adverb (how)
        return None

    def evaluate_understandability(self, poem):
        """
        Evalautes the understandability using the textstat package. The flesch_reading_ease() method
        is used to measure the readability of a poem.
        Args:
            poem (str): the poem to evaluate
        Return
            understandability (float): the flesch reading ease score
        """
        understandability = textstat.flesch_reading_ease(poem)
        return understandability

    
def main():
    t = Tanka()
    t.read_files("input/*")
    print(t.get_next_word(("like", "a")))
    p = t.write_tanka()
    print(p)
    #t.perform_poem(p)
    print(t.syllables(t.line_1))
    print(t.syllables(t.line_2))
    print(t.syllables(t.line_3))
    print(t.syllables(t.line_4))
    print(t.syllables(t.line_5))
    e = t.tag_words()
    t.export_poem()
    #print(t.evaluate_emotions(p))
    #print(t.evaluate_understandability(p))
    print(t.evaluate_grammar(p))
    #print(e)
    #print(pos_tag(word_tokenize("the a an")))
    #print(pos_tag(word_tokenize(p)))

if __name__ == "__main__":
    main()