#!/usr/bin/perl

GetOptions(
    "f=s" => \$config,
    "g=s" => \$GroupInfo,
    "i=s" => \$data_list,
    "n:s" => \$monitor_name,
    "q:s" => \$q_parameter,
    "p:s" => \$p_parameter,
    "o:s" => \$outdir,
    "h:s" => \$help,
);

my $text_usage=<<USAGE;

Program:    CFT ( cell free rna Transcriptome Analysis Software )
Version:    1.0
Usage:      perl $0 [options]

Options:
    -f  <FILE>      *config.param
    -g  <FILE>      *treatment-vs-control.list [only for DiffExpGene analysis]
    -i  <FILE>      *sample.info
    -n  <STR>       project name for monitor [ default : CFT ]
    -q  <STR>       Qsub -q parameter [ default : st.q ]
    -p  <STR>       Qsub -P parameter [ default : P20Z10200N0041 ]
    -o  <STR>       output directory
    -h              more help about input file


USAGE
print "$text_usage\n";
# die $text_usage if (! $data_list || !$config || !$outdir ||$help);