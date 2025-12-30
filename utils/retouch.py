import argparse

ap = argparse.ArgumentParser(description='Modify a touch.txt file')
ap.add_argument("input", help="Path to the input file")
ap.add_argument("output", help="Path to the ouput file (default=touch.txt)", default="touch.txt")
ap.add_argument('--hand-stroke-pause', action='store_true')
ap.add_argument('--cover', action='store_true')
args = ap.parse_args()

infile = open(args.input,'r')
outfile = open(args.output, 'w')

current_line=0
for line in infile:
  current_line=current_line + 1
  sline = line.strip()
  if args.cover:
    sline += "8"
  if args.hand_stroke_pause and current_line % 2 == 0:
    sline += "0"
  sline += "\n"
  outfile.write(sline)

infile.close()
outfile.close()

