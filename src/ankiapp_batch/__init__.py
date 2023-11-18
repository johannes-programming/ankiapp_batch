import argparse as ap
import os

FORBIDDEN_INFILE_EXTENSIONS = [
    '.csv',
    '.tsv',
    '.xml',
]

OLD_LANG = 'de-DE'
NEW_LANG = 'it-IT'

XML_DRAFT="""<deck name="{deckname}">
    <fields>
        <text name='{old_lang}' sides='10'  lang='{old_lang}'></text>
        <tts name='{old_lang}_TTS' sides='10'  lang='{old_lang}' >
            <sources>
                <ref name="{old_lang}" />
            </sources>
        </tts>
        <text name='{new_lang}' sides='01'  lang='{new_lang}'></text>
        <tts name='{new_lang}_TTS' sides='01'  lang='{new_lang}' >
            <sources>
                <ref name="{new_lang}" />
            </sources>
        </tts>
    </fields>
    <cards>
{cards}    </cards>
</deck>
"""


CARD = """\
        <card>
            <field name='{old_lang}'>{old_word}</field>
            <field name='{new_lang}'>{new_word}</field>
        </card>
"""

def get_pairs(infiles):
    ans = []
    for infile in infiles:
        ans += parse_infile(infile)
    return ans

def parse_infile(infile):
    trunk, ext = os.path.splitext(infile)
    if ext in FORBIDDEN_INFILE_EXTENSIONS:
        raise ValueError()
    ans = []
    with open(infile, 'r') as s:
        for rawline in s:
            line = rawline.strip()
            if line == "":
                continue
            pieces = line.split('=')
            pieces = [p.strip() for p in pieces]
            ans.append(pieces)
    return ans

def get_infiles(i, /): 
    if i is None:
        return []
    if type(i) is str:
        return [i]
    ans = []
    for x in i:
        ans += get_infiles(x)
    return ans

def get_xml_text(*, pairs, deckname):
    cards = ""
    for new_word, old_word in pairs:
        card = CARD.format(
            new_word=new_word, 
            old_word=old_word,
            new_lang=NEW_LANG,
            old_lang=OLD_LANG,
        )
        cards += card
    ans = XML_DRAFT.format(
        new_lang=NEW_LANG,
        old_lang=OLD_LANG,
        cards=cards,
        deckname=deckname,
    )
    return ans

def get_outfile(*, infiles, o):
    if o is not None:
        return o
    if len(infiles) == 1:
        infile, = infiles
        trunk, ext = os.path.splitext(infile)
    else:
        trunk = "a"
    return trunk + '.xml'

def get_deckname(*, outfile, n):
    if n is not None:
        return n
    root, filename = os.path.split(outfile)
    ans, ext = os.path.splitext(filename)
    return ans
    
def main():
    parser = ap.ArgumentParser()
    parser.add_argument('--infiles', '-i', dest='i', nargs='+', action='append')
    parser.add_argument('--outfile', '-o', dest='o')
    parser.add_argument('--deckname', '-n', dest='n')
    ns = parser.parse_args()
    infiles = get_infiles(ns.i)
    outfile = get_outfile(infiles=infiles, o=ns.o)
    deckname = get_deckname(outfile=outfile, n=ns.n)
    pairs = get_pairs(infiles)
    xml_text = get_xml_text(
        pairs=pairs, 
        deckname=deckname,
    )
    with open(outfile, 'w') as s:
        s.write(xml_text)

if __name__ == '__main__':
    main()