## Arabic Natural Language Processing 

[![Build Status](https://travis-ci.com/adhaamehab/arabicnlp.svg?branch=develop)](https://travis-ci.com/adhaamehab/arabicnlp)

Arabic NLP is a python package that provides an implementation for natural language processing tasks for arabic language such as part-of-speech tagging, sentiment analysis, text similarity and more.
This projetc is an active project that aims to build a standard tool for more advanced nlp tasks.

![books](./imgs/cover.jpeg)

### Installation

```shell
pip install arabicnlp
```

### Usage

```python
from arabicnlp import tags, tokens, stem

tags("العربية هي شبكة لنقل الاخبار و المعلومات و مقاطع الفيديو إلى عالم عبر عدة وسائط ، تشمل الانترنت و مواقع التواصل الاجتماعي")
'''
{'العربية': 'PART', 'هي': 'ADP', 'شبكة': 'PART', 'لنقل': 'NUM', 'الاخبار': 'SYM', 'و': 'ADP', 'المعلومات': 'SYM', 'مقاطع': 'NUM', 'الفيديو': 'SYM', 'إلى': 'NUM', 'عالم': 'NUM', 'عبر': 'ADP', 'عدة': 'ADP', 'وسائط': 'NUM', '،': 'SYM', 'تشمل': 'SYM', 'الانترنت': 'INTJ', 'مواقع': 'PART', 'التواصل': 'SYM', 'الاجتماعي': 'ADP'}
'''

tokens("العربية هي شبكة لنقل الاخبار و المعلومات و مقاطع الفيديو إلى عالم عبر عدة وسائط ، تشمل الانترنت و مواقع التواصل الاجتماعي")

'''
['العربية', 'هي', 'شبكة', 'لنقل', 'الاخبار', 'و', 'المعلومات', 'و', 'مقاطع', 'الفيديو', 'إلى', 'عالم', 'عبر', 'عدة', 'وسائط', '،', 'تشمل', 'الانترنت', 'و', 'مواقع', 'التواصل', 'الاجتماعي']
'''

stem("العربية هي شبكة لنقل الاخبار و المعلومات و مقاطع الفيديو إلى عالم عبر عدة وسائط ، تشمل الانترنت و مواقع التواصل الاجتماعي")

'''
['عرب', 'هي', 'شبك', 'لنقل', 'اخبار', 'و', 'معلوم', 'و', 'مقاطع', 'فيديو', 'الى', 'عالم', 'عبر', 'عد', 'سايط', '', 'تشمل', 'انتر', 'و', 'مواقع', 'تواصل', 'اجتماع']
'''


```



### arabicnlp

- Arabicnlp is a natural language processing package for python developer 
- Provides a minimal interface for most of basic algorithms 
- Current release has:
    * Tokenization.
    * Stemming and lemmatization.
    * Part-of-speech tagger



### Known issue

- [tagger] Randomly some words that exists in word2index get msilabeled as `-PAD-` 


## Blogs

- [Building the project](https://adhaamehab.me/2019/02/01/gp-docs.html)
- [Building an arabic part-of-speech based on sequence modeling](https://towardsdatascience.com/deep-learning-for-arabic-part-of-speech-tagging-810be7278353)

### Contact
- [@adhaamehab](http://github.com/adhaamehab) 

## LICENSE

MIT License
