import hashlib


# wildcard = " "


class MD5Cracker:
    # def main():
    # 	print("MD5 cracker is about to start working!")
    # 	tocrack = "0d61f8370cad1d412f80b84d143e1257"  # hash of C
    # 	tocrack = "5332ba558c6706d24ae90e9ffdbdac1f"  # hash of aebgc
    # 	tocrack = "68e1c85222192b83c04c0bae564b493d"  # hash of koer
    # 	result = md5_crack(tocrack, "k  r")  # Add input string to crack instead of "k  r"
    # 	if result:
    # 		print("Cracking " + tocrack + " gave " + result)
    # 	else:
    # 		print("Failed to crack " + tocrack)

    def md5_crack(self, hexhash, template, wildcard):
        # print('CRACKER hash: ' + hexhash)
        print('CRACKER template: ' + template)
        # print('CRACKER wildcard: ' + wildcard)

        # Instantiate template and crack all instantiations
        # First block recursively instantiates template
        i = 0
        found = False
        # print(wildcard + " - this is the wildcard!")
        # print(len(template))
        while i < len(template):
            # print("While is running!")
            # print(template)
            # print(template[i])
            if template[i] == wildcard:
                # print("Got here!!!")
                found = True
                char = 32  # Start with this char ascii
                while char < 126:
                    c = str(chr(char))
                    if c != wildcard:  # Cannot check wildcard!
                        ntemplate = template[:i] + c + template[i + 1:]
                        # print("i: "+str(i)+" ntemplate: "+ntemplate)
                        result = self.md5_crack(hexhash, ntemplate, wildcard)
                        if result:  # Stop immediately if cracked
                            return result
                    char += 1
            i += 1
        # Instantiation loop done
        # print("Why did I get here?")
        if not found:
            # No wildcards found in template: crack
            m = hashlib.md5()
            m.update(template.encode('ascii'))
            hash = m.hexdigest()
            # print("Template: "+template+"\nHash: "+hash)
            if hash == hexhash:
                print("I found it!")
                return template  # Cracked!
        # Template contains wildcards
        return None

# if __name__ == '__main__':
#     cracker = MD5Cracker()
#     c = cracker.md5_crack('68e1c85222192b83c04c0bae564b493d', 'koer', '?')
#     print(c)