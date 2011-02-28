#!/usr/bin/env python

__about__ = """HuffmanCoder (huffmancoder)"""

import heapq

class Node:

class HuffmanTree:
	class Node:
		def __init__(self, f, ch=None):
			"""Create a node.
			   - f	The frequency value of this node [mandatory]
			   - ch	This node's character [optional, default=None]

			If a node doesn't have a character value (ch=None), then it is
			considered to be an internal node. Otherwise, it will be a leaf
			node."""

			self.ch = ch
			self.f = f
			self.parent = None
			self.left = None
			self.right = None
	
		def __lt__(self, other):
			"""Overridden less than operator to compare nodes by their
			frequency value."""
			return self.f < other.f

		def __repr__(self):
			return '%s: %s' % (self.ch, self.f,)
	
		def printtree(self):
			"Print this node and all its children in order."
			print '(',
			if self.left is not None:
				self.left.printtree()
			print self,
			if self.right is not None:
				self.right.printtree()
			print ')',

	def __init__(self, text):
		freq_dict = self._make_freq_dict(text)
		nodes = self._make_nodes(freq_dict)
		self.tree = self._make_huffman_tree(nodes)

		self._enumerate_leaves(self.tree)

	def _make_freq_dict(self, text):
		f = {}
		for c in text:
			if c in f:
				f[c] += 1
			else:
				f[c] = 1
		return f

	def _make_nodes(self, freq_dict):
		return [Node(v,k) for k,v in freq_dict.iteritems()]

	def _make_huffman_tree(self, nodes):
		# Use a priority queue (implemented as a min-heap) to generate
		# the internal nodes of the huffman tree, from the given list
		# of leaf nodes

		heapq.heapify(nodes)
	
		while len(nodes) > 1:
			# Get the two smallest nodes
			first = heapq.heappop(nodes)
			second = heapq.heappop(nodes)

			# Make a internal node to join them with
			#  f = sum of children's freq.
			parent = Node(first.f + second.f)
			parent.left = first
			parent.right = second
			first.parent = parent
			second.parent = parent

			# Push it back onto the min-heap
			heapq.heappush(nodes, parent)

		return nodes[0]

	def _enumerate_leaves(self, node):
		# Recursively add each leaf character to its leaf node and place
		# into the leaves dictionary

		if node is None:
			return
		self._enumerate_leaves(node.left)
		if node.ch is not None:
			self.leaves[node.ch] = node
		self._enumerate_leaves(node.right)

	def encode_char(self, c):
		node = self.leaves[c] # TODO: except ValueError

		enc = ""
		while node.parent is not None:
			if node == node.parent.left:
				enc = '0' + enc
			elif node == node.parent.right:
				enc = '1' + enc
			else:
				pass # TODO: raise some Error
		return enc

	def encode(self):
		senc = ""
		for c in self.text:
			senc += self.encode_char(c)
		return senc


	def decode_char(self, enc_c):
		p = self.tree
		while p.ch is None:
			if enc_c == '0': p = p.left
			elif enc_c == '1': p = p.right
			else: pass # TODO: raise some Error
		return p.ch

	def decode(self, enc_text):
		"Decode enc_text according to this coder's huffman tree."
		sdec = ''

		# FIXME: THIS IS BROKEN -- decode_char needs more than one char
		# for the bitstring, and it can be a variable number, which
		# can't(?) be known at this point

		i =0
		l = len(enc_text)
		while i < l:
			sdec += self.decode_char(enc_text[i])
			i += 1
		return sdec