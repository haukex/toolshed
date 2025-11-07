#!/usr/bin/env perl
use 5.014;  # strict, s///r (released 2011)
use warnings;
use Data::Dumper ();

# simple replacement for Data::Dump
sub pp { Data::Dumper->new(\@_)->Terse(@_<2)->Purity(1)->Useqq(1)->Quotekeys(0)->Sortkeys(1)->Indent(1)->Dump =~ s/[\r\n]+\z//r }
# alternative:
sub pp2 { my @v = map { Data::Dumper->new([$_])->Terse(1)->Purity(1)->Useqq(1)->Quotekeys(0)
	->Sortkeys(1)->Indent(0)->Pair('=>')->Dump } @_; @v==1 ? $v[0] : '('.join(', ',@v).')' }

say pp(["Hello", "World!"]);
say pp(["Hello,"], "World!");
say pp2(["Hello,"], "World!");

__END__
### Output:
[
  "Hello",
  "World!"
]
$VAR1 = [
  "Hello,"
];
$VAR2 = "World!";
(["Hello,"], "World!")
