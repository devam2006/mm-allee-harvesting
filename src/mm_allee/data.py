"""Minimal observation split guard; WP03/WP05 add generation and time-window checks."""


def validate_splits(train_ids, val_ids, test_ids):
    groups = [list(ids) for ids in (train_ids, val_ids, test_ids)]
    if any(not ids for ids in groups):
        raise ValueError("Training, validation and test splits must be nonempty")
    if any(len(set(ids)) != len(ids) for ids in groups):
        raise ValueError("Duplicate observation IDs in a split")
    train, val, test = map(set, groups)
    if train & val or train & test or val & test:
        raise ValueError("Observation IDs overlap across splits")
