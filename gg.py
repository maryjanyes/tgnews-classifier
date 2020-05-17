import re
from nltk.corpus import stopwords

text = '<!DOCTYPE html><html><head><meta charset="utf-8"/><meta property="og:site_name" content="The Irish News"/><meta property="og:title" content="New push to restore Assembly needed"/><meta property="og:description" content="There have been growing suggestions that full negotiations over the restoration of the Stormont institutions could start very shortly after the UK general election of December 12."/>'
text2 = '<h1>New push to restore Assembly needed</h1><p>There have been growing suggestions that full negotiations over the restoration of the Stormont institutions could start very shortly after the UK general election of December 12.</p><p>The DUP leader Arlene Foster, speaking at her partys annual conference last month, dropped a heavy hint about reaching an accommodation on a key question when she said that the Irish language and unionism were `not incompatible.</p>'
text3 = '<p>When the Sinn Féin deputy leader Michelle ONeill addressed her Ard Fheis at the weekend, she developed the same theme by declaring that she was ready to form a `credible executive.</p><p>The relationship between the two central figures is vital to any breakthrough, and Ms ONeill can stress that, despite a highly unusual challenge to her position from John ODowd, during which debate was discouraged and the voting figures were not revealed, she remains firmly in office.</p>'
text4 = '<p>Ms Foster is in much more uncertain territory, as she must first cope with a Westminster contest in which a number of DUP seats are under serious risk and then hope that she avoids sweeping criticism when the long awaited report of the Renewable Heat Incentive public inquiry is finally published.</p>'
text5 = '<p>won`t, just go ahead</p>'

to_join = (text, text2, text3)
article_text = '.'.join(to_join)
stop_words_en = stopwords.words('english')
matched_word_sequence = []

for w in range(len(stop_words_en)):
    word = stop_words_en[w]
    pattern = re.compile(word)
    if pattern.match(article_text, 0, len(article_text)):
        matched_word_sequence.append(word)
    elif word in article_text:
        matched_word_sequence.append(word)

print(matched_word_sequence)