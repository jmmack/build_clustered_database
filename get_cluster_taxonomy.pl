#!/usr/bin/env perl -w
use strict;

#---------------------------------------------------------------------------------------------------
# June 25, 2013 - JM
#
# Get lowest common taxonomy for each cluster
# based on: /Volumes/rhamnosus/reference_genomes/cd-hit/vagina/bin/check_cluster_taxonomy.pl
#---------------------------------------------------------------------------------------------------

my $cluster_file = "/Volumes/rhamnosus/reference_genomes/may2013/cluster/uclust/all_bac_ncRNArm_medianorder_id90.uc";
#S	0	801	*	*	*	*	*	gi|326802614|ref|NC_015278.1|:1902091-1902891 Aerococcus urinae ACS-120-V-Col10a chromosome, complete genome	*
# S = SEED; H = Hit; C = cluster SEED
# Need to get S and H and ignore C
my $tax_file = "/Volumes/rhamnosus/reference_genomes/may2013/wget/all_bac.ffn_tax_lookup.txt";
#refseqID	length	accession	taxID	taxonomy

#---------------------------------------------------------------------------------------------------

my %taxonomy;
my %seed;
my $curr_level;

my %tax_lookup;
open(IN, "< $tax_file") or die "Could not open $tax_file: $!\n";
while(defined(my $l = <IN>)){
chomp $l;
	my @hold = split(/\t/, $l);
	my @hold2 = split(/\s+/, $hold[0]);
	$hold2[0] =~ s/\>//;
	$tax_lookup{$hold2[0]} = $hold[-1];

}close IN;

my %cluster_tax;
my %cluster_seed;
open(IN, "< $cluster_file") or die "Could not open $cluster_file: $!\n";
while(defined(my $l = <IN>)){
chomp $l;
	my @hold = split(/\t/, $l);
	my @hold2 = split(/\s+/, $hold[8]);
	$hold2[0] =~ s/\>//;
	my $cluster_num = $hold[1];
	my $refseq = $hold2[0];
	
#test print "$refseq\t$tax_lookup{$refseq}\t$cluster_num\n";close IN;exit;
	my @curr_tax = split(/;/, $tax_lookup{$refseq});
	
	if ($hold[0] eq "S"){
		$cluster_tax{$cluster_num} = join(";", @curr_tax);			# Take the seed seq taxonomy if this is the seed. This will be the first taxonomy we encounter since seeds always come before hits
#test print "$cluster_tax{$cluster_num}\n";close IN;exit;#OK
		$cluster_seed{$cluster_num} = $refseq;						# Seed refseq lookup by cluster number
	}elsif ($hold[0] eq "H"){
		my @hold2 = split(/;/, $cluster_tax{$cluster_num});			# Get the previous taxonomy for this cluster
		my @tax;													# Holds the new common taxonomy
			for (my $i=0; $i<@hold2; $i++){							# Use the previous taxonomy as the reference because some parts of the lineage may already ahve been removed and so curr_tax is longer
#test			print "$hold2[$i]\t$curr_tax[$i]\n";
				push (@tax, $hold2[$i]) if $hold2[$i] eq $curr_tax[$i];		# Start at top (Bacteria) and keep all taxonomy that are common
			}
		$cluster_tax{$cluster_num} = join(";", @tax);						# Make new lineage up to lowest common tax
	}
}close IN;

print "refseqID\tcluster_no\tcommon_taxonomy\n";
foreach(keys(%cluster_seed)){
	print "$cluster_seed{$_}\t$_\t$cluster_tax{$_}\n";
}