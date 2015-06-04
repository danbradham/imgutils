import os
import itertools
import re

I want to use this, but Maya raises a window when trying to import PIL
try:
    from PIL import Image
    use_pil = True
except ImportError:
    from PySide import QtGui, QtCore
    use_pil = False


def _pil_scale_copy(in_file, out_file, scale=1, **kwargs):
    '''PIL implementation of scale_copy'''

    in_img = Image.open(in_file)
    out_img = in_img.resize(in_img.size[0] * scale, in_img.size[1] * scale)
    out_img.save(out_file, **kwargs)


def _pil_copy(in_file, out_file, size=None, **kwargs):
    '''PIL implementation of copy'''

    in_img = Image.open(in_file)
    size = size or in_img.size
    out_img = in_img.resize(*size)
    out_img.save(out_file, **kwargs)


def _pil_thumbnail(in_file, out_file, size=None, **kwargs):
    '''PIL implementation of thumbnail'''

    in_img = Image.open(in_file)
    size = size or (in_img.size[0] * 0.25, in_img.size[1] * 0.25)
    out_img = in_img.thumbnail(*size)
    out_img.save(out_file, **kwargs)


def _pyside_scale_copy(in_file, out_file, scale=1, **kwargs):
    '''PySide implementation of scale_copy'''

    in_img = QtGui.QImage(in_file)
    size = in_img.width() * scale, in_img.height() * scale
    out_img = in_img.scaled(*size)
    out_img.save(out_file, **kwargs)


def _pyside_copy(in_file, out_file, size=None, **kwargs):
    '''PySide implementation of scale_copy'''

    in_img = QtGui.QImage(in_file)
    size = size or (in_img.width(), in_img.height())
    out_img = in_img.scaled(*size)
    out_img.save(out_file, **kwargs)


def _pyside_thumbnail(in_file, out_file, size=None, **kwargs):
    '''PySide implementation of thumbnail'''

    in_img = QtGui.QImage(in_file)
    size = size or (in_img.width() * 0.25, in_img.height() * 0.25)
    out_img = in_img.scaled(*size)
    out_img.save(out_file, **kwargs)


def scale_copy(in_file, out_file, scale=1, **kwargs):
    '''Copy an image file scaling it by a fixed amount, and saving it to
    the provided location.

    :param in_file: Image file to convert
    :param out_file: Output filepath
    :param scale: Uniform scale value (> 0)
    :param kwargs: File format specific kwargs to pass to PIL.Image.save()
    '''

    if use_pil:
        _pil_scale_copy(in_file, out_file, scale, **kwargs)
    else:
        _pyside_scale_copy(in_file, out_file, scale, **kwargs)


def copy(in_file, out_file, size=None, **kwargs):
    '''Copy an image file saving it to the provided location at a specified
    size.

    :param in_file: Image file to convert
    :param out_file: Output filepath
    :param size: out_file size (defaults to in_file size)
    :param kwargs: File format specific kwargs to pass to PIL.Image.save()
    '''

    if use_pil:
        _pil_copy(in_file, out_file, size, **kwargs)
    else:
        _pyside_copy(in_file, out_file, size, **kwargs)


def thumbnail(in_file, out_file, size=None, **kwargs):
    '''Copy an image file saving it to the provided location at a specified
    size.

    :param in_file: Image file to convert
    :param out_file: Output filepath
    :param size: out_file size (defaults to quarter in_file size)
    :param kwargs: File format specific kwargs to pass to PIL.Image.save()
    '''

    if use_pil:
        _pil_thumbnail(in_file, out_file, size, **kwargs)
    else:
        _pyside_thumbnail(in_file, out_file, size, **kwargs)


def find_sequences(files, *predicates):
    '''Returns a list of sequences and non_sequences contained in files.

    :param files: A list of files to parse for sequences
    :param predicates: Predicate functions used to filter input files'''

    sequences = {}
    non_sequences = []

    files = sorted(files)

    for predicate in predicates:
        files = [f for f in files if predicate(f)]

    seq_matcher = re.compile('\.\d+(?=\D*$)')

    while files:

        first = files.pop(0)

        if first and not files:
            non_sequences.append(first)
            break

        match = seq_matcher.search(first)
        if not match:
            non_sequences.append(first)
            continue

        start, end = match.span()
        start += 1
        glob = first[:start] + '*' + first[end:]

        matches = itertools.takewhile(lambda x: fnmatch(x, glob), files)
        matches = list(matches)
        if not matches:
            non_sequences.append(first)
            continue
        matches.insert(0, first)

        seq_start = first[start:end]
        seq_end = matches[-1][start:end]
        name = '{}[{}-{}]{}'.format(
            first[:start],
            seq_start,
            seq_end,
            first[end:])
        sequences[name] = {
            'files': matches,
            'start': seq_start,
            'end': seq_end,
            'first': first}

        last_index = files.index(matches[-1])

        fileset = set(files)
        matchset = set(matches)
        files = sorted(list(fileset - matchset))

    return sequences, non_sequences
