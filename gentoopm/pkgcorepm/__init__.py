#!/usr/bin/python
#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

from pkgcore.config import load_config
from pkgcore.const import VERSION

from ..basepm import PackageManager

from .atom import PkgCoreAtom
from .config import PkgCoreConfig
from .repo import PkgCoreRepoDict, PkgCoreInstalledRepo

class PkgCorePM(PackageManager):
	name = 'pkgcore'

	@property
	def version(self):
		return VERSION

	def reload_config(self):
		c = load_config()
		self._domain = c.get_default('domain')

	@property
	def repositories(self):
		return PkgCoreRepoDict(self._domain)

	@property
	def root(self):
		return self._domain.root

	@property
	def installed(self):
		return PkgCoreInstalledRepo(self._domain.named_repos['vdb'],
				self._domain)

	@property
	def Atom(self):
		return PkgCoreAtom

	@property
	def config(self):
		return PkgCoreConfig(self._domain)
