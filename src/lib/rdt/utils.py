def pair_elements(arr):
    """
    Pair elements of an array into tuples.

    Args:
        arr (list): The input list.

    Returns:
        list: A list of tuples, where each tuple contains two elements from the input list.
              If the input list has an odd length, the last element will be in a tuple by itself.
    """
    pairs = []

    for i in range(0, len(arr), 2):
        if i + 1 < len(arr):
            pairs.append((arr[i], arr[i + 1]))

    # If the array has an odd length, add the last element as a single-element tuple
    if len(arr) % 2 == 1:
        pairs.append((arr[-1],))

    return pairs
