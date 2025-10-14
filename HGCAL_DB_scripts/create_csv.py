# Script to create CSV files for inclusion in CERN DB

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--target", help="Target ECON-D or ECON-T")
parser.add_argument("--batch", help="Batch or tray number")
parser.add_argument("--location", help="Location", default = 'FNAL')
parser.add_argument("--institution", help="Institution", default = 'Fermilab')
parser.add_argument("--comment", help="Comment to add in subfield", default = '')
parser.add_argument("--manufacturer", help="Manufacturer", default = 'TSMC')
parser.add_argument("--date", help="Date format mm/dd/yy hh:mm PM or AM", default = '06/27/23 12:49 PM')
parser.add_argument("--nchips", help="Number of chips up to 100", default = '100')
args = parser.parse_args()

barcodes = {'ECOND' : '320ICECD', 
            'ECON-D' : '320ICECD',
            'ECONT' : '321ICECT',
            'ECON-T' : '321ICECT'
            }

mapping = {'ECOND' : 'ECON-D', 
           'ECON-D' : 'ECON-D',
           'ECONT'  : 'ECON-T',
           'ECON-T' : 'ECON-T',
}

name_label_template = '%s from tray %s at location %d'

if __name__ == '__main__':
    nchips = int(args.nchips)
    

    out_csv = 'KIND_OF_PART,SERIAL_NUMBER,BATCH_NUMBER,BARCODE,NAME_LABEL,LOCATION,INSTITUTION,COMMENT_DESCRIPTION,MANUFACTURER,PRODUCTON_DATE\n'

    csv_tmp = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'

    kind_of_part = mapping[args.target]
    batch_number = args.batch
    location = args.location
    institution = args.institution
    comment_description = args.comment
    manufacturer = args.manufacturer
    production_date = args.date


    for chip in range(nchips):
        serial_number = '%s%d'%(args.batch, chip)
        barcode = serial_number+barcodes[kind_of_part]
        name_label = name_label_template%(kind_of_part,batch_number,chip)
        out_csv += csv_tmp%(kind_of_part,serial_number,batch_number,barcode,name_label,location,institution,comment_description,manufacturer,production_date)

    print(out_csv)

    fname = '%s_%s_%s.csv'%(kind_of_part,batch_number,location)

    out_path = 'csv-files'

    with open('%s/%s'%(out_path,fname) ,'w') as f:
        f.write(out_csv)



