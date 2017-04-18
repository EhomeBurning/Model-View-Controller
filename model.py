
import csv
import collections

data_is_loaded = False

PARTY = True
RAW = True
SORT_ASC = True

csvdata=[]
dem_vote=collections.defaultdict(float)
gop_vote=collections.defaultdict(float)
total_vote=collections.defaultdict(float)

def load_data():
    with open('US_County_Level_Presidential_Results_12-16.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            csvdata.append(row)

        for row in csvdata:
            if len(row)==21 and row[9]!="AK":
                state=row[9]
                dem_vote[state]+=float(row[2])
                gop_vote[state]+=float(row[3])
                total_vote[state]+=float(row[4])
                # print("dem_vote: " + str(dem_vote))
                # print("gop_vote: " + str(gop_vote))
                # print("total_vote: " + str(total_vote))


        global data_is_loaded
        data_is_loaded= True


def get_data(party='dem', raw=True, sort_ascending=True, year=2016):
    data=[]
	
    global PARTY
    global RAW
    global SORT_ASC
	
    PARTY= party
    RAW = raw
    SORT_ASC = sort_ascending
	
	
    if not data_is_loaded:
        load_data()

    for key in dem_vote:
        if party=='dem':
            if raw:
                data.append((key, dem_vote[key]))
            else:
                data.append((key, dem_vote[key]/total_vote[key]))
        else:
            if raw:
                data.append((key, gop_vote[key]))
            else:
                data.append((key, gop_vote[key]/total_vote[key]))

    if sort_ascending:
        data=sorted(data, key=lambda x:x[1] )
    else:
        data=sorted(data, key=lambda x:-x[1] )

    return data



    # build the appropriate list of tuples to return


def main():

	points = 0

	data = get_data()
	if data[0] == ('WY', 55949.0) and data[-1] == ('CA', 7362490.0):
		points += 3.33

	data = get_data(party='gop', raw=False)
	if data [0][0] == 'DC' and int(data[0][1] * 100) == 4 and \
		data[-1][0] == 'WY' and int(data[-1][1] * 100) == 70:
		points += 3.33

	data = get_data(party='dem', raw=True, sort_ascending=False)
	if data[0] == ('CA', 7362490.0) and data[-1] == ('WY', 55949.0):
		points += 3.34

	print("points :", points)

main()
