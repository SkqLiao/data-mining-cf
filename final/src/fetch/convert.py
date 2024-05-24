import json
import csv


def convert(json_path, new_csv_path):
    with open(json_path) as json_file:
        data = json.load(json_file)

    # get all headers
    headers = set()
    for item in data:
        for key in item.keys():
            headers.add(key)

    csv_file = open(new_csv_path, 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(list(headers))
    for item in data:
        row = []
        for header in headers:
            row.append(item.get(header, ''))
        csv_writer.writerow(row)
    csv_file.close()


problem_json = './data/problems/problem_info.json'
contest_json = './data/contests/cf.json'

convert(problem_json, 'problem_info.csv')
convert(contest_json, 'cf.csv')
