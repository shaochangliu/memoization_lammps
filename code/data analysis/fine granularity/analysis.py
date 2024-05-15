'''
def count_lines(file_path):
    with open(file_path, 'r') as file:
        lines = 0
        for line in file:
            lines += 1
    return lines

if __name__ == "__main__":
    file_path = 'output_jj.txt'
    line_count = count_lines(file_path)
    print(f"Number of lines: {line_count}")
'''


def count_duplicates_and_conflicts(file_path):
    counts = {}
    duplicates = 0
    conflicts = 0
    # cnt = 0
    rel_error = 0
    max_rel_error = 0
    avg_rel_error = 0
    for record in read_file(file_path):
        # itype, jtype, q[i], q[j], rsq, factor_lj, factor_coul, fpair
        itype, jtype, qi, qj, rsq, factor_lj, factor_coul, fpair = record
        key = tuple([itype, jtype, qi, qj, rsq, factor_lj, factor_coul])
        # key = tuple(sorted([(itype, qi), (jtype, qj)]) + [rsq, factor_lj, factor_coul])
        fpair_value = counts.get(key)
        if fpair_value is not None:
            if fpair_value != fpair:
                conflicts += 1
                rel_error = abs(fpair_value - fpair) / abs(fpair_value)
                if rel_error > max_rel_error:
                    max_rel_error = rel_error
                avg_rel_error += rel_error
                # if cnt <1000:
                    # print(f"Conflict: {key} -> {fpair_value} vs {fpair}")
                # cnt += 1
            duplicates += 1
        else:
            counts[key] = fpair
    return duplicates, conflicts, max_rel_error, avg_rel_error / conflicts

def read_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split(', ')
            record = [int(fields[0]), int(fields[1])] + [float(field) for field in fields[2:5]] + [int(fields[5]), int(fields[6])] + [float(fields[7])]
            yield record

if __name__ == "__main__":
    file_path = 'output_jj.txt'
    duplicates, conflicts, max_rel_error, avg_rel_error = count_duplicates_and_conflicts(file_path)
    print(f"Duplicates: {duplicates}")
    print(f"Conflicts: {conflicts}")
    print(f"Max relative error: {max_rel_error}")
    print(f"Average relative error: {avg_rel_error}")
