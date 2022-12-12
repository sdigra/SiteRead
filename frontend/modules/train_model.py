# MUSICMA tutorial: https://muscima.readthedocs.io/en/latest/Tutorial.html
# imports important 
# %%
import os
from muscima.io import parse_cropobject_list
import itertools
import numpy
# import matplotlib.pyplot as plt

import os
import numpy as np
import matplotlib.pyplot as plt
# from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
import math
# CROPOBJECT_DIR = os.path.join(os.environ['HOME'], './musicma_training_set/data/cropobjects_withstaff')


# Bear in mind that the outlinks are integers, only valid within the same document.
# Therefore, we define a function per-document, not per-dataset.

def extract_notes_from_doc(cropobjects):
    """Finds all ``(full-notehead, stem)`` pairs that form
    quarter or half notes. Returns two lists of CropObject tuples:
    one for quarter notes, one of half notes.

    :returns: quarter_notes, half_notes
    """
    _cropobj_dict = {c.objid: c for c in cropobjects}

    notes = []
    rests = []
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
        elif c.clsname.endswith('rest'):
            name = ''
            if c.clsname == '16th_rest':
                name = 'sr'
            elif c.clsname == '8th_rest':
                name = 'er'
            elif c.clsname == 'half_rest':
                name = 'hr'
            elif c.clsname == 'quarter_rest':
                name = 'qr'
            elif c.clsname == 'whole_rest':
                name = 'wr'
            
            if name != '':
                rests.append((c, name))
    quarter_notes = [(n, s) for n, s, f, t in notes if t == 'qn']
    half_notes = [(n, s) for n, s, f, t in notes if t == 'hn']
    eighth_notes = [(n, s, f) for n, s, f, t in notes if t == 'en']
    whole_notes = [(n,) for n, s, f, t in notes if t == 'wn']

    quarter_rests = [(n,) for n, t in rests if t == 'qr']
    half_rests = [(n,) for n, t in rests if t == 'hr']
    eighth_rests = [(n,) for n, t in rests if t == 'er']
    whole_rests = [(n,) for n, t in rests if t == 'wr']
    sixteenth_rests = [(n,) for n, t in rests if t == 'sr']
    return quarter_notes, half_notes, eighth_notes, whole_notes, \
        quarter_rests, half_rests, eighth_rests, whole_rests, sixteenth_rests

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
        if c is not None:
        # Get coordinates of upper left corner of the CropObject
        # relative to the canvas
            _pt = c.top - top + margin
            _pl = c.left - left + margin
        # We have to add the mask, so as not to overwrite
        # previous nonzeros when symbol bounding boxes overlap.
            canvas[_pt:_pt+c.height, _pl:_pl+c.width] += c.mask

    canvas[canvas > 0] = 1
    return canvas

def train():
    CROPOBJECT_DIR = '../musicma_training_set/data/cropobjects_withstaff'
    cropobject_fnames = [os.path.join(CROPOBJECT_DIR, f) for f in os.listdir(CROPOBJECT_DIR)]
    docs = [parse_cropobject_list(f) for f in cropobject_fnames]
    notes = [extract_notes_from_doc(cropobjects) for cropobjects in docs]
    qns = list(itertools.chain(*[qn for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))
    hns = list(itertools.chain(*[hn for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))
    # ens = list(itertools.chain(*[en for qn, hn, en, wn in notes]))
    ens = []
    wns = list(itertools.chain(*[wn for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))

    qrs = list(itertools.chain(*[qr for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))
    hrs = list(itertools.chain(*[hr for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))
    ers = list(itertools.chain(*[er for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))
    wrs = list(itertools.chain(*[wr for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))
    srs = list(itertools.chain(*[sr for qn, hn, en, wn, qr, hr, er, wr, sr in notes]))

    qn_images = [[get_image(qn) for qn in qns], [0] *len(qns)]
    hn_images = [[get_image(hn) for hn in hns], [1] *len(hns)]
    en_images = [[get_image(en) for en in ens], [2] *len(ens)]
    wn_images = [[get_image(wn) for wn in wns], [3] *len(wns)]
    # qr_images = [[get_image(qr) for qr in qrs], [4] *len(qrs)]
    qr_images = [[get_image(qr) for qr in qrs], [2] *len(qrs)]
    hr_images = [[get_image(hr) for hr in hrs], [5] *len(hrs)]
    er_images = [[get_image(er) for er in ers], [6] *len(ers)]
    wr_images = [[get_image(wr) for wr in wrs], [7] *len(wrs)]
    sr_images = [[get_image(sr) for sr in srs], [8] *len(srs)]

    data = np.array(qn_images[0] + hn_images[0] + wn_images[0]
        + qr_images[0],dtype=object)

    images_temp = []
    for i in range(len(data)):
        pad_width = 95-data[i].shape[1]
        pad_height = 205-data[i].shape[0]
        data[i] = np.pad(data[i], [(math.ceil(pad_height/2), math.floor(pad_height/2)), (math.ceil(pad_width/2), math.floor(pad_width/2))], mode='constant')
        images_temp.append(data[i])

    images = np.array(images_temp)

    targets = np.array(qn_images[1] + hn_images[1] + wn_images[1] + qr_images[1])

    rng = np.random.default_rng()
    indices = np.arange(images.shape[0])
    rng.shuffle(indices)
    images = images[indices]
    targets = targets[indices]

    notes = images.reshape((len(images), -1))
    Classifier = BernoulliNB()
    Classifier.fit(notes, targets)
    return Classifier
