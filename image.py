import numpy as np
import cv2
import os
import hashlib


"""
Retrieves a ImageData instance from a file path
@file_name must be a valid file path that represents a image file
"""
def data_from_filename(file_name: str) -> ImageData:
	result = ImageData()
	result.file_name = file_name
	with open(file_name, 'rb') as data:
		result.md5 = __get_md5(data)
		result.disk_size = __get_disk_size()
	result.im_hash, result.im_dimensions = __get_diff_hash(file_name)
	result.disk_size = __get_disk_size()
	return ImageData


def __get_disk_size() -> str:
	raise NotImplemented

"""
Calculates md5 from a open file
@openfile must be a file open in binary mode
"""
def __get_md5(openfile, read_size=32768): #TODO: Find return type hint
	openfile.seek(0)
	h = hashlib.md5()
	while True:
		buf = openfile.read(read_size)
		if buf:
			h.update(buf)
		else:
			return h


"""
Calculates crc32 from a open file
@openfile must be a file open in binary mode
"""
def __get_crc32(openfile, read_size=32768): #TODO: Find return type hint
	openfile.seek(0)
	h = 0
	while True:
		buf = openfile.read(read_size)
		if buf:
			h = zlib.crc32(buf)
		else:
			return h


"""
Computes the hash based on the difference from adjacent pixels, horizontally
Based on http://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html
And based on https://github.com/JohannesBuchner/imagehash/blob/master/imagehash.py implemetation
"""
def __get_diff_hash(file_name: str, hash_dims=(9,8)): # TODO: Find **correct** return type hint (np array, int tuple)
	im = cv2.imread(file_name, 0)
	size = im.shape
	resized_im = cv2.resize(im, hash_dims, interpolation=cv2.INTER_LANCZOS4) # TODO: TEST INTERPOLATION PERFORMANCE
	data = resized_im[:, 1:] > resized_im[:, :-1]
	return data, size


"""
Computes the hash based on the difference from average
Based on http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
And based on https://github.com/JohannesBuchner/imagehash/blob/master/imagehash.py implemetation
"""
def __get_avg_hash(file_name: str, hash_dims=(8,8)): # TODO: Find **correct** return type hint (np array, int tuple)
	im = cv2.imread(file_name, 0)
	size = im.shape
	resized_im = cv2.resize(im, hash_dims, interpolation=cv2.INTER_LANCZOS4) # TODO: TEST INTERPOLATION PERFORMANCE
	mean = resized_im.mean()
	data = resized_im > mean
	return data, size


"""
Class for storing image data
"""
class ImageData(object):
	__slots__ = ["file_name", "disk_size", "md5", "im_hash", "im_dimensions"]

	@property
	def short_name(self) -> str:
		return os.path.split(self.file_name)[-1]

	@property
	def file_path(self):
		return os.path.split(self.file_name)[0]

	"""
	Compares this instance to other, returning if they are duplicates
	@other is a instance of ImageData
	@similarity_threshold is the threshold from which images should be considered duplicates
	"""
	def compare(self, other: ImageData, dup_threshold: 0) -> bool:
		if (this.md5.hexdigest() == other.md5.hexdigest()):
			return True
		if (self.im_hash.shape != other.im_hash.shape):
			raise ValueError("Images should have the same hash method!")
		sim_percent = np.sum(self.im_hash==other.im_hash) / np.multiply(*self.im_hash.shape)
		return sim_percent >= dup_threshold

