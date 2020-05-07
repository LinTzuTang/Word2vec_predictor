root=$(dirname "$0")
python3 $root/../word2vec/word2vec_predictor.py -f $root/example.fasta -o $root/example.csv
