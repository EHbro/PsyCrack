# General methodolody - store 4 character strings and feed them into passwords, like 4char + 4char or 4char + bruteforce.
# For keyword you can use keyword + bruteforce, or keyword + substitution + bruteforce.

import sys
import argparse
import re

# Initiate the argument parser
parser = argparse.ArgumentParser()

# Write a help file that gives user syntax for adding in arguments.

# There are 4 "base" use cases below that will make up the base for your password array.
# The others after it will work off the base password array after these have been calculated.

# Year Range  1960-2022  -y --year  DONE
# Repetition  -r --repetition 1111 2222 1212 aaaa    DONE
# Keywords.  -k --keyword  ex. Quark Gluon Electron  This needs to be file input.  Allow 4-8 char here.
# Keyboard patterns -p --pattern.  We're limiting to 4 character patterns.  Simple flag, Y/N from file.   DONE

# Case usage.  -c --case.  This will simply be true or false.  If false, remove all entries from password array with A-Z in it.  Consider not using this?
# substitution  -s --substitution   ex.  e=3  i=1  l=1  o=0  a=4  a=@  b=8  s=5  s=$.   DONE
# special character match at start or end of line. -m --match !@#$   DONE
# Add in masks into buffer space for strings less than 8char.  DONE

# When you go to run this on the cracker, do some sample cases first and make sure it can crack them.
# Example:  get hashes of abcd1234, then some with the ?l?u?d masks also, like abcd?l?u?d

# Maybe check input for character that aren't alphanumeric/special, stuff like AEther.  Throw error if encountered.

# There is a --pw-min=x and --pw-max=y command line option.  Consider taking this as user input.

parser = argparse.ArgumentParser()

#parser.add_argument('-y', '--year', nargs='*')
parser.add_argument('-y','--year')
parser.add_argument('-r','--repetition', action='store_true')
parser.add_argument('-k','--keyword', action='store_true')
parser.add_argument('-p','--pattern', action='store_true')
parser.add_argument('-s','--substitution', action='store_true')
parser.add_argument('-m','--match', action='store_true')

args = parser.parse_args()

#Global variables
yearArray = []
repetitionArray = []
matchArray = []
calcArray = []
keywordArray = []
masterArray = []
passwords=[]

#if args.year == None:
#        print("Invalid year range given.  ex  1960-2022.")
#        print("Exiting...")
#        sys.exit()

if args.year:
        yearRange = str(args.year).replace("'", '')
        yearRange = yearRange.replace('[','')
        yearRange = yearRange.replace(']','')

# Run a regex against the year pattern.  should be /d/d/d/d-/d/d/d/d
        yearRegex = re.match('(\d\d\d\d-\d\d\d\d)', yearRange)
        if yearRegex is None :
                print("Invalid year range given.  ex  1960-2022.")
                print("Exiting...")
                sys.exit()

# This doesn't work right now.  Hardcode now and fix later
#if args.keyword:
#        print("You chose -k/--keyword.")
#        filename = input('Enter a filename: ')
#        print(filename)
#        infile = open(filename,"r")
#        for line in infile:
#                keywordArray.append(line.strip())

# Check for conditional arguments and if present, set their values.
# Update.  This is probably not needed.  You should just call the function if a flag is set.
# Example:  if args.reptition:
#  calcRepetition()



#Removed this since it's just a binary check, Y = include, N = don't include.
#if args.pattern:
#        myPattern = args.pattern


