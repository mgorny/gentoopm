#!/usr/bin/python
#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

import paludis, re

from gentoopm.basepm.atom import PMAtom, PMPackageKey, PMPackageVersion, \
		PMIncompletePackageKey
from gentoopm.exceptions import InvalidAtomStringError

_category_wildcard_re = re.compile(r'\w')

class PaludisPackageKey(PMPackageKey):
	def __init__(self, key):
		self._k = key

	@property
	def category(self):
		return str(self._k.category)

	@property
	def package(self):
		return str(self._k.package)

	def __str__(self):
		return str(self._k)

class PaludisIncompletePackageKey(PMIncompletePackageKey):
	def __init__(self, key):
		self._k = key

	@property
	def package(self):
		return str(self._k)

class PaludisPackageVersion(PMPackageVersion):
	def __init__(self, ver):
		self._v = ver

	@property
	def without_revision(self):
		return str(self._v.remove_revision())

	@property
	def revision(self):
		rs = self._v.revision_only()
		assert(rs.startswith('r'))
		return int(rs[1:])

	def __str__(self):
		return str(self._v)

class PaludisAtom(PMAtom):
	def _init_atom(self, s, env, wildcards = False):
		opts = paludis.UserPackageDepSpecOptions() \
				+ paludis.UserPackageDepSpecOption.NO_DISAMBIGUATION
		if wildcards:
			opts += paludis.UserPackageDepSpecOption.ALLOW_WILDCARDS

		try:
			self._atom = paludis.parse_user_package_dep_spec(
					s, env, opts,
					paludis.Filter.All())
		except (paludis.BadVersionOperatorError, paludis.PackageDepSpecError,
				paludis.RepositoryNameError):
			raise InvalidAtomStringError('Incorrect atom: %s' % s)

	def __init__(self, s, env, pkg = None):
		self._incomplete = False
		if isinstance(s, paludis.PackageDepSpec):
			self._atom = s
		else:
			try:
				self._init_atom(s, env)
			except InvalidAtomStringError:
				# try */ for the category
				self._init_atom(_category_wildcard_re.sub(r'*/\g<0>', s, 1), env, True)
				self._incomplete = True
		self._pkg = pkg
		self._env = env

	def __contains__(self, pkg):
		raise NotImplementedError('Direct atom matching not implemented in Paludis')

	def __str__(self):
		if self._incomplete:
			raise ValueError('Unable to stringify incomplete atom')
		return str(self._atom)

	@property
	def complete(self):
		return not self._incomplete

	@property
	def associated(self):
		return self._pkg is not None

	@property
	def slotted(self):
		assert(self.associated)
		cp = str(self._atom.package)
		slot = self._pkg.metadata['SLOT']
		return PaludisAtom('%s:%s' % (cp, slot), self._env)

	@property
	def unversioned(self):
		assert(self.associated)
		return PaludisAtom(str(self._atom.package), self._env)

	@property
	def key(self):
		if self.complete:
			return PaludisPackageKey(self._atom.package)
		else:
			return PaludisIncompletePackageKey(self._atom.package_name_part)

	@property
	def version(self):
		try:
			vr = next(iter(self._atom.version_requirements))
		except StopIteration:
			return None
		return PaludisPackageVersion(vr.version_spec)
