from argparse import ArgumentParser
from bloom_filter import BloomFilter

parser = ArgumentParser()
parser.add_argument('--array_size', '-s', type=int, default=10000)
parser.add_argument('--num_hashes', '-n', type=int, default=3)
parser.add_argument('--item_length', '-l', type=int, default=2000)
parser.add_argument('--dictionary_path', '-d', type=str, default='/usr/share/dict/words')


def setup_bloomfilter(bloom_filter, words):
    for word in words.readlines():
        bloom_filter.add(word.rstrip('\n'))


def handle_output(bloom_filter, item_length, input_word, output):
    print('OUTPUT', output)
    if output:
        print(
            '{input} has probability {fpp} of being in filter'.format(
                input=input_word,
                fpp=round(1-bloom_filter.fpp(item_length), 3)
            )
        )
    else:
        print('{input} definitely not in filter'.format(input=input_word))


if __name__ == '__main__':
    args = parser.parse_args()
    bf = BloomFilter(args.array_size, args.num_hashes)
    with open(args.dictionary_path, 'rU') as word_file:
        setup_bloomfilter(bf, word_file)
    print('bloom filter has {zeros} zero indices'.format(zeros=len([i for i in bf.array if i == 0])))
    while True:
        input_word = input('Please enter a word to test (entering ":q" will quit the program): ')
        if input_word == ':q':
            break
        else:
            print('Checking bloom filter for {input}'.format(input=input_word))
            output = bf.find(input_word)
            handle_output(bf, args.item_length, input_word, output)
