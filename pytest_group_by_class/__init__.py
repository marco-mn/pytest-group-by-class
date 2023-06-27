# -*- coding: utf-8 -*-
import argparse

import pytest
from _pytest.config import create_terminal_writer


def get_group(class_test_map, group_id, group_name):
    """Get the items from the passed in group based on group count."""
    if group_id is not None:
        for cls in class_test_map:
            if class_test_map[cls]["index"] == int(group_id):
                return class_test_map[cls]["items"]
        raise ValueError(f"Invalid test-group-class-id argument, max index is {len(class_test_map)}")
    if group_name is not None:
        for cls in class_test_map:
            if cls == group_name:
                return class_test_map[cls]["items"]
        raise ValueError(f"Invalid test-group-class-name argument")


def pytest_addoption(parser):
    group = parser.getgroup('split your tests into evenly sized groups and run them')
    group.addoption('--test-group-class', dest='test-group-class', action=argparse.BooleanOptionalAction,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group-class-id', dest='test-group-class-id', type=int, default=None,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group-class-name', dest='test-group-class-name', type=str, default=None,
                    help='The number of groups to split the tests into')


def collect_classes(items):
    data = {}
    counter = 1
    for i in items:
        test_class = i.parent.name
        if test_class not in data:
            data[test_class] = {
                "index": counter,
                "items": [i]
            }
            counter += 1
        else:
            data[test_class]["items"].append(i)
    print("\n")
    for cls in data:
        print(f"Class {cls} has index {data[cls]['index']}")
    return data


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    group_class = config.getoption('test-group-class')
    group_id = config.getoption('test-group-class-id')
    group_name = config.getoption('test-group-class-name')
    if group_class:
        if group_id is not None and group_name is not None:
            raise ValueError("--test-group-class-id or --test-group-class-name must be specified")
        if group_id and group_name:
            raise ValueError("--test-group-class-id or --test-group-class-name cannot be both specified")
    else:
        return
    class_test_map = collect_classes(items)
    items[:] = get_group(class_test_map, group_id, group_name)
    terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
    terminal_writer = create_terminal_writer(config)
    message = terminal_writer.markup(
        'Running test group by class {0} {1} ({2} tests)\n'.format(
            "index" if group_id is not None else "name",
            group_id if group_id is not None else group_name,
            len(items)
        ),
        yellow=True
    )
    terminal_reporter.write(message)
