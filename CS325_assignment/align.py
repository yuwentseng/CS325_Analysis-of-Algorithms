import csv

LOG_TO_TERMINAL = False
DIAGONAL = 1
UP = 2
LEFT = 3


def file_2_dict(f_cost):
    reader = csv.reader(f_cost, delimiter=',')

    # Break the matrix into a 2D array
    a = []
    for row in f_cost.readlines():
        a.append(row.strip().split(','))

        # Creates a 2D Dictionary from the 2D array
    d = {}
    for i in range(1, len(a)):
        d_temp = {}
        for j in range(1, len(a[0])):
            d_temp[a[0][j]] = int(a[i][j])
        d[a[i][0]] = d_temp

        # i.e. d['A']['T'] will return 2, as will d['T']['A']
    return d


def edit_distance(d_cost, A, B):
    # The alignment table uses string A and B with a - prepended to it.
    A = '-' + A
    B = '-' + B

    # Generate empty array
    a_edit_dist = [[0] * len(A) for j in B]
    backtrace = [[0] * len(A) for j in B]

    # Fill like this:
    # 0 1 2 3 4
    # 1 0 0 0 0
    # 2 0 0 0 0
    # 3 0 0 0 0
    # 4 0 0 0 0
    a_edit_dist[0][0] = 0
    for i in range(1, len(A)):
        a_edit_dist[0][i] = a_edit_dist[0][i - 1] + d_cost[A[i]]['-']

    for j in range(1, len(B)):
        a_edit_dist[j][0] = a_edit_dist[j - 1][0] + d_cost[B[j]]['-']

        # Go through and fill the array based on the following:
        # For each letter the effort is the minimum of surrounding blocks + effort to change that letter
        # Keep in mind that matching letters have a cost of 0. i.e d_cost['A']['A'] = 0
    for j in range(1, len(B)):
        for i in range(1, len(A)):
            temp = a_edit_dist[j - 1][i - 1] + d_cost[B[j]][A[i]]

            a_edit_dist[j][i] = min(temp, a_edit_dist[j - 1][i] + d_cost[B[j]]['-'],
                                    a_edit_dist[j][i - 1] + d_cost['-'][A[i]])

            if a_edit_dist[j][i] == temp:
                backtrace[j][i] = DIAGONAL

            elif a_edit_dist[j][i] == a_edit_dist[j - 1][i] + d_cost[B[j]]['-']:
                backtrace[j][i] = UP

            else:
                backtrace[j][i] = LEFT

    if LOG_TO_TERMINAL:
        for u in range(len(B)):
            print(a_edit_dist[u])

    return a_edit_dist, backtrace


def align(A, B, backtrace):
    # The theory here is that we'll start at the bottom right corner for the solved case
    # and step into the direction of lowest cost until we hit the top left corner building the string as we go.
    aligned_A = ""
    aligned_B = ""

    i = len(B)
    j = len(A)
    # i = 0
    # j = 0

    while i > 0 and j > 0:
        # Diagonal step means we either swapped or the letters are equal
        # Order of these matters! A diagonal step is preferred as it implies no change
        if LOG_TO_TERMINAL:
            print (a_edit_dist[" "+ str(i) +" "][" "+ str(j) +" "])
            print (aligned_A)
            print (aligned_B)

        if backtrace[i][j] == DIAGONAL:
            aligned_A = A[j - 1] + aligned_A
            aligned_B = B[i - 1] + aligned_B
            i -= 1
            j -= 1

            # Step up means a gap on string A was matched with a letter at string B
        elif backtrace[i][j] == UP:
            aligned_A = '-' + aligned_A
            aligned_B = B[i - 1] + aligned_B
            i -= 1

            # Step left means a gap on string B was matched with a letter from string A
        else:
            aligned_A = A[j - 1] + aligned_A
            aligned_B = '-' + aligned_B
            j -= 1

    if j > 0:
        aligned_A = A[:j] + aligned_A
        aligned_B = '-' * j + aligned_B

    if i > 0:
        aligned_A = '-' * i + aligned_A
        aligned_B = B[:i] + aligned_B

    if LOG_TO_TERMINAL:
        print (aligned_A)
        print (aligned_B)
    return aligned_A, aligned_B


def main(cost_filepath="imp2cost.txt", data_filepath="imp2input.txt", output_filepath="imp2output.txt"):
    with open('imp2cost.txt','r') as f_cost:
        d_cost = file_2_dict(f_cost)      
    with open("imp2input.txt",'r') as f_data: 
        for line in f_data:
            A, B = line.split(',')
            B = B[:-1]  # B will have a trailing newline, which needs to be removed

            # Generate the edit distance array and use that to build our aligned strings
            a_edit_dist, backtrace = edit_distance(d_cost, A, B)
            a_A, a_B = align(A, B, backtrace)
            with open("imp2output.txt",'w') as f_output: 
                f_output.write(a_A + "," + a_B + ":" + str(a_edit_dist[len(B)][len(A)]) + "\n")


if __name__ == "__main__":
    main()
