#Open list file containing names of xyz files to process
set listfile [open "list" r]
set filenames [split [string trim [read $listfile]]]

#Iterate through each of the files
foreach name $filenames {
	mol load xyz $name
	#Grab the first shell atoms
	set firstshell [atomselect top "same fragment as within 3.5 of index 0"]
	#Grab the number of atoms in the first shell
	set length [llength [$firstshell get {element}]]
	
	#Initialize outputfile
	set outfile [open trimmed-${name} w]
	puts $outfile $length
	puts $outfile "trimmed"
	foreach n [$firstshell get {element x y z}] {
		puts $outfile $n
	}
	close $outfile
	mol delete $name
}
exit
