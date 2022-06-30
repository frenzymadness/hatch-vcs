# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import os
import sys
import zipfile

import pytest
from importlib_metadata import version

from .utils import build_project, read_file

setuptools_scm_major = int(version("setuptools_scm").split(".")[0])


def test_basic(new_project_basic):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_basic, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_basic), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))


def test_write(new_project_write):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_write, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_write), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 5

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))

    version_file = os.path.join(package_directory, '_version.py')
    assert os.path.isfile(version_file)

    lines = read_file(version_file).splitlines()
    if setuptools_scm_major < 7:
        assert lines[3] == "version = '1.2.3'"
    else:
        assert lines[3] == "__version__ = version = '1.2.3'"


@pytest.mark.skipif(sys.version_info[0] == 2, reason='Depends on fix in 6.4.0 which is Python 3-only')
def test_fallback(new_project_fallback):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_fallback, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-7.8.9-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_fallback), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-7.8.9.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))
