# Copyright (c) OpenMMLab. All rights reserved.
from typing import Any, Optional, Sequence

from mmdeploy.utils import get_common_config
from ..base import BACKEND_MANAGERS, BaseBackendManager


@BACKEND_MANAGERS.register('rknn')
class RKNNManager(BaseBackendManager):

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

        from .wrapper import RKNNWrapper
        common_config = get_common_config(deploy_cfg)
        return RKNNWrapper(
            model=backend_files[0],
            common_config=common_config,
            output_names=output_names)
