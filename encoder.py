"""

Encoder ver.1.0.0

Copyright (c) 2023 Tinashe Mashindi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import json
class Encoder:
    def __init__(self):
        pass
    # count the frequency of characters in the text
    def enumerate(self, text):
        count = 1;
        bag = {}

        for char in text:
            if char in bag:
                continue
            # if char doesnt exist add it to the dictionary. Count represents the frequence of the char
            bag[char] = count
            # increment the frequency by 1
            count += 1

        return bag

    # start the encoding process
    def words(self, text, reference_text):
        # create a dictionary of unique words, and their encoded values from the reference text
        mapping = self.enumerate(reference_text)
        # initialize output array
        output = []
        # declare the starting number of the encoder
        count = 0

        # if the char in the input text, exists in the reference text
        # append the encoded char to the output
        for char in text:
            try:
                if char in mapping:
                    output.append(mapping[char])
            except:
                return 'failed'

        # dump the map to json
        mapping = json.dumps(mapping)
        with open(f'./data/map.json', 'w') as file:
            file.write(mapping)

        return output

    # decode an array of encoded values using a provided mapper
    def decode(self, array, mapper):
        output = ""
        # for each encode, parse the mapper & retrieve the key (char), if the value == encode
        for array_value in array:
            for char, map_value in mapper.items():
                if int(array_value) == int(map_value):
                    output += char + " "

        return output

    # infer the encode values of raw text from provided mapper
    # This function is for quickly encoding data, using a pre-generated mapper
    def infer(self, input_text, mapper):
        input_array = input_text.split(' ')
        count = 0
        output = []

        for array_value in input_array:
            for char, map_value in mapper.items():
                if array_value == char:
                    output.append(int(map_value))
                    count += 1

        return output

