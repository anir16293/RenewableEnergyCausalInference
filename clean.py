import csv


def csv_yearly():
    fname = "country_population.csv"
    with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        cname_to_idx = {}
        idx_to_cname = {}
        output = []
        for row in csv_reader:
            if line_count == 0:
                for i, elem in enumerate(row):
                    cname_to_idx[elem] = i
                    idx_to_cname[i] = elem
            else:
                years = row[1:]
                country_code = row[0]
                for j, elem in enumerate(years):
                    if not elem:
                        continue
                    output.append(
                        {"country_code": country_code, "year": int(idx_to_cname[j + 1]), "value": float(elem)})
            line_count += 1

    with open('cleaned/' + fname, 'w') as csv_out:
        fieldnames = ['country_code', 'year', 'value']
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)

        writer.writeheader()
        for elem in output:
            writer.writerow(elem)
    print("fin")

if __name__ == '__main__':
    csv_yearly()