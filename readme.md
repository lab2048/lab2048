# How-to
- Install: `pip install git+https://github.com/lab2048/lab2048.git`

# Description

## TMTool


* Modules for tokens
  * `deStopWords(words)`:  e.g. `df['tokens'].apply(TMTool.deStopWords)`
  * `dePunctuation(words)`:  e.g., `df['tokens'].apply(TMTool.dePunctuation)`
        
* Modules for text
  * `deEmojify(text)` : e.g., `df['text'].apply(TMTool.deEmojify)`
  * `deSpace(text)`   : e.g., `df['text'].apply(TMTool.deSpace) (Questionable!)`

* Modules for list of tokens
  * `get_word2vec(words)`: e.g., `TMTool.get_word2vec(df['tokens'])`
  * `get_common_words(words)`: e.g., `TMTool.get_common_words(df['tokens'],topN=2000)`

# Usage

## TMTool

* Built-in stopwords and userdict for tokenization
  * `setowords`: StopWords of zh-tw, from https://github.com/lab2048/pyCorpus/raw/main/stopwords_tw.txt"
  * `setowords_cn`: StopWords of zh-cn, from https://github.com/lab2048/pyCorpus/raw/main/stopwords_cn.txt"
  
  ```python
  from lab2048 import TMTool
  tm = TMTool.TMTool()
  display(tm.userdict)
  display(tm.stopwords)
  ```



