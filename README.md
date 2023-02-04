# AirG test

Answer as many as you can, as thoroughly as you can.
You can use any version of Python 3.6 or greater.
When working with CSV files, please use the csv module. No pandas.
You can email us your files (zip or gzip) or provide a link to a repository 
where we can view your scripts.

## Task 1
Write a script to connect to the following API ["https://swapi.dev/api/vehicles/"].
Retrieve the JSON data, and list the first 5 unique manufacturers.

## Task 2
Create a script to generate a CSV file with random data.

Example output:

```
1234, randomstring
```

Add the ability to pass in command line parameters. Use an argument to pass 
in the number of rows to generate. 
Add another argument for the filename to use for the CSV file.

If you had to generate a large number of rows (millions or more), is there 
anything you would do differently to handle this? 
Modify your script to handle this requirement.

If this script had to run in a production environment, what tests would you 
include to ensure it's running correctly? Add the tests.

If you were having this code reviewed, what else would you do with your code 
to ensure the code is clean and well-formatted?

## Task 3
Write a function to normalize CSV files by converting a pipe-delimited file 
into a comma-delimited file.
Your original file will look like this:

```
Planet|Manufacturer|Model|Type|Passengers
Yavin|Ubrikkian" Industries|Sail Barge|sailbarge|500
Bespin|Bespin Motors|Storm IV, Twin-Pod|repulsorcraft|0
Kuat|Kuat Drive Yards|AT-ST|walker|0
```

When you run your script, the output should look like this:
```
Planet,Manufacturer,Model,Type,Passengers
Yavin,"Ubrikkian"" Industries",Sail Barge,sailbarge,500
Bespin,Bespin Motors,"Storm IV, Twin-Pod",repulsorcraft,0
Kuat,Kuat Drive Yards,AT-ST,walker,0
```
It's valid for a comma to be in your input data. You'll need to surround 
strings with commas in them with double quotes when writing your output file.

It's also valid for double quote characters to be in your input - you will 
need to double up quotes.

### BONUS 1:
Add in the ability to accept command line parameters for:
    - the input delimiter to use ('|' should be the default)
    - the quote character to use (" by default)

### BONUS 2:
Try to automatically detect the delimiter and quote character if they are 
not supplied on the command line.
If either the delimiter or the quote character are provided, assume the 
other one is the default. But if both are missing, you should try to 
automatically detect them.

***NOTE***: This may not work for all files.
