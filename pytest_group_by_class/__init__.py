# -*- coding: utf-8 -*-
import argparse
from _pytest.config import create_terminal_writer


def get_group(class_test_map, group_id, group_name):
    """Get the items from the passed in group based on group count."""
    if group_id:
        for cls in class_test_map:
            if class_test_map[cls]["index"] == group_id:
                return class_test_map[cls]["items"]
        raise ValueError("Invalid test-group-class-id argument")
    if group_name:
        for cls in class_test_map:
            if cls == group_name:
                return class_test_map[cls]["items"]
        raise ValueError("Invalid test-group-class-name argument")


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
    counter = 0
    for i in items:
        test_class = i.parent.name
        if test_class not in data:
            data[test_class] = {
                "index": counter,
                "item   s": [i]
            }
            counter += 1
        else:
            data[test_class]["items"].append(i)
    for cls in data:
        print(f"{cls}:{data[cls]}")
    return data


def pytest_collection_modifyitems(config, items):
    group_class = config.getoption('test-group-class')
    group_id = config.getoption('test-group-class-id')
    group_name = config.getoption('test-group-class-name')
    if group_class:
        if not group_id and not group_name:
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
        'Running test group by class #{0} ({1} tests)\n'.format(
            group_id,
            len(items)
        ),
        yellow=True
    )
    terminal_reporter.write(message)
