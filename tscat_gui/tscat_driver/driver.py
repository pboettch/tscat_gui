import atexit
from typing import Dict, Union, Optional

from PySide6.QtCore import QObject, QThread, Slot, Signal
from tscat import _Catalogue, _Event

from .actions import Action, GetCataloguesAction, GetCatalogueAction, CreateEntityAction, RemoveEntitiesAction, \
    SetAttributeAction, DeleteAttributeAction, ImportCanonicalizedDictAction


class _TscatDriverWorker(QThread):
    action_done = Signal(Action)

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent=parent)
        self.moveToThread(self)
        self.start()

    @Slot()
    def do_action(self, action: Action) -> None:
        action.action()
        action.completed = True
        self.action_done.emit(action)


class TscatDriver(QObject):
    # internal signals used between driver and worker
    _do_action = Signal(Action)
    action_done = Signal(Action)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent=parent)

        self._worker = _TscatDriverWorker()

        self._do_action.connect(self._worker.do_action)
        self._worker.action_done.connect(self._worker_action_done)

        self._entity_cache: Dict[str, Union[_Event, _Catalogue]] = {}
        self.destroyed.connect(self.stop)  # type: ignore

    def do(self, action: Action) -> None:
        self._do_action.emit(action)

    @Slot()
    def _worker_action_done(self, action: Action) -> None:
        if isinstance(action, GetCataloguesAction):
            for catalogue in action.catalogues:
                self._entity_cache[catalogue.uuid] = catalogue

        elif isinstance(action, GetCatalogueAction):
            for event in action.events:
                self._entity_cache[event.uuid] = event

        elif isinstance(action, CreateEntityAction):
            assert action.entity
            self._entity_cache[action.entity.uuid] = action.entity

        elif isinstance(action, RemoveEntitiesAction):
            for uuid in action.uuids:
                if uuid in self._entity_cache:
                    del self._entity_cache[uuid]

        elif isinstance(action, (SetAttributeAction, DeleteAttributeAction)):
            for e in action.entities:
                self._entity_cache[e.uuid] = e

        elif isinstance(action, ImportCanonicalizedDictAction):
            for c in action.catalogues:
                self._entity_cache[c.uuid] = c

        self.action_done.emit(action)

    def entity_from_uuid(self, uuid: str) -> Union[_Event, _Catalogue]:
        return self._entity_cache[uuid]

    def stop(self):
        self._worker.requestInterruption()
        if not self._worker.wait(1000):
            self._worker.quit()


tscat_driver = TscatDriver()
atexit.register(tscat_driver.stop)