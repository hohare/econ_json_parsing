# Script to prepare pre-series submission CSV file


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

econ_to_digi = {'ECOND' : '1',
                'ECONT' : '0',
                'ECON-D' : '1',
                'ECON-T' : '0',
    }

name_label_template = '%s from tray %s at location %s'

if __name__ == '__main__':
    nchips = int(args.nchips)
    out_csv = 'KIND_OF_PART,SERIAL_NUMBER,BATCH_NUMBER,BARCODE,NAME_LABEL,LOCATION,INSTITUTION,COMMENT_DESCRIPTION,MANUFACTURER,PRODUCTION_DATE\n'

    csv_tmp = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'

    econd_fname = 'pre-series-cm/econd_preseries_cm.csv'
    with open(econd_fname, 'r') as f:
        text = f.read().splitlines()
    counter = 0
    econd = []
    for l in text:
        splits = l.split(',')
        if len(splits) > 1:
            if 'Preseries CM' in splits[1]:
                print(splits)
                counter+=1 
                econd.append(splits)
    

    print(counter)

    econt_fname = 'pre-series-cm/econt_preseries_cm.csv'
    with open(econt_fname, 'r') as f:
        text = f.read().splitlines()
    counter = 0
    econt = []
    for l in text:
        splits = l.split(',')
        if len(splits) > 1:
            if 'Preseries CM' in splits[1]:
                print(splits)
                counter+=1 
                econt.append(splits)
    

    print(counter)

    # fill CSV file
    # ECON-D first
    kind_of_part = 'ECON-D'
    batch_number = 'TO BE FILLED'
    location = 'Baylor'
    institution = 'FermiLab'
    comment_description = 'Pre-series CM'
    manufacturer = args.manufacturer
    production_date = "TO BE FILLED"#args.date

    batch1 = 1
    batch2 = 1
    for el in econd:
        chip = el[0][1:]
        tray = econ_to_digi[kind_of_part]+'000'+el[0][0]
        serial_number = '%s%s'%(tray, chip)
        barcode = barcodes[kind_of_part]+serial_number
        

        ship = '06/20/24'
        batch = '1'
        batch_number =  '0002-PS-18000'
        str_i = ''
        if len(str(batch2)) == 1:
            str_i = '0%d'%batch2
        else:
            str_i = str(batch2)


        if 'June 27' in el[4]:
            ship = '06/27/24'
            batch = '2'
            str_i = ''
            if len(str(batch2)) == 1:
                str_i = '0%d'%batch2
            else:
                str_i = str(batch2)
            batch_number =  '0003-PS-18001' + str_i
            batch = batch_number.split('-')[0]
            batch2+=1


        elif 'June 20' in el[4]:
            ship = '06/20/24'
            batch = '1'
            str_i = ''
            if len(str(batch1)) == 1:
                str_i = '0%d'%batch1
            else:
                str_i = str(batch1)
            batch_number =  '0002-PS-18000'+str_i
            batch = batch_number.split('-')[0]
            batch1+=1


        name_label = name_label_template%(kind_of_part,batch_number.split('-')[2][:5],chip)
        comment_description = 'Shipped on %s (batch %s)'%(ship,batch)
        production_date = '05/31/24'

        out_csv += csv_tmp%(kind_of_part,serial_number,batch_number,barcode,name_label,location,institution,comment_description,manufacturer,production_date)


    #print(out_csv)


    # fill CSV file
    # ECON-D first
    kind_of_part = 'ECON-T'
    location = 'Baylor'
    institution = 'FermiLab'
    comment_description = 'Pre-series CM'
    manufacturer = args.manufacturer
    production_date = '05/31/24'

    batch1 = 1
    batch2 = 1
    for el in econt:
         
        chip = el[0][1:]
        tray = econ_to_digi[kind_of_part]+'000'+el[0][0]
        serial_number = '%s%s'%(tray, chip)
        barcode = barcodes[kind_of_part]+serial_number
        
        ship = '06/20/24'
        batch = '1'
        batch_number =  '0002-PS-08000'
        str_i = ''

        if 'June 27' in el[4]:
            ship = '06/27/24'
            batch = '2'
            str_i = ''
            if len(str(batch2)) == 1:
                str_i = '0%d'%batch2
            else:
                str_i = str(batch2)
            
            batch_number =  '0003-PS-08001'+str_i
            batch = batch_number.split('-')[0]
            batch2 += 1

        elif 'June 20' in el[4]:
            ship = '06/20/24'
            if len(str(batch1)) == 1:
                str_i = '0%d'%batch1
            else:
                str_i = str(batch1)
            batch_number =  '0002-PS-08000'+str_i
            batch = batch_number.split('-')[0]
            batch1+=1


        name_label = name_label_template%(kind_of_part,batch_number.split('-')[2][:5],chip)

        comment_description = 'Shipped on %s (batch %s)'%(ship,batch)
        production_date = '05/31/24'


        out_csv += csv_tmp%(kind_of_part,serial_number,batch_number,barcode,name_label,location,institution,comment_description,manufacturer,production_date)
        

    print(out_csv)

    with open('csv-files/ECON-preseries-CM.csv', 'w') as f:
        f.write(out_csv)



