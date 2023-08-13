import csv
with open('./parsed_data_public_t.csv') as csvfile:
    reader = csv.reader(csvfile)
    # Skip header
    next(reader)
    # Remember answer set sizes
    anssize = []
    # Look at all questions
    for row in reader:
        # Extract the set of possible answers
        ans = set(row[1:])
        if '' in ans:
            ans.remove('')
        # Skip the question if the set of answers is not in reasonable range
        # This is the case for some "summary statistic" data that is included
        # Also ethnicity/country/etc. have many many choices
        if not(len(ans) > 1 and len(ans) < 5):
            continue
        anssize.append(len(ans))
    print(anssize)
    print(len(anssize))
    print(sum(anssize))

