# MUSICMA tutorial: https://muscima.readthedocs.io/en/latest/Tutorial.html
# imports important 
# %%
import os
from muscima.io import parse_cropobject_list
import itertools
import numpy
import matplotlib.pyplot as plt
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
# CROPOBJECT_DIR = os.path.join(os.environ['HOME'], './musicma_training_set/data/cropobjects_withstaff')
CROPOBJECT_DIR = './musicma_training_set/data/cropobjects_withstaff'
cropobject_fnames = [os.path.join(CROPOBJECT_DIR, f) for f in os.listdir(CROPOBJECT_DIR)]
docs = [parse_cropobject_list(f) for f in cropobject_fnames]

# Bear in mind that the outlinks are integers, only valid within the same document.
# Therefore, we define a function per-document, not per-dataset.

# %%
def extract_notes_from_doc(cropobjects):
    """Finds all ``(full-notehead, stem)`` pairs that form
    quarter or half notes. Returns two lists of CropObject tuples:
    one for quarter notes, one of half notes.

    :returns: quarter_notes, half_notes
    """
    _cropobj_dict = {c.objid: c for c in cropobjects}

    notes = []
    for c in cropobjects:
        if (c.clsname == 'notehead-full') or (c.clsname == 'notehead-empty'):
            _has_stem = False
            _has_beam = False
            _has_flag = False
            stem_obj = None
            flag_obj = None
            name = ''
            for o in c.outlinks:
                _o_obj = _cropobj_dict[o]
                if _o_obj.clsname == 'stem':
                    _has_stem = True
                    stem_obj = _o_obj
                elif _o_obj.clsname == 'beam':
                    _has_beam = True
                elif _o_obj.clsname.endswith('flag'):
                    _has_flag = True
                    flag_obj = _o_obj
            if _has_stem and (not _has_beam) and (not _has_flag):
                # We also need to check against quarter-note chords.
                # Stems only have inlinks from noteheads, so checking
                # for multiple inlinks will do the trick.
                if len(stem_obj.inlinks) == 1:
                    if (c.clsname == 'notehead-full'):
                        name = 'qn'
                    else:
                        name = 'hn'
            elif _has_stem and (_has_flag or _has_beam):
                name = 'en'
            elif (not _has_stem):
                name = 'wn'
            if name != '':
                notes.append((c, stem_obj, flag_obj, name))
    quarter_notes = [(n, s) for n, s, f, t in notes if t == 'qn']
    half_notes = [(n, s) for n, s, f, t in notes if t == 'hn']
    eighth_notes = [(n, s, f) for n, s, f, t in notes if t == 'en']
    whole_notes = [(n,) for n, s, f, t in notes if t == 'wn']
    return quarter_notes, half_notes, eighth_notes, whole_notes

# qns_and_hns = [extract_notes_from_doc(cropobjects) for cropobjects in docs]

# qns = list(itertools.chain(*[qn for qn, hn in qns_and_hns]))
# hns = list(itertools.chain(*[hn for qn, hn in qns_and_hns]))
notes = [extract_notes_from_doc(cropobjects) for cropobjects in docs]
qns = list(itertools.chain(*[qn for qn, hn, en, wn in notes]))
hns = list(itertools.chain(*[hn for qn, hn, en, wn in notes]))
ens = list(itertools.chain(*[en for qn, hn, en, wn in notes]))
# ens = []
wns = list(itertools.chain(*[wn for qn, hn, en, wn in notes]))
# %%
def get_image(cropobjects, margin=1):
    """Paste the cropobjects' mask onto a shared canvas.
    There will be a given margin of background on the edges."""

    # Get the bounding box into which all the objects fit
    top = min([c.top for c in cropobjects])
    left = min([c.left for c in cropobjects])
    bottom = max([c.bottom for c in cropobjects])
    right = max([c.right for c in cropobjects])

    # Create the canvas onto which the masks will be pasted
    height = bottom - top + 2 * margin
    width = right - left + 2 * margin
    canvas = numpy.zeros((height, width), dtype='uint8')

    for c in cropobjects:
        # Get coordinates of upper left corner of the CropObject
        # relative to the canvas
        _pt = c.top - top + margin
        _pl = c.left - left + margin
        # We have to add the mask, so as not to overwrite
        # previous nonzeros when symbol bounding boxes overlap.
        canvas[_pt:_pt+c.height, _pl:_pl+c.width] += c.mask

    canvas[canvas > 0] = 1
    return canvas

qn_images = [[get_image(qn) for qn in qns], [0] *len(qns)]
hn_images = [[get_image(hn) for hn in hns], [1] *len(hns)]
en_images = [[get_image(en) for en in ens], [2] *len(ens)]
wn_images = [[get_image(wn) for wn in wns], [3] *len(wns)]

# %%
data = np.array(qn_images[0] + hn_images[0] + en_images[0] + wn_images[0], dtype=object)

images_temp = []
for i in range(len(data)):
    data[i] = np.pad(data[i], [(0, 205-data[i].shape[0]), (0, 70-data[i].shape[1])], mode='constant')
    images_temp.append(data[i])

# %%
images = np.array(images_temp)
targets = np.array(qn_images[1] + hn_images[1] + en_images[1] + wn_images[1])

rng = np.random.default_rng()
indices = np.arange(images.shape[0])
rng.shuffle(indices)
images = images[indices]
targets = targets[indices]

notes = images.reshape((len(images), -1))
X_train, X_test, y_train, y_test = train_test_split(
    notes, targets, test_size=0.5, shuffle=False)

GNB_classifier = GaussianNB()
GNB_classifier.fit(X_train, y_train)
predicted = GNB_classifier.predict(X_test)
_, axes = plt.subplots(2, 20)

images_and_labels = list(zip(images, targets))
for ax, (image, label) in zip(axes[0, :], images_and_labels[:20]):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    ax.set_title('%i' % label)


images_and_predictions = list(zip(images[len(images) // 2:], predicted))
for ax, (image, prediction) in zip(axes[1, :], images_and_predictions[:20]):
    ax.set_axis_off()
    ax.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    ax.set_title('%i' % prediction)
print("\nClassification report for classifier %s:\n%s\n" % (GNB_classifier, metrics.classification_report(y_test, predicted)))
disp = metrics.plot_confusion_matrix(GNB_classifier, X_test, y_test)
disp.figure_.suptitle("Confusion Matrix")
print("\nConfusion matrix:\n%s" % disp.confusion_matrix)
print("\nAccuracy of the Algorithm: ", GNB_classifier.score(X_test, y_test))
plt.show()
# %%
