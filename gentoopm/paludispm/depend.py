#!/usr/bin/python
#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

import paludis

from gentoopm.basepm.depend import PMPackageDepSet, PMConditionalDep, \
	PMOneOfDep, PMAllOfDep, PMBaseDep
from gentoopm.paludispm.atom import PaludisAtom

class PaludisBaseDep(PMBaseDep):
	def __init__(self, deps, pkg):
		self._deps = deps
		self._pkg = pkg

	def __iter__(self):
		for d in self._deps:
			if isinstance(d, paludis.PackageDepSpec):
				yield PaludisAtom(d, self._pkg._env)
			elif isinstance(d, paludis.AnyDepSpec):
				yield PaludisOneOfDep(d, self._pkg)
			elif isinstance(d, paludis.AllDepSpec):
				yield PaludisAllOfDep(d, self._pkg)
			elif isinstance(d, paludis.ConditionalDepSpec):
				yield PaludisConditionalDep(d, self._pkg)
			else:
				raise NotImplementedError('Unable to parse %s' % repr(d))

class PaludisOneOfDep(PMOneOfDep, PaludisBaseDep):
	pass

class PaludisAllOfDep(PMAllOfDep, PaludisBaseDep):
	pass

class PaludisConditionalDep(PMConditionalDep, PaludisBaseDep):
	@property
	def enabled(self):
		return self._deps.condition_met(self._pkg._env, self._pkg._pkg)

class PaludisPackageDepSet(PMPackageDepSet, PaludisBaseDep):
	pass
