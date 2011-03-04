#!/usr/bin/env python

__about__ = """HuffmanCoder (huffmancoder)"""

import heapq

def bits_to_ascii(bitstring):
	leftover = 8 - (len(bitstring) % 8)
	bitstring += '0'*leftover # add 0s to end of bitstring
	asciistring = str(leftover) # first char in ascii huffman-coded string is the leftover bits, which is guarenteed to only be 1 char
	
	i = 0
	while i < len(bitstring):
		s2 = bitstring[i:i+8]
		asciistring += chr(int(s2, 2))
		i += 8
	return asciistring
	
	
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

		self.leaves = {}
		self._enumerate_leaves(self.tree)

		# TODO: We don't really want to save the text within the tree
		# structure, as requiring the full text to construct a tree at
		# the receiving end defeats the purpose of the encoding.
		self.text = text

	def _make_freq_dict(self, text):
		f = {}
		for c in text:
			if c in f:
				f[c] += 1
			else:
				f[c] = 1
		return f

	def _make_nodes(self, freq_dict):
		return [HuffmanTree.Node(v,k) for k,v in freq_dict.iteritems()]

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
			parent = HuffmanTree.Node(first.f + second.f)
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
			node = node.parent
		return enc

	def encode(self):
		senc = ""
		for c in self.text:
			senc += self.encode_char(c)
		return senc


	def _decode_char(self, enc_text, i):
		"""Decodes to a single char of text, returning the char, and the number of
		encoded-text characters to skip as tuple."""

		init_i = i		
		p = self.tree
		while p.ch is None:
			if enc_text[i] == '0': p = p.left
			elif enc_text[i] == '1': p = p.right
			else: pass # TODO: raise some Error
			i += 1
		return (p.ch, i-init_i) 

	def decode(self, enc_text):
		"Decode enc_text according to this coder's huffman tree."
		sdec = ''

		i =0
		l = len(enc_text)
		while i < l:
			dec, n = self._decode_char(enc_text, i)

			sdec += dec
			i += n
		return sdec
