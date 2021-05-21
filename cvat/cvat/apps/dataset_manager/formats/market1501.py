# Copyright (C) 2021 Intel Corporation
#
# SPDX-License-Identifier: MIT

import zipfile
from tempfile import TemporaryDirectory

from datumaro.components.dataset import Dataset
from datumaro.components.extractor import (AnnotationType, Label,
    LabelCategories, Transform)

from cvat.apps.dataset_manager.bindings import (CvatTaskDataExtractor,
    import_dm_annotations)
from cvat.apps.dataset_manager.util import make_zip_archive

from .registry import dm_env, exporter, importer

class AttrToLabelAttr(Transform):
    def __init__(self, extractor, label):
        super().__init__(extractor)

        assert isinstance(label, str)
        self._categories = {}
        label_cat = self._extractor.categories().get(AnnotationType.label)
        if not label_cat:
            label_cat = LabelCategories()
        self._label = label_cat.add(label)
        self._categories[AnnotationType.label] = label_cat

    def categories(self):
        return self._categories

    def transform_item(self, item):
        annotations = item.annotations
        if item.attributes:
            annotations.append(Label(self._label, attributes=item.attributes))
            item.attributes = {}
        return item.wrap(annotations=annotations)

class LabelAttrToAttr(Transform):
    def __init__(self, extractor, label):
        super().__init__(extractor)

        assert isinstance(label, str)
        label_cat = self._extractor.categories().get(AnnotationType.label)
        self._label = label_cat.find(label)[0]

    def transform_item(self, item):
        annotations = item.annotations
        attributes = item.attributes
        if self._label != None:
            labels = [ann for ann in annotations
                if ann.type == AnnotationType.label \
                    and ann.label == self._label]
            if len(labels) == 1:
                attributes.update(labels[0].attributes)
                annotations.remove(labels[0])
        return item.wrap(annotations=annotations, attributes=attributes)


@exporter(name='Market-1501', ext='ZIP', version='1.0')
def _export(dst_file, task_data, save_images=False):
    dataset = Dataset.from_extractors(CvatTaskDataExtractor(
        task_data, include_images=save_images), env=dm_env)
    with TemporaryDirectory() as temp_dir:
        dataset.transform(LabelAttrToAttr, 'market-1501')
        dataset.export(temp_dir, 'market1501', save_images=save_images)
        make_zip_archive(temp_dir, dst_file)

@importer(name='Market-1501', ext='ZIP', version='1.0')
def _import(src_file, task_data):
    with TemporaryDirectory() as tmp_dir:
        zipfile.ZipFile(src_file).extractall(tmp_dir)

        dataset = Dataset.import_from(tmp_dir, 'market1501', env=dm_env)
        dataset.transform(AttrToLabelAttr, 'market-1501')
        import_dm_annotations(dataset, task_data)
