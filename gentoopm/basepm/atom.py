#!/usr/bin/python
#	vim:fileencoding=utf-8
# (c) 2011 Michał Górny <mgorny@gentoo.org>
# Released under the terms of the 2-clause BSD license.

from abc import abstractmethod, abstractproperty

from gentoopm.util import ABCObject

class PMAtom(ABCObject):
	"""
	A base class for PM-specific atom (dependency specification).
	"""

	@abstractmethod
	def __init__(self, s):
		"""
		Create a new atom from string.

		@param s: atom-formatted string
		@type s: string
		"""
		pass

	@abstractmethod
	def __contains__(self, pkg):
		"""
		Check whether a package matches the atom (is contained in the set
		of packages matched by atom).

		@param pkg: a package to match
		@type pkg: L{PMPackage}
		"""
		pass

	@abstractmethod
	def __str__(self):
		"""
		Return the string representation of the atom.

		If the atom is incomplete (misses a category), the result is undefined.
		It can raise an exception then.
		"""
		pass

	@abstractproperty
	def complete(self):
		"""
		Whether the atom is complete, i.e. whether the category is specified.

		If an atom is incomplete, it is impossible to stringify it. Using such
		an atom with L{PMPackageSet.select()} may result
		in an L{AmbiguousPackageSetError}.

		@type: bool
		"""
		pass
