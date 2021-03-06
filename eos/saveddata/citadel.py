#coding: UTF-8
#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from eos.modifiedAttributeDict import ModifiedAttributeDict, ItemAttrShortcut
from eos.effectHandlerHelpers import HandledItem
from eos.saveddata.mode import Mode
import eos.db
from eos.types import Ship
import logging

logger = logging.getLogger(__name__)

class Citadel(Ship):

    def validate(self, item):
        if item.category.name != "建筑":
            raise ValueError('Passed item "%s" (category: (%s)) is not under Structure category'%(item.name, item.category.name))

    def __deepcopy__(self, memo):
        copy = Citadel(self.item)
        return copy

    def __repr__(self):
        return "Citadel(ID={}, name={}) at {}".format(
            self.item.ID, self.item.name, hex(id(self))
        )
