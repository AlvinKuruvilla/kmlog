def duplicate_events(df):
    try:
        data = df["Press or Release"].values.tolist()
    except KeyError:
        data = df.iloc[:, 0].values.tolist()
    chunks = list(divide_chunks(data))
    peek_index = 0
    indices = []
    for chunk in chunks:
        if chunk[0] == chunk[1]:
            indices.append(peek_index)
        peek_index += 2
    return indices


#! FIXME: Crashes
def find_invalid_time_indices(df):
    try:
        data = df["Time"].tolist()
    except KeyError:
        data = df.iloc[:, 2].tolist()
    # print(data)
    # input("HOLD")
    current_max = data[0]
    invalids = [current_max]
    for k in range(0, len(data) - 2):
        current_max = data[k]
        if data[k] < current_max:
            invalids.append(k)
        current_max = data[k]
    return invalids


def divide_chunks(l, n=2):
    chunked_list = [l[i : i + n] for i in range(0, len(l), n)]
    return list(chunked_list)
