import csv

def partition_file(input_file, output_prefix):
    # Read and parse the input file
    data = []
    with open(input_file, 'r') as txtfile:
        lines = txtfile.readlines()
        for line in lines:
            parts = line.strip().split(',')
            data.append((parts[0], float(parts[1])))

    # Sort the data based on scores
    sorted_data = sorted(data, key=lambda x: x[1])

    # Calculate partition indices for the bottom and top 10%
    total_rows = len(sorted_data)
    bottom_10 = int(total_rows * 0.1)
    top_10 = int(total_rows * 0.9)

    # Partition and write to separate files
    bottom_10_data = sorted_data[:bottom_10]
    top_10_data = sorted_data[top_10:]

    with open(f"{output_prefix}_bottom_10.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(bottom_10_data)

    with open(f"{output_prefix}_top_10.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(top_10_data)

input_file = "combined.txt"
output_prefix = "output_partitioned"
partition_file(input_file, output_prefix)