#You may want to use an openfile for patternArray too, although you can hardcode it if you want.
#Also can do both, option for loading a pattern.txt file, and if not present then just use the hardcoded one here.
patternArray = ['1234', 'qwer', 'asdf', 'ASDF', 'QWER', '!@#$', '2345', 'wert', 'sdfg', 'SDFG', 'WERT', '@#$%', '3456', 'erty', 'dfgh', 'DFGH', 'ERTY', '#$%^', '4567', 'rtyu', 'fghj', 'FGHJ', 'RTYU', '$%^&', '5678', 'tyui', 'ghjk', 'GHJK', 'TYUI', '%^&*', '6789', 'yuio', 'hjkl', 'HJKL', 'YUIO', '^&*(', '7890', 'uiop', 'jkl;', 'JKL:', 'UIOP', '&*()', '890-', 'iop[', "kl;'", 'KL:"', 'IOP{', '*()_', 'zxcv', 'ZXCV', 'xcvb', 'XCVB', 'cvbn', 'CVBN', 'vbnm', 'VBNM', 'bnm,', 'BNM<', 'nm,.', 'NM<>', 'm,./', 'M<>?', '1qaz', '2wsx', '3edc', '#EDC', '@WSX', '!QAZ', '4rfv', '$RFV', '5tgb', '%TGB', '6yhn', '^YHN', '7ujm', '&UJM', '8ik,', '*IK<', '9ol.', '(OL>', '0p;/', ')P:?', 'zse4', 'xdr5', 'cft6', 'CFT^', 'XDR%', 'ZSE$', 'vgy7', 'VGY&', 'bhu8', 'BHU*', 'nji9', 'NJI(', 'mko0', 'MKO)', ',lp-', '<LP_', '.;[=', '>:{+', '4esz', '5rdx', '6tfc', '^TFC', '%RDX', '$ESZ', '7ygv', '&YGV', '8uhb', '*UHB', '9ijn', '(IJN', '0okm', ')OKM', '-pl,', '_PL<', '=[;.', '+{:>', 'zaq1', 'xsw2', 'cde3', 'CDE#', 'XSW@', 'ZAQ!', 'vfr4', 'VFR$', 'bgt5', 'BGT%', 'nhy6', 'NHY^', 'mju7', 'MJU&', ',ki8', '<KI*', '.lo9', '>LO(', '/;p0', '?:P)', 'rewq', '4321', 'FDSA', 'REWQ', '$#@!', 'trew', '5432', 'GFDS', 'TREW', '%$#@', 'ytre', '6543', 'HGFD', 'YTRE', '^%$#', 'uytr', '7654', 'JHGF', 'UYTR', '&^%$', 'iuyt', '8765', 'KJHG', 'IUYT', '*&^%', 'oiuy', '9876', 'LKJH', 'OIUY', '(*&^', 'poiu', '0987', ':LKJ', 'POIU', ')(*&', '[poi', '-098', '":LK', '{POI', '_)(*']

# Let's try doing the logic for year range here.  Assuming we're given 1960-2022, let's populate all the values and..store them in an array
def calcYear():
        myYear = re.search(r'(\d\d\d\d)-(\d\d\d\d)', yearRange)
        year1 = int(myYear.group(1))
        year2 = int(myYear.group(2))
        while year1 <= year2:
                yearArray.append(year1)
                year1+=1
        for i in yearArray:
                passwords.append(i)
#calcYear()

# There are 5184 4char strings for the repetition 'array'.
# Rather than calculating the array whenever this script runs, or hardcoding in that many entries, just read it from a file.
def calcRepetition():
        infile=open("repetition.txt","r")
        for line in infile:
                repetitionArray.append(line.strip())
        for i in repetitionArray:
                passwords.append(i)

def calcPattern():
        for i in patternArray:
                passwords.append(i)

# Placeholder for keyword stuff.  Need to redo this later to accept any filename input
def calcKeyword():
        infile=open("keywords.txt","r")
        for line in infile:
                keywordArray.append(line.strip())
        for i in keywordArray:
                passwords.append(i)

# Here you need to setup combos and then append to password list.
# Check to see if 2 flags are set.  If so, combine their strings and append is to password array.
# Example:  if args.pattern && args.repetition:
#                blah blah logic here, then passwords.append
# Keep doing this until all flags are accounted for.

def calcPasswords():
        for i in yearArray:
                if args.pattern:
                        for j in patternArray:
                                passwords.append(str(i)+j)

#calcPasswords()

# This function needs to be run after the 'base' passwords array has been filled, but before the substitution function.
# Matching is going to offer to either begin or end a string with the following 'special' characters.  !@#$
# If this flag is set, add the special characters to the start and end of every entry in the passwords array.  If start, shift the string to the right.
# Example.  'abcd1234', when doing the ! match the string becomes !abcd123 and abcd123!.  Append these to passwords array.
# Also, you need to hold all these entries in a temporary array, then append them at the end.  Otherwise you can't iterate over passwords array since you keep appending to it.
# Update:  This is too messy to do with padding.  If this option is checked, we'll add it to the start of the string only.
def calcMatch():

        for i in passwords:
                i = str(i)
                # This first set of replacements will put the special chars at the start of the line, and shift the rest to the right one spot, truncating the last character.
                myString1 = "!" + i
                if len(myString1) > 8:
                        myString1 = myString1[:-1]
                matchArray.append(myString1)
                myString2 = "@" + i
                if len(myString2) > 8:
                        myString2 = myString2[:-1]
                matchArray.append(myString2)
                myString3 = "#" + i
                if len(myString3) > 8:
                        myString3 = myString3[:-1]
                matchArray.append(myString3)
                myString4 = "$" + i
                if len(myString4) > 8:
                        myString4 = myString4[:-1]
                matchArray.append(myString4)


                #Removed block
                # Now we replace the last character with the special instead
                #myString = i.replace(i[7], "!")
                #matchArray.append(myString)
                #myString = i.replace(i[7], "@")
                #matchArray.append(myString)
                #myString = i.replace(i[7], "#")
                #matchArray.append(myString)
                #myString = i.replace(i[7], "$")
                #matchArray.append(myString)

        # Consider checking to see if what you're going to append already exists in passwords array.
        # Example:  if i in matchArray notin passwords....
        for i in matchArray:
                passwords.append(i)

