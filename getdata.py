import csv


def read_csv():
    data = []
    with open("./data/movies.csv", "r", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data


def get_data_chunk(data, page_number):
    page_size = 10  # Adjust page size as needed
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    data_chunk = data[start_index:end_index]
    return data_chunk
