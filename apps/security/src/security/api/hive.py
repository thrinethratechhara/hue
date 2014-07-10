#!/usr/bin/env python
# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from django.http import HttpResponse
from django.utils.translation import ugettext as _

from libsentry.api import get_api


def list_sentry_roles_by_group(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    roles = get_api(request.user).list_sentry_roles_by_group()
    result['roles'] = roles
    result['message'] = ''
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")


def list_sentry_privileges_for_provider(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    groups = json.loads(request.POST['groups'])
    roleSet = json.loads(request.POST['roleSet'])
    authorizableHierarchy = json.loads(request.POST['authorizableHierarchy'])

    sentry_privileges = get_api(request.user).list_sentry_privileges_for_provider(groups=groups, roleSet=roleSet, authorizableHierarchy=authorizableHierarchy)
    result['sentry_privileges'] = sentry_privileges
    result['message'] = ''
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")


def list_sentry_privileges_by_role(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    roleName = request.POST['roleName']
    sentry_privileges = get_api(request.user).list_sentry_privileges_by_role(roleName)
    result['sentry_privileges'] = sentry_privileges
    result['message'] = ''
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")


def _hive_add_privileges(user, role, privileges):
    api = get_api(user)

    _priviledges = {}

    for priviledge in privileges:
      api.alter_sentry_role_grant_privilege(role['name'], {
          'privilegeScope': priviledge['privilegeScope'],
          'serverName': priviledge['serverName'],
          'dbName': priviledge['dbName'],
          'tableName': priviledge['tableName'],
          'URI': priviledge['URI'],
          'action': priviledge['action']
      })

    return _priviledges


def hive_create_role(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    role = json.loads(request.POST['role'])

    api = get_api(request.user)

    api.create_sentry_role(role['name'])
    result['privileges'] = _hive_add_privileges(request.user, role, role['privileges'])
    api.alter_sentry_role_add_groups(role['name'], role['groups'])

    result['role'] = {"name": role['name'], "groups": [], "grantorPrincipal": request.user.username}

    result['message'] = ''
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")


def hive_add_privileges(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    role = json.loads(request.POST['role'])

    result['privileges'] = _hive_add_privileges(request.user, role, role['newPrivileges'])

    result['message'] = ''
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")


def create_sentry_role(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    roleName = request.POST['roleName']

    get_api(request.user).create_sentry_role(roleName)
    result['message'] = ''
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")


def create_sentry_role(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    roleName = request.POST['roleName']

    get_api(request.user).create_sentry_role(roleName)
    result['message'] = ''
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")


def drop_sentry_role(request):
  result = {'status': -1, 'message': 'Error'}

  try:
    roleName = request.POST['roleName']

    get_api(request.user).drop_sentry_role(roleName)
    result['message'] = _('Role and privileges deleted.')
    result['status'] = 0
  except Exception, e:
    result['message'] = unicode(str(e), "utf8")

  return HttpResponse(json.dumps(result), mimetype="application/json")
