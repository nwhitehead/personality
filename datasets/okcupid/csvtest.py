import csv
import numpy as np

with open('./parsed_data_public_t.csv') as csvfile:
    reader = csv.reader(csvfile)
    # Get column size from header (ignore labels for columns)
    cols = len(next(reader)[1:])
    print(f'There are {cols} people responding')
    print('Reading rows...')
    # Now count rows by reading the file
    rows = sum(1 for row in reader)
    print(f'There are {rows} questions (some will be skipped)')
    # Rewind file to do it again, storing actual data this time
    csvfile.seek(0)
    reader = csv.reader(csvfile)
    next(reader)
    # Remember answer set sizes
    anssize = []
    dataset = np.zeros((rows, cols))
    # Look at all questions
    r = 0
    skipped = 0
    for row in reader:
        # Extract the set of possible answers
        ans = sorted(list(set(row[1:])))
        # Skip the question if the set of answers is not in reasonable range
        # This is the case for some "summary statistic" data that is included
        # Also ethnicity/country/etc. have many many choices
        if not(len(ans) > 1 and len(ans) < 5):
            skipped += 1
            continue
        anssize.append(len(ans))
        d = {}
        for ind, a in enumerate(ans):
            d[a] = ind
        answers = [d[x] for x in row[1:]]
        # Zero pad out answers to cols size
        answers += [0] * (cols - len(answers))
        answers = np.array([answers], dtype=int)
        dataset[r, :] = answers
        r += 1
        print(f'{100 * (r + skipped) / rows:.1f}% done')
    print(anssize)
    print(len(anssize))
    print(sum(anssize))
    dataset = dataset[:r, :]
    print(dataset.shape)
    with open('okcupid.npz', 'wb') as fout:
        np.savez_compressed(fout, dataset=dataset, anssize=anssize)
