#!/bin/bash
set -euo pipefail

## tbd: Dockerfile: ENV NLTK_DATA /usr/share/nltk_data
mkdir ${APP_DIR}/nltk_data

# MODEL_____________________  TERMS____
# averaged_perceptron_tagger: 17sp 16fa
#                    cmudict:      16fa
#          maxent_ne_chunker: 17sp 16fa
#                      punkt: 17sp 16fa
#                  stopwords: 17sp
#                    wordnet: 17sp 16fa
#                      words: 17sp 16fa
python -m nltk.downloader -d /srv/app/nltk_data \
    averaged_perceptron_tagger \
    cmudict \
    maxent_ne_chunker \
    punkt \
    stopwords \
    wordnet \
    words \
    ;
