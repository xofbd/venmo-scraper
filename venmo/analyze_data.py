from spacy.lang.en import STOP_WORDS

from spot_fake_data import load_data


def data_generator(json_paths):
    """Generator yielding transactions across all JSONs."""
    for f in json_paths:
        date = f.split('_')[-1].split('.')[0]
        if date < '2020-03-27':
            data = load_data(f)
            for x in data:
                yield x


def most_common_names(json_paths):
    """Return count of unique first names."""
    name_counter = {}

    for x in data_generator(json_paths):
        name = x['actor']['firstname'].lower()
        if name not in name_counter:
            name_counter[name] = 1
        else:
            name_counter[name] += 1

    return name_counter, len(set(name_counter.keys()))


def most_common_tokens(json_paths):
    """Return count of all tokens in the transaction message."""
    token_counter = {}

    for x in data_generator(json_paths):
        for token in x['message'].split():
            if (token.lower() not in token_counter and
                    token.lower() not in STOP_WORDS):
                token_counter[token.lower()] = 1
            elif token.lower() not in STOP_WORDS:
                token_counter[token.lower()] += 1

    return token_counter, len(set(token_counter.keys()))


def top_keys(counter, N=10):
    """Print top key and their count."""
    for key, count in sorted(counter.items(), key=lambda x: -x[1])[:N]:
        print(f"{key}: {count}")


if __name__ == '__main__':
    import glob

    json_paths = glob.glob('daily/*.json')
    name_counter, num_names = most_common_names(json_paths)
    token_counter, num_tokens = most_common_tokens(json_paths)

    top_keys(name_counter)
    print()
    top_keys(token_counter)
