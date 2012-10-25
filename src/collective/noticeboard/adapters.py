#!/usr/bin/python
# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.interface import implements
from collective.noticeboard.interfaces import INote

ANNOTATION_KEY = 'collective.noticeboard'


def image_tag(object, field):
    scale = "mini"
    if object.portal_type == 'Image':
        scale = "preview"
    scales = getMultiAdapter((object, object.REQUEST), name="images")
    if scales:
        scale = scales.scale(field, scale)
        if scale:
            tag = scale.tag()
            return tag
    return False


class BaseNoteAdapter(object):
    implements(INote)
    def __init__(self, context):
        self.context = context
        try:
            self.annotations = \
                IAnnotations(self.context)[ANNOTATION_KEY]
        except KeyError:
            self.annotations = \
                IAnnotations(self.context)[ANNOTATION_KEY] = \
                PersistentDict()

    @property
    def position_x(self):
        return self.annotations.get('position_x', '50%')

    @position_x.setter
    def position_x(self, value):
        self.annotations['position_x'] = value

    @property
    def position_y(self):
        return self.annotations.get('position_y', '50%')

    @position_y.setter
    def position_y(self, value):
        self.annotations['position_y'] = value

    @property
    def height(self):
        return self.annotations.get('height', 150)

    @height.setter
    def height(self, value):
        self.annotations['height'] = int(value)

    @property
    def width(self):
        return self.annotations.get('width', 200)

    @width.setter
    def width(self, value):
        self.annotations['width'] = int(value)

    @property
    def color(self):
        return self.annotations.get('color', 'yellow')

    @color.setter
    def color(self, value):
        self.annotations['color'] = str(value)

    @property
    def zIndex(self):
        return self.annotations.get('zIndex', 'top')

    @zIndex.setter
    def zIndex(self, value):
        self.annotations['zIndex'] = str(value)

    @property
    def id_(self):
        return self.context.id

    @property
    def url(self):
        return self.context.absolute_url()

    @property
    def jsonable(self):
        return dict(
                portal_type=self.context.portal_type.lower(),
                title=self.title,
                url=self.context.absolute_url() + '/xx',
                id=self.id_,
                description=self.description,
                text=self.text,
                image_tag=self.image_tag,
                color=self.color,
                zIndex=self.zIndex,
                height=self.height,
                width=self.width,
                position_x=self.position_x,
                position_y=self.position_y,
                )


class ArchetypesNoteAdapter(BaseNoteAdapter):

    @property
    def title(self):
        return self.context.Title()

    @property
    def description(self):
        return self.context.Description()

    @property
    def text(self):
        text = getattr(self.context, 'getText', None)
        if text:
            return text()

    @property
    def image_tag(self):
        if getattr(self.context, 'getImage', None):
            tag = image_tag(self.context, 'image')
            if tag:
                return tag


class DexterityNoteAdapter(BaseNoteAdapter):

    @property
    def title(self):
        return self.context.title

    @property
    def description(self):
        return self.context.description

    @property
    def text(self):
        text = getattr(self.context, 'text', None)
        if text:
            return text.render()

    @property
    def image_tag(self):
        if getattr(self.context, 'image', None):
            tag = image_tag(self.context, 'image')
            if tag:
                return tag
