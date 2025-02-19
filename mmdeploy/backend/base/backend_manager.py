# Copyright (c) OpenMMLab. All rights reserved.
import importlib
from abc import ABCMeta
from typing import Any, Optional, Sequence


class BaseBackendManager(metaclass=ABCMeta):
    """Abstract interface of backend manager."""

    @classmethod
    def build_wrapper(cls,
                      backend_files: Sequence[str],
                      device: str = 'cpu',
                      input_names: Optional[Sequence[str]] = None,
                      output_names: Optional[Sequence[str]] = None,
                      deploy_cfg: Optional[Any] = None,
                      **kwargs):
        """Build the wrapper for the backend model.

        Args:
            backend_files (Sequence[str]): Backend files.
            device (str, optional): The device info. Defaults to 'cpu'.
            input_names (Optional[Sequence[str]], optional): input names.
                Defaults to None.
            output_names (Optional[Sequence[str]], optional): output names.
                Defaults to None.
            deploy_cfg (Optional[Any], optional): The deploy config. Defaults
                to None.
        """
        raise NotImplementedError(
            f'build_wrapper has not been implemented for {cls}')


class BackendManagerRegistry:
    """backend manager registry."""

    def __init__(self):
        self._module_dict = {}

    def register(self, name: str, enum_name: Optional[str] = None):
        """register backend manager.

        Args:
            name (str): name of the backend
            enum_name (Optional[str], optional): enum name of the backend.
                if not given, the upper case of name would be used.
        """
        from mmdeploy.utils import get_root_logger
        logger = get_root_logger()

        if enum_name is None:
            enum_name = name.upper()

        def wrap_manager(cls):

            from mmdeploy.utils import Backend

            if not hasattr(Backend, enum_name):
                from aenum import extend_enum
                extend_enum(Backend, enum_name, name)
                logger.info(f'Registry new backend: {enum_name} = {name}.')

            if name in self._module_dict:
                logger.info(
                    f'Backend manager of `{name}` has already been registered.'
                )

            self._module_dict[name] = cls

            return cls

        return wrap_manager

    def find(self, name: str) -> BaseBackendManager:
        """Find the backend manager with name.

        Args:
            name (str): backend name.

        Returns:
            BaseBackendManager: backend manager of the given backend.
        """
        # try import backend if backend is in `mmdeploy.backend`
        try:
            importlib.import_module('mmdeploy.backend.' + name)
        except Exception:
            pass
        return self._module_dict.get(name, None)


BACKEND_MANAGERS = BackendManagerRegistry()
