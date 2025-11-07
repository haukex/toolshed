#!/usr/bin/env perl
use warnings;
use strict;
use Text::CSV;     # sudo apt install libtext-csv-perl
use Text::CSV_XS;  # sudo apt install libtext-csv-xs-perl
# Text::CSV will automatically use Text::CSV_XS if it is installed.

# Note ->say was added in Text::CSV_XS 1.17/2015-04-24
# As far as I can tell Text::CSV caught up in 1.91/2017-01-28

my $csv = Text::CSV->new({ binary=>1, auto_diag=>2 });
	#quote_char=>"'", sep_char=>";", always_quote=>1, allow_whitespace=>1,  # optional

while ( my $row = $csv->getline(*DATA) ) {
    $csv->say(*STDOUT, $row);
}
$csv->eof or $csv->error_diag;

__DATA__
Hello,"World"
Foo,Ba r