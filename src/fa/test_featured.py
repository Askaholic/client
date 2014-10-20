from _ctypes import ArgumentError
from _pytest.python import isfunction

__author__ = 'Thygrrr'

import featured
import updater
from PyQt4 import QtGui, QtCore
import types
import pytest


class TestObjectWithoutIsFinished(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    def __init__(self, QObject_parent=None):
        QtCore.QObject.__init__(self, QObject_parent)

def noop_thread(self):
    QtCore.QThread.yieldCurrentThread(self)

def test_updater_is_a_dialog(application):
    assert isinstance(updater.UpdaterProgressDialog(None), QtGui.QDialog)


def test_updater_has_progress_bar_game_progress(application):
    assert isinstance(updater.UpdaterProgressDialog(None).gameProgress, QtGui.QProgressBar)


def test_updater_has_progress_bar_map_progress(application):
    assert isinstance(updater.UpdaterProgressDialog(None).mapProgress, QtGui.QProgressBar)


def test_updater_has_progress_bar_mod_progress(application):
    assert isinstance(updater.UpdaterProgressDialog(None).mapProgress, QtGui.QProgressBar)


def test_updater_has_method_append_log(application):
    assert callable(updater.UpdaterProgressDialog(None).appendLog)


def test_updater_append_log_accepts_string(application):
    updater.UpdaterProgressDialog(None).appendLog("Hello Test")


def test_updater_has_method_add_watch(application):
    assert callable(updater.UpdaterProgressDialog(None).addWatch)


def test_updater_append_log_accepts_qobject_with_signals_finished(application):
    updater.UpdaterProgressDialog(None).addWatch(QtCore.QThread())


def test_updater_add_watch_raises_error_on_watch_without_signal_finished(application):
    with pytest.raises(AttributeError):
        updater.UpdaterProgressDialog(None).addWatch(QtCore.QObject())


def test_updater_watch_finished_raises_error_on_watch_without_method_is_finished(application):
    u = updater.UpdaterProgressDialog(None)
    u.addWatch(TestObjectWithoutIsFinished())
    with pytest.raises(AttributeError):
        u.watchFinished()


def test_updater_hides_and_accepts_if_all_watches_are_finished(application):
    u = updater.UpdaterProgressDialog(None)
    t = QtCore.QThread()
    t.run = noop_thread

    u.addWatch(t)
    u.show()
    t.start()

    while not t.isFinished():
        pass

    application.processEvents()
    assert not u.isVisible()
    assert u.result() == QtGui.QDialog.Accepted


def test_updater_does_not_hide_and_accept_before_all_watches_are_finished(application):
    u = updater.UpdaterProgressDialog(None)
    t = QtCore.QThread()
    t.run = noop_thread
    t_not_finished = QtCore.QThread()

    u.addWatch(t)
    u.addWatch(t_not_finished)
    u.show()
    t.start()

    while not t.isFinished():
        pass

    application.processEvents()
    assert u.isVisible()
    assert not u.result() == QtGui.QDialog.Accepted