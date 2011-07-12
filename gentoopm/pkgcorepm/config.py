#!/usr/bin/python
#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

from gentoopm.basepm.config import PMConfig

class PkgCoreConfig(PMConfig):
	def __init__(self, domain):
		self._domain = domain