# substitution  -s --substitution   ex.  a=4 a=@ e=3 i=1 l=1 o=0 s=5  s=$
# Using regex here to replace for both upper/lower.
# We're going to do one fell swoop of a word and do ALL replacements, or none at all.  To do this, we'll do the singles first
# so e/i/l/o
# Since a and s have 2 replacements, they will work off the modified string once the above characters are done.

def calcSub():
        for i in passwords:
                myString = str(i)
                myString2 = None
                myString3 = None

                if ("e" or "E") in myString:
                        patternE = re.compile('e', re.IGNORECASE)
                        myString = patternE.sub("3", myString)

                if ("i" or "I") in myString:
                        patternI = re.compile('i', re.IGNORECASE)
                        myString = patternI.sub("1", myString)

                if ("l" or "L") in myString:
                        patternL = re.compile('l', re.IGNORECASE)
                        myString = patternL.sub("1", myString)

                if ("o" or "O") in myString:
                        patternO = re.compile('o', re.IGNORECASE)
                        myString = patternO.sub("0", myString)

                if ("a" or "A") in myString:
                        patternA = re.compile('a', re.IGNORECASE)
                        myString2 = patternA.sub("4", myString)
                        myString3 = patternA.sub("@", myString)

                # Leave an option here to leave s as they are since sometimes people don't l33t speak them as opposed to vowels.
                if ("s" or "S") in myString:
                        if myString2 is not None:
                                calcArray.append(myString2)
                                calcArray.append(myString3)
                                patternS = re.compile('s', re.IGNORECASE)
                                myString4 = patternS.sub("5", myString2)
                                calcArray.append(myString4)
                                myString4 = patternS.sub("5", myString3)
                                calcArray.append(myString4)
                                myString5 = patternS.sub("$", myString2)
                                calcArray.append(myString5)
                                myString5 = patternS.sub("$", myString3)
                                calcArray.append(myString5)
                        else:
                                calcArray.append(myString)
                                patternS = re.compile('s', re.IGNORECASE)
                                myString2 = patternS.sub("5", myString)
                                calcArray.append(myString2)
                                myString3 = patternS.sub("$", myString)
                                calcArray.append(myString3)
                elif myString2 is not None:
                        calcArray.append(myString2)
                        calcArray.append(myString3)

                else:
                        calcArray.append(myString)



        for i in calcArray:
                passwords.append(i)

# We need to add padding to our password entries that are less than 8char.
# Hashcat will do this using an .hcmask file, if formatted correctly.
# ex.  ?l?u?d,hashcat?1    This will replace the final character with all (l)owercase (u)ppercase and (d)igits.
# There is the possibility that we can accept user input for which characters they want to use in the mask, but for now let's just hardcode it to use lower/upper/digit.
# After you're done adding the padding, remove any entry that is less than 8char from the passwords array.
# Had to add ?s here to get special chars.  There is also the option in hashcat for ?a which includes ?l ?u ?d ?s.  Consider adding this in.

def calcPadding():
        onePad = "?1"
        myPad = "?l?u?d?s"
        for i in passwords:
                i = str(i)
                myLen = len(i)
                if myLen == 4:
                        myString = "?l?u?d?s," + i + "?1?1?1?1"
                        if myString not in passwords:
                                passwords.append(myString)

                if myLen == 5:
                        myString = "?l?u?d?s," + i + "?1?1?1"
                        if myString not in passwords:
                                passwords.append(myString)

                if myLen == 6:
                        myString = "?l?u?d?s," + i + "?1?1"
                        if myString not in passwords:
                                passwords.append(myString)

                if myLen == 7:
                        myString = "?l?u?d?s," + i + "?1"
                        if myString not in passwords:
                                passwords.append(myString)


# Here we'll do any final cleanup to passwords array.
# Remove all entries that are less than 8char.
def calcMaster():
        for i in passwords:
                if len(str(i)) > 7:
                        masterArray.append(i)
# Uncomment this line once padding is turned on
#                if len(i) >=8:
#                        masterArray.append(i)



# Let's call all our functions here:
if args.year:
        calcYear()
if args.repetition:
        calcRepetition()
if args.pattern:
        calcPattern()
if args.keyword:
        calcKeyword()
if args.match:
        calcMatch()
if args.substitution:
        calcSub()

calcPadding()
calcMaster()

with open("master.txt", "w") as outfile:
        for i in masterArray:
                outfile.write(str(i)+"\n")
