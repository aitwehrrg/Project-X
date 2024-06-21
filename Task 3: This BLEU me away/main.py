from collections import Counter
import math

TEST_CASE_1: tuple[list[str], str] = (['It is a guide to action that ensures that the military will forever heed Party '
                                       'commands',
                                       'It is the guiding principle which guarantees the military forces always being '
                                       'under the command of the Party',
                                       'It is the practical guide for the army always to heed the directions of the '
                                       'party'],
                                      'It is a guide to action which ensures that the military always obeys the '
                                      'commands of the party')

TEST_CASE_2: tuple[list[str], str] = (['It is a guide to action that ensures that the military will forever heed Party '
                                       'commands',
                                       'It is the guiding principle which guarantees the military forces always being '
                                       'under the command of the Party',
                                       'It is the practical guide for the army always to heed the directions of the '
                                       'party'],
                                      'It is the to action the troops forever hearing the activity guidebook that '
                                      'party direct')

# Maximum number of n-grams
N: int = 4


# Compute n-grams
def n_grams(sentence: str, n: int = 1) -> list[str]:
    words: list[str] = sentence.split()
    if n == 1:
        return words
    n_grams_: list[str] = []
    for i in range(len(words) - n + 1):
        n_grams_.append(' '.join(words[i:i + n]))
    return n_grams_


# Count frequency of n-grams
def count(n_gram: list[str]) -> int:
    return sum(Counter(n_gram).values())


# Count frequency of clipped n-grams
def count_clip(candidate: str, references: list[str], n: int) -> int:
    n_gram_candidate: list[str] = n_grams(candidate, n)
    n_gram_references: list[list[str]] = [n_grams(reference, n) for reference in references]
    counts: Counter = Counter(n_gram_candidate)
    for key in counts:
        max_reference_count: int = 0
        for n_gram_reference in n_gram_references:
            # n_gram_reference_count: Counter = Counter(n_gram_reference)
            max_reference_count = max(max_reference_count, n_gram_reference.count(key))
        counts[key] = min(counts[key], max_reference_count)
    return sum(counts.values())


# Calculate p_n
def precision(candidate: str, references: list[str], n: int) -> float:
    count_: int = count(n_grams(candidate, n))
    count_clip_: int = count_clip(candidate, references, n)
    # print(n, f'{count_clip_}/{count_}')
    return count_clip_ / count_ if count_ != 0 else 0


# Calculate BP
def brevity_penalty(candidate: str, references: list[str]) -> float:
    c: int = len(n_grams(candidate))  # total length of candidate
    word_count_references: list[int] = [len(n_grams(reference)) for reference in references]
    deviations: list[int] = [abs(c - reference) for reference in word_count_references]
    r: int = word_count_references[deviations.index(min(deviations))]  # best match reference length
    if c > r:
        return 1
    return math.exp(1 - r / c)


# Required function
def bleu_score(references: list[str], candidate: str) -> float:
    bleu: float = 1
    bp: float = brevity_penalty(candidate, references)
    print(f'BP: {bp}')
    for n in range(1, N + 1):
        p_n: float = precision(candidate, references, n)
        bleu *= p_n
    bleu **= 1 / N
    bleu *= bp
    return bleu


def main():
    test_cases: tuple = (TEST_CASE_1, TEST_CASE_2)
    for test_case in test_cases:
        bleu: float = bleu_score(test_case[0], test_case[1])
        print(f'BLEU score: {bleu}\n')


if __name__ == '__main__':
    main()
