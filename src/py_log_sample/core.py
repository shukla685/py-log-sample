"""Sample repetitive log lines while always keeping the first and last."""


class LogSampler:
    """
    Sample consecutive duplicate log lines, keeping the first occurrence,
    the last occurrence, and the count of repetitions for each group.

    A group is a maximal run of consecutive lines that are equal under
    the configured equality function. Only the first line of each group
    is kept (the last line is equal to the first, so keeping the first
    also satisfies the "keep the last" requirement).
    """

    def __init__(self):
        # Stateless: we only implement the pure transformation. If
        # streaming reduction is later needed, the same group-detection
        # logic can be used inside a generator without changing callers'
        # expectations of sample().
        pass

    def sample(self, lines):
        """
        Return a list of (line, count) pairs for each maximal group of
        consecutive duplicate lines.

        Groups are detected by ``line == previous_line`` (exact equality).
        The first line of each group is kept; the count includes all
        members of the group, so it is always >= 1. The last line of the
        input is the last member of the final group, so it is always
        represented in the output.

        Parameters
        ----------
        lines : iterable of str
            The log lines to sample. Each element should support ``==``
            with the other elements.

        Returns
        -------
        list of tuple(str, int)
            One (line, count) pair per group, in order of appearance.
        """
        result = []
        current = None
        count = 0

        for line in lines:
            if current is None:
                current = line
                count = 1
            elif line == current:
                count += 1
            else:
                result.append((current, count))
                current = line
                count = 1

        if count > 0:
            result.append((current, count))

        return result
