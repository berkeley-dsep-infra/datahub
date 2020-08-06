#!/bin/bash
set -euo pipefail

mkdir ${NLTK_DATA}

# MODEL_____________________  TERMS____
# averaged_perceptron_tagger: 17sp 16fa
#                    cmudict:      16fa
#          maxent_ne_chunker: 17sp 16fa
#                      punkt: 17sp 16fa
#                  stopwords: 17sp
#                    wordnet: 17sp 16fa
#                      words: 17sp 16fa
python -m nltk.downloader -d ${NLTK_DATA} \
    averaged_perceptron_tagger \
    cmudict \
    maxent_ne_chunker \
    punkt \
    stopwords \
    wordnet \
    words
