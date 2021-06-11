import spacy
import phonlp

NLP_DIR = './pretrained_phonlp'
nlp_ner = phonlp.load(save_dir=NLP_DIR)
nlp_spacy = spacy.load('vi_spacy_model')


class Model:
    nlp_ner = None
    nlp_spacy = None

    def __init__(self):
        """ Virtually private constructor. """
        if Model.nlp_ner is not None or Model.nlp_spacy is not None:
            raise Exception("This class is a singleton!")
        else:
            Model.nlp_ner = phonlp.load(save_dir=NLP_DIR)
            Model.nlp_spacy = spacy.load('vi_spacy_model')

    @staticmethod
    def get_nlp_ner():
        if Model.nlp_ner is None:
            Model()
        return Model.nlp_ner

    @staticmethod
    def get_nlp_spacy():
        if Model.nlp_spacy is None:
            Model()
        return Model.nlp_spacy


class Extractor:
    @staticmethod
    def sentence_to_token(sentence):
        doc = nlp_spacy(sentence)
        result = []
        for token in doc:
            result.append(token.text)
        return " ".join(result)

    @staticmethod
    def extract_company_name(text):
        sentence = Extractor.sentence_to_token(text)
        result = []

        res = nlp_ner.annotate(text=sentence)
        nlp_ner.print_out(res)
        for i in range(len(res[2][0])):
            if res[2][0][i].find('ORG') != -1:
                result.append(res[0][0][i])
        return " ".join(result).replace("_", " ")
