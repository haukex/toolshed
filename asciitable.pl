#!/usr/bin/env perl
use warnings;
use 5.014;  # strict, s///r
use open qw/:std :utf8/;
use charnames ':full';

print '_Dec_Hx_Oct_Character', '_'x16, '_+_Dec_Hx_Oct_Chr_'x3, "\n";
for my $y (0..0x1F) {
    print ' ';
    for my $x (0..3) {
        my $v = $y + $x*0x20;
        my $c = chr( $v<33 ? 0x2400+$v : $v==127 ? 0x2421 : $v );
        printf '%3d %1$02X %1$03o  %s ', $v, $c;
        printf '%-21s', lc(charnames::viacode(0x2400+$v) =~ s/symbol for//ir
            =~ s/transmission block/trans. block/ir =~ s/tab\Kulation//ir) unless $x;
        print '  ', $x<3?'| ':'';
    }
    print "\n";
}

__END__

_Dec_Hx_Oct_Character_________________+_Dec_Hx_Oct_Chr__+_Dec_Hx_Oct_Chr__+_Dec_Hx_Oct_Chr_
   0 00 000  ␀  null                  |  32 20 040  ␠   |  64 40 100  @   |  96 60 140  `   
   1 01 001  ␁  start of heading      |  33 21 041  !   |  65 41 101  A   |  97 61 141  a   
   2 02 002  ␂  start of text         |  34 22 042  "   |  66 42 102  B   |  98 62 142  b   
   3 03 003  ␃  end of text           |  35 23 043  #   |  67 43 103  C   |  99 63 143  c   
   4 04 004  ␄  end of transmission   |  36 24 044  $   |  68 44 104  D   | 100 64 144  d   
   5 05 005  ␅  enquiry               |  37 25 045  %   |  69 45 105  E   | 101 65 145  e   
   6 06 006  ␆  acknowledge           |  38 26 046  &   |  70 46 106  F   | 102 66 146  f   
   7 07 007  ␇  bell                  |  39 27 047  '   |  71 47 107  G   | 103 67 147  g   
   8 08 010  ␈  backspace             |  40 28 050  (   |  72 48 110  H   | 104 68 150  h   
   9 09 011  ␉  horizontal tab        |  41 29 051  )   |  73 49 111  I   | 105 69 151  i   
  10 0A 012  ␊  line feed             |  42 2A 052  *   |  74 4A 112  J   | 106 6A 152  j   
  11 0B 013  ␋  vertical tab          |  43 2B 053  +   |  75 4B 113  K   | 107 6B 153  k   
  12 0C 014  ␌  form feed             |  44 2C 054  ,   |  76 4C 114  L   | 108 6C 154  l   
  13 0D 015  ␍  carriage return       |  45 2D 055  -   |  77 4D 115  M   | 109 6D 155  m   
  14 0E 016  ␎  shift out             |  46 2E 056  .   |  78 4E 116  N   | 110 6E 156  n   
  15 0F 017  ␏  shift in              |  47 2F 057  /   |  79 4F 117  O   | 111 6F 157  o   
  16 10 020  ␐  data link escape      |  48 30 060  0   |  80 50 120  P   | 112 70 160  p   
  17 11 021  ␑  device control one    |  49 31 061  1   |  81 51 121  Q   | 113 71 161  q   
  18 12 022  ␒  device control two    |  50 32 062  2   |  82 52 122  R   | 114 72 162  r   
  19 13 023  ␓  device control three  |  51 33 063  3   |  83 53 123  S   | 115 73 163  s   
  20 14 024  ␔  device control four   |  52 34 064  4   |  84 54 124  T   | 116 74 164  t   
  21 15 025  ␕  negative acknowledge  |  53 35 065  5   |  85 55 125  U   | 117 75 165  u   
  22 16 026  ␖  synchronous idle      |  54 36 066  6   |  86 56 126  V   | 118 76 166  v   
  23 17 027  ␗  end of trans. block   |  55 37 067  7   |  87 57 127  W   | 119 77 167  w   
  24 18 030  ␘  cancel                |  56 38 070  8   |  88 58 130  X   | 120 78 170  x   
  25 19 031  ␙  end of medium         |  57 39 071  9   |  89 59 131  Y   | 121 79 171  y   
  26 1A 032  ␚  substitute            |  58 3A 072  :   |  90 5A 132  Z   | 122 7A 172  z   
  27 1B 033  ␛  escape                |  59 3B 073  ;   |  91 5B 133  [   | 123 7B 173  {   
  28 1C 034  ␜  file separator        |  60 3C 074  <   |  92 5C 134  \   | 124 7C 174  |   
  29 1D 035  ␝  group separator       |  61 3D 075  =   |  93 5D 135  ]   | 125 7D 175  }   
  30 1E 036  ␞  record separator      |  62 3E 076  >   |  94 5E 136  ^   | 126 7E 176  ~   
  31 1F 037  ␟  unit separator        |  63 3F 077  ?   |  95 5F 137  _   | 127 7F 177  ␡   
