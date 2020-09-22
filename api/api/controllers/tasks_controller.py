# Copyright (C) 2015-2020, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

import logging

from aiohttp import web

from api.encoder import dumps, prettify
from api.util import remove_nones_to_dict, raise_if_exc
from wazuh.core.cluster.dapi.dapi import DistributedAPI
from wazuh.tasks import get_task_status

logger = logging.getLogger('wazuh')


async def get_tasks_status(request, list_tasks=None, pretty=False, wait_for_complete=False):
    """Check the status of the specified tasks

    Parameters
    ----------
    request
    list_tasks : list
        List of task's IDs
    pretty : bool, optional
        Show results in human-readable format
    wait_for_complete : bool, optional
        Disable timeout response

    Returns
    -------
    Tasks's status
    """
    f_kwargs = {'task_list': list_tasks}

    dapi = DistributedAPI(f=get_task_status,
                          f_kwargs=remove_nones_to_dict(f_kwargs),
                          request_type='local_master',
                          is_async=False,
                          wait_for_complete=wait_for_complete,
                          logger=logger,
                          rbac_permissions=request['token_info']['rbac_policies']
                          )
    data = raise_if_exc(await dapi.distribute_function())

    return web.json_response(data=data, status=200, dumps=prettify if pretty else dumps)