import itertools


class Ranges:

    def make_ranges(self, slaves_count):
        all = self.calc_all()
        each_count = int(len(all) / slaves_count)
        ret = []

        for i in range(0, slaves_count):
            start = int(i) * each_count
            end = int((i+1)) * each_count
            if i == slaves_count-1:
                ret.append(all[start:])
            else:
                ret.append(all[start:end])

        return ret

    def calc_all(self):
        # alphab = ''
        # for c in range(32, 126):
        #     alphab += str(chr(c))
        #
        # three = [''.join(i + ('?',)) for i in itertools.product(alphab, repeat = 1)]
        # four = [''.join(i + ('??',)) for i in itertools.product(alphab, repeat = 2)]
        #
        # return ['?', '??'] + three + four

        three_c = ['?', '??']
        for c in range(32, 126):
            if chr(c) == '?':
                continue
            three_c.append(str(chr(c)) + '??')

        return three_c

if __name__ == '__main__':
    ranges = Ranges()
    r = ranges.calc_all();
    for m in ranges.calc_all():
        print(m)
        print('noo')
    for m in ranges.make_ranges(3):
        print(m)
        print(len(m))
