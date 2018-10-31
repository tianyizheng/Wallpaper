import sys
import goes
import simpleDesktop

def usage():
    print("Usage: python wallpaper.py earth")
    print("       python wallpaper.py simple")

def main():
    if len(sys.argv) == 1:
      usage()
      exit(0)
    arg = sys.argv[1]
    if arg == "earth":
      goes.main()
    elif arg == "simple":
      simpleDesktop.main()
    else:
      usage()

if __name__ == '__main__':
    main()
