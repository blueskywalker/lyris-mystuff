#!/usr/bin/env perl


sub main
{
	$_ = shift;

	if( defined $_ )	 {
		open INPUT,"< $_";
		while(<INPUT>) {
			chomp $_;	
			$lookup{$_}=1;
		}

		close INPUT;
		
		$_ = shift;

		open INPUT,"< $_";
		while(<INPUT>) {
			my ($org,$subOrg) = split(/_/,$_);
			my $key = $org . "_" .$subOrg;
			print "$key\n" if( exists $lookup{$key} );
		}	
	}

}

main(@ARGV);
