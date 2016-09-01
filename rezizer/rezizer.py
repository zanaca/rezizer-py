# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib
import re

__concatenatedOperations = ['tint', 'background', 'blur', 'format', 'max-age',
                          'max-kb', 'overlay', 'quality', 'rotate', 'align']

__simpleOperations = ['distort', 'extend', 'fit', 'fit-in', 'flip', 'flop',
                    'tile', 'grayscale', 'invert', 'map', 'max', 'min',
                    'progressive', 'round']


def __buildPath(operations):
    parts = []

    if 'tile' in operations:
        parts.append('tile')
        return '/'.join(parts)

    if 'map' in operations:
        parts.append('map')
        return '/'.join(parts)

    if 'palette' in operations:
        paletteStr = 'palette'
        if operations['palette'].isdigit():
            paletteStr += ':' + operations['palette']
        parts.append(paletteStr)
        return '/'.join(parts)

    if 'resize' in operations:
        resizeStr = 'x'.join(operations['resize'])
        if 'retina' in operations:
            resizeStr += '@' + operations['retina'] + 'x'
            del operations['retina']
        del operations['resize']
        parts.append(resizeStr)

    if 'crop' in operations:
        parts.append(operations['crop'])
        del operations['crop']

    for operation in operations:
        if operation == 'align':
            alignment = operations[operation].lower()

            if alignment == 'top':
                alignment = 'north'

            elif alignment == 'left':
                alignment = 'weast'

            elif alignment == 'right':
                alignment = 'east'

            elif alignment == 'bottom':
                alignment = 'south'

            elif alignment in ['north', 'east', 'south', 'west', 'northeast',
                               'southeast', 'southwest', 'northwest', 'middle',
                               'center', 'smart']:
                True  # ok
            else:
                alignment = None

            if alignment:
                parts.append(alignment)

        elif operation == 'face':
            faceOperation = operation
            if operations[operataion] == 'focused':
                faceOperataion += ':focused'

            parts.append(faceOperataion)

        elif operation in __concatenatedOperations:
            if not operations[operation]:
                operations[operation] = ''
            parts.append(operation + ':' + operations[operation])

        else:
            parts.append(operation)

    return '/'.join(parts)


def __generateHash(secret=None, url=None):
    if not secret:
        return None

    hash = base64.encodestring(hmac.new(secret, url, hashlib.sha1).digest())
    return hash.replace('+', '-').replace('/', '_').strip()


class rezizerUrl:
    serverUrl = None
    secret = None
    operations = {}
    rawImageUrl = None

    def __init__(self, url=None, secret=None):
        self.serverUrl = url
        self.secret = secret

    def __str__(self):
        return self.generate()

    def generate(self):
        path = __buildPath(self.operations)
        if self.secret:
            path = __generateHash(self.secret, path) + '/' + path

        path += '/' + self.rawImageUrl

        return self.serverUrl + '/' + path

    def withUrl(self, url=None):
        self.rawImageUrl = url

        return self

    def resize(self, width=0, height=0):
        if not isinstance(width, int) or not isinstance(height, int):
            raise Exception('Either the height or the width are not valid \
integers', {'width': width, 'height': height})

        self.operations['resize'] = [str(width), str(height)]
        return self

    def crop(self, top=0, left=0, bottom=0, right=0):
        if not isinstance(top, int) or not isinstance(left, int) or not isinstance(bottom, int) or not isinstance(right, int):
            raise Exception('At least one of top, left, bottom or right are not \
valid integers')

        self.operations['crop'] = [str(top), str(left),
                                   str(bottom), str(right)]
        return self

    def overlay(self, url='', align='center'):
        self.operations['overlay'] = url + ':' + align
        return self

    def faceDetection(self, inFocus=False):
        self.operations['face'] = 'focused' if inFocus else True
        return self

    def smart(self):
        self.operations['align'] = 'smart'
        return self


def __simpleFunction(name):
    def _method(self):
        self.operations[name] = True
        return self

    return _method


for operation in __simpleOperations:
    _method = __simpleFunction(operation)
    if operation == 'fit-in':
        operation = 'fitIn'

    setattr(rezizerUrl, operation, _method)


def __concatenatedFunction(name, value=None):
    value = value

    def _method(self, value=None):
        if isinstance(value, list):
            value = ','.join(map(str, value))
        if value:
            value = re.sub('/[^0-9a-zA-Z,\.]/g', '', str(value))

        self.operations[name] = value
        return self

    return _method

for operation in __concatenatedOperations:
    _method = __concatenatedFunction(operation)
    if operation == 'overlay':
        continue

    if operation == 'max-kb':
        method = 'maxKb'

    if operation == 'max-age':
        method = 'maxAge'

    setattr(rezizerUrl, operation, _method)

__all__ = rezizerUrl
