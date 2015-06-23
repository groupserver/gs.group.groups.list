# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.privacy import GroupVisibility
from gs.group.member.base import user_member_of_group


class MemberGroups(object):

    def __init__(self, context, groups):
        self.context = context
        self.origGroups = groups

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

#FIXME: Deal with ""manager: looking at the groups.


class PublicGroups(MemberGroups):
    # --=mpj17=-- should this be moved to gs.group.member.base?

    @Lazy
    def groups(self):
        retval = []
        for g in self.origGroups:
            if GroupVisibility(g).isPublic:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        retval.sort(key=lambda g: g.name.lower())
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)


class RestrictedGroups(MemberGroups):
    @Lazy
    def groups(self):
        retval = []
        for g in self.origGroups:
            if GroupVisibility(g).isPublicToSite:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        retval.sort(key=lambda g: g.name.lower())
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)


class PrivateGroups(MemberGroups):
    # --=mpj17=-- should this be moved to gs.group.member.base?

    @Lazy
    def groups(self):
        retval = []
        for g in self.origGroups:
            if GroupVisibility(g).isPrivate:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        retval.sort(key=lambda g: g.name.lower())
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)


class SecretGroups(MemberGroups):
    # --=mpj17=-- should this be moved to gs.group.member.base?

    @Lazy
    def groups(self):
        retval = []
        for g in self.origGroups:
            if GroupVisibility(g).isSecret:
                g.member = user_member_of_group(self.loggedInUser, g)
                retval.append(g)
        retval.sort(key=lambda g: g.name.lower())
        return retval

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        return iter(self.groups)