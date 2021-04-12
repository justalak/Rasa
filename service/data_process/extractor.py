import spacy

nlp = spacy.load('vi_spacy_model')
not_included_words = ["cổ_phiếu", "thông_tin", "hồ_sơ"]
not_in_cluded_depth = ["ROOT", "nsubj"]


class Extractor:
    @staticmethod
    def extract_company_name(text):
        doc = nlp(text)
        result = []
        for token in doc:
            if not token.is_stop and token.dep_ not in not_in_cluded_depth and token.text not in not_included_words:
                result.append(token.text)
        return " ".join(result).replace("_", " ")
