# Synthetic unigram fixture

`synthetic-gigafida.tsv` is project-authored test data. It contains no copied
Gigafida rows or counts and is covered by the repository `LICENSE`. Its first
fourteen lines are synthetic metadata placeholders so the observed header stays
at line 15. All fields are quoted; the focused contract test supplies UTF-8
CRLF bytes to the importer.
