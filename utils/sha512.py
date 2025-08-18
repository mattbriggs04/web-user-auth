"""
This is my personal implementation of SHA512, and was developed in a Computer Security course.
The database does not manage passwords with this implementation, rather this file exists solely for the 
purpose of demonstrating how a hashing algorithm works.
"""

from BitVector import BitVector
import sys
from typing import Tuple, List

class SHA512():
    def __init__(self):
        # registers / hash buffer
        # storing these in the class itself allows for the previous hash buffer to be kept at all times
        self.a = BitVector(hexstring="6a09e667f3bcc908")
        self.b = BitVector(hexstring="bb67ae8584caa73b")
        self.c = BitVector(hexstring="3c6ef372fe94f82b")
        self.d = BitVector(hexstring="a54ff53a5f1d36f1")
        self.e = BitVector(hexstring="510e527fade682d1")
        self.f = BitVector(hexstring="9b05688c2b3e6c1f")
        self.g = BitVector(hexstring="1f83d9abfb41bd6b")
        self.h = BitVector(hexstring="5be0cd19137e2179")

        # round constants
        self.const_K = [0x428a2f98d728ae22,0x7137449123ef65cd,0xb5c0fbcfec4d3b2f,0xe9b5dba58189dbbc,
                        0x3956c25bf348b538,0x59f111f1b605d019,0x923f82a4af194f9b,0xab1c5ed5da6d8118,
                        0xd807aa98a3030242,0x12835b0145706fbe,0x243185be4ee4b28c,0x550c7dc3d5ffb4e2,
                        0x72be5d74f27b896f,0x80deb1fe3b1696b1,0x9bdc06a725c71235,0xc19bf174cf692694,
                        0xe49b69c19ef14ad2,0xefbe4786384f25e3,0x0fc19dc68b8cd5b5,0x240ca1cc77ac9c65,
                        0x2de92c6f592b0275,0x4a7484aa6ea6e483,0x5cb0a9dcbd41fbd4,0x76f988da831153b5,
                        0x983e5152ee66dfab,0xa831c66d2db43210,0xb00327c898fb213f,0xbf597fc7beef0ee4,
                        0xc6e00bf33da88fc2,0xd5a79147930aa725,0x06ca6351e003826f,0x142929670a0e6e70,
                        0x27b70a8546d22ffc,0x2e1b21385c26c926,0x4d2c6dfc5ac42aed,0x53380d139d95b3df,
                        0x650a73548baf63de,0x766a0abb3c77b2a8,0x81c2c92e47edaee6,0x92722c851482353b,
                        0xa2bfe8a14cf10364,0xa81a664bbc423001,0xc24b8b70d0f89791,0xc76c51a30654be30,
                        0xd192e819d6ef5218,0xd69906245565a910,0xf40e35855771202a,0x106aa07032bbd1b8,
                        0x19a4c116b8d2d0c8,0x1e376c085141ab53,0x2748774cdf8eeb99,0x34b0bcb5e19b48a8,
                        0x391c0cb3c5c95a63,0x4ed8aa4ae3418acb,0x5b9cca4f7763e373,0x682e6ff3d6b2b8a3,
                        0x748f82ee5defb2fc,0x78a5636f43172f60,0x84c87814a1f0ab72,0x8cc702081a6439ec,
                        0x90befffa23631e28,0xa4506cebde82bde9,0xbef9a3f7b2c67915,0xc67178f2e372532b,
                        0xca273eceea26619c,0xd186b8c721c0c207,0xeada7dd6cde0eb1e,0xf57d4f7fee6ed178,
                        0x06f067aa72176fba,0x0a637dc5a2c898a6,0x113f9804bef90dae,0x1b710b35131c471b,
                        0x28db77f523047d84,0x32caab7b40c72493,0x3c9ebe0a15c9bebc,0x431d67c49c100d4c,
                        0x4cc5d4becb3e42b6,0x597f299cfc657e2a,0x5fcb6fab3ad6faec,0x6c44198c4a475817]

        self.K_bv = [BitVector(intVal=k, size=64) for k in self.const_K]

    def round_function(self, msch: List[BitVector]) -> None:
        prev_regs = [self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h]

        # run the registers through 80 rounds utilizing the message schedule and round constants
        for i in range(80):
            ch = (self.e & self.f) ^ ((~self.e) & self.g)
            maj = (self.a & self.b) ^ (self.a & self.c) ^ (self.b & self.c)
            sum_a = (self.a.deep_copy() >> 28) ^ (self.a.deep_copy() >> 34) ^ (self.a.deep_copy() >> 39)
            sum_e = (self.e.deep_copy() >> 14) ^ (self.e.deep_copy() >> 18) ^ (self.e.deep_copy() >> 41)

            T1 = BitVector(intVal = (int(self.h) + int(ch) + int(sum_e) + int(msch[i]) + int(self.K_bv[i])) & 0xffffffffffffffff, size=64)
            T2 = BitVector(intVal = (int(sum_a) + int(maj)) & 0xffffffffffffffff, size=64)
            self.h = self.g
            self.g = self.f
            self.f = self.e
            self.e = BitVector(intVal = (int(self.d) + int(T1)) & 0xffffffffffffffff, size=64)
            self.d = self.c
            self.c = self.b
            self.b = self.a
            self.a = BitVector(intVal = (int(T1) + int(T2)) & 0xffffffffffffffff, size=64)
        
        # add all the previous registers to the final result of the 80 rounds
        self.a = BitVector(intVal = (int(self.a) + int(prev_regs[0])) & 0xffffffffffffffff, size=64)
        self.c = BitVector(intVal = (int(self.c) + int(prev_regs[2])) & 0xffffffffffffffff, size=64)
        self.b = BitVector(intVal = (int(self.b) + int(prev_regs[1])) & 0xffffffffffffffff, size=64)
        self.d = BitVector(intVal = (int(self.d) + int(prev_regs[3])) & 0xffffffffffffffff, size=64)
        self.e = BitVector(intVal = (int(self.e) + int(prev_regs[4])) & 0xffffffffffffffff, size=64)
        self.f = BitVector(intVal = (int(self.f) + int(prev_regs[5])) & 0xffffffffffffffff, size=64)
        self.g = BitVector(intVal = (int(self.g) + int(prev_regs[6])) & 0xffffffffffffffff, size=64)
        self.h = BitVector(intVal = (int(self.h) + int(prev_regs[7])) & 0xffffffffffffffff, size=64)


    # helper functions for generating message schedule
    def __sigma0(self, bv: BitVector) -> BitVector:
        return (bv.deep_copy() >> 1) ^ (bv.deep_copy() >> 8) ^ bv.deep_copy().shift_right(7)
    def __sigma1(self, bv: BitVector) -> BitVector:
        return (bv.deep_copy() >> 19) ^ (bv.deep_copy() >> 61) ^ bv.deep_copy().shift_right(6)
    
    def gen_message_schedule(self, msg_bv: BitVector) -> List[BitVector]:
        if msg_bv.size != 1024:
            sys.exit(f"gen_message_schedule error: invalid block size {msg_bv.size} != 1024")

        msg_sch: list = [None] * 80 # 80 64-bit words
        num_words_in_message = 1024 // 64 # word (in this context) = 8 bytes = 64 bits
        for i in range(80):
            if i < num_words_in_message:
                msg_sch[i] = msg_bv[64*i:64*i+64]
            else:
                msg_sch[i] = BitVector(intVal = (int(msg_sch[i-16]) + int(self.__sigma0(msg_sch[i-15])) + int(msg_sch[i-7]) + int(self.__sigma1(msg_sch[i-2]))) & 0xffffffffffffffff, size=64)
        
        return msg_sch
    
    def pad_block(self, block_bv: BitVector, mlen_bv: BitVector) -> Tuple[BitVector, BitVector]:
        if mlen_bv.size != 128:
            sys.exit(f"mlen_bv has an invalid size, expected 128, got {mlen_bv.size}")

        # case 1: block is a perfect multiple of 1024 bits
        if block_bv.size == 1024:
            next_bv = BitVector(bitlist=[1])
            next_bv.pad_from_right(1024 - (1 + 128))
            next_bv += mlen_bv

            return block_bv, next_bv

        # case 2: block can fit '1' + 128 bit message length at the end
        elif block_bv.size + 128 + 1 <= 1024:
            block_bv += BitVector(bitlist=[1])
            block_bv.pad_from_right(1024 - (block_bv.size + 128)) # leave room for 128 bit message
            block_bv += mlen_bv # append message length bv

            return block_bv, BitVector(size=0)

        # case 3: block is less than 1024 bits, able to fit the '1', but not the 128 bit message length
        else:
            block_bv += BitVector(bitlist=[1])
            block_bv.pad_from_right(1024 - block_bv.size)
            next_bv = BitVector(size=0)
            next_bv.pad_from_right(1024 - 128)
            next_bv += mlen_bv

            return block_bv, next_bv

    def hash_file(self, inp_file, hashed_file) -> None:
        file_bv = BitVector(filename=inp_file)
        file_out = open(hashed_file, "w")
        message_len = 0
        
        # update hashing function as a stream of blocks
        while file_bv.more_to_read:
            block_bv = file_bv.read_bits_from_file(1024)
            message_len += block_bv.size

            # if we have not reached the end of the file, padding is not necessary
            # -> run message schedule and compression function on block
            if file_bv.more_to_read:
                msg_schedule = self.gen_message_schedule(block_bv)
                self.round_function(msg_schedule)

            # if we have reached the end of the file, padding and message length is needed
            else:
                # create mlen_bv which stores the message length
                mlen_bv = BitVector(intVal=message_len, size=128)

                # add the '1', padding, and message length
                block_bv, next_bv = self.pad_block(block_bv, mlen_bv)

                # hash the now padded block
                msg_schedule = self.gen_message_schedule(block_bv)
                self.round_function(msg_schedule)

                # if the padding block required the generation of another block, run the hash
                if next_bv.size == 1024:
                    msg_schedule = self.gen_message_schedule(next_bv)
                    self.round_function(msg_schedule)

        # concatenate the registers to form the final hash buffer
        hash_buffer_bv = self.a + self.b + self.c + self.d + self.e + self.f + self.g + self.h
        file_out.write(hash_buffer_bv.get_bitvector_in_hex())

        file_bv.close_file_object()
        file_out.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"Expected 4 arguments, {len(sys.argv)} given.\nUsage: python3 sha512.py [input filename] [output filename]")
    hasher = SHA512()

    hasher.hash_file(sys.argv[1], sys.argv[2])
