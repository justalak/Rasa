import spacy
import re
from underthesea import ner, classify
from ORMModels import company
from service.data_process.extractor import *
# nlp = spacy.load('vi_spacy_model')
text = "Tôi muốn biết giá cổ phiếu"
#
# doc = nlp(text)
#
# print(spacy.explain("ccomp"))
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#         token.shape_, token.is_alpha, token.is_stop)
#
# print(Extractor.extract_company_name(text))
# res = company.Company.search_by_name("Hoàng anh gia lai")
# for company in res:
#     print(company.name)

for res in ner(text):
    print(res)