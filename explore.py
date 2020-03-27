folder = '/Users/dpetzoldt/Downloads/'

small = 'Why.enex'
big = 'All.enex'

line_chars = []

for line in open(folder + big):
    line_chars.append(len(line))

print(f'{len(line_chars)} lines: {line_chars[:100]}')
