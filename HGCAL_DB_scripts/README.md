# HGCAL CERN database

Scripts useful to prepare CSV files for submission in CERN HGCAL database

# Instructions to submit CSV files from Jeremy

```
The simplest process is to do the following:
Send me your LXPLUS user name so that I can register you for database upload rights
Create a CSV file of the attached format
Check out the ssh://git@gitlab.cern.ch:7999/hgcal-database/usefull-scripts.git to get the XML conversion tools
Use the csv_to_xml.py to convert the CSV into XML.
For the first upload, we will need to work together to upload and validate. 
After that, the steps are:
scp the XML file to lxplus
ssh to lxplus.cern.ch and from there ssh to dbloader-hgcal.cern.ch
cp [xmlfile] /home/dbspool/spool/hgc/int2r   (or /home/dbspool/spool/hgc/cmsr for production)
check /home/dbspool/state/hgc/int2r/[your xml filename] to see if it succeeded (zero is good, anything else is bad)
look at /home/dbspool/logs/hgc/int2r/[your xml filename] to see any error messages
```

# Naming conventions

```
Danny's proposal for the batch number:
XXXX-YY-ZZZZZZZ
XXXX  is a 4 digit number for the shipment batch (since maybe we’ll be preparing the shipment data before we have the MMR, maybe just a chronological 1/2/3/… numbering rather than the MMR number).  These 150 chips are actually shipment batch 0002 (0001 would chronologically would be the 12 that went into the partial CM’s, 0003 are the chips that went to FSU, 0004 is the shipment last week to UMN, and 0005 will be this next shipment)
YY is a grade or other information.  For all of these chips I propose we label them PS for preseries (not graded, and not “final” tests and cuts)
ZZZZZZZ is the tray location of the chip after sorting.  We didn’t directly track this for these 150 chips, but they went into new trays that didn’t have numbers, so we’ll just assign them numbers.  I’d propose tray number 18000 and 18001  (or 08000 and 08001 for T) for these trays, with 8XXX trays being new empty trays we sorted chips into (like we did here), and we’ll have 9XXX trays be the new tray numbers we’ll sort bad chips into
```

# Create XML file 

```
git clone ssh://git@gitlab.cern.ch:7999/hgcal-database/usefull-scripts.git
cd usefull-scripts
python csv_to_xml.py --task newparts [my_csv.csv] [my_xml.xml]
```
