# AUTOGENERATED! DO NOT EDIT! File to edit: 04_analysis.binary.ipynb (unless otherwise specified).

__all__ = ['threshold_argmax', 'youdens_jstats', 'performance']

# Cell
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, confusion_matrix

# Cell
def threshold_argmax(y_score_1c, thresh:float=0.5):
    '''Converts a sequence of floats into a list of zeros and ones.

    Float values in the sequence are converted to 0 if they are smaller or equal to a set treshold
    or 1 if they are larger than the treshold.

    Parameters
    ----------
    y_score_1c : 1d array-like of floats
                 Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of
                 decisions (as returned by “decision_function” on some classifiers). For binary y_true, y_score is supposed to be the score of the class with greater label.

    tresh : float, default=0.5
            Treshold used for converting numbers in sequence

    Returns
    -------
    y_pred : 1d array-like of integers
             Converted scores to integers between 0 and 1

    '''
    y_pred = np.array([1 if score > thresh else 0 for score in y_score_1c])
    return y_pred

# Cell
def youdens_jstats(sens:float, spec:float):
    '''Calculates Youden's J-statistic

    Parameters
    ----------
    sens : float
           Sensitivity

    spec : float
           Specificity

    Returns
    -------
    youden : float
             Youden's J-statistic
    '''

    youden = sens + spec - 1
    return youden

# Cell
def performance(y_true, y_score_1c, thresh=0.5, labels:list=[0, 1],
                bal_acc:bool=False, youden:bool=False, auroc:bool=False, err_rate:bool=False, bal_err_rate:bool=False):
    '''Compute various performance metrics for binary classification predictions

    Computes sensitivity, specificity and accuracy (optional: balanced accuracy, youden's j-statistic, roc auc) given a sequence of target scores
    (i.e. probabilities) and the respective ground truth for a binary classification. All metrics are evaluated at a given treshold.

    Parameters
    ----------
    y_true : 1d array-like
             Ground truth (correct) target values

    y_score_1c : 1d array-like of floats
                 Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of
                 decisions (as returned by “decision_function” on some classifiers). For binary y_true, y_score is supposed to be the score of the class with greater label.

    tresh : float
            Treshold

    bal_acc : bool, default=False
              Whether to compute or not compute balanced accuracy

    youden : bool, default=False
             Whether to compute or not compute Youden's J-statistic

    auroc : bool, default=False
            Whether to compute or not compute area under the receiver operating characteristic curve (ROC AUC)

    Returns
    -------
    perf_metrics : dict
                   Contains all calculated metrics
    '''
    y_pred = threshold_argmax(y_score_1c, thresh=thresh)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=labels).ravel()

    # calculate all metrics
    perf_metrics = dict()

    perf_metrics["acc"] = (tn+tp) / (tn+tp+fn+fp)
    perf_metrics["sens"] = tp / (tp+fn)
    perf_metrics["spec"] = tn / (tn+fp)

    if bal_acc:
        perf_metrics["bal_acc"] = balanced_accuracy_score(y_true, y_pred)
    if youden:
        perf_metrics["youden"] = youdens_jstats(perf_metrics["sens"], perf_metrics["spec"])
    if auroc:
        if len(set(y_true.tolist())) > 1:
            perf_metrics["auroc"] = roc_auc_score(y_true, y_score_1c)
        else:
            perf_metrics["auroc"] = np.nan
    if err_rate:
        perf_metrics["err_rate"] = 1 - perf_metrics["acc"]
    if bal_err_rate:
        perf_metrics["bal_err_rate"] = 1 - balanced_accuracy_score(y_true, y_pred)

    return perf_metrics