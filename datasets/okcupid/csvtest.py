import csv
with open('./parsed_data_public_t.csv') as csvfile:
    reader = csv.reader(csvfile)
    # Skip header
    next(reader)
    # Remember answer set sizes
    anssize = []
    dataset = []
    # Look at all questions
    for row in reader:
        # Extract the set of possible answers
        ans = sorted(list(set(row[1:])))
        # Skip the question if the set of answers is not in reasonable range
        # This is the case for some "summary statistic" data that is included
        # Also ethnicity/country/etc. have many many choices
        if not(len(ans) > 1 and len(ans) < 5):
            continue
        anssize.append(len(ans))
        d = {}
        for ind, a in enumerate(ans):
            d[a] = ind
        answers = [d[x] for x in row[1:]]
        dataset.append(answers)
        print(len(dataset))
    print(anssize)
    print(len(anssize))
    print(sum(anssize))
