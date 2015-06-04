========
imgutils
========
Useful Image Utilities.


Copy an image
=============

::

    import imgutils

    source_image = 'path/to/my/img.tif'
    dest_image = 'path/to/my/img_copy.jpg'

    imgutils.copy(source_image, dest_image)


Copy and resize an image
========================

::

    source_image = 'path/to/my/img.tif'
    dest_image = 'path/to/my/img_resized_copy.jpg'

    imgutils.copy(source_image, dest_image, size=(960, 540), quality=50)


Scale and copy an image
=======================

::

    source_image = 'path/to/my/img.tif'
    dest_image = 'path/to/my/img_scaled_copy.jpg'

    imgutils.copy(source_image, dest_image, scale=0.5, quality=95)


Create a thumbnail
==================

::

    source_image = 'path/to/my/img.tif'
    dest_image = 'path/to/my/img_thumb.jpg'

    imgutils.thumbnail(source_image, dest_image, size=(128, 128))


Find image sequences in a list of files
=======================================

::

    files = os.listdir('path/to/my/image/files')

    sequences, non_sequences = imgutils.find_sequences(files)

    print sequences
    # {'img.[001-003].png': {
    #     'files': ['img.001.png', 'img.002.png', 'img.003.png'],
    #     'start': '001',
    #     'end': '003',
    #     'first': 'img.001.png'},
    # }

    print non_sequences
    # ['img_a.png', 'img_x.png']
