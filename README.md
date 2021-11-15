# sort_data_away

## good examples
https://martin.hoppenheit.info/blog/2015/useful-exiftool-commands/

## Write Comment Tag
exiftool -Comment='TEST' 20201117_134332.jpg

## list files with Comment tag = TEST (recursively)
exiftool -if '$Comment =~ /(TEST)/' -Directory -FileName -T -R .

