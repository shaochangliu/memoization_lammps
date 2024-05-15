'''
def count_lines(file_path):
    with open(file_path, 'r') as file:
        lines = 0
        for line in file:
            lines += 1
    return lines

if __name__ == "__main__":
    file_path = 'output_f.txt'
    line_count = count_lines(file_path)
    print(f"Number of lines: {line_count}")
'''


def count_duplicates_and_conflicts(file_path):
    counts = {}
    duplicates = 0
    conflicts = 0
    rel_error = 0
    max_rel_error = 0
    avg_rel_error = 0
    for i_info, neighbors_info, force in read_file(file_path):
        # atom info: qi, itype, xi, yi, zi
        # force: fx, fy, fz
        key = (tuple(i_info), tuple(tuple(info) for info in neighbors_info))
        force = tuple(force)
        force_value = counts.get(key)
        if force_value is not None:
            rel_error = max(abs((f1 - f2) / f2) for f1, f2 in zip(force, force_value))
            if rel_error > 1e-5:
                conflicts += 1
                if rel_error > max_rel_error:
                    max_rel_error = rel_error
                avg_rel_error += rel_error
            duplicates += 1
        else:
            counts[key] = force
    return duplicates, conflicts, max_rel_error, avg_rel_error / conflicts

def read_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split(', ')
            i_info = [float(fields[0]), int(fields[1])] + [float(field) for field in fields[2:5]]
            neighbors_info = []
            # top-k neighbors when k=10
            for j in range(10):
                start = 5 + j * 5
                neighbor_info = [float(fields[start]), int(fields[start+1])] + [float(field) for field in fields[start+2:start+5]]
                neighbors_info.append(neighbor_info)
            force = [float(field) for field in fields[-3:]]
            yield i_info, neighbors_info, force

if __name__ == "__main__":
    file_path = 'output_f.txt'
    duplicates, conflicts, max_rel_error, avg_rel_error = count_duplicates_and_conflicts(file_path)
    print(f"Duplicates: {duplicates}")
    print(f"Conflicts: {conflicts}")
    print(f"Max relative error: {max_rel_error}")
    print(f"Average relative error: {avg_rel_error}")
